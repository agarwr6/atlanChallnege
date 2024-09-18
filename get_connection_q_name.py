from atlan_client_connect import client

def get_connection_qualified_name(connection_name, connector_type):
    """Retrieves the qualified name of a connection by name and type.

    Args:
        connection_name (str): Name of the connection.
        connector_type (str): Type of the connection (e.g., 'postgres', 'snowflake', 's3').

    Returns:
        str: The qualified name of the connection if found, None otherwise.
    """

    try:
        connection = client.asset.find_connections_by_name(
            name=connection_name,
            connector_type=connector_type
        )
        if connection:
            return connection[0].attributes.qualified_name
        else:
            print(f"Connection '{connection_name}' not found")
            return None
    except Exception as e:
        print(f"Error getting connection qualified name: {e}")
        return None


