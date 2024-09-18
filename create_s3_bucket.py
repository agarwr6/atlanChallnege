from pyatlan.model.assets import Connection, S3Bucket, S3Object

def createS3Bucket(client, s3_con_q_name):
    """
    Creates an S3 Bucket asset in Atlan.

    Args:
        client (AtlanClient): An instance of the Atlan client.
        connection_qualified_name (str): The qualified name of the connection asset
            used to access the S3 bucket.

    Returns:
        str: The qualified name of the created S3 Bucket asset, or None on error.

    Raises:
        Exception: If an unexpected error occurs.
    """

    try:
        # Create the S3Bucket object
        s3bucket = S3Bucket.creator(
            name="aws-s3-bucket--atlan-tech-challenge-ra",
            connection_qualified_name=s3_con_q_name,
            aws_arn="arn:aws:s3:::aws-s3-bucket--atlan-tech-challenge-ra"
        )

        # Save the S3 Bucket asset
        response = client.asset.save(s3bucket)

        # Check for successful creation
        if response.is_successful():
            # Get the qualified name of the created asset
            bucket_qualified_name = response.assets_created(asset_type=AssetType.S3_BUCKET)[0].qualified_name
            print(f"S3 Bucket created successfully: {bucket_qualified_name}")
            return bucket_qualified_name
        else:
            # Handle creation errors
            print(f"Error creating S3 Bucket: {response.error}")
            return None

    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None
