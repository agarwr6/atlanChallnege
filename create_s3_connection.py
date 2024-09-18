from pyatlan.cache.role_cache import RoleCache
from pyatlan.model.assets import Connection, S3Bucket, S3Object
from pyatlan.model.enums import AtlanConnectorType


def create_s3_connection(client):
    try:
        # Get the admin role GUID
        admin_role_guid = RoleCache.get_id_for_name("$admin")

        # Create the connection object
        connection = Connection.creator(
            name="aws-s3-connection--atlan-tech-challenge-ra",  # 
            connector_type=AtlanConnectorType.S3,  # 
            admin_roles=[admin_role_guid],  # 
            #admin_groups=["atlan-tech-challenge"],  #Enter pre exist group name
            admin_users=["agarwal.ro"],  #
        )

        # Save the connection using the Atlan client
        response = client.asset.save(connection)

        # Check for successful creation
        if response.is_successful():
            # Get the qualified name of the created connection
            connection_qualified_name = response.assets_created(asset_type=Connection)[0].qualified_name
            return connection_qualified_name
            print(f"Connection created successfully: {connection_qualified_name}")
        else:
            # Handle creation errors
            print(f"Error creating connection: {response.error}")

    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {e}")