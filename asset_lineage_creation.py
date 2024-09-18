import random
from pyatlan.model.assets import Process, Table
from atlan_client_connect import client

def create_asset_lineage(qualified_connection, source_guid, destination_guid):
    """
    Creates an asset lineage in Atlan with error handling.

    Args:
        qualified_connection (str): The qualified connection name.
        source_guid (str): The GUID of the source table.
        destination_guid (str): The GUID of the destination table.

    Returns:
        bool: True if the asset lineage is created successfully, False otherwise.
    """

    try:
        # Determine process name based on connection type
        process_name = {
            "postgres": "ra postgres -> S3",
            "s3": "ra S3 -> snowflake"
        }.get(qualified_connection.split("/")[1], "Unknown Connection")

        # Generate unique process ID
        process_id = f"{process_name}_{random.randint(5, 100)}"

        # Create the process object
        process = Process.creator(
            name=process_name,
            connection_qualified_name=qualified_connection,
            process_id=process_id,
            inputs=[Table.ref_by_guid(guid=source_guid)],
            outputs=[Table.ref_by_guid(guid=destination_guid)]
        )

        # Save the process and handle potential errors
        response = client.asset.save(process)
        if not response:
            raise AtlanClientError("AtlanClient returned an empty response")

        # Validate asset creation and update information
        created_processes = response.assets_created(Process)
        assert len(created_processes) == 1, "Expected number of created processes"

        updated_tables = response.assets_updated(Table)
        assert len(updated_tables) == 1, "Expected number of updated tables"

        return True

    except (AtlanClientError, AssertionError) as e:
        print(f"Error creating asset lineage: {e}")
        return False

# Custom error class for AtlanClient-specific issues
class AtlanClientError(Exception):
    pass