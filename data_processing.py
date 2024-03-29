from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime, timedelta

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["cve_database"]
cve_collection = db["cves"]

# Implementation to synchronize CVEs to MongoDB


def sync_cves_to_mongo(staging_data):

    # Extract relevant information from staging data and insert or update in MongoDB\
    res = {}
    try:
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
        
        res = {
            "statusCode": 200,
            "response": f"Synced Successfully by Inserting {inserted} CVE's  and Updating {updated} CVE's"
        }

        return res
    except Exception as e:
        res = {
            "statusCode": 500,
            "error": e
        }
        
        return res


def filter_cves_by_id(cve_id):
    """
    Filter CVEs by CVE ID.

    Args:
        cve_id (str): CVE ID to filter.

    Returns:
        dict: CVE details if found, or None if not found.
    """
    response = {}
    try:
        # Convert the provided cve_id to ObjectId
        # Search for the CVE in the MongoDB collection by ObjectId
        result = cve_collection.find_one({"id": cve_id}, {"_id": 0})
        response = {
            "statusCode": 200,
            "statusMessage": f"CVE Details has been fetched successfully for the CVE ID: {cve_id}",
            "response": result
        }
        return response
    except Exception as e:
        # Handle the exception (e.g., invalid ObjectId)
        # print(f"Error: {e}")
        response = {
            "statusCode": 500,
            "statusMessage": "Internal Server Error in retrieving the CVE Details by Id. Please contact your Adminstrator",
            "error": e
        }
        return response


def filter_cves_by_scores(base_score):
    """
   Filter CVEs by base score.

   Args:
       base_score (float): Base score to filter.

   Returns:
       list: List of CVEs with a base score greater than or equal to the provided score.
   """
    response = {}
    try:
        # Search for CVEs in the MongoDB collection with a base score greater than or equal to the provided score
        results = cve_collection.find(
            {"metrics.cvssMetricV2.cvssData.baseScore": {"$gte": base_score}, }, {"_id": 0})

        response = {
            "statusCode": 200,
            "statusMessage": f"CVE Details has been fetched successfully based on the Base score greater than or equal to {base_score}",
            "response": list(results)
        }

    except Exception as e:
        response = {
            "statusCode": 500,
            "statusMessage": "Internal Server Error happened on the filter cves by scores API. Please contact the Adminstrator",
            "error": str(e)
        }

    return response


def filter_cves_by_last_modified(days_modified):
    """
   Filter CVEs by last modified date within a specified number of days.

   Args:
       days_modified (int): Number of days for filtering.

   Returns:
       list: List of CVEs modified within the specified number of days.
   """
    response = {}
    try:
        threshold_date = datetime.utcnow() - timedelta(days=days_modified)

        # Search for CVEs in the MongoDB collection modified within the specified number of days
        results = cve_collection.find(
        {"lastModifiedDate": {"$gte": threshold_date}})

        response = {
            "statusCode": 200,
            "statusMessage": f"CVE Details has been fetched successfully based on the Days Modified: {days_modified}",
            "response": list(results)
        }
    
    except Exception as e:
        response = {
            "statusCode": 500,
            "statusMessage": "Internal Server Error happened on the filter cves by Last Modified date API. Please contact the Adminstrator",
            "error": str(e)
        }

    return response
