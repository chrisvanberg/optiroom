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
from datetime import timedelta, datetime
from dateutil import parser
from enum import Enum
from flask_mail import Mail, Message
import os

global DEBUG
global VERSION
global BRUT_MARGIN
global VAT

DEBUG = os.environ['DEBUG']
VERSION = "0.4"
BRUT_MARGIN = float(0.30)
VAT = float(0.21)

api = Api()
app = Flask(__name__)
api.init_app(app)

bcrypt = Bcrypt(app)

#MySQLConfig
mysql = MySQL()
app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
mysql.init_app(app)

#JWTConfig
app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

#MailConfig
app.config['MAIL_SERVER']= os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = int(os.environ['MAIL_PORT'])
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = os.environ['MAIL_DEFAULT_SENDER']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

if DEBUG:
    #Cors let the API being accessed localy when developping a client who respect Cors policy
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

class bookingStatus(Enum):
    OK = 1
    WAITING_FOR_PAYMENT = 2
    PAYMENT_ERROR = 3
    CANCELED = 4

@app.route('/system', methods=['GET'])
def system():
    return jsonify({'state': 'up','version': VERSION})

@app.route('/auth/signup', methods=['POST'])
def Signin():

    json_data = request.get_json(force=True)
    posted_email = json_data['mail']
    posted_last_name = json_data['name']
    posted_first_name = json_data['firstname']
    posted_password = json_data['password']
    posted_phone = json_data['phone']
    hashed_password = (bcrypt.generate_password_hash(posted_password)).decode('UTF-8')

    user_data = [posted_first_name, posted_last_name, posted_email, posted_phone, hashed_password]

    try:
        opti_db = mysql.connection.cursor()
        opti_db.callproc('sign_up', user_data)
        mysql.connection.commit()

        signup_msg = Message('Bienvenue sur Optiroom !', sender=("Optiroom", "no-reply@optiroom.net"), recipients = [str(posted_email)])

        signup_msg.html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> <head> <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta> <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0"></meta> </head> <body leftmargin="0" topmargin="0" marginwidth="0" margheight="0"> <table bgcolor="#228b22" width="100%" border="0" cellpadding="0" cellspacing="0"><tbody style="font-family: Helvetica, sans-serif"><tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr><tr> <td style="text-align: center"> <a href="https://dev.optiroom.net"> <img alt="Logo Optiroom" src="https://dev.optiroom.net/img/logo_christmas.png" width="300" border="0"></img> </a> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; font-size: 40px; color: white; text-align: center; line-height: 40px;">"""
        signup_msg.html += "Bienvenue sur Optiroom "+posted_first_name+" "+posted_last_name
        signup_msg.html += """ ! </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr><tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> Bonjour, nous sommes très heureux de confirmer votre inscription chez Optiroom. Nous sommes une plateforme en ligne de location d\'espaces de travail et de mise en location des vos espaces de travail. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr><tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> Rendez-vous sur Optiroom pour plus d\'informations. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="text-align: center"> <div><!--[if mso]> <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://dev.optiroom.net" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="125%" strokecolor="#1e3650" fillcolor="#FDE9E0"> <w:anchorlock/> <center style="color:#228b22;font-family:sans-serif;font-size:13px;font-weight:bold;">Mon compte Optiroom</center> </v:roundrect> <![endif]--><a href="https://dev.optiroom.net" style="background-color:#FDE9E0;border:1px solid #1e3650; border-radius:50px; color:#228b22; display:inline-block; font-family:sans-serif;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:200px;-webkit-text-size-adjust:none;mso-hide:all;">Mon compte Optiroom</a></div> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;<hr/></td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> <h4>Qu\'est ce qu\'optiroom ?</h4> Vous êtes à la recherche d’un espace de travail ? Notre plateforme vous permet de trouver un espace qui répond à vos besoins en quelques secondes. Il vous suffit d’effectuer une recherche et de choisir l\'espace qui vous convient le mieux selon son prix, son nombre de place et une multitude d\'autres critères. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> Bonne journée, <br/>L\'équipe Optiroom. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> </tbody> </table> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%"> This communication may contain privileged or other confidential information. If you are not the intended recipient , or believe that you may have received this communication in error, please reply to the sender indicating that fact and delete the copy you received. In addition, if you are not the intended recipient, you should not print, copy, retransmit, disseminate, or otherwise use the information contained in this communication. Thank you. </p> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%; color: green; font-weight: bolder"> Please consider your environmental responsibility before printing this e-mail </p> </body></html>"""

        mail.send(signup_msg)

        return jsonify({'Status': 'Success'}), 201
    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({'Status': 'Error', 'Code': 'S001'}), 409

        elif "Recipient address rejected" in str(e):
            opti_db = mysql.connection.cursor()
            opti_db.callproc('deleteUserByUserEmail', [posted_email])
            mysql.connection.commit()
            return jsonify({'Status': 'Error', 'Code': 'S002'}), 409

        elif DEBUG:
            return jsonify({'Status': 'Error', 'e': str(e)}), 409

        else:
            return jsonify({'Status': 'Error'}), 409

