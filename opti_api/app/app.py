from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask_mysqldb import MySQL
from flask_restplus import Resource, Api
from flask import request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import *
from datetime import timedelta
from enum import Enum
import os
global _debug_
global _version_
global _margin_
global _vat_
api = Api()

app = Flask(__name__)
#api = Api(app, doc='/api/')
api.init_app(app)

bcrypt = Bcrypt(app)

_debug_ = os.environ['DEBUG']
_version_ = "0.3.5"
_brutMargin_ = float(0.30)
_vat_ = float(0.21)

mysql = MySQL()
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
mysql.init_app(app)
jwt = JWTManager(app)

class bookingStatus(Enum):
    OK = 1
    WAITING_FOR_PAYMENT = 2
    PAYMENT_ERROR = 3
    CANCELED = 4

@app.route('/system', methods=['GET'])
def system():
    return jsonify({'state': 'up','version': _version_, 'motd': 'N/A'})

@app.route('/motd')
def motd():
    return jsonify({'motd': 'N/A'})

@app.route('/workspace/availability')
@jwt_required
def addAvailability():
    json_data = request.get_json(force=True)

    posted_workspace_id = json_data['workspace_id']
    posted_openingDays = json_data['openingDays']
    posted_monOpeningHour = json_data['monOpeningHour']
    posted_monClosingHour = json_data['monClosingHour']
    posted_tueOpeningHour = json_data['tueOpeningHour']
    posted_tueOpeningHour = json_data['tueOpeningHour']
    posted_wedOpeningHour = json_data['wedOpeningHour']
    posted_wedClosingHour = json_data['wedClosingHour']
    posted_thuOpeningHour = json_data['thuOpeningHour']
    posted_thuClosingHour = json_data['thuClosingHour']
    posted_friOpeningHour = json_data['friOpeningHour']
    posted_friClosingHour = json_data['friClosingHour']
    posted_satOpeningHour = json_data['satOpeningHour']
    posted_satClosingHour = json_data['satClosingHour']
    posted_sunOpeningHour = json_data['sunOpeningHour']
    posted_sunClosingHour = json_data['sunClosingHour']

    availability = [posted_workspace_id, posted_openingDays, posted_monOpeningHour, posted_monClosingHour, posted_tueOpeningHour, posted_tueOpeningHour, posted_wedOpeningHour, posted_wedClosingHour, posted_thuOpeningHour, posted_thuClosingHour, posted_friOpeningHour, posted_friClosingHour, posted_satOpeningHour, posted_satClosingHour, posted_sunOpeningHour, posted_sunClosingHour]

    cur = mysql.connection.cursor()
    cur.callproc('checkIfAvailabilityExist', [posted_workspace_id])

    if cur.rowcount is not 0:

        cur.close()
        cur = mysql.connection.cursor()
        cur.callproc('updateAvailability', availability)
        mysql.connection.commit()
        cur.close()

        return jsonify({}),201

    else:
        cur.close()
        cur = mysql.connection.cursor()
        cur.callproc('checkIfWorkspaceExist', [posted_workspace_id])

        if cur.rowcount is not 0:

            cur.close()
            cur = mysql.connection.cursor()
            cur.callproc('addAvailability', availability)
            mysql.connection.commit()
            cur.close()

            return jsonify({}),201


        else:
            return jsonify({'Status': 'Error', 'Code': 'A001'}), 404


@app.route('/workspace/<string:workspace_id>/availability')
def getWorkspaceAvailability(workspace_id):
    posted_workspace_id = workspace_id

    cur = mysql.connection.cursor()
    cur.callproc('checkIfAvailabilityExist', [posted_workspace_id])

    if cur.rowcount is not 0:
        cur.close()
        cur = mysql.connection.cursor()
        cur.callproc('get_availability_byWorkspaceId', workspace_id)
        result = cur.fetchone()

        availability = {
            'workspace_id' : result[0],
            'openingDays' : result[1],
            'monOpeningHour' : str(result[2]),
            'monClosingHour' : str(result[3]),
            'tueOpeningHour' : str(result[4]),
            'tueClosingHour' : str(result[5]),
            'wedOpeningHour' : str(result[6]),
            'wedClosingHour' : str(result[7]),
            'thuOpeningHour' : str(result[8]),
            'thuClosingHour' : str(result[9]),
            'friOpeningHour' : str(result[10]),
            'friClosingHour' : str(result[11]),
            'satOpeningHour' : str(result[12]),
            'satClosingHour' : str(result[13]),
            'sunOpeningHour' : str(result[14]),
            'sunClosingHour' : str(result[15])}
        return jsonify(availability)
    else:
        return jsonify({'status': 'error', 'code': 'A001'}), 404

