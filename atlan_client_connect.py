from pyatlan.client.atlan import AtlanClient
import os

postgres_connection_name = 'postgres-ra'
snowflake_connection_name = 'snowflake-ra'
s3_connection_name = 'aws-s3-connection--atlan-tech-challenge-ra'

client = AtlanClient(
    base_url="https://tech-challenge.atlan.com/",
    api_key=os.getenv('ATLAN_API_KEY')
)