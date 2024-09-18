from atlan_client_connect import client
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.assets import Asset, connection, Table, S3Object, Process, S3Bucket

def get_asset_guids(connection_qualified_name, asset_type):
    """Retrieves GUIDs of assets based on connection and type.

    Args:
        connection_qualified_name (str): Qualified name of the connection.
        asset_type (pyatlan.model.assets.Asset): Class representing the asset type (e.g., Table, S3Object).

    Returns:
        dict: Dictionary mapping asset names to their GUIDs.
    """
    try:
        request = (FluentSearch()
           .where(CompoundQuery.asset_type(asset_type))
           .where(CompoundQuery.active_assets())
            .where(Asset.CONNECTION_QUALIFIED_NAME.eq(connection_qualified_name))
        ).to_request()
        response = client.asset.search(request)  

        if asset_type == S3Bucket:
            return {asset.attributes.qualified_name for asset in response}
        elif 's3' in connection_qualified_name:
            return {((asset.name).split('.csv'))[0]: asset.guid for asset in response}
        else:
            return {asset.name: asset.guid for asset in response}


        '''if 's3' in connection_qualified_name:
            return {((asset.name).split('.csv'))[0]: asset.guid for asset in response}
        else:
            return {asset.name: asset.guid for asset in response}'''
    except Exception as e:
        print(f"Error retrieving asset GUIDs: {e}")
        return {}
