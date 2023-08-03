import os
from http import HTTPStatus
from os.path import join
from pathlib import Path

from api.route.authController.acount_verification_token import confirm_token
from api.route.configController.db_connect import Neo4jConnection
from dotenv import load_dotenv
# from flasgger import swag_from
from flask import Blueprint, jsonify, make_response, redirect, request
from passlib.apps import custom_app_context as pwd_context

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

confirmAccount_api = Blueprint('confirmAccount_api', __name__)

@confirmAccount_api.route('/confirm/<token>', methods=['GET'])
# @swag_from({
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Company confirmAccount with filters',
#             # 'schema': WelcomeSchema
#         }
#     }
# })
def confirmAccount(token):
    """
    confirmAccount using provided username and passowrd
    ---
    tags:
      - confirmAccount API endpoints
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email parameter from user
      - name: password
        in: query
        type: string
        required: true
        description: password parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: A user object based on confirmAccount params
    """
    #query_param = request.args.get('query_string', default='', type=str)
   

    # Database connection parameters
    neo4j_uri = f"bolt://{os.environ.get('NEO4J_CONNECTION_URI')}"
    neo4j_username = os.environ.get('NEO4J_USERNAME')
    neo4j_password = os.environ.get('NEO4J_PASSWORD')
    
    try:
        email_var = confirm_token(token)
      
    except:
        return make_response( 'The confirmation link is invalid or has expired.', 400)


    try:
        conn = Neo4jConnection(neo4j_uri, neo4j_username, neo4j_password)
        try:
            check_user_query = '''MATCH (user:User) where user.email = $email
                                  with {
                                      id:user.user_id,
                                      email_verification_status: user.email_verification_status

                                  } as retrieved_user
                                  return retrieved_user;
                                '''
            check_user_result = conn.query(check_user_query, db='neo4j', param={'email':email_var})
            if check_user_result[0]['email_verification_status'] == True:
              print('---------------------78-----------------', flush=True)
              return redirect('https://smarttest.infomoby.com/account-verification-status-warning')


              # return make_response(jsonify({'success': 'Account already confirmed. Please login.'}), 200)

            else:  
             
              query_string = '''MATCH (u:User) where u.email = $email
with u
SET u.email_verification_status = true, u.email_verification_date = datetime()
                              '''
              data = conn.query(query_string, db='neo4j', param={'email':email_var})
              
              print('---------------91--------------', flush=True)
              return redirect('https://smarttest.infomoby.com/account-verification-status-success')
 
              # return make_response(jsonify({'success': 'You have confirmed your account. Thanks!'}), 200)
        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    print('----------101---------', flush=True)
    return redirect('https://smarttest.infomoby.com/login')