@app.route('/auth/login', methods=['POST'])
def login():
    json_data = request.get_json(force=True)
    posted_email = json_data['username']
    posted_password = json_data['password']

    opti_db = mysql.connection.cursor()
    opti_db.callproc('getHash', [posted_email])

    #If the is no user registered with this email address
    if opti_db.rowcount is 0:
        return jsonify({'Status': 'Error', 'Code': 'L001'}), 401

    #If there is an user registered with this email address
    else:
        result = opti_db.fetchone()
        first_name = result[0]
        last_name = result[1]
        hashed_password = result[2]

        if bcrypt.check_password_hash(hashed_password, posted_password) :
            token = create_access_token(identity=posted_email)
            return jsonify({'access_token': token}), 200
        else:
            return jsonify({'Status': 'Error', 'Code': 'L002'}), 401


@app.route('/workspaces')
def Workspaces():
    workspaces = []
    opti_db = mysql.connection.cursor()
    opti_db.execute("SELECT * FROM get_workspace")
    for workspace in opti_db:
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
    opti_db = mysql.connection.cursor()
    opti_db.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
    result = opti_db.fetchone()
    owner_id = result[0]
    opti_db.close()

    json_data = request.get_json(force=True)
    json_address = json_data['address']
    address = [json_address['buildingName'], json_address['street'], json_address['number'], json_address['postcode'], json_address['city'], json_address['country'], json_address['latitude'], json_address['longitude']]

    json_workspace = json_data['workspace']

    opti_db = mysql.connection.cursor()
    opti_db.callproc('checkIfAddressExist', address)

    #If the address already exist
    if opti_db.rowcount is not 0:
        result = opti_db.fetchone()
        address_id = result[0]
        opti_db.close()


        workspace = [owner_id, json_workspace['workspaceName'], json_workspace['seats'], json_workspace['description'], json_workspace['hasProjector'], json_workspace['hasWifi'],json_workspace['minPrice'], address_id]


        opti_db = mysql.connection.cursor()
        opti_db.callproc('addWorkspace', workspace)
        mysql.connection.commit()
        opti_db.close()

        return jsonify({}),201

    #If the address doesn't exist yet
    else:
        opti_db.close()
        opti_db = mysql.connection.cursor()
        opti_db.callproc('addWorkspaceAddress', address)
        mysql.connection.commit()
        opti_db.close()

        opti_db = mysql.connection.cursor()
        opti_db.callproc('checkIfAddressExist', address)
        result = opti_db.fetchone()
        address_id = result[0]
        opti_db.close()

        workspace = [owner_id, json_workspace['workspaceName'], json_workspace['seats'], json_workspace['description'], json_workspace['hasProjector'], json_workspace['hasProjector'],json_workspace['minPrice'], address_id]

        opti_db = mysql.connection.cursor()
        opti_db.callproc('addWorkspace', workspace)
        mysql.connection.commit()
        opti_db.close()

        return jsonify({}),201

