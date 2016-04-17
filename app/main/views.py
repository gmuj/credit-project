from flask import render_template, redirect, url_for, abort, flash
from flask.ext.login import login_required, current_user
from . import main
from app.models import Appointment
from .forms import EditProfileForm, EditProfileAdminForm, AppointmentForm, CreditSimulatorForm, CreditSimulatorResult
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
    return render_template('edit_profile.html', form=form)


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
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(name=form.name.data,
                                  email=form.email.data,
                                  phone=form.phone.data,
                                  details=form.details.data,
                                  agency_id=form.agency.data)
        db.session.add(appointment)
        db.session.commit()
        flash('Your appointment has been registered. We will contact you soon')
        return redirect(url_for('main.index'))
    return render_template('appointment.html', form=form)

@main.route('/credit-simulator', methods=['GET', 'POST'])
def credit_simulator():
    form = CreditSimulatorForm()
    result_form = None
    if form.validate_on_submit():
        result_form = CreditSimulatorResult()
        result_form.total_amount.data = 44
        result_form.dae.data = 4.33

    return render_template('credit_simulator.html', form=form, result_form=result_form)