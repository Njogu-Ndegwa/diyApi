from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from api.route.home import home_api
from api.route.authController.login import login_api
from api.route.authController.signup import signup_api
from api.route.diyController.five_step_process import five_step_process_api
from api.route.diyController.update_themes import update_theme_api
from api.route.test import test_api
from api.route.authController.delete import delete_api
from api.route.diyController.saveSso import save_sso_api
from api.route.paymentController.payments import payment_api
from api.route.paymentController.verifyPayment import verify_payment_api
from api.route.diyController.generate_sso import generate_sso_api
from api.route.diyController.getSite import get_sites_api
from api.route.diyController.publishApi import publish_site_api
from api.route.emailController.finance_email import send_mail_finance_api
from api.route.diyController.hire_proffessional import hire_professional_api
# from api.route.emailController.reset_password_email import send_reset_password_email_api
from api.route.authController.reset_password import reset_password_api
from api.route.authController.confirm_verification_code import confirm_verification_code_api
from api.route.authController.change_password import change_password_api
from api.route.authController.confirm_email import confirmAccount_api
from api.route.authController.profile import profile_api
from api.route.authController.uploads import serve_uploads_api
from api.route.authController.getProfile import get_profile_api
from api.route.authController.resend_verification_email import resend_verification_email_api
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
    app.register_blueprint(update_theme_api, url_prefix='/api')
    app.register_blueprint(test_api, url_prefix='/api')
    app.register_blueprint(delete_api, url_prefix='/api')
    app.register_blueprint(save_sso_api, url_prefix='/api')
    app.register_blueprint(payment_api, url_prefix='/api')
    app.register_blueprint(verify_payment_api, url_prefix='/api')
    app.register_blueprint(generate_sso_api, url_prefix='/api')
    app.register_blueprint(get_sites_api, url_prefix='/api')
    app.register_blueprint(publish_site_api, url_prefix='/api')
    app.register_blueprint(send_mail_finance_api, url_prefix='/api')
    app.register_blueprint(hire_professional_api, url_prefix='/api')
    # app.register_blueprint(send_reset_password_email_api, url_prefix='/api')
    app.register_blueprint(reset_password_api, url_prefix='/api')
    app.register_blueprint(confirm_verification_code_api, url_prefix='/api')
    app.register_blueprint(change_password_api, url_prefix='/api')
    app.register_blueprint(confirmAccount_api, url_prefix='/api')
    app.register_blueprint(profile_api, url_prefix='/api')
    app.register_blueprint(serve_uploads_api, url_prefix='/api')
    app.register_blueprint(get_profile_api, url_prefix='/api')
    app.register_blueprint(resend_verification_email_api, url_prefix='/api')
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app = create_app()

    app.run(host='0.0.0.0', port=port)
