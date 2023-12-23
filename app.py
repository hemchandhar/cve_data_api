from flask import Flask
from nvd_api import fetch_cves_from_nvd
from data_processing import sync_cves_to_mongo, filter_cves_by_id, filter_cves_by_scores, filter_cves_by_last_modified

app = Flask(__name__)




if __name__ == "__main__":
    app.run(debug=True)
