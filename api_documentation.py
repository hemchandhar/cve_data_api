import json
from flask_swagger_ui import get_swaggerui_blueprint

swagger_url = '/swagger'


# Define your API documentation in JSON format
swagger_data = {
    "swagger": "2.0",
    "info": {
        "title": "CVE API Documentation",
        "version": "1.0",
        "description": "API documentation for CVEs",
    },
    # Add other Swagger metadata, paths, etc.
}

# Save the Swagger JSON to a file (e.g., swagger.json)
with open("static/swagger.json", "w") as json_file:
    json.dump(swagger_data, json_file)

swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_url,
    '/static/swagger.json',
    config={'app_name': "CVE API Documentation"}
)
