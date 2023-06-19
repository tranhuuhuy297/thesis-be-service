import boto3
import json
from util.logger_util import logger


class SQS:
    def __init__(self, region_name='ap-southeast-1', queue_name='test', fifo='true'):
        self.region_name = region_name
        self.queue_name = f'{queue_name}.fifo' if fifo == 'true' else queue_name
        self.fifo = fifo
        self.sqs_client = boto3.client("sqs", region_name=self.region_name)

    def create_queue(self):
        response = None
        try:
            response = self.sqs_client.create_queue(
                QueueName=self.queue_name,
                Attributes={'FifoQueue': self.fifo}
            )
        except Exception as e:
            logger.error(e)
            return response

        return response

    def get_queue_url(self):
        response = None
        try:
            response = self.sqs_client.get_queue_url(
                QueueName=self.queue_name,
            )
        except Exception as e:
            logger.error(e)
            return response

        return response["QueueUrl"]

    def send_message(self, message, group_id):
        response = None
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.get_queue_url(),
                MessageBody=json.dumps(message),
                MessageDeduplicationId=group_id,
                MessageGroupId=group_id
            )
        except Exception as e:
            logger.error(e)
            return response

        return response

    def receive_message(self):
        messages = []
        try:
            queue_url = self.get_queue_url()
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=5,
                WaitTimeSeconds=10,
            )
            messages = response.get('Messages', [])
            if len(messages) > 0:
                message_ids = [{
                    'Id': message['MessageId'],
                    'ReceiptHandle': message['ReceiptHandle']
                } for message in messages]
                self.sqs_client.delete_message_batch(QueueUrl=queue_url,
                                                     Entries=message_ids)
        except Exception as e:
            logger.error(e)
            return response

        return messages
