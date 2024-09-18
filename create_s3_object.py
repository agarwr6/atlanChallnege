

def create_s3_object(client, object_name, connection_qualified_name, bucket_qualified_name):
    """
    Creates an S3 Object asset in Atlan.

    Args:
        client (AtlanClient): An instance of the Atlan client.
        object_name (str): The name of the S3 object.
        connection_qualified_name (str): The qualified name of the connection asset
            used to access the S3 bucket.
        bucket_qualified_name (str): The qualified name of the S3 Bucket asset.

    Returns:
        None: This function does not return a value, it prints success or error messages.

    Raises:
        Exception: If an unexpected error occurs.
    """

    try:
        #print(client, object_name, connection_qualified_name, bucket_qualified_name)
        # Create the S3Object object
        s3object = S3Object.creator(
            name=object_name,
            connection_qualified_name=connection_qualified_name,
            aws_arn=f"{bucket_qualified_name}-{object_name}",
            s3_bucket_qualified_name=bucket_qualified_name
        )

        # Save the S3 Object asset
        response = client.asset.save(s3object)

        # Check for successful creation
        if response.is_successful():
            print(f"S3 Object '{object_name}' created successfully.")
        else:
            # Handle creation errors
            print(f"Error creating S3 Object '{object_name}': {response.error}")

    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")