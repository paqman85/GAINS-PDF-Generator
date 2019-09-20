from flask import Flask, render_template,request, abort, jsonify
from flask_heroku import Heroku
import os
import pdfkit
from flask_mail import Mail, Message

app = Flask(__name__)

#easy change variable for the apps email
appmail = "YourEMAILhere"
apppass = "YourEMAILpasswordHERE"

# Mail client settings -- enable emails of pdf
app.config.update(
	DEBUG=False,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
    # MAIL_USE_TLS= True,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = appmail,
	MAIL_PASSWORD = apppass
)
mail = Mail(app)

WEBHOOK_VERIFY_TOKEN = os.getenv('BNI_WebHook_Fo_Super_Awesome_GAINS')
CLIENT_AUTH_TIMEOUT = 24 # in Hours
app.config["SECRET_KEY"] = "BNI_For_life_fo_Shizzle"
heroku = Heroku(app)


#     print ('loading wkhtmltopdf path on heroku')
MYDIR = os.path.dirname(__file__)
WKHTMLTOPDF_CMD = os.path.join(MYDIR + "/vendor/wkhtmltox/lib/", "libwkhtmltox.so")

# For production on heroku
config = pdfkit.configuration(wkhtmltopdf=os.path.join(MYDIR + '/bin/',"wkhtmltopdf"))

#pdfkit options
pdfoption = options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
}
# Load the form template as the home page
@app.route('/')
def index():
    return render_template('index.html')

# simple webhook and pdf mailer -- consumes webhook json data and useses it in the pdf generator, sends it to user email
@app.route('/webhook2', methods=['POST'])
def webhook2():
    if request.method == 'POST':
        print (request.is_json)
        content = request.get_json()
        useremail=content['form_response']['answers'][1]['email']

        rendered = render_template(
            'pdf_template.html',
            pdf_name=content['form_response']['answers'][0]['text'],
            pdf_email=content['form_response']['answers'][1]['email'],
            pdf_tel=content['form_response']['answers'][2]['phone_number'],
            pdf_about=content['form_response']['answers'][3]['text'],
            pdf_goals=content['form_response']['answers'][4]['text'],
            pdf_accomplishments=content['form_response']['answers'][5]['text'],
            pdf_interests=content['form_response']['answers'][6]['text'],
            pdf_networks=content['form_response']['answers'][7]['text'],
            pdf_skills=content['form_response']['answers'][8]['text'],
            pdf_referrals=content['form_response']['answers'][9]['text'],
        )

        css = ['materialize.css']
        pdfkit.from_string(rendered,'GAINS.pdf',configuration=config, options=pdfoption,css=css)

        msg = Message("Your GAINS Profile PDF",
            sender=appmail,
            recipients=[useremail])
        msg.body = "Here\'s you\'re GAINS profile as a pdf! \n" \
                   "Thank you for using our GAINS profile PDF Generator! \n \n"\
                   "All the best,\n" \
                   "-Glenn Paquette\n" \
                   "atomicgrowth.co"\

        with app.open_resource("GAINS.pdf") as fp:
            msg.attach("GAINS.pdf", "application/pdf", fp.read())
        mail.send(msg)
        return jsonify({'status':'success Mail Sent!'}), 200

    else:
        abort(400)

if __name__ == "__main__":
    #app.debug = True)
    app.run()
