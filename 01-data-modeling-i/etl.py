import glob
import json
import os
from typing import List

import psycopg2


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


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)
    print(all_files)

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                
                if each["type"] == "IssueCommentEvent":
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                        each["payload"]["issue"]["url"],
                    )
                else:
                    print(
                        each["id"], 
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["created_at"],
                    )

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO actors (
                        id,
                        login
                    ) VALUES ({each["actor"]["id"]}, '{each["actor"]["login"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO events (
                        id,
                        type,
                        actor_id
                    ) VALUES ('{each["id"]}', '{each["type"]}', '{each["actor"]["id"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                # print(insert_statement)
                cur.execute(insert_statement)
                
  # Insert data into tables here (assuming payload has appropriate fields)
                insert_statement = f"""
                    INSERT INTO payload (
                        push_id,
                        size,
                        distinct_size,
                        ref,
                        head,
                        before_code,
                        commits
                    ) VALUES (
                        '{each.get("payload", {}).get("push_id", "")}',
                        {each.get("payload", {}).get("size", 0)},
                        {each.get("payload", {}).get("distinct_size", 0)},
                        '{each.get("payload", {}).get("ref", "")}',
                        '{each.get("payload", {}).get("head", "")}',
                        '{each.get("payload", {}).get("before_code", "")}',
                        '{each.get("payload", {}).get("commits", "")}'
                    )
                    ON CONFLICT (push_id) DO NOTHING
                """
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO repo (
                        repo_id,
                        repo_name,
                        repo_url
                    ) VALUES (
                        {each.get("repo", {}).get("id", "")},
                        '{each.get("repo", {}).get("name", "")}',
                        '{each.get("repo", {}).get("url", "")}'
                    )
                    ON CONFLICT (repo_id) DO NOTHING
                """
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO org (
                        org_id,
                        org_login,
                        org_gravatar_id,
                        org_url,
                        org_avatar_url
                    ) VALUES (
                        {each.get("org", {}).get("id", "")},
                        '{each.get("org", {}).get("login", "")}',
                        '{each.get("org", {}).get("gravatar_id", "")}',
                        '{each.get("org", {}).get("url", "")}',
                        '{each.get("org", {}).get("avatar_url", "")}'
                    )
                    ON CONFLICT (org_id) DO NOTHING
                """
                cur.execute(insert_statement)
                conn.commit()


def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    process(cur, conn, filepath="../data")

    conn.close()


if __name__ == "__main__":
    main()