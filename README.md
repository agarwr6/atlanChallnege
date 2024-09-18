# Delta Arc Corp ETL Pipeline Visualization on Atlan

This document guides you through a custom solution for visualizing the ETL pipeline in Delta Arc Corp on Atlan. The pipeline currently flows data from Postgres to S3, then to Snowflake, and ultimately to Looker.

**Challenge:**

To enable users to view and understand the entire pipeline on Atlan, we need to:

1- Catalog S3 Objects: Ingest the objects within the provided S3 bucket as assets on Atlan.

2- Establish Lineage: Define the relationships between the S3 assets, existing Postgres assets, and Snowflake assets. Currently, Atlan has native connectors for Postgres, Snowflake, and Looker, but not for S3.

**Solution**
# This project utilizes the Atlan SDK (available in Java or Python) to address the challenge:

**Part 1**
**S3 Object Ingestion:** 
    1- Use file **S3_check_create.py** - In this file I have performed 3 operations

        a- Check if S3 Connection exist in Atlan
            i - If not exist create it
        b- Check if S3 Bucket exist in Atlan 
            i - If not exist create it
        c- Check if S3 Objects exists in Atlan
            i - If not exist
                i - Retrieve AWS Objects from pulic S3 bucket -  https://atlan-tech-challenge.s3.amazonaws.com
                ii- Ingest asset from public bucket in Atlan Bucket.
        
    2- Once you run the file you will get below o/p -:
        (.venv) C:\Users\Rohit Agarwal\Desktop\Atlan_Challenge>python S3_check_create.py
        S3 Connection Already Exist
        S3 Bucket Already Exist
        S3 Objects Already Exist

    3- As you can see everything is already set up. you can search the same in Atlan instance by visiting
        a- https://tech-challenge.atlan.com/assets
        b- use S3 connection name as - aws-s3-connection--atlan-tech-challenge-ra
        c- you will see (1 connection, 1 Bucket, 8 Objects, 8 Process(for lineage I will explain in part 2))


**Part 2**
**Lineage Establishment**
    1- Use file **asset_lineage_check_create.py** - This file will check and automatically create downstream lineage from end to end
    **Note** As of now all lineage has been establish so if you run this file you will probably see o/p below - 
        (.venv) C:\Users\Rohit Agarwal\Desktop\Atlan_Challenge>python asset_lineage_check_create.py 
        Lineage already been established on all assets
        Lineage already been established on all assets
        Lineage already been established on all assets
        Lineage already been established on all assets
        Lineage already been established on all assets
        Lineage already been established on all assets
        Lineage already been established on all assets
        Lineage already been established on all assets
    
    2- In order to see the action in real time  (**optional**)
        a- **asset_lineage_delete.py** -  run this file and it will delete all the lineages (upstream & downstream) - This is very raw file and can be optimized.
        b- run **asset_lineage_check_create.py** - This will create the lineages again for all the objects (Postgres - S3 - Snowflake) and o/p will look like this - 
                (.venv) C:\Users\Rohit Agarwal\Desktop\Atlan_Challenge>python asset_lineage_check_create.py
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
                    First Lineage Created
                    Second Lineage Created
    
    3- First lineage created - Means Postgres - S3 / Second Lineage Created meaning - S3 - Snowflake.

**Working of this file** - #Note we are assuming all the connections & Objects are already established in Atlan Instance. The role of this file to create lineage.
    1- In this file I have performed various operations using different libraries of Atlan SDK
        main function will do following steps
        a- Retrieve connection qualified name for (Postgres, S3, Snowflake) - File name - **get_connection_q_name.py**
        b- Retrieve all the assets GUID from Table and Object of (Postgress, S3, Snowgflake) - File Name - **get_assets_guid,py**
        c- Traverse lineage using Postgres as main and get the count of depth - This will get us if lineage is present or not. **get_lineage_count_by_guid.py**
        d- Then perform lineage creattion operation based on depth we got above. File Name - **asset_lineage_creation.py**
            i- If depth is 0 = Then create both lineage
            ii- If depth is 2 = then create s3 - snowflake lineage
            iii-If depth is 4 = Lineage already been establishged.
    2- The project libraries are running in virtual env.

**Prerequisites:**
1- An Atlan instance with access to the Postgres and Snowflake assets already established.
2- The S3 bucket containing the data objects: https://atlan-tech-challenge.s3.amazonaws.com/
3- The chosen Atlan SDK (Java or Python) installed with appropriate configuration.

**Execution Steps Prep Work - Scripts will not run before doing these below steps**
1- In **atlan_client_connect.py** use your own API KEY - Mine is stored in ENV Variables.
2- In order to access Public AWS Bucket you need to install BOTO3 library. Make sure to keep your client secret and Client Token handy.You can retrieve it from IAMUSER in aws console. Mine is stored in my local dir = C:\Users\Rohit Agarwal\.aws as (credentials)
3- Once above 2 is done.
    i- Run **S3_check_create.py** - to establish s3 connection, bucket, objects
    ii- Run **asset_lineage_check_create.py** to create lineages.
    **Note** (Optional)- you can first delete lineage by running **raw file - asset_lineage_delete.py**

**Expected Outcome**
    Upon successful execution, the S3 objects will be represented as assets on Atlan and their relationships with the existing Postgres and Snowflake assets will be defined as lineage connections. This allows users to visualize the complete ETL pipeline within Atlan.


**By following these steps, you can create a custom solution to visualize the Delta Arc Corp ETL pipeline on Atlan, empowering users to understand data flow and dependencies.**
