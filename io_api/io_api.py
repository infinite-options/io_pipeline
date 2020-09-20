#To run program:  python3 io_api.py 

#README:  if conn error make sure password is set properly in RDS PASSWORD section

#README:  Debug Mode may need to be set to False when deploying live (although it seems to be working through Zappa)

#README:  if there are errors, make sure you have all requirements are loaded
#pip3 install flask
#pip3 install flask_restful
#pip3 install flask_cors
#pip3 install Werkzeug
#pip3 install pymysql
#pip3 install python-dateutil
#pip3 install twilio

import os
import uuid
import boto3
import json
import math
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import random
import string
import stripe

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_mail import Mail, Message
# used for serializer email and error handling
#from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
#from flask_cors import CORS

from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import generate_password_hash, \
     check_password_hash


#  NEED TO SOLVE THIS
# from NotificationHub import Notification
# from NotificationHub import NotificationHub

import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from twilio.rest import Client

from dateutil.relativedelta import *
from decimal import Decimal
from datetime import datetime, date, timedelta
from hashlib import sha512
from math import ceil
import string
import random

# BING API KEY
# Import Bing API key into bing_api_key.py

#  NEED TO SOLVE THIS
# from env_keys import BING_API_KEY, RDS_PW

import decimal
import sys
import json
import pytz
import pymysql
import requests

#RDS_HOST = 'pm-mysqldb.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
RDS_HOST = 'io-mysqldb8.cxjnrciilyjq.us-west-1.rds.amazonaws.com'
#RDS_HOST = 'localhost'
RDS_PORT = 3306
#RDS_USER = 'root'
RDS_USER = 'admin'
#RDS_DB = 'feed_the_hungry'
RDS_DB = 'sf'

#app = Flask(__name__)
app = Flask(__name__, template_folder='assets')

# --------------- Stripe Variables ------------------
# these key are using for testing. Customer should use their stripe account's keys instead
import stripe
stripe_public_key = 'pk_test_6RSoSd9tJgB2fN2hGkEDHCXp00MQdrK3Tw'
stripe_secret_key = 'sk_test_fe99fW2owhFEGTACgW3qaykd006gHUwj1j'

#this is a testing key using ptydtesting's stripe account.
# stripe_public_key = "pk_test_51H0sExEDOlfePYdd9TVlnhVDOCmmnmdxAxyAmgW4x7OI0CR7tTrGE2AyrTk8VjftoigEOhv2RTUv5F8yJrfp4jWQ00Q6KGXDHV"
# stripe_secret_key = "sk_test_51H0sExEDOlfePYdd9UQDxfp8yoY7On272hCR9ti12WSNbIGTysaJI8K2W8NhCKqdBOEhiNj4vFOtQu6goliov8vF00cvqfWG6d"

stripe.api_key = stripe_secret_key
# Allow cross-origin resource sharing
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})

# --------------- Mail Variables ------------------
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
# app.config['MAIL_USERNAME'] = ''
# app.config['MAIL_PASSWORD'] = ''

# Setting for mydomain.com
app.config['MAIL_SERVER'] = 'smtp.mydomain.com'
app.config['MAIL_PORT'] = 465

# Setting for gmail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



# Set this to false when deploying to live application
#app.config['DEBUG'] = True
app.config['DEBUG'] = False

app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY')

mail = Mail(app)

# API
api = Api(app)

# convert to UTC time zone when testing in local time zone
utc = pytz.utc
def getToday(): return datetime.strftime(datetime.now(utc), "%Y-%m-%d")
def getNow(): return datetime.strftime(datetime.now(utc),"%Y-%m-%d %H:%M:%S")

# Get RDS password from command line argument
def RdsPw():
    if len(sys.argv) == 2:
        return str(sys.argv[1])
    return ""

# RDS PASSWORD
# When deploying to Zappa, set RDS_PW equal to the password as a string
# When pushing to GitHub, set RDS_PW equal to RdsPw()
RDS_PW = 'prashant'
# RDS_PW = RdsPw()


s3 = boto3.client('s3')

# aws s3 bucket where the image is stored
# BUCKET_NAME = os.environ.get('MEAL_IMAGES_BUCKET')
BUCKET_NAME = 'servingnow'
# allowed extensions for uploading a profile photo file
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



getToday = lambda: datetime.strftime(date.today(), "%Y-%m-%d")
getNow = lambda: datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

# For Push notification
isDebug = False
NOTIFICATION_HUB_KEY = os.environ.get('NOTIFICATION_HUB_KEY')
NOTIFICATION_HUB_NAME = os.environ.get('NOTIFICATION_HUB_NAME')

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')	
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

