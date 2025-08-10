#!/bin/bash

# Deploy the SAM application
cd sam-app
sam build && sam deploy --guided

# Get API URL
API_URL = $(aws cloudformation describe-stacks --stack-name TodoAppStack --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text)

# Update the React app with the API URL
# sed -i '' "s|const API_BASE_URL = '.*';|const API_BASE_URL = '$API_URL';|" ../frontend/src/App.
cd ../frontend
echo "VITE_API_BASE_URL=$API_URL" > .env

# Build and deploy frontend
npm run build

aws s3 sync dist/ s3://react-spa-frontend/ --delete

echo "Deployment complete. Your React app is now connected to the API at $API_URL."