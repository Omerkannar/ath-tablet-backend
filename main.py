import threading
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory, request
from marshmallow import Schema, fields
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask import Flask, jsonify
from flask_cors import CORS
from array import array
from datetime import datetime
import json
import threading
import time
import random

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

_CMDS_Panel_Data_List = [
    {"LAYER_NAME": "LAYER_1", "LAYER_TYPE": "Stratus", "LAYER_BASE_ALT": 1000, "LAYER_CEILING_ALT": 5000, "LAYER_COVERAGE": 3}]



# =======================================================================================================================
# Data Definition
# =======================================================================================================================
class CMDS_Schema(Schema):
    LAYER_Name = fields.Str()
    LAYER_TYPE = fields.Str()
    LAYER_BASE_ALT = fields.Int()
    LAYER_CEILING_ALT = fields.Int()
    LAYER_COVERAGE = fields.Int()

class CMDS_List_Schema(Schema):
    list = fields.List(fields.Nested(CMDS_Schema))


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
# setCMDSPanelData
# =======================================================================================================================
@app.route("/setCMDSPanelData", methods=["POST"])
def setCMDSPanelData():
    """Post registerData
          ---
          post:
            requestBody:
                required: true
                content:
                    application/json:
                        schema: CMDS_Schema
          """
    print('start -> setCMDSPanelData')
    if request.is_json:
        request_json = request.get_json()

        LAYER_NAME = request_json["LAYER_NAME"]
        LAYER_TYPE = request_json["LAYER_TYPE"]
        LAYER_BASE_ALT = request_json['LAYER_BASE_ALT']
        LAYER_CEILING_ALT = request_json["LAYER_CEILING_ALT"]
        LAYER_COVERAGE = request_json["LAYER_COVERAGE"]


        _CMDS_Panel_Data_List[0]["LAYER_NAME"] = LAYER_NAME
        _CMDS_Panel_Data_List[0]["LAYER_TYPE"] = LAYER_TYPE
        _CMDS_Panel_Data_List[0]["LAYER_BASE_ALT"] = LAYER_BASE_ALT
        _CMDS_Panel_Data_List[0]["LAYER_CEILING_ALT"] = LAYER_CEILING_ALT
        _CMDS_Panel_Data_List[0]["LAYER_COVERAGE"] = LAYER_COVERAGE


        print(request_json)
        print('finish -> setCMDSPanelData')
        return "success set CMDS Panel Data", 200
    return {"Error": "Request must be JSON"}, 415


##################################################################
# getCMDSPanelData
##################################################################
@app.get("/getCMDSPanelData")
def getCMDSPanelData():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: CMDS_Schema
        """
    print('### get -> getCMDSPanelData')
    print(_CMDS_Panel_Data_List[0])
    return jsonify(_CMDS_Panel_Data_List[0])


##################################################################
# getCMDSPanelDataList
##################################################################
@app.get("/getCMDSPanelDataList")
def getCMDSPanelDataList():
    """Get Test List
        ---
        get:
            description: get
            responses:
                200:
                    description: Return Test List
                    content:
                        application/json:
                            schema: CMDS_List_Schema
        """
    print('start -> getData')
    return jsonify(_CMDS_Panel_Data_List)


# Define a function that will be executed in the new thread
def internal_thread_function():
    while (True):
        time.sleep(10)


# =======================================================================================================================
# Swagger Content
# =======================================================================================================================
with app.test_request_context():
    spec.path(view=setCMDSPanelData)
    spec.path(view=getCMDSPanelData)
    spec.path(view=getCMDSPanelDataList)


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
