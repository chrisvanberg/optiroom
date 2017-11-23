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
import os
global _debug_
global _version_

app = Flask(__name__)
api = Api(app, doc='/api/')

bcrypt = Bcrypt(app)

_debug_ = os.environ['DEBUG']
_version_ = "0.2.18"

mysql = MySQL()
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
mysql.init_app(app)
jwt = JWTManager(app)

@api.route('/system')
class System(Resource):
    def get(self):
        return {'state': 'up','version': _version_, 'motd': 'N/A'}

@api.route('/motd')
class System(Resource):
    def get(self):
        return {'motd': 'N/A'}

@api.route('/workspace/availability')
class addAvailability(Resource):
    def post(self):
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

            return {},201

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

                return {},201


            else:
                return {'Status': 'Error', 'Code': 'A001'}, 404



@api.route('/workspace/<string:workspace_id>')
class RoomID(Resource):
    def get(self, workspace_id):

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
            'minPrice': str(result[10]),
            'nbSeats': result[11],
            'hasProjector': result[12],
            'hasWifi': result[13] }

        return jsonify(workspace)



@api.route('/user/workspaces')
class UserWorkspaces(Resource):
    def get(self):
        return {'message': 'user/workspaces is not implemented'}, 501

@api.route('/search/<float:centerLatitude>/<float:centerLongitude>/<int:rangeInKm>/<string:day>/<int:minSeats>')
class Search(Resource):
    def get(self, centerLatitude, centerLongitude, rangeInKm, day, minSeats):
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
                'minPrice' : str(workspace[15]),
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

        return workspaces



@api.route('/signup', methods=['POST'])
class Signin(Resource):
    def post(self):

        json_data = request.get_json(force=True)
        posted_username = json_data['mail']
        posted_name = json_data['name']
        posted_firstname = json_data['firstname']
        posted_password = json_data['password']
        hashedPwd = bcrypt.generate_password_hash(posted_password)

        data = [posted_firstname, posted_name, posted_username, hashedPwd.decode('UTF-8')]

        try:
            cur = mysql.connection.cursor()
            cur.callproc('sign_up', data)
            mysql.connection.commit()
            return {'Status': 'Success'}, 201
        except Exception as e:
            if "Duplicate entry" in str(e):
                return {'Status': 'Error', 'Code': 'S001'}, 409
            elif _debug_:
                return {'Status': 'Error', 'e': str(e)}, 409
            else:
                return {'Status': 'Error'}, 409

@api.route('/workspaces')
class Workspaces(Resource):
    def get(self):
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

@api.route('/workspace/add')
class WorkspaceAdd(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        jsonAddress = json_data['address']
        address = [jsonAddress['buildingName'], jsonAddress['street'], jsonAddress['number'], jsonAddress['postcode'], jsonAddress['city'], jsonAddress['country']]
        jsonWorkspace = json_data['workspace']


        cur = mysql.connection.cursor()
        cur.callproc('checkIfAddressExist', address)

        if cur.rowcount is not 0:
            result = cur.fetchone()
            addressId = result[0]
            cur.close()

            workspace = [jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasProjector'],jsonWorkspace['minPrice'], addressId]


            cur = mysql.connection.cursor()
            cur.callproc('addWorkspace', workspace)
            mysql.connection.commit()
            cur.close()

            return {},201

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

            return {},201

@api.route('/auth/login', methods=['POST'])
class Login(Resource):
    def post(self):

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
                ret = {'access_token': token}
                return ret, 200
            else:
                return {'Status': 'Error', 'Code': 'L002'}, 401
        else:
            return {'Status': 'Error', 'Code': 'L001'}, 401

### Old Optiroom
@api.route('/buildings')
class Buildings(Resource):
    def get(self):
        buildings = []
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM get_buildings")
        for building in cur:
            building = {
            'building_id': building[0],
            'building_name': building[1],
            'nb_floors': building[2] }
            buildings.append(building)
        return jsonify(buildings)

@api.route('/room/<string:room_id>')
class RoomID(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1', 'opti_light': 'avaliable', 'opti_heat': 'avaliable', 'nbSeats': '250', 'projector' : 'true', 'soundSystem': 'true'}}

        elif room_id == 'L04':
            return {'L04': {'numFloor': '0','idBuilding': '1', 'typeRoom': '2', 'opti_light': 'false', 'opti_heat': 'avaliable', 'nbSeats': '70', 'projector' : 'true', 'soundSystem': 'false'}}
        else:
        	return {'error':'Invalid room number'}, 404

@api.route('/state/<string:room_id>')
class RoomState(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'state': 'busy'}}
        elif room_id == 'L04':
            return {'L04': {'state': 'available'}}
        else:
        	return {'error':'Invalid room number'}, 404

if __name__ == '__main__':
    app.run(debug=_debug_, host='0.0.0.0', port=5000)