@app.route('/workspace/update', methods=['POST'])
@jwt_required
def workspaceUpdate():
    json_data = request.get_json(force=True)
    json_address = json_data['address']
    address = [json_address['buildingName'], json_address['street'], json_address['number'], json_address['postcode'], json_address['city'], json_address['country'], json_address['latitude'], json_address['longitude']]
    json_workspace = json_data['workspace']


    opti_db = mysql.connection.cursor()
    opti_db.callproc('checkIfAddressExist', address)

    if opti_db.rowcount is not 0:
        result = opti_db.fetchone()
        address_id = result[0]
        opti_db.close()

        workspace = [json_workspace['workspace_id'], json_workspace['workspaceName'], json_workspace['seats'], json_workspace['description'], json_workspace['hasProjector'], json_workspace['hasWifi'],json_workspace['minPrice'], address_id]


        opti_db = mysql.connection.cursor()
        opti_db.callproc('updateWorkspace', workspace)
        mysql.connection.commit()
        opti_db.close()

        return jsonify({}),201

    else:
        opti_db.close()
        opti_db = mysql.connection.cursor()
        opti_db.callproc('addWorkspaceAddress', address)
        mysql.connection.commit()
        opti_db.close()

        opti_db = mysql.connection.cursor()
        opti_db.callproc('checkIfAddressExist', address)
        result = opti_db.fetchone()
        address_id = result[0]
        opti_db.close()

        workspace = [json_workspace['workspace_id'], json_workspace['workspaceName'], json_workspace['seats'], json_workspace['description'], json_workspace['hasProjector'], json_workspace['hasProjector'], address_id]


        opti_db = mysql.connection.cursor()
        opti_db.callproc('updateWorkspace', workspace)
        mysql.connection.commit()
        opti_db.close()

        return jsonify({}),201



@app.route('/workspace/<int:workspace_id>')
def workspaceId(workspace_id):
    opti_db = mysql.connection.cursor()
    opti_db.callproc('get_workspace_byWorkspaceId', [workspace_id])
    result = opti_db.fetchone()

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
        'price': str(round((float(result[10])/(1-BRUT_MARGIN))*(1+VAT),2)),
        'nbSeats': result[11],
        'hasProjector': result[12],
        'hasWifi': result[13] }

    return jsonify(workspace)

@app.route('/workspace/<int:workspace_id>/availability')
def getWorkspaceAvailability(workspace_id):
    posted_workspace_id = int(workspace_id)
    opti_db = mysql.connection.cursor()
    opti_db.callproc('checkIfAvailabilityExist', [posted_workspace_id])

    if opti_db.rowcount is not 0:
        opti_db.close()
        opti_db = mysql.connection.cursor()
        opti_db.callproc('get_availability_byWorkspaceId', [posted_workspace_id])
        result = opti_db.fetchone()

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


