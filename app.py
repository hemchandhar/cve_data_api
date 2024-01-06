from flask import Flask, request
from nvd_api import fetch_cves_from_nvd
from data_processing import sync_cves_to_mongo, filter_cves_by_id, filter_cves_by_scores, filter_cves_by_last_modified
from flasgger import Swagger


app = Flask(__name__)

swagger = Swagger(app)

# Registering the Swagger UI blueprint
# app.register_blueprint(swaggerui_blueprint, url_prefix="/swagger")

# Endpoint to fetch and sync CVEs from NVD API to MongoDB


@app.route("/sync_cves", methods=["POST"])
def sync_cves():
    """
    Sync CVEs from NVD API's.

    ---
    tags:
      - CVE Sync
    parameters:
      - name: full_load
        in: formData
        type: boolean
        required: true
        description: Set to true for a full load.
      - name: pubStartDate
        in: formData
        type: string
        description: Start date for syncing.
      - name: resultsPerPage
        in: formData
        type: integer
        description: Number of results per page (default-2000).
      - name: startIndex
        in: formData
        type: integer
        description: Start index for paging (default-0).
    responses:
      200:
        description: statusCode:200, statusMessage:Successfully Fectched the data from CVE API, response:Response from DB whether it is successfull load
      500:
        description: statusCode:500, statusMessage:Internal Server Error happened on the Sync CVE from NVE API to database. Please contact the Adminstrator, error:Internal Error Happened will return

    """
    res = {}
    try:
        req_parameters = request.json

        # Required Parameter to check for full load
        # type: Boolean
        if 'full_load' in req_parameters:
            full_load = req_parameters['full_load']
        else:
            full_load = True

        # Checking for any start date is mentioned in input.
        if 'pubStartDate' in req_parameters:
            pubStartDate = req_parameters['pubStartDate']
        else:
            pubStartDate = ''

        # Checking for the results per page parameters (Default: 10000)
        if 'resultsPerPage' in req_parameters:
            resultsPerPage = req_parameters['resultsPerPage']
        else:
            resultsPerPage = 2000

        # Checking for the Start Index in request parameters (Default: 0)
        if 'startIndex' in req_parameters:
            startIndex = req_parameters['startIndex ']
        else:
            startIndex = 0

        response = fetch_cves_from_nvd(
            pubStartDate=pubStartDate, resultsPerPage=resultsPerPage, startIndex=startIndex, full_load=full_load)

        if response['statusCode'] == 200:
            sync_res = sync_cves_to_mongo(response['response'])
            print(sync_res)
            if sync_res['statusCode'] == 200:
                res = {
                    "statusCode": "200",
                    "statusMessage": "Successfully Fectched the data from CVE API",
                    "response": sync_res
                }
            else:
                res = {
                    "statusCode": "500",
                    "statusMessage": "Internal Server Error in Syncing the CVE's to Database. Please Contact your adminstrator",
                    "error": response['error']
                }
        else:
            res = {
                "statusCode": "500",
                "statusMessage": "Internal Server Error in Fetching the CVE's from NVD API. Please Contact your adminstrator",
                "error": response['error']
            }
        return res
    except Exception as e:
        res = {
            "statusCode": "500",
            "statusMessage": "Internal Server Error happened on the Sync CVE from NVE API to database. Please contact the Adminstrator",
            "error": str(e)
        }
        return res


# Endpoint to get CVE details by CVE ID
@app.route("/get_cve/<cve_id>", methods=["GET"])
def get_cve_by_id(cve_id):
    """
    Get CVE details by CVE ID.

    ---
    tags:
      - CVE Details
    parameters:
      - name: cve_id
        in: path
        type: string
        required: true
        description: The CVE ID.
    responses:
      200:
        description: CVE details
      404:
        description: CVE not found
    """
    res = {}
    try:
        response = filter_cves_by_id(cve_id)
        if response['statusCode'] == 200:
            res = {
                "statusCode": 200,
                "statusMessage": response['statusMessage'],
                "response": response['response']
            }
        else:
            res = {
                "statusCode": 500,
                "statusMessage": response['statusMessage'],
                "error": response['error']
            }
    except Exception as e:
        res = {
            "statusCode": 500,
            "statusMessage": "Internal Server Error in retrieving the CVE Details by Id. Please contact your Adminstrator",
            "error": str(e)
        }
    return res

# Endpoint to filter CVEs by scores or last modified


@app.route("/filter_cves", methods=["GET"])
def filter_cves():
    """
    Filter CVEs by scores or last modified date.

    ---
    tags:
      - CVE Filtering
    parameters:
      - name: base_score
        in: query
        type: number
        description: Filter CVEs by base score.
      - name: days_modified
        in: query
        type: integer
        description: Filter CVEs by last modified date within N days.
    responses:
      200:
        description:  statusCode:200, statusMessage:Succssfully Filtered the values as per the Input, response:Response consists of Filtered values

      400:
        description: statusCode":400, statusMessage:"Internal Filter Parameters. Please Try again!",
    """
    res = {}
    try:    
      base_score = request.args.get("base_score")
      days_modified = request.args.get("days_modified")
      
      if base_score != None:
        response = filter_cves_by_scores(float(base_score))
        if response['statusCode'] == 200:
            res = {
                "statusCode": "200",
                "statusMessage": response['statusMessage'],
                "response": response["response"]
            }
        else:
            res = {
                "statusCode": "500",
                "statusMessage": response['statusMessage'],
                "error": response['error']
            }
      elif days_modified != None:
        response = filter_cves_by_last_modified(int(days_modified))
        if response['statusCode'] == 200:
            res = {
                "statusCode": 200,
                "statusMessage": response['statusMessage'],
                "response": response["response"]
            }
        else:
            res = {
                "statusCode": 500,
                "statusMessage": response['statusMessage'],
                "error": response['error']
            }
      else:
        res = {
            "statusCode": 400,
            "statusMessage": "Internal Filter Parameters. Please Try again!",
        }
    except Exception as e:
        res = {
            "statusCode": "500",
            "statusMessage": "Internal Server Error in Filtering the CVE's. Please contact your Adminstrator",
            "error": str(e)
        }

    return res


if __name__ == "__main__":
    app.run(debug=True)
