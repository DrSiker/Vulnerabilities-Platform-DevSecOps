import * as cdk from 'aws-cdk-lib'; 
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import { Construct } from 'constructs';

export class VulnerabilitiesPlatformStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ✅ 1. Crear VPC con una AZ y sin NAT Gateway (Free Tier)
    const vpc = new ec2.Vpc(this, 'VulnerabilitiesVpc', {
      maxAzs: 1,
      natGateways: 0,
      subnetConfiguration: [
        { name: 'Public', subnetType: ec2.SubnetType.PUBLIC, cidrMask: 24 }
      ],
    });

    // ✅ 2. Grupos de Seguridad
    const ecsSecurityGroup = new ec2.SecurityGroup(this, 'ECSSecurityGroup', { 
      vpc,
      allowAllOutbound: true,
      description: 'Security group for ECS services'
    });

    // 🔓 Permitir tráfico en los puertos necesarios
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP traffic');
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(5000), 'Allow Backend API access');
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(3000), 'Allow Frontend access');
    ecsSecurityGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(5432), 'Allow Database access');

    // ✅ 3. Crear un Cluster ECS
    const cluster = new ecs.Cluster(this, 'VulnerabilitiesCluster', { vpc });

    // ✅ 4. Obtener imágenes desde ECR
    const dbRepo = ecr.Repository.fromRepositoryName(this, 'DBRepo', 'vulnerabilities-db');
    const backendRepo = ecr.Repository.fromRepositoryName(this, 'BackendRepo', 'vulnerabilities-backend');
    const frontendRepo = ecr.Repository.fromRepositoryName(this, 'FrontendRepo', 'vulnerabilities-frontend');

    // ✅ 5. Definir tareas ECS
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

    // ✅ 6. Definir contenedores
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

    // ✅ 7. Definir servicios ECS en Fargate
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

    // ✅ 8. Outputs (para ver los endpoints generados)
    new cdk.CfnOutput(this, 'FrontendURL', { value: 'http://frontend:3000', description: 'Frontend service URL' });
    new cdk.CfnOutput(this, 'BackendAPI', { value: 'http://backend:5000', description: 'Backend API endpoint' });
  }
}