# Connect to MySQL database (API v2)
def connect():
    global RDS_PW
    global RDS_HOST
    global RDS_PORT
    global RDS_USER
    global RDS_DB

    print("Trying to connect to RDS (API v2)...")
    try:
        conn = pymysql.connect( RDS_HOST,
                                user=RDS_USER,
                                port=RDS_PORT,
                                passwd=RDS_PW,
                                db=RDS_DB,
                                cursorclass=pymysql.cursors.DictCursor)
        print("Successfully connected to RDS. (API v2)")
        return conn
    except:
        print("Could not connect to RDS. (API v2)")
        raise Exception("RDS Connection failed. (API v2)")

# Disconnect from MySQL database (API v2)
def disconnect(conn):
    try:
        conn.close()
        print("Successfully disconnected from MySQL database. (API v2)")
    except:
        print("Could not properly disconnect from MySQL database. (API v2)")
        raise Exception("Failure disconnecting from MySQL database. (API v2)")

# Serialize JSON
def serializeResponse(response):
    try:
        print("In Serialize JSON")
        for row in response:
            for key in row:
                if type(row[key]) is Decimal:
                    row[key] = float(row[key])
                elif type(row[key]) is date or type(row[key]) is datetime:
                    row[key] = row[key].strftime("%Y-%m-%d")
        print("In Serialize JSON response", response)
        return response
    except:
        raise Exception("Bad query JSON")








# Execute an SQL command (API v2)
# Set cmd parameter to 'get' or 'post'
# Set conn parameter to connection object
# OPTIONAL: Set skipSerialization to True to skip default JSON response serialization
def execute(sql, cmd, conn, skipSerialization = False):
    response = {}
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            if cmd is 'get':
                result = cur.fetchall()
                response['message'] = 'Successfully executed SQL query.'
                # Return status code of 280 for successful GET request
                response['code'] = 280
                if not skipSerialization:
                    result = serializeResponse(result)
                response['result'] = result
            elif cmd in 'post':
                conn.commit()
                response['message'] = 'Successfully committed SQL command.'
                # Return status code of 281 for successful POST request
                response['code'] = 281
            else:
                response['message'] = 'Request failed. Unknown or ambiguous instruction given for MySQL command.'
                # Return status code of 480 for unknown HTTP method
                response['code'] = 480
    except:
        response['message'] = 'Request failed, could not execute MySQL command.'
        # Return status code of 490 for unsuccessful HTTP request
        response['code'] = 490
    finally:
        response['sql'] = sql
        return response

# Close RDS connection
def closeRdsConn(cur, conn):
    try:
        cur.close()
        conn.close()
        print("Successfully closed RDS connection.")
    except:
        print("Could not close RDS connection.")

# Runs a select query with the SQL query string and pymysql cursor as arguments
# Returns a list of Python tuples
def runSelectQuery(query, cur):
    try:
        cur.execute(query)
        queriedData = cur.fetchall()
        return queriedData
    except:
        raise Exception("Could not run select query and/or return data")


# ===========================================================
# Additional Helper Functions from sf_api.py
# Need to revisit to see if we need these

def helper_upload_meal_img(file, bucket, key):
    if file and allowed_file(file.filename):
        filename = 'https://s3-us-west-1.amazonaws.com/' \
                   + str(bucket) + '/' + str(key)
       
        upload_file = s3.put_object(
                            Bucket=bucket,
                            Body=file,
                            Key=key,
                            ACL='public-read',
                            ContentType='image/jpeg'
                        )
        return filename
    return None

def helper_upload_refund_img(file, bucket, key):
    print("Bucket = ", bucket)
    print("Key = ", key)
    if file:
        filename = 'https://s3-us-west-1.amazonaws.com/' \
                   + str(bucket) + '/' + str(key)
        #print('bucket:{}'.format(bucket))
        upload_file = s3.put_object(
                            Bucket=bucket,
                            Body=file,
                            Key=key,
                            ACL='public-read',
                            ContentType='image/png'
                        )
        return filename
    return None

