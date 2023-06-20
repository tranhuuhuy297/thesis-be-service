from util.pinecone import Pinecone
from util.sqs import SQS
from dotenv import load_dotenv
from util.s3_util import S3

load_dotenv(dotenv_path='.env')

sqs = SQS()
s3_image = S3(bucket_name='image')
pinecone = Pinecone()
