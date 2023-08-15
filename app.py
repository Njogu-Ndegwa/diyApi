from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from api.route.home import home_api
from api.route.authController.login import login_api
from api.route.authController.signup import signup_api
from api.route.diyController.five_step_process import five_step_process_api
from api.route.diyController.get_templates import get_templates_api
from api.route.diyController.update_themes import update_theme_api
from api.route.test import test_api
from api.route.authController.delete import delete_api
from api.route.diyController.saveSso import save_sso_api
from api.route.paymentController.payments import payment_api
from api.route.paymentController.sendMpesa import send_mpesa_api
from api.route.paymentController.payWithCard import card_payment_api
from api.route.paymentController.verifyPayment import verify_payment_api
from api.route.diyController.generate_sso import generate_sso_api
from api.route.diyController.getSite import get_sites_api


def create_app():
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        'title': 'Flask API Starter Kit',
    }
    swagger = Swagger(app)

    CORS(app, resource={
        r"*":{
            "origins":"*"
        }
    })
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(login_api, url_prefix='/api')
    app.register_blueprint(signup_api, url_prefix='/api')
    app.register_blueprint(five_step_process_api, url_prefix='/api')
    app.register_blueprint(get_templates_api, url_prefix='/api')
    app.register_blueprint(update_theme_api, url_prefix='/api')
    app.register_blueprint(test_api, url_prefix='/api')
    app.register_blueprint(delete_api, url_prefix='/api')
    app.register_blueprint(save_sso_api, url_prefix='/api')
    app.register_blueprint(payment_api, url_prefix='/api')
    app.register_blueprint(send_mpesa_api, url_prefix='/api')
    app.register_blueprint(card_payment_api, url_prefix='/api')
    app.register_blueprint(verify_payment_api, url_prefix='/api')
    app.register_blueprint(generate_sso_api, url_prefix='/api')
    app.register_blueprint(get_sites_api, url_prefix='/api')


    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
