# AWS Three-Tier Serverless Todo Application

A modern, serverless three-tier web application built on AWS, demonstrating best practices for cloud-native architecture using React, AWS Lambda, API Gateway, DynamoDB, S3, and CloudFront.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Architecture Deep Dive](#architecture-deep-dive)
- [IAM Roles & Permissions](#iam-roles--permissions)
- [Service Interactions](#service-interactions)
- [Deployment](#deployment)
- [Cleanup](#cleanup)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🏗️ Architecture Overview

This application implements a **three-tier serverless architecture** on AWS:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Presentation   │    │   Application    │    │      Data       │
│      Tier       │    │      Tier        │    │      Tier       │
├─────────────────┤    ├──────────────────┤    ├─────────────────┤
│   React SPA     │    │   AWS Lambda     │    │   DynamoDB      │
│   S3 Bucket     │◄──►│   API Gateway    │◄──►│   NoSQL DB      │
│   CloudFront    │    │   Python 3.13    │    │   Pay-per-use   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Features
- ✅ **Serverless**: No server management required
- ✅ **Scalable**: Auto-scaling based on demand
- ✅ **Cost-effective**: Pay only for what you use
- ✅ **Secure**: IAM-based access control
- ✅ **Fast**: Global CDN distribution
- ✅ **Modern**: React SPA with responsive design

## 📁 Project Structure

```
aws-three-tier-architecture/
├── frontend/                    # Presentation Tier (React SPA)
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── TodoForm.jsx   # Todo creation/editing form
│   │   │   ├── TodoItem.jsx   # Individual todo item
│   │   │   └── TodoList.jsx   # Todo list container
│   │   ├── App.jsx            # Main application component
│   │   └── main.jsx           # Application entry point
│   ├── package.json           # Dependencies and scripts
│   └── vite.config.js         # Vite build configuration
├── sam-app/                    # Application & Data Tiers (SAM)
│   ├── todo_function/         # Lambda function code
│   │   ├── app.py            # Main Lambda handler
│   │   └── requirements.txt  # Python dependencies
│   ├── events/               # Test events for local development
│   ├── tests/                # Unit and integration tests
│   └── template.yaml         # SAM/CloudFormation template
├── deploy.sh                  # Automated deployment script
└── delete.sh                 # Cleanup script
```

## 🔧 Prerequisites

### Required Tools & Technologies

1. **AWS CLI** - Configure AWS credentials
   ```bash
   aws configure
   ```
   - [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. **AWS SAM CLI** - Deploy serverless applications
   ```bash
   # macOS
   brew install aws-sam-cli
   
   # Windows/Linux
   # Follow: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
   ```

3. **Node.js & npm** - Frontend development
   ```bash
   node --version  # v18+ recommended
   npm --version
   ```
   - [Node.js Download](https://nodejs.org/)

4. **Python 3.13** - Lambda runtime
   ```bash
   python3 --version
   ```

### AWS Account Requirements
- Active AWS account with appropriate permissions
- IAM user with programmatic access
- Sufficient service limits for:
  - Lambda functions
  - API Gateway APIs
  - DynamoDB tables
  - S3 buckets
  - CloudFront distributions

## 🚀 Getting Started

### Quick Deployment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aws-three-tier-architecture
   ```

2. **Make deployment script executable**
   ```bash
   chmod +x deploy.sh
   ```

3. **Deploy the application**
   ```bash
   ./deploy.sh
   ```

4. **Access your application**
   - The script will output the CloudFront URL
   - Open the URL in your browser

### Manual Deployment

If you prefer manual deployment:

1. **Deploy SAM application**
   ```bash
   cd sam-app
   sam build
   sam deploy --guided
   ```

2. **Build and deploy frontend**
   ```bash
   cd ../frontend
   npm install
   npm run build
   
   # Upload to S3 (replace with your bucket name)
   aws s3 sync dist/ s3://your-bucket-name --delete
   ```

## 🏛️ Architecture Deep Dive

### Presentation Tier
- **Technology**: React 18 with Vite
- **Hosting**: Amazon S3 static website hosting
- **CDN**: Amazon CloudFront for global distribution
- **Features**: 
  - Single Page Application (SPA)
  - Responsive design
  - Environment-based API configuration

### Application Tier
- **Compute**: AWS Lambda (Python 3.13)
- **API**: Amazon API Gateway (REST API)
- **Features**:
  - Serverless compute
  - Auto-scaling
  - CORS enabled
  - RESTful API design

### Data Tier
- **Database**: Amazon DynamoDB
- **Configuration**: 
  - Pay-per-request billing
  - Single table design
  - Partition key: `id` (String)

## 🔐 IAM Roles & Permissions

### Lambda Execution Role

The SAM template automatically creates an IAM role for the Lambda function with these policies:

#### 1. DynamoDBCrudPolicy
```yaml
Policies: 
  - DynamoDBCrudPolicy:
      TableName: !Ref DynamoDBTable
```
**Purpose**: Grants Lambda function permissions to perform CRUD operations on the DynamoDB table.

**AWS Managed Policy**: Provides these permissions:
- `dynamodb:GetItem` - Read individual items
- `dynamodb:PutItem` - Create new items
- `dynamodb:UpdateItem` - Modify existing items
- `dynamodb:DeleteItem` - Remove items
- `dynamodb:Scan` - Read all items
- `dynamodb:Query` - Query items with conditions

**Documentation**: [DynamoDB IAM Policies](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/using-identity-based-policies.html)

#### 2. AWSLambdaBasicExecutionRole
```yaml
Policies:
  - AWSLambdaBasicExecutionRole
```
**Purpose**: Provides basic Lambda execution permissions.

**AWS Managed Policy**: Includes:
- `logs:CreateLogGroup` - Create CloudWatch log groups
- `logs:CreateLogStream` - Create log streams
- `logs:PutLogEvents` - Write logs to CloudWatch

**Documentation**: [Lambda Execution Role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)

### CloudFront Origin Access Control (OAC)

#### S3 Bucket Policy
```yaml
CloudFrontS3AccessBucketPolicy:
  Type: AWS::S3::BucketPolicy
  Properties:
    PolicyDocument:
      Statement:
        - Effect: Allow
          Principal: 
            Service: cloudfront.amazonaws.com
          Action: s3:GetObject
          Resource: !Sub "arn:aws:s3:::${FrontendBucket}/*"
          Condition:
            StringEquals:
              AWS:SourceArn: !Sub "arn:aws:cloudfront::${AWS::AccountId}:distribution/${CloudFrontDistribution}"
```

**Purpose**: Allows CloudFront to access S3 bucket objects while keeping the bucket private.

**Security Benefits**:
- S3 bucket remains private (no public access)
- Only CloudFront can access bucket contents
- Prevents direct S3 access bypassing CloudFront

**Documentation**: [CloudFront OAC](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)

## 🔄 Service Interactions

### Complete Request Flow

#### 1. User Interaction → CloudFront
```
User Browser → CloudFront Distribution
```
- User accesses application via CloudFront URL
- CloudFront serves cached content when possible
- Routes requests based on path patterns

#### 2. Static Content Delivery
```
CloudFront → S3 Bucket (via OAC)
```
**Configuration in template.yaml:**
```yaml
Origins:
  - Id: S3Origin
    DomainName: !GetAtt FrontendBucket.RegionalDomainName
    OriginAccessControlId: !GetAtt OriginAccessControl.Id
```
- React SPA files served from S3
- OAC ensures secure access
- Cached globally for performance

#### 3. API Request Routing
```
CloudFront → API Gateway → Lambda → DynamoDB
```

**CloudFront Cache Behavior:**
```yaml
CacheBehaviors:
- PathPattern: "/api/*"
  TargetOriginId: ApiOrigin
  MinTTL: 0
  DefaultTTL: 0
  MaxTTL: 0  # No caching for API calls
```

**API Gateway Integration:**
```yaml
Origins:
  - Id: ApiOrigin
    DomainName: !Sub "${TodoAPI}.execute-api.${AWS::Region}.amazonaws.com"
    OriginPath: "/prod"
```

#### 4. Lambda Function Routing
**Event Configuration in template.yaml:**
```yaml
Events:
  GetTodos:
    Type: Api
    Properties:
      RestApiId: !Ref TodoAPI
      Path: /api/todos
      Method: get
```

**Lambda Handler Logic:**
```python
def lambda_handler(event, context):
    method = event.get('httpMethod')
    path_parameters = event.get('pathParameters') or {}
    todo_id = path_parameters.get('id')
    
    if method == 'GET' and not todo_id:
        return get_todos()
    elif method == 'POST' and not todo_id:
        return create_todo(body)
    # ... other routes
```

#### 5. DynamoDB Operations
**Table Configuration:**
```yaml
DynamoDBTable:
  Type: AWS::DynamoDB::Table
  Properties:
    TableName: todos
    AttributeDefinitions:
      - AttributeName: id 
        AttributeType: S
    KeySchema:
      - AttributeName: id
        KeyType: HASH
    BillingMode: PAY_PER_REQUEST
```

**Lambda DynamoDB Access:**
```python
# Initialize DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("todos")

# CRUD operations
def get_todos():
    result = table.scan()
    return response(200, result["Items"])

def create_todo(data):
    todo = {
        "id": str(uuid.uuid4()),
        "text": data["text"],
        "completed": False,
        "createdAt": now_iso_ms(),
    }
    table.put_item(Item=todo)
    return response(201, todo)
```

### Environment Variables & Configuration

**SAM Template Global Variables:**
```yaml
Globals:
  Function:
    Environment:
      Variables:
        BUCKET_NAME: !Ref BucketName
        TABLE_NAME: !Ref DynamoDBTable
```

**React Environment Configuration:**
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";
```

## 📦 Deployment

### Automated Deployment Script

The [`deploy.sh`](./deploy.sh) script automates the entire deployment process:

```bash
#!/bin/bash
set -e

echo "🚀 Starting deployment of AWS Three-Tier Architecture..."

# 1. Deploy SAM application
cd sam-app
echo "📦 Building and deploying SAM application..."
sam build
sam deploy

# 2. Extract CloudFormation outputs
echo "📋 Extracting deployment outputs..."
STACK_NAME=$(grep stack_name samconfig.toml | cut -d'"' -f2)
API_URL=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`TodoApiUrl`].OutputValue' --output text)
CLOUDFRONT_URL=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontUrl`].OutputValue' --output text)
S3_BUCKET=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' --output text)

# 3. Build and deploy frontend
cd ../frontend
echo "🏗️  Building React application..."
echo "VITE_API_BASE_URL=$CLOUDFRONT_URL/api" > .env.production
npm install
npm run build

# 4. Upload to S3
echo "☁️  Uploading to S3..."
aws s3 sync dist/ s3://$S3_BUCKET --delete

echo "✅ Deployment completed successfully!"
echo "🌐 Application URL: $CLOUDFRONT_URL"
```

**Key Features:**
- Builds and deploys SAM application
- Extracts CloudFormation outputs
- Configures React environment variables
- Uploads built frontend to S3
- Provides final application URL

### Manual Deployment Steps

1. **Deploy Backend Infrastructure**
   ```bash
   cd sam-app
   sam build
   sam deploy --guided
   ```

2. **Configure Frontend Environment**
   ```bash
   cd ../frontend
   echo "VITE_API_BASE_URL=https://your-cloudfront-url/api" > .env.production
   ```

3. **Build and Deploy Frontend**
   ```bash
   npm install
   npm run build
   aws s3 sync dist/ s3://your-bucket-name --delete
   ```

## 🧹 Cleanup

### Automated Cleanup Script

The [`delete.sh`](./delete.sh) script safely removes all AWS resources:

```bash
#!/bin/bash
set -e

echo "🗑️  Starting cleanup of AWS Three-Tier Architecture..."

cd sam-app
STACK_NAME=$(grep stack_name samconfig.toml | cut -d'"' -f2)

# 1. Empty S3 bucket (required before deletion)
echo "🪣 Emptying S3 bucket..."
S3_BUCKET=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`S3BucketName`].OutputValue' --output text)
aws s3 rm s3://$S3_BUCKET --recursive

# 2. Delete CloudFormation stack
echo "☁️  Deleting CloudFormation stack..."
sam delete --stack-name $STACK_NAME

echo "✅ Cleanup completed successfully!"
```

**Important**: S3 buckets must be empty before CloudFormation can delete them.

### Manual Cleanup

1. **Empty S3 Bucket**
   ```bash
   aws s3 rm s3://your-bucket-name --recursive
   ```

2. **Delete SAM Stack**
   ```bash
   cd sam-app
   sam delete
   ```

## 📚 API Documentation

### Base URL
```
https://your-cloudfront-url/api
```

### Endpoints

#### GET /todos
Retrieve all todos
```bash
curl https://your-cloudfront-url/api/todos
```

**Response:**
```json
[
  {
    "id": "uuid",
    "text": "Sample todo",
    "completed": false,
    "createdAt": "2024-01-01T00:00:00.000Z"
  }
]
```

#### POST /todos
Create a new todo
```bash
curl -X POST https://your-cloudfront-url/api/todos \
  -H "Content-Type: application/json" \
  -d '{"text": "New todo item"}'
```

#### PUT /todos/{id}
Update an existing todo
```bash
curl -X PUT https://your-cloudfront-url/api/todos/uuid \
  -H "Content-Type: application/json" \
  -d '{"text": "Updated text", "completed": true}'
```

#### DELETE /todos/{id}
Delete a todo
```bash
curl -X DELETE https://your-cloudfront-url/api/todos/uuid
```

## 🔧 Troubleshooting

### Common Issues

#### 1. CORS Errors
**Symptom**: Browser console shows CORS errors
**Solution**: Verify API Gateway CORS configuration in template.yaml

#### 2. 403 Forbidden on S3
**Symptom**: CloudFront returns 403 for static files
**Solution**: Check S3 bucket policy and OAC configuration

#### 3. Lambda Function Errors
**Symptom**: 500 errors from API
**Solution**: Check CloudWatch logs for Lambda function

#### 4. DynamoDB Access Denied
**Symptom**: Lambda cannot access DynamoDB
**Solution**: Verify IAM role has DynamoDBCrudPolicy

### Debugging Commands

```bash
# Check SAM deployment status
sam list stack-outputs

# View Lambda logs
sam logs -n TodoFunction --stack-name your-stack-name

# Test Lambda function locally
sam local start-api

# Validate SAM template
sam validate
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📖 Additional Resources

### AWS Documentation
- [AWS SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
- [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/)
- [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- [Amazon DynamoDB](https://docs.aws.amazon.com/dynamodb/)
- [Amazon S3](https://docs.aws.amazon.com/s3/)
- [Amazon CloudFront](https://docs.aws.amazon.com/cloudfront/)

### Best Practices
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Serverless Application Lens](https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)

---

**Built with ❤️ using AWS Serverless Technologies**