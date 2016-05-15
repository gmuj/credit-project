import datetime
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required, current_user

from . import agent
from .forms import AddVacancyForm
from .. import db
from app.models import UserVacancy
from ..models import Appointment


@agent.route('/appointments/list', methods=['GET'])
@agent.route('/appointments/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_appointments(page=1):
    appointments = Appointment.query.order_by('is_new desc', 'created_at desc').paginate(page, 10, False)
    return render_template("agent/list_appointments.html",
                           appointments=appointments)

@agent.route('/appointments/detail/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def detail_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template("agent/detail_appointment.html", appointment=appointment)


@agent.route('/appointments/update/<int:appointment_id>', methods=['POST'])
@login_required
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if request.form.get('taken', None):
        appointment.is_new = False
        appointment_date = datetime.datetime.strptime(
            request.form.get('appointment_date'),
            "%m/%d/%Y"
        ).date()
        appointment_hour = datetime.datetime.strptime(
            request.form.get('appointment_time'),
            "%H:%M"
        ).time()
        if Appointment.query.filter(
            Appointment.agent_id == current_user.id,
            Appointment.reserved_hour == appointment_hour,
            Appointment.reserved_date == appointment_date).count():
            flash('Exista deja o programare pt aceasta data!')
            return redirect(url_for("agent.detail_appointment", appointment_id=appointment_id))
        else:
            appointment.reserved_date = appointment_date
            appointment.reserved_hour = appointment_hour
            appointment.agent_id = current_user.id
            db.session.add(appointment)
            flash('Programarea a fost salvata cu succes.')
    elif request.form.get('delete', None):
        db.session.delete(appointment)
        flash('Programarea a fost stearsa cu succes.')
    return redirect(url_for("agent.list_appointments"))


@agent.route('/list_current_appointments/list/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
@login_required
def list_current_appointments(year, month, day):
    specified_date = datetime.date(year, month, day)
    appointments = Appointment.query.order_by('is_new desc', 'created_at desc')\
        .filter(Appointment.reserved_date == specified_date).all()
    return render_template("agent/list_current_appointments.html",
                           appointments=appointments, specified_date=specified_date)

@agent.route('/vacancy/add', methods=['GET', 'POST'])
@login_required
def add_vacancy():
    form = AddVacancyForm()
    if form.validate_on_submit():
        vacancy = UserVacancy(user_id=current_user.id,
                              first_day=form.first_day.data,
                              last_day=form.last_day.data)
        db.session.add(vacancy)
        db.session.commit()
        flash('Cererea de concediu a fost trimisa.')
        return redirect(url_for('main.index'))
    return render_template("agent/add_vacancy.html", form=form)