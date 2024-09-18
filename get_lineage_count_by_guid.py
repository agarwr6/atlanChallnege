from pyatlan.model.enums import LineageDirection
from pyatlan.model.assets import Asset
from pyatlan.model.lineage import FluentLineage
from atlan_client_connect import client

def retrieve_lineage(guid):
    """Retrieves the lineage count for a given asset GUID.

    Args:
        guid (str): The GUID of the asset.

    Returns:
        int: The number of downstream assets in the lineage, or None if an error occurs.
    """

    try:
        count = 0
        request = FluentLineage(
            starting_guid=guid,
            depth=1000000,
            direction=LineageDirection.DOWNSTREAM,
            size=10,
            includes_on_results=Asset.NAME
        ).request
        response = client.asset.get_lineage_list(request)
        for asset in response:
            count += 1
        return count

    except Exception as e:
        print(f"Error retrieving lineage for asset {guid}: {e}")
        return None