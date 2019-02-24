import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create', methods=['GET', 'POST'])
def create_donation():
    if request.method == 'POST':
        donors = Donor.select(Donor.name)
        don = []
        for donor in donors:
            don.append(donor.name)

        if request.form['donor'] not in don:
            donor = Donor(name=request.form['donor'])
            donor.save()

        donor = Donor.select().where(Donor.name == request.form['donor']).get()
        Donation(donor=donor,
                 value=int(request.form['donation'])).save()

        return redirect(url_for('all'))

    elif request.method == 'GET':
        return render_template('create_donation.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

