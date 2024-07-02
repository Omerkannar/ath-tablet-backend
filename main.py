from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import render_template, send_from_directory, request
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
from flask import Flask, jsonify
from flask_cors import CORS
import threading
import time

# =======================================================================================================================
# Global Data
# =======================================================================================================================
app = Flask(__name__, template_folder='./swagger/templates')
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5000"}})

spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

fuel_increase_or_decrease = 1

# =======================================================================================================================
# Data Definition
# =======================================================================================================================

CLOUD_LAYER_Data_List = [{
    "LAYER_NAME": "Layer 1",
    "LAYER_TYPE": "Stratus",
    "LAYER_BASE_ALT": 0,
    "LAYER_CEILING_ALT": 0,
    "LAYER_COVERAGE": 0
}, {
    "LAYER_NAME": "Layer 2",
    "LAYER_TYPE": "Stratus",
    "LAYER_BASE_ALT": 0,
    "LAYER_CEILING_ALT": 0,
    "LAYER_COVERAGE": 0
}, {
    "LAYER_NAME": "Layer 3",
    "LAYER_TYPE": "Stratus",
    "LAYER_BASE_ALT": 0,
    "LAYER_CEILING_ALT": 0,
    "LAYER_COVERAGE": 0
}]

WIND_LAYER_Data_List = [{
    "LAYER_NAME": "Layer 1",
    "LAYER_BASE_ALT": 0,
    "LAYER_CEILING_ALT": 0,
    "LAYER_SPEED": 0,
    "LAYER_DIRECTION": 0,
}, {
    "LAYER_NAME": "Layer 2",
    "LAYER_BASE_ALT": 0,
    "LAYER_CEILING_ALT": 10000,
    "LAYER_SPEED": 50,
    "LAYER_DIRECTION": 90,
}, {
    "LAYER_NAME": "Layer 3",
    "LAYER_BASE_ALT": 2000,
    "LAYER_CEILING_ALT": 12000,
    "LAYER_SPEED": 10,
    "LAYER_DIRECTION": 275,
}]


# =======================================================================================================================
# Data Definition
# =======================================================================================================================
class Cloud_Layer_Schema(Schema):
    LAYER_NAME = fields.Str()
    LAYER_TYPE = fields.Str()
    LAYER_BASE_ALT = fields.Int()
    LAYER_CEILING_ALT = fields.Int()
    LAYER_COVERAGE = fields.Int()


class Cloud_Layer_List_Schema(Schema):
    list = fields.List(fields.Nested(Cloud_Layer_Schema))


class Wind_Layer_Schema(Schema):
    LAYER_NAME = fields.Str()
    LAYER_BASE_ALT = fields.Int()
    LAYER_CEILING_ALT = fields.Int()
    LAYER_SPEED = fields.Int()
    LAYER_DIRECTION = fields.Int()


class Wind_Layer_List_Schema(Schema):
    list = fields.List(fields.Nested(Wind_Layer_Schema))


# =======================================================================================================================
# Swagger Route Definition
# =======================================================================================================================
@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', secure_filename(path))


@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


# =======================================================================================================================
# setCloudLayerData
# =======================================================================================================================
@app.route("/setCloudLayerData", methods=["POST"])
def setCloudLayerData():
    """Post registerData
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: Cloud_Layer_Schema
          """
    print('start -> setCloudLayerData')
    if request.is_json:
        request_json = request.get_json()

        LAYER_NAME = request_json["LAYER_NAME"]
        LAYER_TYPE = request_json["LAYER_TYPE"]
        LAYER_BASE_ALT = request_json['LAYER_BASE_ALT']
        LAYER_CEILING_ALT = request_json["LAYER_CEILING_ALT"]
        LAYER_COVERAGE = request_json["LAYER_COVERAGE"]

        change_index = -1
        if LAYER_NAME == "Layer 1":
            change_index = 0
        if LAYER_NAME == "Layer 2":
            change_index = 1
        if LAYER_NAME == "Layer 3":
            change_index = 2

        if change_index >= 0:
            CLOUD_LAYER_Data_List[change_index]["LAYER_NAME"] = LAYER_NAME
            CLOUD_LAYER_Data_List[change_index]["LAYER_TYPE"] = LAYER_TYPE
            CLOUD_LAYER_Data_List[change_index]["LAYER_BASE_ALT"] = LAYER_BASE_ALT
            CLOUD_LAYER_Data_List[change_index]["LAYER_CEILING_ALT"] = LAYER_CEILING_ALT
            CLOUD_LAYER_Data_List[change_index]["LAYER_COVERAGE"] = LAYER_COVERAGE

        print(request_json)
        print('finish -> setCloudLayerData')
        return "success set Cloud layer Data", 200
    return {"Error": "Request must be JSON"}, 415


