from datetime import datetime
import json
import urllib
import urllib2
from flask import render_template, redirect, url_for, abort, flash, request
from flask.ext.login import login_required, current_user
from . import main
from app.main.forms import CreditType, CreditCurrency
from app.models import Appointment
from .forms import EditProfileForm, EditProfileAdminForm, AppointmentForm, CreditSimulatorForm, CreditSimulatorResult, \
    CompanyAppointmentForm
from .. import db
from ..models import Role, User
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form, user=current_user)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role_id = form.role.data
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.agency_id = form.agency.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    form.agency.data = user.agency_id
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/delete-profile/<int:id>', methods=['GET'])
@login_required
@admin_required
def delete_profile_admin(id):
    user = User.query.get_or_404(id)
    name = user.name
    username = user.username
    db.session.delete(user)
    flash('The profile {} (username: {}) has been deleted.'.format(name, username))
    return redirect(url_for('admin.list_agents'))

@main.route('/appointment', methods=['GET', 'POST'])
def create_appointment():
    form1 = AppointmentForm()
    form2 = CompanyAppointmentForm()

    if 'company_submit' in request.form:
        if form2.validate_on_submit():
            appointment = Appointment(
                name=form2.company_name.data,
                email=form2.company_email.data,
                phone=form2.company_phone.data,
                details=form2.company_details.data,
                agency_id=form2.company_agency.data,
                cif=form2.company_cif.data)
            db.session.add(appointment)
            db.session.commit()
            flash('Programarea a fost inregistrata. Te vom contacta in curand!')
            return redirect(url_for('main.index'))
        else:
            return render_template('appointment.html', form1=form1, form2=form2, form2_class="active")
    elif 'submit' in request.form:
        if form1.validate_on_submit():
            appointment = Appointment(
                name=form1.name.data,
                email=form1.email.data,
                phone=form1.phone.data,
                details=form1.details.data,
                agency_id=form1.agency.data)
            db.session.add(appointment)
            db.session.commit()
            flash('Your appointment has been registered. We will contact you soon')
            return redirect(url_for('main.index'))
        else:
            return render_template('appointment.html', form1=form1, form2=form2, form1_class="active")
    return render_template('appointment.html', form1=form1, form2=form2, form1_class="active")





@main.route('/credit-simulator', methods=['GET', 'POST'])
def credit_simulator():
    form = CreditSimulatorForm()
    result_form = None
    if form.validate_on_submit():
        if form.currency.data == CreditCurrency.EUR:
            amount = convert_eur_to_ron(form.amount.data)
        else:
            amount = form.amount.data
        rate, dobanda = calculate_rate(amount, form.credit_type.data, form.duration.data)
        total_amount = (rate * form.duration.data) + (dobanda * form.duration.data)
        result_form = CreditSimulatorResult()
        result_form.rate.data = "%.2f RON" % rate
        result_form.total_amount.data = "%.2f RON" % total_amount
        result_form.dobanda.data = "%.2f RON" % dobanda

    return render_template('credit_simulator.html', form=form, result_form=result_form)

DOBANDA = {
    CreditType.CREDIT_EXPRESSO: 9.75,
    CreditType.PRIMA_CASA: 2.0,
    CreditType.CREDIT_IMOBILIAR: 5.7,
}


def calculate_rate(credit, credit_type, period):
    rata_dobanda = DOBANDA[credit_type]
    rate = credit/period
    dobanda = credit*(rata_dobanda/100.0)*(period*30/360.0)
    return rate, dobanda


EXCHANGE_URL = "http://openapi.ro/api/exchange/eur.json?date={}"


def convert_eur_to_ron(amount):
    current_date = datetime.now().strftime("%Y-%m-%d")
    exchange_url = EXCHANGE_URL.format(current_date)
    response = urllib2.urlopen(exchange_url)
    response_data = json.loads(response.read())
    return amount * float(response_data["rate"])