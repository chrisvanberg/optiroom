from flask import Flask
from flask import abort
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/system')
class System(Resource):
    def get(self):
        return {'state': 'up','network': 'optiroom.net','version': '0.1.2'}
        
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
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
