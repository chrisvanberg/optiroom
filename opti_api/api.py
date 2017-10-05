from flask import Flask
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

@api.route('/system')
class HelloWorld(Resource):
    def get(self):
        return {'state': 'up',
		'network': 'optiroom.net',
		'version': '0.1'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
