from flask import Flask, render_template, make_response, request, abort, jsonify
from flask_heroku import Heroku
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os
import pdfkit
from datetime import datetime, timedelta
import json

def temp_token():
    import binascii
    temp_token = binascii.hexlify(os.urandom(24))
    return temp_token.decode('utf-8')

authorised_clients = {}

app = Flask(__name__)

WEBHOOK_VERIFY_TOKEN = os.getenv('BNI_WebHook_Fo_Super_Awesome_GAINS')
CLIENT_AUTH_TIMEOUT = 24 # in Hours
app.config["SECRET_KEY"] = "BNI_For_life_fo_Shizzle"
heroku = Heroku(app)



#WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')],
                                   # stdout=subprocess.PIPE).communicate()[0].strip()


# print('loading wkhtmltopdf path on localhost')
# MYDIR = os.path.dirname(__file__)
# WKHTMLTOPDF_CMD = os.path.join(MYDIR + "/vendor/wkhtmltox/lib/", "libwkhtmltox.so")
# pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)


# # WKHTMLTOPDF config
# if 'DYNO' in os.environ:
#     print ('loading wkhtmltopdf path on heroku')
MYDIR = os.path.dirname(__file__)
# WKHTMLTOPDF_CMD = os.path.join(MYDIR + "/vendor/wkhtmltox/lib/", "libwkhtmltox.so")

# # For production on heroku
# config = pdfkit.configuration(wkhtmltopdf=os.path.join(MYDIR + '/bin/',"wkhtmltopdf"))

# for Windows Deployment
config = pdfkit.configuration(wkhtmltopdf=os.path.join(MYDIR + '\\bin\\',"wkhtmltopdf.exe"))

# else:
#     print ('loading wkhtmltopdf path on localhost')
#     MYDIR = os.path.dirname(__file__)
#     WKHTMLTOPDF_CMD = os.path.join(MYDIR + "/static/executables/bin/", "wkhtmltopdf.exe")


# def _get_pdfkit_config():
#     """wkhtmltopdf lives and functions differently depending on Windows or Linux. We
#      need to support both since we develop on windows but deploy on Heroku.
#
#     Returns:
#         A pdfkit configuration
#     """
#     if platform.system() == 'Windows':
#         return pdfkit.configuration(
#             wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
#     else:
#         WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
#                                            stdout=subprocess.PIPE).communicate()[0].strip()
#         return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)


# class GainsForm(FlaskForm):
#     name = StringField('Your Name', validators=[DataRequired()])
#     email = StringField('Your Email', validators=[DataRequired()])
#     tel = StringField('Best Tel Number To Reach You', validators=[DataRequired()])
#     about = StringField('Describe Yourself in 2 Sentences', validators=[DataRequired()])
#     goals = StringField('Your Goals', validators=[DataRequired()])
#     accomplishments = StringField('Your Accomplishments', validators=[DataRequired()])
#     interests = StringField('Your Interests', validators=[DataRequired()])
#     networks = StringField('Your Networks', validators=[DataRequired()])
#     skills = StringField('Your Skills', validators=[DataRequired()])
#     referrals = StringField('Great Referrals would be...', validators=[DataRequired()])

# @app.route('/', methods=['GET','POST'])
# def index():
#     form = GainsForm()
#     if form.validate_on_submit():
#         rendered = render_template(
#             'pdf_template.html',
#             pdf_name=form.name.data,
#             pdf_about=form.about.data,
#             pdf_goals=form.goals.data,
#             pdf_accomplishments=form.accomplishments.data,
#             pdf_interests=form.interests.data,
#             pdf_networks=form.networks.data,
#             pdf_skills=form.skills.data,
#             pdf_referrals=form.referrals.data,
#             pdf_email=form.email.data,
#             pdf_tel=form.tel.data
#             )

#         css = ['materialize.css']
#         pdf = pdfkit.from_string(rendered, False, configuration=config, css=css)

#         response = make_response(pdf)
#         response.headers['Content-Type'] = 'application/pdf'
#         response.headers['Content-Disposition'] = 'attachment; filename=Gainsprofile.pdf'

#         return response

#     return render_template('index.html', form=form)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get('verify_token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            authorised_clients[request.remote_addr] = datetime.now()
            print (request.is_json)
            content = request.get_json()
            print (content)
            return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'bad token'}), 401

    elif request.method == 'POST':
        client = request.remote_addr
        if client in authorised_clients:
            if datetime.now() - authorised_clients.get(client) > timedelta(hours=CLIENT_AUTH_TIMEOUT):
                authorised_clients.pop(client)
                return jsonify({'status':'authorisation timeout'}), 401
            else:
                print(request.json)
                return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'not authorised'}), 401

    else:
        abort(400)

if __name__ == '__main__':
    if WEBHOOK_VERIFY_TOKEN is None:
        print('WEBHOOK_VERIFY_TOKEN has not been set in the environment.\nGenerating random token...')
        token = temp_token()
        print('Token: %s' % token)
        WEBHOOK_VERIFY_TOKEN = token
    app.run()


# simple webhook
@app.route('/webhook2', methods=['POST'])
def webhook2():
    if request.method == 'POST':
        print (request.is_json)
        content = request.get_json()
        

        return pdfgeneration(content), 200
    else:
        abort(400)


def pdfgeneration(jsdata):
        rendered = render_template(
            'pdf_template.html',
            pdf_name=jsdata['form_response']['answers'][0]['text'],
            pdf_email=jsdata['form_response']['answers'][1]['email'],
            pdf_tel=jsdata['form_response']['answers'][2]['phone_number'],
            pdf_about=jsdata['form_response']['answers'][3]['text'],
            pdf_goals=jsdata['form_response']['answers'][4]['text'],
            pdf_accomplishments=jsdata['form_response']['answers'][5]['text'],
            pdf_interests=jsdata['form_response']['answers'][6]['text'],
            pdf_networks=jsdata['form_response']['answers'][7]['text'],
            pdf_skills=jsdata['form_response']['answers'][8]['text'],
            pdf_referrals=jsdata['form_response']['answers'][9]['text'],
            )

        css = ['materialize.css']
        pdf = pdfkit.from_string(rendered, False, configuration=config, css=css)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=Gainsprofile.pdf'

        return response

    # return render_template('index.html', form=form)
if __name__ == "__main__":
    #app.debug = True)
    app.run()