@app.route('/workspace/book/status', methods=['POST'])
@jwt_required
def workSpaceBookStatus():
    json_data = request.get_json(force=True)

    posted_booking_id = json_data['booking_id']
    posted_status = json_data['status']

    data = [posted_booking_id, posted_status]

    cur = mysql.connection.cursor()
    cur.callproc('updateBookingStatus', data)
    mysql.connection.commit()
    cur.close

    return jsonify({'Status': 'ok'}),201


@app.route('/workspace/book', methods=['POST'])
@jwt_required
def workspaceBook():
    json_data = request.get_json(force=True)

    posted_workspace_id = json_data['workspace_id']
    posted_startDateTime = json_data['startDateTime']
    posted_enDateTime = json_data['endDateTime']
    posted_price = json_data['price']

    cur = mysql.connection.cursor()
    data = [posted_workspace_id, posted_startDateTime, posted_enDateTime]


    cur.callproc('checkIfScheduleIsOK', data)

    if cur.rowcount is not 0:

        return jsonify({'Status': 'Error', 'Code': 'B001'}), 409

    else:
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
        result = cur.fetchone()
        customer_id = result[0]
        cur.close()
        cur = mysql.connection.cursor()

        data = [posted_workspace_id, customer_id, posted_startDateTime, posted_enDateTime, posted_price, bookingStatus.OK.value]
        cur.callproc('addBooking', data)

        mysql.connection.commit()
        cur.close()

        return jsonify({'Status': 'ok'}),201




@app.route('/workspace/<string:workspace_id>')
def workspaceId(workspace_id):

    cur = mysql.connection.cursor()
    cur.callproc('get_workspace_byWorkspaceId', workspace_id)
    result = cur.fetchone()

    workspace = {
        'workspace_name': result[0],
        'description': result[1],
        'building_name': result[2],
        'latitude': str(result[3]),
        'longitude': str(result[4]),
        'street': result[5],
        'building_number': result[6],
        'postcode': result[7],
        'city': result[8],
        'country': result[9],
        'price': str(round((float(result[10])/(1-_brutMargin_))*(1+_vat_),2)),
        'nbSeats': result[11],
        'hasProjector': result[12],
        'hasWifi': result[13] }

    return jsonify(workspace)



@app.route('/user/workspaces')
@jwt_required
def UserWorkspaces():

    cur = mysql.connection.cursor()
    cur.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
    result = cur.fetchone()
    owner_id = result[0]
    cur.close()

    workspaces = []

    cur = mysql.connection.cursor()
    cur.callproc('get_workspaces_byOwnerId', [int(owner_id)])

    for workspace in cur:
        workspace = {
            'workspace_id' : workspace[0],
            'workspace_name': workspace[1],
            'description': workspace[2],
            'building_name': workspace[3],
            'latitude': str(workspace[4]),
            'longitude': str(workspace[5]),
            'street': workspace[6],
            'building_number': workspace[7],
            'postcode': workspace[8],
            'city': workspace[9],
            'country': workspace[10],
            'price': str(round((float(workspace[11])/(1-_brutMargin_))*(1+_vat_),2)),
            'nbSeats': workspace[12],
            'hasProjector': workspace[13],
            'hasWifi': workspace[14] }

        workspaces.append(workspace)

    return jsonify(workspaces)



@app.route('/search/<float:centerLatitude>/<float:centerLongitude>/<int:rangeInKm>/<string:day>/<int:minSeats>')
def Search(centerLatitude, centerLongitude, rangeInKm, day, minSeats):
    rangeInDegree = (rangeInKm / 40000) * 360
    radiusInDegree = rangeInDegree / 2

    openingDays = {}
    openingDays['mon'] = "1______"
    openingDays['tue'] = "_1_____"
    openingDays['wed'] = "__1____"
    openingDays['thu'] = "___1___"
    openingDays['fri'] = "____1__"
    openingDays['sat'] = "_____1_"
    openingDays['sun'] = "______1"

    minLatitude = centerLatitude - radiusInDegree
    maxLatitude = centerLatitude + radiusInDegree

    minLongitude = centerLongitude - radiusInDegree
    maxLongitude = centerLongitude + radiusInDegree

    searchInputs = [minLatitude, maxLatitude, minLongitude, maxLongitude, minSeats, openingDays[day.lower()]]
    workspaces = []
    cur = mysql.connection.cursor()
    cur.callproc("simple_search", searchInputs)

    for workspace in cur:
        workspace = {
            'address_id' : workspace[0],
            'building_name' : workspace[1],
            'street' : workspace[2],
            'building_number' : workspace[3],
            'postcode' : workspace[4],
            'city' : workspace[5],
            'country' : workspace[6],
            'latitude' : str(workspace[7]),
            'longitude' : str(workspace[8]),
            'workspace_id' : workspace[9],
            'workspace_name' : workspace[10],
            'nbSeats' : workspace[11],
            'description' : workspace[12],
            'hasProjector' : workspace[13],
            'hasWifi' : workspace[14],
            'price' : str(round((float(result[15])/(1-_brutMargin_))*(1+_vat_),2)),
            'openingDays' : workspace[16],
            'monOpeningHour' : str(workspace[17]),
            'monClosingHour' : str(workspace[18]),
            'tueOpeningHour' : str(workspace[19]),
            'tueClosingHour' : str(workspace[20]),
            'wedOpeningHour' : str(workspace[21]),
            'wedClosingHour' : str(workspace[22]),
            'thuOpeningHour' : str(workspace[23]),
            'thuClosingHour' : str(workspace[24]),
            'friOpeningHour' : str(workspace[25]),
            'friClosingHour' : str(workspace[26]),
            'satOpeningHour' : str(workspace[27]),
            'satClosingHour' : str(workspace[28]),
            'sunOpeningHour' : str(workspace[29]),
            'sunClosingHour' : str(workspace[30]),
            'owner_id' : workspace[31],
            'firstname' : workspace[32],
            'lastName' : workspace[33],
            'email' : workspace[34] }
        workspaces.append(workspace)

    return jsonify(workspaces)



