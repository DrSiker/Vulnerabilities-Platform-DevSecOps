#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { VulnerabilitiesPlatformStack } from '../lib/stack';

const app = new cdk.App();
new VulnerabilitiesPlatformStack(app, 'VulnerabilitiesPlatformStack', {
  env: { 
    account: process.env.CDK_DEFAULT_ACCOUNT, 
    region: process.env.CDK_DEFAULT_REGION 
  },
});