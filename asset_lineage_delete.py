from atlan_client_connect import client
from pyatlan.model.fluent_search import CompoundQuery, FluentSearch
from pyatlan.model.assets import Process, Asset

postgres_connection_name = 'postgres-ra'
s3_connection_name = 'aws-s3-connection--atlan-tech-challenge-ra'

def delete_postgres_lineage(postgres_connection_name):
    connection_qualified_name = ''
    connection = client.asset.find_connections_by_name(
                name=postgres_connection_name,
                connector_type='postgres'
            )
    if connection:
        connection_qualified_name = connection[0]
        connection_qualified_name =  connection_qualified_name.attributes.qualified_name

    request = (FluentSearch()
            .where(CompoundQuery.asset_type(Process))
            .where(CompoundQuery.active_assets())
                .where(Asset.CONNECTION_QUALIFIED_NAME.eq(connection_qualified_name))
        ).to_request()
    response = client.asset.search(request)
    for asset in response:
        print(f'{asset.name}, {asset.guid}')
        delete = client.asset.purge_by_guid(guid=asset.guid)


def delete_s3_lineage(s3_connection_name):
    connection_qualified_name = ''
    connection = client.asset.find_connections_by_name(
                name=s3_connection_name,
                connector_type='s3'
            )
    if connection:
        connection_qualified_name = connection[0]
        connection_qualified_name =  connection_qualified_name.attributes.qualified_name

    request = (FluentSearch()
            .where(CompoundQuery.asset_type(Process))
            .where(CompoundQuery.active_assets())
                .where(Asset.CONNECTION_QUALIFIED_NAME.eq(connection_qualified_name))
        ).to_request()
    response = client.asset.search(request)
    for asset in response:
        print(f'{asset.name}, {asset.guid}')
        delete = client.asset.purge_by_guid(guid=asset.guid)


 
delete_postgres_lineage(postgres_connection_name)
delete_s3_lineage(s3_connection_name)