@app.route('/workspace/availability', methods=['POST'])
@jwt_required
def addAvailability():
    json_data = request.get_json(force=True)

    posted_workspace_id = json_data['workspace_id']
    posted_opening_days = json_data['openingDays']
    posted_mon_opening_hour = json_data['monOpeningHour']
    posted_mon_closing_hour = json_data['monClosingHour']
    posted_tue_opening_hour = json_data['tueOpeningHour']
    posted_tue_closing_hour = json_data['tueClosingHour']
    posted_wed_opening_hour = json_data['wedOpeningHour']
    posted_wed_closing_hour = json_data['wedClosingHour']
    posted_thu_opening_hour = json_data['thuOpeningHour']
    posted_thu_closing_hour = json_data['thuClosingHour']
    posted_fri_opening_hour = json_data['friOpeningHour']
    posted_fri_closing_hour = json_data['friClosingHour']
    posted_sat_opening_hour = json_data['satOpeningHour']
    posted_sat_closing_hour = json_data['satClosingHour']
    posted_sun_opening_hour = json_data['sunOpeningHour']
    posted_sun_closing_hour = json_data['sunClosingHour']

    availability = [posted_workspace_id, posted_opening_days, posted_mon_opening_hour, posted_mon_closing_hour, posted_tue_opening_hour, posted_tue_opening_hour, posted_wed_opening_hour, posted_wed_closing_hour, posted_thu_opening_hour, posted_thu_closing_hour, posted_fri_opening_hour, posted_fri_closing_hour, posted_sat_opening_hour, posted_sat_closing_hour, posted_sun_opening_hour, posted_sun_closing_hour]

    opti_db = mysql.connection.cursor()
    opti_db.callproc('checkIfAvailabilityExist', [posted_workspace_id])

    if opti_db.rowcount is not 0:
        opti_db.close()
        opti_db = mysql.connection.cursor()
        opti_db.callproc('updateAvailability', availability)
        mysql.connection.commit()
        opti_db.close()

        return jsonify({}),201

    else:
        opti_db.close()
        opti_db = mysql.connection.cursor()
        opti_db.callproc('checkIfWorkspaceExist', [posted_workspace_id])

        if opti_db.rowcount is not 0:
            opti_db.close()
            opti_db = mysql.connection.cursor()
            opti_db.callproc('addAvailability', availability)
            mysql.connection.commit()
            opti_db.close()
            return jsonify({}),201

        else:
            return jsonify({'Status': 'Error', 'Code': 'A001'}), 404



