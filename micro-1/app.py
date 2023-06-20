from flask import Flask, render_template, request, redirect
import boto3
import json
import os

app = Flask(__name__)


# AWS SQS configuration
region = os.environ.get('region')
queue_url = os.environ.get('queue_url')


# Create an SQS client
sqs = boto3.client('sqs', region_name=region)

# Function to store data in SQS
def store_data_in_sqs(name, email, additional_data):
    data = {
        'name': name,
        'email': email,
        'additionalData': additional_data
    }

    message_body = json.dumps(data)

    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )

    return response

# Function to retrieve messages from SQS
def retrieve_messages_from_sqs():
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10
    )

    messages = response.get('Messages', [])

    return messages

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Store data route
@app.route('/store_data', methods=['POST'])
def store_data():
    name = request.form.get('name')
    email = request.form.get('email')
    additional_data = request.form.get('additional_data')

    response = store_data_in_sqs(name, email, additional_data)
    print("data insert sucessfully")

    return ("successfull")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    