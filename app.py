from flask import Flask, request
import requests
import boto3
import json

BUCKET = 'tanvicsci5409assignment2'
OBJECT = 'tanvicsci5409assignment2.txt'
AWS_ACCESS_KEY_ID = 'ASIAX4HPI5JNSAMJJM5S'
AWS_SECRET_ACCESS_KEY = 'AHSZhy5D9DzGpbqAVGVzJd4UIGs1PhQHfiCnAg/A'
AWS_SESSION_TOKEN = 'FwoGZXIvYXdzEBYaDIt9aia4iT4rufquRiLAATBhyQwKwZf2BS1ltmd/ThNVSgIv8Td+Zc5caYsvTzFqSNDiqM3YnF1BqR5gNbUuOm9T6qs+MrP9avl2g4LIPCZyqtuiO+WanuXAzTmGjeXUNX9kWCWMpQSCnsscJJFZhUwVraYGX6+Q1cC/JOKchGlqUYFwx1rz70LaDG+ItSRc1C2h9hxRXtrjyNx79rWs6SKZ3B7f2AcTNy3IN87QvQlho7VCbR62t6GKOX3m1Hm1Z4DbqopJDK2TLt0wujCk7Cij2ouRBjItjUj4qHyHLDB19ZUTDlcpC9jEJZkcdMShZzwPIQqeptPT3EpdsoDVUvo9DKYJ'
BANNER_ID = 'B00875949'
EC2_IPADDRESS = '54.226.247.98:5000'

app = Flask(__name__)

@app.route('/')
def begin():
    appInput = {
        "banner": BANNER_ID,
        "ip": EC2_IPADDRESS
    }
    response = requests.post('http://3.88.132.229:80/begin', json=appInput)
    return response.text


@app.route('/storedata', methods=['POST'])
def storeData():
    aws_session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN
    )

    s3_session = aws_session.resource('s3')
    s3_object = s3_session.Object(BUCKET, OBJECT)
    data = request.json
    s3_object.put(Body=data['data'], ACL='public-read')

    return json.dumps({
        "s3uri": "https://" + BUCKET + ".s3.amazonaws.com/" + OBJECT
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
