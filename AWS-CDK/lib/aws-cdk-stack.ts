import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as amplify from '@aws-cdk/aws-amplify-alpha';
import * as logs from 'aws-cdk-lib/aws-logs';
import * as iam from 'aws-cdk-lib/aws-iam';
import { Construct } from 'constructs';

export class VulnerabilitiesPlatformStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // VPC with proper isolation
    const vpc = new ec2.Vpc(this, 'VulnerabilitiesVpc', {
      maxAzs: 2,
      natGateways: 1,
      subnetConfiguration: [
        {
          name: 'Private',
          subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS,
          cidrMask: 24,
        },
        {
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
      ],
    });

    // ECS Cluster with Container Insights
    const cluster = new ecs.Cluster(this, 'VulnerabilitiesCluster', {
      vpc,
      containerInsights: true,
    });

    // ECR Repositories
    const backendRepo = ecr.Repository.fromRepositoryName(this, 'BackendRepo', 'vulnerabilities-backend');
    const frontendRepo = ecr.Repository.fromRepositoryName(this, 'FrontendRepo', 'vulnerabilities-frontend');

    // Database Security Group
    const dbSecurityGroup = new ec2.SecurityGroup(this, 'DatabaseSecurityGroup', {
      vpc,
      description: 'Security group for RDS database',
      allowAllOutbound: false,
    });

    // Database Secrets
    const dbSecret = new secretsmanager.Secret(this, 'DBSecret', {
      secretName: 'VulnDBSecret',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'admin' }),
        generateStringKey: 'password',
        excludeCharacters: '\"@/\\',
      },
    });

    // RDS Instance with enhanced security
    const db = new rds.DatabaseInstance(this, 'PostgresDB', {
      engine: rds.DatabaseInstanceEngine.postgres({ version: rds.PostgresEngineVersion.VER_13_4 }),
      vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS },
      allocatedStorage: 20,
      credentials: rds.Credentials.fromSecret(dbSecret),
      databaseName: 'vulndb',
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
      removalPolicy: cdk.RemovalPolicy.SNAPSHOT,
      deletionProtection: true,
      securityGroups: [dbSecurityGroup],
      backupRetention: cdk.Duration.days(7),
      storageEncrypted: true,
      port: 5432,
    });

    // Task Role for Backend Service
    const backendTaskRole = new iam.Role(this, 'BackendTaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    });

    backendTaskRole.addToPolicy(new iam.PolicyStatement({
      actions: ['secretsmanager:GetSecretValue'],
      resources: [dbSecret.secretArn],
    }));

    // Backend Service
    const backendService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'BackendService', {
      cluster,
      taskImageOptions: {
        image: ecs.ContainerImage.fromEcrRepository(backendRepo),
        environment: {
          DATABASE_HOST: db.instanceEndpoint.hostname,
          DB_SECRET_ARN: dbSecret.secretArn,
        },
        taskRole: backendTaskRole,
        logDriver: ecs.LogDrivers.awsLogs({
          streamPrefix: 'backend',
          logRetention: logs.RetentionDays.ONE_MONTH,
        }),
      },
      memoryLimitMiB: 512,
      cpu: 256,
      desiredCount: 2,
      assignPublicIp: false,
    });

    // Frontend Service
    const frontendService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'FrontendService', {
      cluster,
      taskImageOptions: {
        image: ecs.ContainerImage.fromEcrRepository(frontendRepo),
        logDriver: ecs.LogDrivers.awsLogs({
          streamPrefix: 'frontend',
          logRetention: logs.RetentionDays.ONE_MONTH,
        }),
      },
      memoryLimitMiB: 512,
      cpu: 256,
      desiredCount: 2,
      assignPublicIp: false,
    });

    // API Gateway with security configurations
    const api = new apigateway.RestApi(this, 'VulnerabilitiesAPI', {
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
      },
      deploy: true,
      deployOptions: {
        stageName: 'prod',
        loggingLevel: apigateway.MethodLoggingLevel.INFO,
        dataTraceEnabled: true,
      },
    });

    // Rate limiting for API
    const usagePlan = api.addUsagePlan('UsagePlan', {
      throttle: {
        rateLimit: 10,
        burstLimit: 2,
      },
    });

    api.root.addMethod('ANY');
    api.root.addProxy({
      defaultIntegration: new apigateway.HttpIntegration(
        `http://${backendService.loadBalancer.loadBalancerDnsName}`
      ),
    });

    // Allow database access from backend service
    dbSecurityGroup.addIngressRule(
      backendService.service.connections.securityGroups[0],
      ec2.Port.tcp(5432),
      'Allow backend service to access database'
    );

    // Amplify App
    const amplifyApp = new amplify.App(this, 'FrontendApp', {
      sourceCodeProvider: new amplify.GitHubSourceCodeProvider({
        owner: 'DrSiker',
        repository: 'Vulnerabilities-Platform-DevSecOps',
        oauthToken: cdk.SecretValue.secretsManager('github-token'),
      }),
    });

    amplifyApp.addBranch('main');

    // Stack Outputs
    new cdk.CfnOutput(this, 'BackendURL', { value: backendService.loadBalancer.loadBalancerDnsName });
    new cdk.CfnOutput(this, 'FrontendURL', { value: frontendService.loadBalancer.loadBalancerDnsName });
    new cdk.CfnOutput(this, 'ApiGatewayURL', { value: api.url });
  }
}