@app.route('/signup', methods=['POST'])
def Signin():

    json_data = request.get_json(force=True)
    posted_username = json_data['mail']
    posted_name = json_data['name']
    posted_firstname = json_data['firstname']
    posted_password = json_data['password']
    posted_phone = json_data['phone']
    hashedPwd = bcrypt.generate_password_hash(posted_password)

    data = [posted_firstname, posted_name, posted_username, posted_phone, hashedPwd.decode('UTF-8')]

    try:
        cur = mysql.connection.cursor()
        cur.callproc('sign_up', data)
        mysql.connection.commit()
        return jsonify({'Status': 'Success'}), 201
    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({'Status': 'Error', 'Code': 'S001'}), 409
        elif _debug_:
            return jsonify({'Status': 'Error', 'e': str(e)}), 409
        else:
            return jsonify({'Status': 'Error'}), 409

@app.route('/workspaces')
def Workspaces(self):
    workspaces = []
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM get_workspace")
    for workspace in cur:
        workspace = {
        'address_id': workspace[0],
        'building_name': workspace[1],
        'country': workspace[2],
        'city': workspace[3],
        'street': workspace[4],
        'postcode': workspace[5],
        'building_number': workspace[6],
        'workspace_id': workspace[7],
        'workspace_name': workspace[8],
        'nbPlace': workspace[9],
        'description': workspace[10],
        'hasProjector': workspace[11],
        'hasWifi': workspace[12] }
        workspaces.append(workspace)
    return jsonify(workspaces)

@app.route('/workspace/add', methods=['POST'])
@jwt_required
def WorkspaceAdd():
    json_data = request.get_json(force=True)
    jsonAddress = json_data['address']
    address = [jsonAddress['buildingName'], jsonAddress['street'], jsonAddress['number'], jsonAddress['postcode'], jsonAddress['city'], jsonAddress['country'], jsonAddress['latitude'], jsonAddress['longitude']]
    jsonWorkspace = json_data['workspace']


    cur = mysql.connection.cursor()
    cur.callproc('checkIfAddressExist', address)

    if cur.rowcount is not 0:
        result = cur.fetchone()
        addressId = result[0]
        cur.close()

        workspace = [jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasWifi'],jsonWorkspace['minPrice'], addressId]


        cur = mysql.connection.cursor()
        cur.callproc('addWorkspace', workspace)
        mysql.connection.commit()
        cur.close()

        return jsonify({}),201

    else:
        cur.close()
        cur = mysql.connection.cursor()
        cur.callproc('addWorkspaceAddress', address)
        mysql.connection.commit()
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc('checkIfAddressExist', address)
        result = cur.fetchone()
        addressId = result[0]
        cur.close()

        workspace = [jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasProjector'], addressId]


        cur = mysql.connection.cursor()
        cur.callproc('addWorkspace', workspace)
        mysql.connection.commit()
        cur.close()

        return jsonify({}),201

@app.route('/auth/login', methods=['POST'])
def login():
    json_data = request.get_json(force=True)
    email = json_data['username']
    password = json_data['password']

    cur = mysql.connection.cursor()
    cur.callproc('getHash', [email])

    if cur.rowcount is not 0:

        result = cur.fetchone()
        firstname = result[0]
        lastname = result[1]
        hash = result[2]

        if bcrypt.check_password_hash(hash, password) :
            token = create_access_token(identity=email)
            return jsonify({'access_token': token}), 200
        else:
            return jsonify({'Status': 'Error', 'Code': 'L002'}), 401
    else:
        return jsonify({'Status': 'Error', 'Code': 'L001'}), 401

if __name__ == '__main__':
    app.run(debug=_debug_, host='0.0.0.0', port=5000)
