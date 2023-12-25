from flask import Flask, request
from nvd_api import fetch_cves_from_nvd
from data_processing import sync_cves_to_mongo, filter_cves_by_id, filter_cves_by_scores, filter_cves_by_last_modified
from api_documentation import swaggerui_blueprint

app = Flask(__name__)

# Registering the Swagger UI blueprint
app.register_blueprint(swaggerui_blueprint, url_prefix="/swagger")

# Endpoint to fetch and sync CVEs from NVD API to MongoDB


@app.route("/sync_cves", methods=["POST"])
def sync_cves():
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
    if response['status'] == 200:
        res = sync_cves_to_mongo(response['response'])
    else:
        res = "Error in Fetching the CVE's from NVD API"
    return res

# Endpoint to get CVE details by CVE ID


@app.route("/get_cve/<cve_id>", methods=["GET"])
def get_cve_by_id(cve_id):
    return filter_cves_by_id(cve_id)

# Endpoint to filter CVEs by scores or last modified
@app.route("/filter_cves", methods=["GET"])
def filter_cves():
    base_score = request.args.get("base_score")
    days_modified = request.args.get("days_modified")

    if base_score:
        return filter_cves_by_scores(float(base_score))
    elif days_modified:
        return filter_cves_by_last_modified(int(days_modified))
    else:
        return "Invalid filter parameters."


if __name__ == "__main__":
    app.run(debug=True)
