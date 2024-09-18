from pyatlan.cache.role_cache import RoleCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, S3Bucket, S3Object
from pyatlan.model.enums import AtlanConnectorType
from atlan_client_connect import client, s3_connection_name
from get_connection_q_name import get_connection_qualified_name
from get_assets_guid import get_asset_guids
from create_s3_connection import create_s3_connection
from create_s3_bucket import createS3Bucket
from create_s3_object import create_s3_object
import boto3
import botocore.exceptions

BUCKET_NAME = 'atlan-tech-challenge'

s3 = boto3.client('s3', region_name='us-east-1')



def s3_object_lifecycle(bucket_name, s3_connection_name): #rename to create objects
    try:

        # first check if Atlan s3 connection, bucket, object is available or not
        s3_con_q_name = get_connection_qualified_name(s3_connection_name, 's3')
        bucket_q_name = get_asset_guids(s3_con_q_name, S3Bucket)
        s3_guid_dict = get_asset_guids(s3_con_q_name, S3Object) 

        # create s3 connection
        if len(s3_con_q_name) == 0:
            create_s3_connection(client)
        else:
            print('S3 Connection Already Exist')

        if len(bucket_q_name) == 0:
            #create bucket
            s3_q_name = get_connection_qualified_name(s3_connection_name, 's3')
            create_bucket = createS3Bucket(client, s3_q_name)
        else:
            print('S3 Bucket Already Exist')

        if len(s3_guid_dict) == 0:
        # get Objects from AWS S3 link provided - https://atlan-tech-challenge.s3.amazonaws.com/
            buckets_resp = s3.list_objects_v2(Bucket=BUCKET_NAME)
            if 'Contents' in buckets_resp:
                for bucket in buckets_resp["Contents"]:
                    print(bucket['Key'])
                    create_s3_object(client, bucket['Key'], s3_q_name, create_bucket)
            else:
                print(f"Bucket from AWS Client {bucket_name} is empty.")
        else:
            print('S3 Objects Already Exist')

    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"An error occurred: {error_code}")    

if __name__ == "__main__":
    s3_object_lifecycle(BUCKET_NAME, s3_connection_name)