import requests

NVD_API_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_cves_from_nvd(pubStartDate, resultsPerPage, startIndex, full_load):
    # Initialize an empty list to store fetched CVEs

    try:
        all_cves = []

        headers = {'Content-Type': 'application/json'}

        if pubStartDate != '':
            params = {
                "pubStartDate": pubStartDate,
                "startIndex": startIndex,
                "resultsPerPage": resultsPerPage,
            }
        else:
            params = {
                "startIndex": startIndex,
                "resultsPerPage": resultsPerPage,
            }

        if full_load:
            res = requests.get(
                f"{NVD_API_BASE_URL}", headers=headers)
            response = res.json()
            # print(response)
        else:
            res = requests.get(
                f"{NVD_API_BASE_URL}", params=params, headers=headers)
            response = res.json()

        # Extract CVEs from the response and add them to the list
        if "vulnerabilities" in response:
            all_cves.extend(response["vulnerabilities"])

        res = {
            'statusCode': 200,
            'response': all_cves
        }
        return res
    
    except Exception as e:
        res={
            'statusCode': 400,
            'statusMessage':"Error in Fetching the data from the NVE API's",
            'Error': e
        }

        return res

# You may need to implement pagination, data cleansing, and de-duplication here
