#!/bin/bash

echo "🗑️  Starting cleanup of AWS resources..."

# Get bucket names from CloudFormation stack
echo "📦 Getting S3 bucket names..."
FRONTEND_BUCKET=$(aws cloudformation describe-stacks --stack-name sam-app --query "Stacks[0].Outputs[?OutputKey=='S3BucketName'].OutputValue" --output text 2>/dev/null || echo "")
SAM_BUCKET=$(aws s3 ls | grep "aws-sam-cli-managed-default-samclisourcebucket" | awk '{print $3}' | head -1)

# Empty frontend bucket
if [ ! -z "$FRONTEND_BUCKET" ]; then
    echo "🧹 Emptying frontend bucket: $FRONTEND_BUCKET"
    aws s3 rm s3://$FRONTEND_BUCKET --recursive
    echo "✅ Frontend bucket emptied"
else
    echo "⚠️  Frontend bucket not found or already deleted"
fi

# Empty SAM managed bucket
if [ ! -z "$SAM_BUCKET" ]; then
    echo "🧹 Emptying SAM managed bucket: $SAM_BUCKET"
    aws s3 rm s3://$SAM_BUCKET --recursive
    echo "✅ SAM bucket emptied"
else
    echo "⚠️  SAM managed bucket not found"
fi

# Delete CloudFormation stack
echo "🔥 Deleting CloudFormation stack: sam-app"
aws cloudformation delete-stack --stack-name sam-app

# Wait for stack deletion to complete
echo "⏳ Waiting for stack deletion to complete..."
aws cloudformation wait stack-delete-complete --stack-name sam-app

# Check if deletion was successful
STACK_STATUS=$(aws cloudformation describe-stacks --stack-name sam-app --query 'Stacks[0].StackStatus' --output text 2>/dev/null || echo "DELETED")

if [ "$STACK_STATUS" = "DELETED" ]; then
    echo "✅ Stack deleted successfully"
else
    echo "❌ Stack deletion failed. Status: $STACK_STATUS"
    exit 1
fi

# Clean up local build artifacts
echo "🧹 Cleaning up local build artifacts..."
rm -rf sam-app/.aws-sam/
rm -f frontend/.env

echo "🎉 Cleanup complete!"
echo "📋 Summary:"
echo "   - Frontend bucket emptied and deleted"
echo "   - SAM managed bucket emptied"
echo "   - CloudFormation stack deleted"
echo "   - Local build artifacts cleaned"
