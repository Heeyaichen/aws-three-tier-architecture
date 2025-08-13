import json
import boto3
import uuid
from botocore.exceptions import ClientError
from datetime import datetime, timezone
import os

if os.environ.get('AWS_SAM_LOCAL'):
    # In a local SAM environment, use the local DynamoDB endpoint
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
else:   
    dynamodb = boto3.resource("dynamodb")

# Initialize the DynamoDB table                   
table = dynamodb.Table("todos")

def lambda_handler(event, context):
    """
    Main entry point for the Lambda function.
    Routes requests based on HTTP method and path.
    """
    try:
        method = event.get('httpMethod')
        path_parameters = event.get('pathParameters') or {}
        todo_id = path_parameters.get('id')

        if method == 'GET' and not todo_id:
            return get_todos()

        elif method == 'POST' and not todo_id:
            body = json.loads(event['body'] or "{}")
            return create_todo(body)

        elif method == 'PUT' and todo_id:
            body = json.loads(event['body'] or "{}")
            return update_todo(todo_id, body)

        elif method == 'DELETE' and todo_id:
            return delete_todo(todo_id)
            
        else:
            return response(404, {"message": "Invalid request"})                        
    except Exception as e:    # Catch all errors (JSON parsing, missing event keys, etc.)
        return response(500, {"error": str(e)})
    
def get_todos():
    """
    Fetches all todo items from the DynamoDB table.
    """
    try:
        result = table.scan()
        return response(200, result["Items"])
    except ClientError as e:    # Catches/Handles only DynamoDB client errors
        return response(500, {"error": str(e)})
 
def create_todo(data):
    """
    Creates a new todo item in the DynamoDB table.
    """
    try:
        todo = {
            "id": str(uuid.uuid4()),
            "text": data["text"],
            "completed": False,
            "createdAt": now_iso_ms(),
        }
        table.put_item(Item=todo)
        return response(201, todo)    # Return the created todo item, not the DynamoDB response
    except ClientError as e:
        return response(500, {"error": str(e)})

def update_todo(todo_id, data):
    """
    Updates an existing todo item in the DynamoDB table.
    - Fixes the bug where update expression was not correctly constructed.
    - Uses ReturnValues='ALL_NEW' to get the updated item directly.
    """
    try:
        existing_item = table.get_item(Key={"id": todo_id})
        if 'Item' not in existing_item:
            return response(404, {"message": "Todo item not found"})
        
        update_expression = []
        expression_values = {}
        expression_names = {}

        if "text" in data:
            update_expression.append("#txt = :text")
            expression_values[":text"] = data["text"]
            expression_names["#txt"] = "text" 

        if "completed" in data:
            update_expression.append("#completed = :completed")
            expression_values[":completed"] = bool(data["completed"])
            expression_names["#completed"] = "completed"

        if not update_expression:
            return response(400, {"message": "No updatable fields provided"})

        # Remove trailing comma and space
        update_expression = "SET " + ", ".join(update_expression)

        params = {
            "Key": {"id": todo_id},
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_values,
            "ReturnValues": "ALL_NEW"
        }
        if expression_names:
            params["ExpressionAttributeNames"] = expression_names
            
        result = table.update_item(**params)

        # Preserve original createdAt in the response
        updated_item = result["Attributes"]
        updated_item["createdAt"] = existing_item["Item"]["createdAt"]

        return response(200, updated_item)

    except ClientError as e:
        return response(500, {"error": str(e)}) 
    
def delete_todo(todo_id):
    """
    Deletes a specific todo item.
    - Checks if the item exists before attempting to delete it.
    """
    try:
        result = table.get_item(Key={"id": todo_id})
        if 'Item' not in result:
            return response(404, {"message": "Todo item not found"})
        
        # Proceed to delete the item if it exists
        table.delete_item(Key={"id": todo_id})
        return response(200, {"message": "Todo item deleted successfully"})
    
    except ClientError as e:
        return response(500, {"error": str(e)})

def now_iso_ms():
    """Returns the current time in ISO 8601 format with milliseconds."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

def response(status_code, body):
    """
    Constructs a standardized API Gateway response.
    """
    if isinstance(body, dict) and "createdAt" in body:
        try:
            body["createdAt"] = datetime.fromisoformat(body["createdAt"].replace("Z", "+00:00")).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        except (ValueError, TypeError):
            pass

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