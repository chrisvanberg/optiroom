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
global _margin_
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
app.config['MAIL_SERVER']='ssl0.ovh.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'no-reply@optiroom.net'
app.config['MAIL_PASSWORD'] = '4pfXkqXj9xRPI0loj1eWr0UPQ9R5G6'
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@optiroom.net'
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

        msg = Message('Bienvenue sur Optiroom !', sender=("Optiroom", "no-reply@optiroom.net"), recipients = [str(posted_username)])

        msg.html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> <head> <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta> <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0"></meta> </head> <body leftmargin="0" topmargin="0" marginwidth="0" margheight="0"> <table bgcolor="#228b22" width="100%" border="0" cellpadding="0" cellspacing="0"><tbody style="font-family: Helvetica, sans-serif"><tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr><tr> <td style="text-align: center"> <a href="https://dev.optiroom.net"> <img alt="Logo Optiroom" src="https://dev.optiroom.net/img/logo_christmas.png" width="300" border="0"></img> </a> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; font-size: 40px; color: white; text-align: center; line-height: 40px;">"""
        msg.html += "Bienvenue sur Optiroom "+posted_firstname+" "+posted_name
        msg.html += """ ! </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr><tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> Bonjour, nous sommes très heureux de confirmer votre inscription chez Optiroom. Nous sommes une plateforme en ligne de location d\'espaces de travail et de mise en location des vos espaces de travail. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr><tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> Rendez-vous sur Optiroom pour plus d\'informations. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="text-align: center"> <div><!--[if mso]> <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://dev.optiroom.net" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="125%" strokecolor="#1e3650" fillcolor="#FDE9E0"> <w:anchorlock/> <center style="color:#228b22;font-family:sans-serif;font-size:13px;font-weight:bold;">Mon compte Optiroom</center> </v:roundrect> <![endif]--><a href="https://dev.optiroom.net" style="background-color:#FDE9E0;border:1px solid #1e3650; border-radius:50px; color:#228b22; display:inline-block; font-family:sans-serif;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:200px;-webkit-text-size-adjust:none;mso-hide:all;">Mon compte Optiroom</a></div> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;<hr/></td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> <h4>Qu\'est ce qu\'optiroom ?</h4> Vous êtes à la recherche d’un espace de travail ? Notre plateforme vous permet de trouver un espace qui répond à vos besoins en quelques secondes. Il vous suffit d’effectuer une recherche et de choisir l\'espace qui vous convient le mieux selon son prix, son nombre de place et une multitude d\'autres critères. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: #FDE9E0; text-align: center; line-height: 28px; padding-left: 10%; padding-right: 10%"> Bonne journée, <br/>L\'équipe Optiroom. </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> </tbody> </table> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%"> This communication may contain privileged or other confidential information. If you are not the intended recipient , or believe that you may have received this communication in error, please reply to the sender indicating that fact and delete the copy you received. In addition, if you are not the intended recipient, you should not print, copy, retransmit, disseminate, or otherwise use the information contained in this communication. Thank you. </p> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%; color: green; font-weight: bolder"> Please consider your environmental responsibility before printing this e-mail </p> </body></html>"""

        mail.send(msg)

        return jsonify({'Status': 'Success'}), 201
    except Exception as e:
        if "Duplicate entry" in str(e):
            return jsonify({'Status': 'Error', 'Code': 'S001'}), 409
        elif DEBUG:
            return jsonify({'Status': 'Error', 'e': str(e)}), 409
        else:
            return jsonify({'Status': 'Error'}), 409

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
    cur = mysql.connection.cursor()
    cur.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
    result = cur.fetchone()
    customer_id = result[0]
    cur.close()

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


        workspace = [customer_id, jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasWifi'],jsonWorkspace['minPrice'], addressId]


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

        workspace = [customer_id, jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasProjector'],jsonWorkspace['minPrice'], addressId]


        cur = mysql.connection.cursor()
        cur.callproc('addWorkspace', workspace)
        mysql.connection.commit()
        cur.close()

        return jsonify({}),201

@app.route('/workspace/update', methods=['POST'])
@jwt_required
def workspaceUpdate():
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

        workspace = [jsonWorkspace['workspace_id'], jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasWifi'],jsonWorkspace['minPrice'], addressId]


        cur = mysql.connection.cursor()
        cur.callproc('updateWorkspace', workspace)
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

        workspace = [jsonWorkspace['workspace_id'], jsonWorkspace['workspaceName'], jsonWorkspace['seats'], jsonWorkspace['description'], jsonWorkspace['hasProjector'], jsonWorkspace['hasProjector'], addressId]


        cur = mysql.connection.cursor()
        cur.callproc('updateWorkspace', workspace)
        mysql.connection.commit()
        cur.close()

        return jsonify({}),201



@app.route('/workspace/<int:workspace_id>')
def workspaceId(workspace_id):

    cur = mysql.connection.cursor()
    cur.callproc('get_workspace_byWorkspaceId', [workspace_id])
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
        'price': str(round((float(result[10])/(1-BRUT_MARGIN))*(1+VAT),2)),
        'nbSeats': result[11],
        'hasProjector': result[12],
        'hasWifi': result[13] }

    return jsonify(workspace)

@app.route('/workspace/<int:workspace_id>/availability')
def getWorkspaceAvailability(workspace_id):
    posted_workspace_id = int(workspace_id)
    cur = mysql.connection.cursor()
    cur.callproc('checkIfAvailabilityExist', [posted_workspace_id])

    if cur.rowcount is not 0:
        cur.close()
        cur = mysql.connection.cursor()
        cur.callproc('get_availability_byWorkspaceId', [posted_workspace_id])
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



@app.route('/workspace/book', methods=['POST'])
@jwt_required
def workspaceBook():
    json_data = request.get_json(force=True)

    posted_workspace_id = json_data['workspace_id']
    posted_startDateTime = json_data['startDateTime']

    posted_nbHours = json_data['nbHours']

    posted_endDateTime = datetime.strptime(posted_startDateTime, '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=int(posted_nbHours))





    #bookingDuration = timedelta(json_data['startDateTime'], json_data['endDateTime'])

    cur = mysql.connection.cursor()
    data = [posted_workspace_id]
    cur.callproc('getMinPriceByWorkspaceId', data)
    result = cur.fetchone()
    price = str(round((float(result[0])/(1-BRUT_MARGIN))*(1+VAT),2))
    cur.close()




    cur = mysql.connection.cursor()
    data = [posted_workspace_id, posted_startDateTime, posted_endDateTime]
    #return jsonify(data)

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

        data = [posted_workspace_id, customer_id, posted_startDateTime, posted_endDateTime, price, bookingStatus.OK.value]
        cur.callproc('addBooking', data)

        mysql.connection.commit()
        cur.close()


        #Mail for booker

        cur = mysql.connection.cursor()
        cur.callproc('get_workspace_byWorkspaceId', [posted_workspace_id])
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
            'price': str(round((float(result[10])/(1-BRUT_MARGIN))*(1+VAT),2)),
            'nbSeats': result[11],
            'hasProjector': result[12],
            'hasWifi': result[13] }
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc('getUserInfoByEmail', [str(get_jwt_identity())])
        bookerInfo = cur.fetchone()


        booker_name=str(bookerInfo[1])
        booker_fullName=str(bookerInfo[1]+" "+bookerInfo[2])
        booker_mail=str(bookerInfo[3])
        booker_tel=str(bookerInfo[4])
        cur.close()

        cur = mysql.connection.cursor()
        cur.callproc('getUserInfoByWorkspaceId', [posted_workspace_id])
        ownerInfo = cur.fetchone()

        ownerId = str(ownerInfo[0])
        ownerFirstName = str(ownerInfo[1])
        ownerFullName = str(ownerInfo[1]+" "+ownerInfo[2])
        ownerEmail = str(ownerInfo[3])
        ownerTel = str(ownerInfo[4])

        cur.close()


        msg = Message('Votre réservation sur Optiroom !', sender=("Optiroom", "no-reply@optiroom.net"), recipients = [str(get_jwt_identity())])

        msg.html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"> <head> <meta http-equiv="content-type" content="text/html; charset=utf-8"></meta> <meta name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1.0"></meta> </head> <body leftmargin="0" topmargin="0" marginwidth="0" margheight="0"> <table bgcolor="#228b22" width="100%" border="0" cellpadding="0" cellspacing="0"> <tbody style="font-family: Helvetica, sans-serif"> <tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr> <tr> <td style="text-align: center"> <a href="https://dev.optiroom.net"> <img alt="Logo Optiroom" src="https://dev.optiroom.net/img/logo_christmas.png" width="300" border="0"></img> </a> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px;">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; font-size: 40px; color: white; text-align: center; line-height: 40px;">"""
        msg.html += "Bonjour "+booker_name
        msg.html += """ ! </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;">"""

        msg.html += "Vous avez réservé l'espace de travail \""+str(result[0])+"\"<br> à partir du "+str(posted_startDateTime)+"<br>jusqu'au "+str(posted_endDateTime)+"<br>Adresse : "+str(result[5])+" "+str(result[6])+", "+str(result[7])+" "+str(result[8])+", "+str(result[9])+"<br>Prix : "+str(price)

        msg.html += """€</td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="text-align: center"> <div> <!--[if mso]> <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="https://dev.optiroom.net" style="height:40px;v-text-anchor:middle;width:200px;" arcsize="125%" strokecolor="#1e3650" fillcolor="#FDE9E0"> <w:anchorlock/> <center style="color:#228b22;font-family:sans-serif;font-size:13px;font-weight:bold;">Mes réservations</center> </v:roundrect> <![endif]--> <a href="https://dev.optiroom.net" style="background-color:#FDE9E0;border:1px solid #1e3650;border-radius:50px;color:#228b22;display:inline-block;font-family:sans-serif;font-size:13px;font-weight:bold;line-height:40px;text-align:center;text-decoration:none;width:200px;-webkit-text-size-adjust:none;mso-hide:all;">Mes réservations</a> </div> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp; <hr/> </td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;"> Informations de contacts : </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td align="center" style="font-family: Helvetica, sans-serif; color: white; text-align: center; line-height: 28px;"> <table align="center"> <tbody> <tr> <td>"""
        msg.html += "<span style=\"color:white;text-align:center;\">"+ownerFullName+"</span><br><span style=\"color:white;text-align:center;\">"+ownerTel+"</span><br><span style=\"color:white;text-align:center;\">"+ownerEmail+"</span>"

        msg.html += """ </td> <td height="30" style="font-size: 30px; line-height: 30px; width: 7%; padding-left: 20%; padding-right: 20%">&nbsp;</td> <td> <img alt="Room" src="https://raw.githubusercontent.com/NathVoss/optiroom/dev/app/img/default-room.jpg" width="300" border="0" style="border-radius: 25px"></img> </td> </tr> </tbody> </table> </td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> <tr> <td height="30" style="font-size: 30px; line-height: 30px; width: 60%; padding-left: 20%; padding-right: 20%">&nbsp;</td> </tr> </tbody> </table> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%"> This communication may contain privileged or other confidential information. If you are not the intended recipient , or believe that you may have received this communication in error, please reply to the sender indicating that fact and delete the copy you received. In addition, if you are not the intended recipient, you should not print, copy, retransmit, disseminate, or otherwise use the information contained in this communication. Thank you. </p> <p align="center" style="padding-left: 5%; padding-right: 5%; padding-top: 1%; color: green; font-weight: bolder"> Please consider your environmental responsibility before printing this e-mail </p> </body></html>"""

        mail.send(msg)

        ownerMsg = Message('Nouvelle réservation sur Optiroom !', sender=("Optiroom", "no-reply@optiroom.net"), recipients = [ownerEmail])

        ownerMsg.html = """<?xml version="1.0" encoding="UTF-8"?>
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
                    Bonjour """+ownerFirstName+""" !
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
                        Votre espace de travail \""""+str(result[0])+"""\" à été réservé :<br/>
                      Date de début : """+str(posted_startDateTime)+"""<br/>
                      Date de fin : """+str(posted_endDateTime)+"""<br/>
                      Prix : """+str(price)+"""<br/>
                      Adresse : """+str(result[5])+""" """+str(result[6])+""", """+str(result[7])+""" """+str(result[8])+""", """+str(result[9])+"""<br/>
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
                    """+booker_fullName+"""<br/>
                    """+booker_tel+"""<br/>
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
        </html>

"""

        mail.send(ownerMsg)

        return jsonify({'Status': 'ok'}),201


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
            'price': str(round((float(workspace[11])/(1-BRUT_MARGIN))*(1+VAT),2)),
            'nbSeats': workspace[12],
            'hasProjector': workspace[13],
            'hasWifi': workspace[14] }

        workspaces.append(workspace)

    return jsonify(workspaces)

@app.route('/user/bookings')
@jwt_required
def userBookings():
    cur = mysql.connection.cursor()
    cur.callproc('getUserIdByUserEmail', [str(get_jwt_identity())])
    result = cur.fetchone()
    customer_id = result[0]
    cur.close()
    bookings = []

    cur = mysql.connection.cursor()
    cur.callproc('getBookingByCustomerId', [customer_id])

    for booking in cur:
        booking = {
        'booking_id': booking[0],
        'workspace_id': booking[1],
        'customer_id': booking[2],
        'startDate': booking[3],
        'endDate': booking[4],
        'price': str(booking[5]),
        'firstname': booking[6],
        'lastname': booking[7],
        'email': booking[8],
        'phone': booking[9]
        }

        bookings.append(booking)
    return jsonify(bookings)

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
            'price' : str(round((float(workspace[15])/(1-BRUT_MARGIN))*(1+VAT),2)),
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

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
