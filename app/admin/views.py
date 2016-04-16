from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

from . import admin
from .. import db
from ..models import Agency
from .forms import AgencyForm


@admin.route('/agency/add', methods=['GET', 'POST'])
@login_required
def add_agency():
    form = AgencyForm()
    if form.validate_on_submit():
        agency = Agency(name=form.name.data,
                        address=form.address.data)
        db.session.add(agency)
        db.session.commit()
        flash('Agency {} was added to database.'.format(agency.name))
        return redirect(url_for('main.index'))
    return render_template("admin/add_agency.html", form=form)


@admin.route('/agency/list', methods=['GET'])
@admin.route('/agency/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_agencies(page=1):
    agencies = Agency.query.paginate(page, 10, False)
    return render_template("admin/list_agencies.html", agencies=agencies)