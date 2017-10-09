from flask import Flask
from flask import abort
from flask_restplus import Resource, Api
import socket

app = Flask(__name__)
api = Api(app)

@api.route('/system')
class System(Resource):
    def get(self):
        return {'state': 'up','version': '0.1.5', 'motd': 'N/A'}
        
@api.route('/motd')
class System(Resource):
    def get(self):
        return {'motd': 'N/A'}
        
@api.route('/rooms')
class Rooms(Resource):
    def get(self):
           return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1'},'L04': {'numFloor': '0','idBuilding': '1','typeRoom': '2'},'L35': {'numFloor': '0','idBuilding': '1','typeRoom': '2'}}

@api.route('/rooms/full')
class Rooms(Resource):
    def get(self):
           return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1', 'opti_light': 'avaliable', 'opti_heat': 'avaliable', 'nbSeats': '250', 'projector' : 'true', 'soundSystem': 'true'},'L04': {'numFloor': '0','idBuilding': '1','typeRoom': '2', 'opti_light': 'false', 'opti_heat': 'avaliable', 'nbSeats': '70', 'projector' : 'true', 'soundSystem': 'false'},'L35': {'numFloor': '0','idBuilding': '1','typeRoom': '2', 'opti_light': 'avaliable', 'opti_heat': 'false', 'nbSeats': '40', 'projector' : 'false', 'soundSystem': 'true'}}

                     
@api.route('/room/<string:room_id>')
class Room(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1', 'opti_light': 'avaliable', 'opti_heat': 'avaliable', 'nbSeats': '250', 'projector' : 'true', 'soundSystem': 'true'}}
        elif room_id == 'L04':
            return {'L04': {'numFloor': '0','idBuilding': '1', 'typeRoom': '2', 'opti_light': 'false', 'opti_heat': 'avaliable', 'nbSeats': '70', 'projector' : 'true', 'soundSystem': 'false'}}
        else:
        	return {'error':'Invalid room number'}, 404

@api.route('/state/<string:room_id>')
class Room(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'state': 'busy'}}
        elif room_id == 'L04':
            return {'L04': {'state': 'available'}}
        else:
        	return {'error':'Invalid room number'}, 404
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
