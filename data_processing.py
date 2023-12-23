from pymongo import MongoClient
from datetime import datetime, timedelta

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["cve_database"]
cve_collection = db["cves"]