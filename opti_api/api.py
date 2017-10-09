from flask import Flask
from flask import abort
from flask_restplus import Resource, Api
import socket

app = Flask(__name__)
api = Api(app)

@api.route('/system')
class System(Resource):
    def get(self):
        return {'state': 'up','version': '0.1.4', 'motd': 'N/A'}
        
@api.route('/motd')
class System(Resource):
    def get(self):
        return {'motd': 'N/A'}
        
@api.route('/rooms')
class Rooms(Resource):
    def get(self):
           return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1'},'L04': {'numFloor': '0','idBuilding': '1','typeRoom': '2'},'L35': {'numFloor': '0','idBuilding': '1','typeRoom': '2'}}
                     
@api.route('/room/<string:room_id>')
class Room(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'A10': {'numFloor': '0','idBuilding': '1','typeRoom': '1'}}
        elif room_id == 'L04':
            return {'L04': {'numFloor': '0','idBuilding': '1', 'typeRoom': '2'}}
        else:
        	return {'error':'Invalid room number'}

@api.route('/state/<string:room_id>')
class Room(Resource):
    def get(self, room_id):
        if room_id == 'A10':
            return {'state': 'busy'}
        elif room_id == 'L04':
            return {'L04': {'numFloor': '0','idBuilding': '1', 'typeRoom': '2'}}
        else:
        	return {'error':'Invalid room number'}
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