##################################################################
# getCloudLayerData
##################################################################
@app.get("/getCloudLayerData")
def getCloudLayerData():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: Cloud_Layer_Schema
        """
    print('### get -> getCloudLayerData')
    print(CLOUD_LAYER_Data_List)
    return jsonify(CLOUD_LAYER_Data_List)


##################################################################
# getCloudLayerDataList
##################################################################
@app.get("/getCloudLayerDataList")
def getCloudLayerDataList():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: Cloud_Layer_List_Schema
        """
    print('start -> getData')
    return jsonify(CLOUD_LAYER_Data_List)


# Define a function that will be executed in the new thread
def internal_thread_function():
    while True:
        time.sleep(10)


# =======================================================================================================================
# setWindLayerData
# =======================================================================================================================
@app.route("/setWindLayerData", methods=["POST"])
def setWindLayerData():
    """Post registerData
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: Wind_Layer_Schema
          """
    print('start -> setWindLayerData')
    if request.is_json:
        request_json = request.get_json()


        LAYER_NAME = request_json["LAYER_NAME"]
        LAYER_BASE_ALT = request_json["LAYER_BASE_ALT"]
        LAYER_CEILING_ALT = request_json["LAYER_CEILING_ALT"]
        LAYER_SPEED = request_json["LAYER_SPEED"]
        LAYER_DIRECTION = request_json["LAYER_DIRECTION"]

        change_index = -1
        if LAYER_NAME == "Layer 1":
            change_index = 0
        if LAYER_NAME == "Layer 2":
            change_index = 1
        if LAYER_NAME == "Layer 3":
            change_index = 2

        if change_index >= 0:
            WIND_LAYER_Data_List[change_index]["LAYER_NAME"] = LAYER_NAME
            WIND_LAYER_Data_List[change_index]["LAYER_BASE_ALT"] = LAYER_BASE_ALT
            WIND_LAYER_Data_List[change_index]["LAYER_CEILING_ALT"] = LAYER_CEILING_ALT
            WIND_LAYER_Data_List[change_index]["LAYER_SPEED"] = LAYER_SPEED
            WIND_LAYER_Data_List[change_index]["LAYER_DIRECTION"] = LAYER_DIRECTION

        print(request_json)
        print('finish -> setWindLayerData')
        return "success set Wind layer Data", 200
    return {"Error": "Request must be JSON"}, 415


##################################################################
# getWindLayerData
##################################################################
@app.get("/getWindLayerData")
def getWindLayerData():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: Wind_Layer_Schema
        """
    print('### get -> getWindLayerData')
    print(WIND_LAYER_Data_List)
    return jsonify(WIND_LAYER_Data_List)


##################################################################
# getWindLayerDataList
##################################################################
@app.get("/getWindLayerDataList")
def getWindLayerDataList():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: Wind_Layer_List_Schema
        """
    print('start -> getData')
    return jsonify(WIND_LAYER_Data_List)


# =======================================================================================================================
# Swagger Content
# =======================================================================================================================
with app.test_request_context():
    spec.path(view=setCloudLayerData)
    spec.path(view=getCloudLayerData)
    spec.path(view=getCloudLayerDataList)


def flask_run():
    print("Running RestAPI")
    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    print('ATH Flight Data Python Server Started ...')

    internal_thread = threading.Thread(target=internal_thread_function)
    flask_thread = threading.Thread(target=flask_run)

    internal_thread.start()
    flask_thread.start()

    internal_thread.join()
    flask_thread.join()
