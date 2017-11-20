from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from flask_mysqldb import MySQL
from flask_restplus import Resource, Api
from flask import request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
global _debug_
global _version_

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)

_debug_ = True
_version_ = "0.2.9"

mysql = MySQL()
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['JWT_SECRET_KEY'] = 'optiroom'  # Change this!
app.config['MYSQL_HOST'] = 'dev.optiroom.net'
app.config['MYSQL_USER'] = 'opti_api'
app.config['MYSQL_PASSWORD'] = 'YFdcxYJS:ng3PcvndfGeIeRxhuOYiP'
app.config['MYSQL_DB'] = 'optiroom'
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

@api.route('/rooms')
class Rooms(Resource):
    def get(self):
        rooms = []
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM get_rooms")
        for row in cur:
            room = {
            'building_id': row[0],
            'building_name': row[1],
            'room_id': row[2],
            'floorNum': row[3],
            'roomType': row[4],
            'roomDescription': row[5]}
            rooms.append(room)
        return jsonify(rooms)

@api.route('/rooms/full')
class RoomsFull(Resource):
    def get(self):
        rooms = []
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM get_roomsFull")
        for row in cur:
            room = {
            'building_id': row[0],
            'building_name': row[1],
            'room_id': row[2],
            'floorNum': row[3],
            'roomType': row[4],
            'roomDescription': row[5],
            'nbPlace': row[6],
            'hasSpeaker': row[7],
            'hasProjector': row[8]}
            rooms.append(room)
        return jsonify(rooms)

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

if __name__ == '__main__':
    app.run(debug=_debug_, host='0.0.0.0', port=5000)
