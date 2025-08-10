import json
import boto3
import uuid
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("todos")

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']

    try:
        if http_method == 'GET' and path == '/todos':
            return get_todos()
        
        elif http_method == 'POST' and path == '/todos':
            body = json.loads(event['body'])
            return create_todo(body)

        elif http_method == 'PUT' and '/todos/' in path:
            todo_id = event['pathParameters']['id']
            body = json.loads(event['body'])
            return update_todo(todo_id, body)

        elif http_method == 'DELETE' and '/todos/' in path:
            todo_id = event['pathParameters']['id']
            return delete_todo(todo_id)
            
        else:
            return response(404, {"message": "Invalid request"})                        
    except Exception as e:    # Catch all errors (JSON parsing, missing event keys, etc.)
        return response(500, {"error": str(e)})
    
def get_todos():
    try:
        result = table.scan()
        return response(200, result["Items"])
    except ClientError as e:    # Catches/Handles only DynamoDB client errors
        return response(500, {"error": str(e)})
 
def create_todo(data):
    try:
        todo = {
            "id": str(uuid.uuid4()),
            "text": data["text"],
            "completed": False,
            "created_at": datetime.now().isoformat(),
        }
        table.put_item(Item=todo)
        return response(201, todo)    # Return the created todo item, not the DynamoDB response
    except ClientError as e:
        return response(500, {"error": str(e)})

def update_todo(todo_id, data):
    try:
        update_expression = "SET "
        expression_values = {}

        if "text" in data:
            update_expression += "text = :text, "
            expression_values[":text"] = data["text"]
        if "completed" in data:
            update_expression += "completed = :completed, "
            expression_values[":completed"] = data["completed"]

        # Remove trailing comma and space
        update_expression = update_expression.rstrip(", ")

        table.update_item(
            Key={"id": todo_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames={'#text': 'text'} if 'text' in data else {},
            ExpressionAttributeValues=expression_values
        )
        result = table.get_item(Key={"id": todo_id})
        return response(200, result["Item"])
    
    except ClientError as e:
        return response(500, {"error": str(e)}) 
    
def delete_todo(todo_id):
    try:
        table.delete_item(Key={"id": todo_id})
        return response(200, {"message": "Todo deleted successfully"})
    except ClientError as e:
        return response(500, {"error": str(e)})

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps(body, default=str)  # Use default=str to handle Decimal types
    }