def allowed_file(filename):
    """Checks if the file is allowed to upload"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def kitchenExists(kitchen_id):
    # scan to check if the kitchen name exists
    kitchen = db.scan(TableName='kitchens',
        FilterExpression='kitchen_id = :val',
        ExpressionAttributeValues={
            ':val': {'S': kitchen_id}
        }
    )

    return not kitchen.get('Items') == []

def couponExists(coupon_id):
    # scan to check if the kitchen name exists
    coupon = db.scan(TableName='coupons',
        FilterExpression='coupon_id = :val',
        ExpressionAttributeValues={
            ':val': {'S': coupon_id}
        }
    )

    return not coupon.get('Items') == []


# ===========================================================













# -- Table of Contents -------------------------------------------------------------------------------
# -- 1.  GET Query
# -- 2.  GET Query using a / to pass in a parameter
# -- 3.  GET Query using a argument to pass in a parameter
# -- 4.  POST Query using a / to pass in a parameter
# -- 5.  POST Query using a JSON object to pass in a parameter




# -- Queries start here -------------------------------------------------------------------------------

# -- 1.  GET Query
class Businesses(Resource):
    # QUERY 1 RETURNS ALL BUSINESSES
    def get(self):
        response = {}
        items = {}
        try:
            conn = connect()
            query = """ # QUERY 1 RETURNS ALL BUSINESSES
                SELECT * FROM sf.businesses; """
            items = execute(query, 'get', conn)

            response['message'] = 'Businesses successful'
            response['result'] = items['result']
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)
            
        # ENDPOINT THAT WORKS
        # http://localhost:4000/api/v2/businesses
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/businesses



# -- 2.  GET Query using a / to pass in a parameter
# -- include parameter in get 
class OneBusiness(Resource):
    # QUERY 2 RETURNS A SPECIFIC BUSINESSES
    def get(self, business_uid):
        response = {}
        items = {}
        print("business_uid", business_uid)
        try:
            conn = connect()
            query = """
                    SELECT * FROM sf.businesses 
                    WHERE business_uid = \'""" + business_uid + """\';
                    """
            items = execute(query, 'get', conn)

            response['message'] = 'Specific Business successful'
            response['result'] = items['result']
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)
        
        # ENDPOINT THAT WORKS
        # http://localhost:4000/api/v2/onebusiness/200-000003
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/onebusiness/200-000003
    


# -- 3.  GET Query using a argument to pass in a parameter
# -- include parameter in request.args
class OneBusinessArg(Resource):
    # QUERY 3 RETURNS A SPECIFIC BUSINESSES
    def get(self):
        response = {}
        items = {}
        try:
            conn = connect()
            Business_uid = request.args['business_uid']
            # print("Business_uid", business_uid)  <== Can't put a print in a try
            query = """ # QUERY 1 RETURNS ALL BUSINESSES
                SELECT * FROM sf.businesses 
                WHERE business_uid = \'""" + Business_uid + """\';
                """
            items = execute(query, 'get', conn)

            response['message'] = 'Businesses successful'
            response['result'] = items['result']
            return response, 200
        except:
            raise BadRequest('Request failed, please try again later.')
        finally:
            disconnect(conn)
        
        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/onebusinessarg?business_uid=200-000001
        # https://tsx3rnuidi.execute-api.us-west-1.amazonaws.com/dev/api/v2/onebusinessarg?business_uid=200-000001
    



# -- 4.  POST Query using a / to pass in a parameter
# -- include parameter in post 
class UpdateBusinessParam(Resource):
    # QUERY 4 UPDATE A SPECIFIC BUSINESS PARAMETER
    def post(self, business_type):
            response = {}
            items = []
            print("business_type", business_type)
            try:
                conn = connect()
                query = """
                        UPDATE sf.businesses
                        SET business_type = \'""" + business_type + """\'
                        WHERE business_uid = '200-000001';
                        """
                items = execute(query, 'post', conn)


                items['message'] = 'Business Type info updated'
                items['code'] = 200
                return items
            except:
                print("Error happened while updating businesses table")
                raise BadRequest('Request failed, please try again later.')
            finally:
                disconnect(conn)
                print('process completed')
       
        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/updatebusinessparam/unique




# -- 5.  POST Query using a JSON object to pass in a parameter
# -- include parameter in json object
class UpdateBusinessParamJSON(Resource):
    # QUERY 4 UPDATE A SPECIFIC BUSINESS PARAMETER
    def post(self):
        response = {}
        items = {}
        try:
            conn = connect()
            data = request.get_json(force=True)
            business_uid = data['business_uid']
            business_type = data['business_type']
            print("business_uid", business_uid)
            print("business_type", business_type)

            query = """
                    UPDATE sf.businesses
                    SET business_type = \'""" + business_type + """\'
                    WHERE business_uid = \'""" + business_uid + """\';
                    """
            items = execute(query, 'post', conn)

            response['message'] = 'JSON POST successful'
            response['result'] = items
            return response, 200
        except:
            raise BadRequest('JSON POST Request failed, please try again later.')
        finally:
            disconnect(conn)

        # ENDPOINT AND JSON OBJECT THAT WORKS
        # http://localhost:4000/api/v2/updatebusinessparamjson
        # {"business_uid":"200-000001", "business_type":"unique"}




# -- DEFINE APIS -------------------------------------------------------------------------------




# Define API routes

api.add_resource(Businesses, '/api/v2/businesses')
api.add_resource(OneBusiness, '/api/v2/onebusiness/<string:business_uid>') 
api.add_resource(OneBusinessArg, '/api/v2/onebusinessarg')
api.add_resource(UpdateBusinessParam, '/api/v2/updatebusinessparam/<string:business_type>') 
api.add_resource(UpdateBusinessParamJSON, '/api/v2/updatebusinessparamjson') 


# Run on below IP address and port
# Make sure port number is unused (i.e. don't use numbers 0-1023)
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4000)

