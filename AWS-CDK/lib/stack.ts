import * as cdk from 'aws-cdk-lib';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import { Construct } from 'constructs';

export class VulnerabilitiesPlatformStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new ec2.Vpc(this, 'VulnerabilitiesVpc', {
      maxAzs: 1,
      natGateways: 0,
      subnetConfiguration: [{ name: 'Public', subnetType: ec2.SubnetType.PUBLIC, cidrMask: 24 }],
    });

    const ecsSecurityGroup = new ec2.SecurityGroup(this, 'ECSSecurityGroup', {
      vpc,
      allowAllOutbound: true,
      description: 'Security group for ECS services'
    });

    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80));
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(5000));
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(3000));
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(5432));

    const cluster = new ecs.Cluster(this, 'VulnerabilitiesCluster', { vpc });

    const dbRepo = ecr.Repository.fromRepositoryName(this, 'DBRepo', 'vulnerabilities-db');
    const backendRepo = ecr.Repository.fromRepositoryName(this, 'BackendRepo', 'vulnerabilities-backend');
    const frontendRepo = ecr.Repository.fromRepositoryName(this, 'FrontendRepo', 'vulnerabilities-frontend');

    const dbTask = new ecs.FargateTaskDefinition(this, 'DBTask', {
      memoryLimitMiB: 512,
      cpu: 256
    });

    const backendTask = new ecs.FargateTaskDefinition(this, 'BackendTask', {
      memoryLimitMiB: 512,
      cpu: 256
    });

    const frontendTask = new ecs.FargateTaskDefinition(this, 'FrontendTask', {
      memoryLimitMiB: 512,
      cpu: 256
    });

    dbTask.addContainer('DBContainer', {
      image: ecs.ContainerImage.fromEcrRepository(dbRepo),
      memoryLimitMiB: 512,
      cpu: 256,
      environment: {
        POSTGRES_USER: 'admin',
        POSTGRES_PASSWORD: 'password123',
        POSTGRES_DB: 'vulndb'
      },
      portMappings: [{ containerPort: 5432 }],
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'db', logRetention: 7 })
    });

    backendTask.addContainer('BackendContainer', {
      image: ecs.ContainerImage.fromEcrRepository(backendRepo),
      memoryLimitMiB: 512,
      cpu: 256,
      environment: {
        DATABASE_URL: 'postgresql://admin:password123@db:5432/vulndb'
      },
      portMappings: [{ containerPort: 5000 }],
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'backend', logRetention: 7 })
    });

    frontendTask.addContainer('FrontendContainer', {
      image: ecs.ContainerImage.fromEcrRepository(frontendRepo),
      memoryLimitMiB: 256,
      cpu: 256,
      environment: {
        BACKEND_URL: 'http://backend:5000'
      },
      portMappings: [{ containerPort: 3000 }],
      logging: ecs.LogDrivers.awsLogs({ streamPrefix: 'frontend', logRetention: 7 })
    });

    new ecs.FargateService(this, 'DBService', {
      cluster,
      taskDefinition: dbTask,
      desiredCount: 1,
      assignPublicIp: true,
      securityGroups: [ecsSecurityGroup]
    });

    new ecs.FargateService(this, 'BackendService', {
      cluster,
      taskDefinition: backendTask,
      desiredCount: 1,
      assignPublicIp: true,
      securityGroups: [ecsSecurityGroup]
    });

    new ecs.FargateService(this, 'FrontendService', {
      cluster,
      taskDefinition: frontendTask,
      desiredCount: 1,
      assignPublicIp: true,
      securityGroups: [ecsSecurityGroup]
    });

    new cdk.CfnOutput(this, 'FrontendURL', { value: 'http://frontend:3000', description: 'Frontend service URL' });
    new cdk.CfnOutput(this, 'BackendAPI', { value: 'http://backend:5000', description: 'Backend API endpoint' });
  }
}
