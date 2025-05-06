import os
import json
import boto3
import logging

# Initialize clients
s3_client = boto3.client('s3')
sagemaker_runtime = boto3.client('sagemaker-runtime')

# Environment variables from SAM
UPLOADS_BUCKET = os.environ['UPLOADS_BUCKET']
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
SAGEMAKER_ENDPOINT = os.environ['resume-improver-t5-endpoint']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        # Step 1: Extract S3 object info from event
        record = event['Records'][0]
        bucket_name = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        logger.info(f"Triggered by file: s3://{bucket_name}/{object_key}")

        # Step 2: Download the uploaded resume from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        resume_text = response['Body'].read().decode('utf-8')

        # Step 3: Prepare payload for SageMaker endpoint
        prompt = f"Improve this resume text: {resume_text.strip()}"
        sm_payload = json.dumps({"inputs": prompt})

        # Step 4: Invoke SageMaker endpoint
        sm_response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT,
            ContentType='application/json',
            Body=sm_payload
        )

        result = json.loads(sm_response['Body'].read().decode('utf-8'))
        improved_text = result[0]['generated_text']

        logger.info(f"Improved resume content generated successfully.")

        # Step 5: Save the improved resume to OUTPUT_BUCKET
        improved_key = object_key.replace(".txt", "_improved.txt")
        s3_client.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=improved_key,
            Body=improved_text.encode('utf-8')
        )

        logger.info(f"Improved resume saved to s3://{OUTPUT_BUCKET}/{improved_key}")

        return {
            'statusCode': 200,
            'body': json.dumps('Resume improved and saved successfully!')
        }

    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
