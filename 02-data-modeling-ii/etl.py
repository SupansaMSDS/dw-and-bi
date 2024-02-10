import glob
import json
import os
from typing import List

from cassandra.cluster import Cluster


#Drop table to run next time
table_drop = "DROP TABLE events"

table_create = """
    CREATE TABLE IF NOT EXISTS events
    (
        id                  text,
        created_at          text,
        type                text,
        actor_id            text,
        actor_login         text,
        repo_id             text,
        repo_name           text,
        PRIMARY KEY ((type), actor_login)
    )
"""

create_table_queries = [
    table_create,
]
drop_table_queries = [
    table_drop,
]

def drop_tables(session):
    for query in drop_table_queries:
        try:
            rows = session.execute(query)
        except Exception as e:
            print(e)


def create_tables(session):
    for query in create_table_queries:
        try:
            session.execute(query)
        except Exception as e:
            print(e)

#Function pull data from .json 
def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def process(session, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            for each in data:

                # Insert data into tables here
                try:
                    query = """
                    INSERT INTO events (
                        id, 
                        type, 
                        created_at, 
                        actor_id, 
                        actor_login, 
                        repo_id, 
                        repo_name
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    session.execute(query, 
                                    (each["id"], each["type"], 
                                    each["created_at"], each["actor"]["id"], 
                                    each["actor"]["login"], each["repo"]["id"], 
                                    each["repo"]["name"]))
                
                except:
                    query = f"""
                    INSERT INTO events (
                        id, 
                        type, 
                        created_at, 
                        actor_id, 
                        actor_login, 
                        repo_id, 
                        repo_name
                    ) 
                    VALUES ('{each["id"]}', 
                            '{each["type"]}', 
                            '{each["created_at"]}', 
                            '{each["actor"]["id"]}', 
                            '{each["actor"]["login"]}', 
                            '{each["repo"]["id"]}', 
                            '{each["repo"]["name"]}'
                    )
                    """
                    session.execute(query)

event_types = ['IssuesEvent','PullRequestReviewCommentEvent','CreateEvent','PullRequestEvent','PushEvent','PublicEvent',
               'WatchEvent','DeleteEvent','PullRequestReviewEvent','ReleaseEvent', 'IssueCommentEvent']

#connect to cassandra 
def main():
    cluster = Cluster(['127.0.0.1'])  # set IP: 127.0.0.1, port: 9042
    session = cluster.connect()  # connect to session in cassandra

    # Create keyspace 
    try:
        session.execute(
            """
            CREATE KEYSPACE IF NOT EXISTS github_events
            WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
            """
        )
    except Exception as e:
        print(e)

    # Set keyspace, table, query
    try:
        session.set_keyspace("github_events")
    except Exception as e:
        print(e)

    drop_tables(session)
    create_tables(session)

    process(session, filepath="../data")

    print("Query for \'Events\' events")

    # Select data in Cassandra and print them to stdout
    query = """
    SELECT id, type, created_at, actor_id, actor_login, repo_id, repo_name from events WHERE type = 'Events' ALLOW FILTERING
    """
    try:
        rows = session.execute(query)
    except Exception as e:
        print(e)

    for row in rows:
        print(row)

    print("Number of each event by type, created_at: >= '2022-08-17T15:54:00Z'")

    for event_type in event_types:
        # Select data in Cassandra and print them to stdout
        query = """
        SELECT type, count(*) from events WHERE type = '"""+event_type+"""' AND created_at >= '2022-08-17T15:54:00Z' GROUP BY type ALLOW FILTERING;
        """
        try:
            rows = session.execute(query)
        except Exception as e:
            print(e)

        for row in rows:
            print(row)



if __name__ == "__main__":
    main()