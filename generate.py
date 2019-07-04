from flask import Flask, render_template, make_response, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

import pdfkit

app = Flask(__name__)
app.config["SECRET_KEY"] = "BNI_For_life_fo_Shizzle"


class GainsForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Your Email', validators=[DataRequired()])
    tel = StringField('Best Tel Number To Reach You', validators=[DataRequired()])
    about = StringField('Describe Yourself in 2 Sentences', validators=[DataRequired()])
    goals = StringField('Your Goals', validators=[DataRequired()])
    accomplishments = StringField('Your Accomplishments', validators=[DataRequired()])
    interests = StringField('Your Interests', validators=[DataRequired()])
    networks = StringField('Your Networks', validators=[DataRequired()])
    skills = StringField('Your Skills', validators=[DataRequired()])
    referrals = StringField('Great Referrals would be...', validators=[DataRequired()])

@app.route('/', methods=['GET','POST'])
def index():
    form = GainsForm()
    if form.validate_on_submit():
        rendered = render_template(
            'pdf_template.html',
            pdf_name=form.name.data,
            pdf_about=form.about.data,
            pdf_goals=form.goals.data,
            pdf_accomplishments=form.accomplishments.data,
            pdf_interests=form.interests.data,
            pdf_networks=form.networks.data,
            pdf_skills=form.skills.data,
            pdf_referrals=form.referrals.data,
            pdf_email=form.email.data,
            pdf_tel=form.tel.data
            )

        css = ['materialize.css']
        pdf = pdfkit.from_string(rendered, False,css=css)

        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=Gainsprofile.pdf'

        return response

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
