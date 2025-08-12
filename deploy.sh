#!/bin/bash

# Deploy the SAM application (infrastructure)
cd sam-app
sam build   # This handles/installs dependencies in requirements.txt automatically 

# Check if stack exists and is in failed state
STACK_STATUS=$(aws cloudformation describe-stacks --stack-name sam-app --query 'Stacks[0].StackStatus' --output text 2>/dev/null || echo "DOES_NOT_EXIST")

if [ "$STACK_STATUS" = "ROLLBACK_COMPLETE" ] || [ "$STACK_STATUS" = "CREATE_FAILED" ]; then
    echo "Stack is in failed state ($STACK_STATUS). Deleting and recreating..."
    aws cloudformation delete-stack --stack-name sam-app
    aws cloudformation wait stack-delete-complete --stack-name sam-app
    echo "Stack deleted. Proceeding with deployment..."
fi

# Deploy the SAM application
sam deploy 

# Get invoke URL of the deployed API Gateway (retrieves the API URL from the CloudFormation stack outputs)
API_URL=$(aws cloudformation describe-stacks --stack-name sam-app --query "Stacks[0].Outputs[?OutputKey=='TodoApiUrl'].OutputValue" --output text)

# Get CloudFront URL for the frontend (retrieves the CloudFront URL from the CloudFormation stack outputs)
CLOUDFRONT_URL=$(aws cloudformation describe-stacks --stack-name sam-app --query "Stacks[0].Outputs[?OutputKey=='CloudFrontUrl'].OutputValue" --output text)

BUCKET_NAME=$(aws cloudformation describe-stacks --stack-name sam-app --query "Stacks[0].Outputs[?OutputKey=='S3BucketName'].OutputValue" --output text)
if [ -z "$API_URL" ]; then
  echo "Error: API URL not found. Please check the deployment."
  exit 1
fi
echo "API URL: $API_URL"

# Check if the bucket exists
if ! aws s3 ls "s3://$BUCKET_NAME" > /dev/null 2>&1; then
  echo "Error: S3 bucket $BUCKET_NAME does not exist. Please check the deployment."
  exit 1
fi
echo "S3 Bucket: $BUCKET_NAME"

# Navigate to the frontend directory
cd ../frontend 

# Install dependencies
npm install

# Update the React app with the API URL
echo "VITE_API_BASE_URL=$API_URL" > .env

# Build and deploy frontend
npm run build

# Sync the build output to the S3 bucket
echo "Syncing build output to S3 bucket..."
aws s3 sync dist/ s3://$BUCKET_NAME/ --delete


echo "✅ Deployment complete. Your React app is now connected to the API and hosted on S3."
echo "🌐 You can access your app at: $CLOUDFRONT_URL"
echo "🔗 API endpoint: $API_URL"