from flask_swagger_ui import get_swaggerui_blueprint

swagger_url = '/swagger'
swaggerui_blueprint = get_swaggerui_blueprint(
    swagger_url,
    '/static/swagger.json',
    config={'app_name': "CVE API Documentation"}
)
