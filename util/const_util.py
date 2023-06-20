import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
# aws
AWS_CDN = os.getenv('AWS_CDN')
# pinecone
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_ENV')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
PINECONE_NAMESPACE_USER = os.getenv('PINECONE_NAMESPACE_USER')
# openai
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# sqs
SQS_NAME = os.getenv('SQS_NAME')