@app.route('/workspace/book', methods=['POST'])
@jwt_required
def workspaceBook():
    json_data = request.get_json(force=True)

    posted_workspace_id = json_data['workspace_id']
    posted_start_datetime = json_data['startDateTime']
    posted_nb_hours = json_data['nbHours']
    posted_end_datetime = datetime.strptime(posted_start_datetime, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=int(posted_nb_hours))

    opti_db = mysql.connection.cursor()
    opti_db.callproc('getMinPriceByWorkspaceId', [posted_workspace_id])
    result = opti_db.fetchone()
    min_price = result[0]
    price = str(round((float(min_price)/(1-BRUT_MARGIN))*(1+VAT),2))
    opti_db.close()

    opti_db = mysql.connection.cursor()
    booking = [posted_workspace_id, posted_start_datetime, posted_end_datetime]

    opti_db.callproc('checkIfScheduleIsOK', booking)

    if opti_db.rowcount is not 0:

        return jsonify({'Status': 'Error', 'Code': 'B001'}), 409

    else:
        opti_db.close()

        opti_db = mysql.connection.cursor()
        opti_db.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
        result = opti_db.fetchone()
        customer_id = result[0]
        opti_db.close()
        opti_db = mysql.connection.cursor()

        booking = [posted_workspace_id, customer_id, posted_start_datetime, posted_end_datetime, price, bookingStatus.OK.value]
        opti_db.callproc('addBooking', booking)

        mysql.connection.commit()
        opti_db.close()

        #Mail Infos
        opti_db = mysql.connection.cursor()
        opti_db.callproc('get_workspace_byWorkspaceId', [posted_workspace_id])
        result = opti_db.fetchone()

        booked_workspace = {
            'workspace_name': str(result[0]),
            'description': str(result[1]),
            'building_name': str(result[2]),
            'latitude': str(result[3]),
            'longitude': str(result[4]),
            'street': str(result[5]),
            'building_number': str(result[6]),
            'postcode': str(result[7]),
            'city': str(result[8]),
            'country': str(result[9]),
            'minPrice': str(result[10]),
            'price': str(round((float(result[10])/(1-BRUT_MARGIN))*(1+VAT),2)),
            'nbSeats': str(result[11]),
            'hasProjector': str(result[12]),
            'hasWifi': str(result[13]) }
        opti_db.close()

        opti_db = mysql.connection.cursor()
        opti_db.callproc('getUserInfoByEmail', [str(get_jwt_identity())])

        booker_infos = opti_db.fetchone()
        booker_first_name=str(booker_infos[1])
        booker_full_name=str(booker_infos[1]+" "+booker_infos[2])
        booker_email=str(booker_infos[3])
        booker_phone=str(booker_infos[4])
        opti_db.close()

        opti_db = mysql.connection.cursor()
        opti_db.callproc('getUserInfoByWorkspaceId', [posted_workspace_id])

        owner_infos = opti_db.fetchone()
        owner_id = str(owner_infos[0])
        owner_first_name = str(owner_infos[1])
        owner_full_name = str(owner_infos[1]+" "+owner_infos[2])
        owner_email = str(owner_infos[3])
        owner_phone = str(owner_infos[4])
        opti_db.close()


        booker_msg = Message('Votre réservation sur Optiroom !', sender=("Optiroom", "no-reply@optiroom.net"), recipients = [str(get_jwt_identity())])

        booker_msg.html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> <head> <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta> <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0"></meta> </head> <body leftmargin="0" topmargin="0" marginwidth="0" margheight="0"> <table bgcolor="#228b22" width="100%" border="0" cellpadding="0" cellspacing="0"> <tbody style="font-family: Helvetica, sans-serif"> <tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr> <tr> <td style="text-align: center"> <a href="https://dev.optiroom.net"> <img alt="Logo Optiroom" src="https://dev.optiroom.net/img/logo_christmas.png" width="300" border="0"></img> </a> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; font-size: 40px; color: white; text-align: center; line-height: 40px;">"""
        booker_msg.html += "Bonjour "+booker_first_name
        booker_msg.html += """ ! </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;">"""

        booker_msg.html += "Vous avez réservé l'espace de travail \""+booked_workspace['workspace_name']+"\"<br> à partir du "+str(posted_start_datetime)+"<br>jusqu'au "+str(posted_end_datetime)+"<br>Adresse : "+booked_workspace['street']+" "+booked_workspace['building_number']+", "+booked_workspace['postcode']+" "+booked_workspace['city']+", "+booked_workspace['country']+"<br>Prix : "+booked_workspace['price']

        booker_msg.html += """€</td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="text-align: center"> <div> <!--[if mso]> <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://dev.optiroom.net" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="125%" strokecolor="#1e3650" fillcolor="#FDE9E0"> <w:anchorlock/> <center style="color:#228b22;font-family:sans-serif;font-size:13px;font-weight:bold;">Mes réservations</center> </v:roundrect> <![endif]--> <a href="https://dev.optiroom.net" style="background-color:#FDE9E0;border:1px solid #1e3650;border-radius:50px;color:#228b22;display:inline-block;font-family:sans-serif;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:200px;-webkit-text-size-adjust:none;mso-hide:all;">Mes réservations</a> </div> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp; <hr/> </td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;"> Informations de contacts : </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;"> <table align="center"> <tbody> <tr> <td>"""
        booker_msg.html += "<span style=\"color:white;text-align:center;\">"+owner_full_name+"</span><br><span style=\"color:white;text-align:center;\">"+owner_phone+"</span><br><span style=\"color:white;text-align:center;\">"+owner_email+"</span>"

        booker_msg.html += """ </td> <td height="30" style="font-size: 30px; line-height: 30px; width: 7%; padding-left: 20%; padding-right: 20%">&nbsp;</td> <td> <img alt="Room" src="https://raw.githubusercontent.com/NathVoss/optiroom/dev/app/img/default-room.jpg" width="300" border="0" style="border-radius: 25px"></img> </td> </tr> </tbody> </table> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> </tbody> </table> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%"> This communication may contain privileged or other confidential information. If you are not the intended recipient , or believe that you may have received this communication in error, please reply to the sender indicating that fact and delete the copy you received. In addition, if you are not the intended recipient, you should not print, copy, retransmit, disseminate, or otherwise use the information contained in this communication. Thank you. </p> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%; color: green; font-weight: bolder"> Please consider your environmental responsibility before printing this e-mail </p> </body></html>"""

        mail.send(booker_msg)

        owner_msg = Message('Nouvelle réservation sur Optiroom !', sender=("Optiroom", "no-reply@optiroom.net"), recipients = [owner_email])

        owner_msg.html = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html
                PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta>
            <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0"></meta>
        </head>
        <body leftmargin="0" topmargin="0" marginwidth="0" margheight="0">
        <table bgcolor="#228b22" width="100%" border="0" cellpadding="0" cellspacing="0">
            <tbody style="font-family: Helvetica, sans-serif">
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px;"></td>
            </tr>
            <tr>
                <td colspan="2" style="text-align: center">
                    <a href="https://dev.optiroom.net">
                        <img alt="Logo Optiroom" src="https://dev.optiroom.net/img/logo_christmas.png" width="300" border="0"></img>
                    </a>
                </td>
            </tr>
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td>
            </tr>
            <tr>
                <td colspan="2" align="center" style="font-family: Helvetica, sans-serif; font-size: 40px; color: white; text-align: center; line-height: 40px;">
                    Bonjour """+owner_first_name+""" !
                </td>
            </tr>
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td>
            </tr>
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td>
            </tr>
            <tr>
                <td colspan="2" align="center" style="text-align: center">
                    <div><!--[if mso]>
                        <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://dev.optiroom.net" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="125%" strokecolor="#1e3650" fillcolor="#FDE9E0">
                            <w:anchorlock/>
                            <center style="color:#228b22;font-family:sans-serif;font-size:13px;font-weight:bold;">Mes workspaces</center>
                        </v:roundrect>
                        <![endif]--><a href="https://dev.optiroom.net"
                                       style="background-color:#FDE9E0;border:1px solid #1e3650;border-radius:50px;color:#228b22;display:inline-block;font-family:sans-serif;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:200px;-webkit-text-size-adjust:none;mso-hide:all;">Mes workspaces</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td>
            </tr>
            <tr>
                <td align="right" style="font-family: Helvetica, sans-serif; color: white; text-align: right; line-height: 28px;">
                      <div style="margin:1em;">
                        Votre espace de travail \""""+booked_workspace['workspace_name']+"""\" à été réservé :<br/>
                      Date de début : """+str(posted_start_datetime)+"""<br/>
                      Date de fin : """+str(posted_end_datetime)+"""<br/>
                      Prix : """+booked_workspace['price']+"""<br/>
                      Adresse : """+booked_workspace['street']+""" """+booked_workspace['building_number']+""", """+booked_workspace['postcode']+""" """+booked_workspace['city']+""", """+booked_workspace['country']+"""<br/>
                    </div>
                </td>
                <td align="left" style="text-align:left">
                    <img alt="Room" src="https://raw.githubusercontent.com/NathVoss/optiroom/dev/app/img/default-room.jpg" width="300" border="0" style="border-radius: 25px"></img>
                </td>
            </tr>



            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%"><hr></td>
            </tr>

            <tr>
                <td colspan="2" align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;">
                    <h3>Informations de contacts :</h3>
                    """+booker_full_name+"""<br/>
                    """+booker_phone+"""<br/>
                    """+str(get_jwt_identity())+"""<br/>
                </td>
            </tr>
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td>
            </tr>
            <tr>
                <td colspan="2" align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;">
                    Bien à vous<br/>
                    L'équipe d'Optiroom !
                </td>
            </tr>
            <tr>
                <td colspan="2" height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td>
            </tr>
            </tbody>
        </table>
        <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%">
            Thish communication may contain privileged or other confidential information. If you are not the intended recipient , or believe that you may have received this communication in error, please reply to the sender indicating that fact and delete the copy you received. In addition, if you are not the intended recipient, you should not print, copy, retransmit, disseminate, or otherwise use the information contained in this communication. Thank you.
        </p>
        <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%; color: green; font-weight: bolder">
            Please consider your environmental responsibility before printing this e-mail
        </p>
        </body>
        </html>"""

        mail.send(owner_msg)

        return jsonify({'Status': 'ok'}),201


@app.route('/workspace/book/status', methods=['POST'])
@jwt_required
def workSpaceBookStatus():
    json_data = request.get_json(force=True)

    posted_booking_id = json_data['booking_id']
    posted_status = json_data['status']

    booking = [posted_booking_id, posted_status]

    opti_db = mysql.connection.cursor()
    opti_db.callproc('updateBookingStatus', booking)
    mysql.connection.commit()
    opti_db.close

    return jsonify({'Status': 'ok'}),201



@app.route('/user/workspaces')
@jwt_required
def UserWorkspaces():
    opti_db = mysql.connection.cursor()
    opti_db.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
    result = opti_db.fetchone()
    owner_id = result[0]
    opti_db.close()

    workspaces = []

    opti_db = mysql.connection.cursor()
    opti_db.callproc('get_workspaces_byOwnerId', [int(owner_id)])

    for workspace in opti_db:
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
            'price': str(round((float(workspace[11])/(1-BRUT_MARGIN))*(1+VAT),2)),
            'nbSeats': workspace[12],
            'hasProjector': workspace[13],
            'hasWifi': workspace[14] }

        workspaces.append(workspace)

    return jsonify(workspaces)

@app.route('/user/bookings')
@jwt_required
def userBookings():
    opti_db = mysql.connection.cursor()
    opti_db.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
    result = opti_db.fetchone()
    customer_id = result[0]
    opti_db.close()

    bookings = []

    opti_db = mysql.connection.cursor()
    opti_db.callproc('getBookingByCustomerId', [customer_id])

    for booking in opti_db:
        booking = {
        'booking_id': booking[0],
        'workspace_id': booking[1],
        'customer_id': booking[2],
        'startDate': booking[3],
        'endDate': booking[4],
        'price': str(booking[5]),
        'first_name': booking[6],
        'last_name': booking[7],
        'email': booking[8],
        'phone': booking[9]
        }

        bookings.append(booking)
    return jsonify(bookings)

@app.route('/search/<float:center_latitude>/<float:center_longitude>/<int:range_in_km>/<string:day>/<int:min_seats>')
def Search(center_latitude, center_longitude, range_in_km, day, min_seats):
    range_in_degree = (range_in_km / 40000) * 360
    radius_in_degree = range_in_degree / 2

    opening_days = {}
    #Used in a 'LIKE' condition in MySQL
    opening_days['mon'] = "1______"
    opening_days['tue'] = "_1_____"
    opening_days['wed'] = "__1____"
    opening_days['thu'] = "___1___"
    opening_days['fri'] = "____1__"
    opening_days['sat'] = "_____1_"
    opening_days['sun'] = "______1"

    min_latitude = center_latitude - radius_in_degree
    max_latitude = center_latitude + radius_in_degree

    minLongitude = center_longitude - radius_in_degree
    maxLongitude = center_longitude + radius_in_degree

    searchInputs = [min_latitude, max_latitude, minLongitude, maxLongitude, min_seats, opening_days[day.lower()]]

    workspaces = []

    opti_db = mysql.connection.cursor()
    opti_db.callproc("simple_search", searchInputs)

    for workspace in opti_db:
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
            'price' : str(round((float(workspace[15])/(1-BRUT_MARGIN))*(1+VAT),2)),
            'opening_days' : workspace[16],
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
            'first_name' : workspace[32],
            'last_name' : workspace[33],
            'email' : workspace[34] }
        workspaces.append(workspace)

    return jsonify(workspaces)

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
