from get_connection_q_name import get_connection_qualified_name
from get_assets_guid import get_asset_guids
from get_lineage_count_by_guid import retrieve_lineage
from asset_lineage_creation import create_asset_lineage
from pyatlan.model.assets import Table, S3Object
from atlan_client_connect import postgres_connection_name, s3_connection_name, snowflake_connection_name


def retrieve_and_create_lineage(postgres_connection_name, snowflake_connection_name, s3_connection_name):
    """Retrieves asset GUIDs and creates lineages between them.

    Args:
        postgres_connection_name (str): Name of the Postgres connection.
        snowflake_connection_name (str): Name of the Snowflake connection.
        s3_connection_name (str): Name of the S3 connection.

    Returns:
        None
    """


    """
        Get connection qualified name for (postgres, s3, snowflake)
    
    """
    postgres_con_q_name = get_connection_qualified_name(postgres_connection_name, 'postgres')
    s3_con_q_name = get_connection_qualified_name(s3_connection_name, 's3')
    snowflake_con_q_name = get_connection_qualified_name(snowflake_connection_name, 'snowflake')

    if not postgres_con_q_name or not s3_con_q_name:
        return

    """
        Get GUID for Table & Objects
    """
    postgres_guid_dict = get_asset_guids(postgres_con_q_name, Table)
    s3_guid_dict = get_asset_guids(s3_con_q_name, S3Object)       
    snowflake_guid_dict = get_asset_guids(snowflake_con_q_name, Table)


    """
        Keeping postgres as primary sources
        Looping throug GUID of postgress and retrieving lineage
        retrieve_lineage will return count of depth
        If Depth = 0 - Meaning there is no lineage downwards
        If Depth = 2 - Meaning Postgres to S3 Lineage is established
        If Depth => 4 - Meaning Postgres - S3 - Snowflake - Total lineage is established - No more lineage needed.
        
    """

    for name, guid in postgres_guid_dict.items():
        count = retrieve_lineage(guid) # Retriveing Lineage Count

        s3id_guid = s3_guid_dict[name] # GUID of S3 (Based on name of Postgress)
        snow_guid = snowflake_guid_dict[name] # GUID of Snowflake (Based on name of Postgress)

        if count == 0: # create both lineage
            first_lineage = create_asset_lineage(postgres_con_q_name, guid, s3id_guid)
            if first_lineage == True:
                print('First Lineage Created')
                second_lineage = create_asset_lineage(s3_con_q_name, s3id_guid, snow_guid)
                if second_lineage == True:
                    print('Second Lineage Created')
        elif count == 2: # create second lineage
            second_lineage = create_asset_lineage(s3_con_q_name, s3id_guid, snow_guid)
            if second_lineage == True:
                    print('Only Second Lineage Created')
        elif count >= 4: #Lineage not required
            print("Lineage already been established on all assets")



"""
    Main function that will run the show.
"""
if __name__ == "__main__":
    retrieve_and_create_lineage(postgres_connection_name, snowflake_connection_name, s3_connection_name)