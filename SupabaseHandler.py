import psycopg2
    
    
#Add supabase connection string here
conn_string = "<connection string>"

def get_keys(namespace, group_id):
    """
    Fetches a list of keys from the upsertion_record table based on the namespace and group_id.

    Args:
        namespace (str): The namespace to filter.
        group_id (str): The group_id to filter.

    Returns:
        list: A list of keys matching the criteria.
    """
    # Database connection string

    try:
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # SQL query to fetch keys based on namespace and group_id
        query = """
       SELECT key FROM upsertion_record
        WHERE namespace = %s AND group_id = %s
        ORDER BY updated_at;
        """

        # Execute the query
        cursor.execute(query, (namespace, group_id))

        # Fetch all results
        results = cursor.fetchall()

        # Extract keys from the results
        keys = [row[0] for row in results]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return keys

    except Exception as e:
        print(f"Error: {e}")
        return []

def get_all_group_ids(namespace):
    """
    Fetches a list of all unique group_id values from the upsertion_record table filtered by namespace.

    Args:
        namespace (str): The namespace to filter.

    Returns:
        list: A list of all unique group_id values matching the namespace.
    """
    # Database connection string

    try:
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # SQL query to fetch all unique group_id values filtered by namespace
        query = """
        SELECT DISTINCT group_id FROM upsertion_record
        WHERE namespace = %s;
        """

        # Execute the query
        cursor.execute(query, (namespace,))

        # Fetch all results
        results = cursor.fetchall()

        # Extract group_ids from the results
        group_ids = [row[0] for row in results]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return group_ids

    except Exception as e:
        print(f"Error: {e}")
        return []



def delete_record_by_key(namespace, key):
    """
    Deletes a record from the upsertion_record table based on the namespace and key.

    Args:
        namespace (str): The namespace to filter.
        key (str): The key of the record to delete.

    Returns:
        bool: True if the record was deleted successfully, False otherwise.
    """
    # Database connection string

    try:
        # Connect to the database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        # SQL query to delete the record based on namespace and key
        query = """
        DELETE FROM upsertion_record
        WHERE namespace = %s AND key = %s;
        """

        # Execute the query
        cursor.execute(query, (namespace, key))

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


# namespace = "supabase/empty_new"

# group_ids = get_all_group_ids(namespace)

# # Example usage
# group_id = group_ids[1]

# keys = get_keys(namespace, group_id)
# print("Keys:", len(keys))

# print("Group IDs:", group_ids)
