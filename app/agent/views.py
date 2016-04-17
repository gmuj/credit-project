from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

from . import agent
from .. import db
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
        db.session.add(appointment)
        flash('Appointment was updated successfully.')
    elif request.form.get('delete', None):
        db.session.delete(appointment)
        flash('Appointment was deleted successfully.')
    return redirect(url_for("agent.list_appointments"))