from pymongo import MongoClient
from datetime import datetime, timedelta

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["cve_database"]
cve_collection = db["cves"]

# Implementation to synchronize CVEs to MongoDB


def sync_cves_to_mongo(staging_data):

    # Extract relevant information from staging data and insert or update in MongoDB
    updated = 0
    inserted = 0
    for data in staging_data:
        cve = data.get("cve")
        id = cve['id']

        existing_cve = cve_collection.find_one({"id": id})

        if existing_cve:
            # CVE already exists, update it if needed
            # Update the MongoDB collection with the modified CVE data
            cve_collection.replace_one(
                {"id": existing_cve["id"]}, existing_cve)
            updated += 1
        else:
            # CVE does not exist, insert it
            cve_collection.insert_one(cve)
            inserted += 1
    res = f"Synced Successfully by Inserting {inserted} CVE's  and Updating {updated} CVE's"

    return res


def filter_cves_by_id(cve_id):
    # Implementation to filter CVEs by CVE ID
    # ...
    return True


def filter_cves_by_scores(base_score):
    # Implementation to filter CVEs by scores
    # ...
    return True


def filter_cves_by_last_modified(days_modified):
    # Implementation to filter CVEs by last modified date
    # ...
    return True
