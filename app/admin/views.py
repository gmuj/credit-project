import datetime
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_required

from . import admin
from .. import db
from app.models import UserActivity, UserVacancy, Company, VacancyStatus
from ..models import Agency, User, Role
from ..email import send_email
from .forms import AddAgencyForm, EditAgencyForm, AddCompanyForm, EditCompanyForm


@admin.route('/agency/add', methods=['GET', 'POST'])
# @login_required
def add_agency():
    form = AddAgencyForm()
    if form.validate_on_submit():
        agency = Agency(name=form.name.data,
                        address=form.address.data)
        db.session.add(agency)
        db.session.commit()
        flash('Agency {} was added to database.'.format(agency.name))
        return redirect(url_for('main.index'))
    return render_template("admin/add_agency.html", form=form)

@admin.route('/agency/detail/<int:agency_id>', methods=['GET', 'POST'])
@login_required
def detail_agency(agency_id):
    agency = Agency.query.get_or_404(agency_id)
    form = EditAgencyForm(obj=agency)
    if form.validate_on_submit():
        if form.update.data:
            form.populate_obj(agency)
            flash('Agency {} was updated successfully.'.format(agency.name))
        elif form.delete.data:
            db.session.delete(agency)
            db.session.commit()
            flash('Agency {} was deleted successfully.'.format(agency.name))
        return redirect(url_for("admin.list_agencies"))

    return render_template("admin/detail_agency.html", form=form)


@admin.route('/agency/list', methods=['GET'])
@admin.route('/agency/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_agencies(page=1):
    agencies = Agency.query.paginate(page, 10, False)
    return render_template("admin/list_agencies.html", agencies=agencies)


@admin.route('/agent/list', methods=['GET'])
@admin.route('/agent/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_agents(page=1):
    agents = User.query.filter_by(role_id=Role.AGENT).paginate(page, 10, False)
    return render_template("admin/list_agents.html", agents=agents)

@admin.route('/activities/list/<int:year>/<int:month>/<int:day>', methods=['GET'])
@admin.route('/activities/list/<int:year>/<int:month>/<int:day>/<int:page>', methods=['GET', 'POST'])
@login_required
def list_activities(year, month, day, page=1):
    specified_date = datetime.date(year, month, day)
    activities = UserActivity.query.filter_by(day=specified_date).paginate(page, 10, False)
    return render_template("admin/list_activities.html",
                           activities=activities, selected_date=specified_date)


@admin.route('/activities/list', methods=['GET'])
@admin.route('/activities/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_current_activities(page=1):
    current_date = datetime.datetime.utcnow()
    return list_activities(current_date.year, current_date.month, current_date.day, page=page)


@admin.route('/vacancies/list', methods=['GET'])
@admin.route('/vacancies/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_vacancies(page=1):
    vacancies = UserVacancy.query.order_by('status', 'first_day desc').paginate(page, 10, False)
    return render_template("admin/list_vacancies.html", vacancies=vacancies)


@admin.route('/vacancies/update/<int:vacancy_id>/<string:status>', methods=['GET'])
@login_required
def update_vacancy(vacancy_id, status):
    vacancy = UserVacancy.query.get_or_404(vacancy_id)
    if status == "approved":
        vacancy.status = VacancyStatus.APPROVED
        flash('Concediul pentru {} a fost aprobat.'.format(vacancy.user.name))
        send_email(vacancy.user.email, 'Concediu aprobat',
                   'admin/email/vacancy_approved', user=vacancy.user,
                   first_day=vacancy.first_day, last_day=vacancy.last_day)
    elif status == "canceled":
        vacancy.status = VacancyStatus.CANCELED
        flash('Concediul pentru {} a fost anulat.'.format(vacancy.user.name))
        send_email(vacancy.user.email, 'Concediu nu a fost aprobat',
                   'admin/email/vacancy_canceled', user=vacancy.user,
                   first_day=vacancy.first_day, last_day=vacancy.last_day)

    db.session.add(vacancy)
    db.session.commit()

    return redirect(url_for("admin.list_vacancies"))


@admin.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company():
    form = AddCompanyForm()
    if form.validate_on_submit():
        company = Company(cif=form.cif.data,
                          name=form.name.data,
                          address=form.address.data,
                          city=form.city.data,
                          state=form.state.data,
                          phone=form.phone.data,
                          registration_id=form.registration_id.data)
        db.session.add(company)
        db.session.commit()
        flash('Compania {} a fost adaugata.'.format(company.name))
        return redirect(url_for('main.index'))
    return render_template("admin/add_company.html", form=form)


@admin.route('/companies/list', methods=['GET', 'POST'])
@admin.route('/companies/list/<int:page>', methods=['GET', 'POST'])
@login_required
def list_companies(page=1):
    term = request.form.get('search_term')
    if term:
        companies = Company.query.filter(Company.cif.like('{}%'.format(term)) |
                                         Company.name.like('{}%'.format(term)) |
                                         Company.city.like('{}%'.format(term)) |
                                         Company.state.like('{}%'.format(term)) |
                                         Company.registration_id.like('{}%'.format(term)))\
                                 .paginate(page, 10, False)
    else:
        companies = Company.query.paginate(page, 10, False)
    return render_template("admin/list_companies.html", companies=companies, term=term)


@admin.route('/companies/detail/<int:company_id>', methods=['GET', 'POST'])
def detail_company(company_id):
    company = Company.query.get_or_404(company_id)
    form = EditCompanyForm(obj=company)
    if form.validate_on_submit():
        if form.update.data:
            form.populate_obj(company)
            flash('Compania {} a fost salvata.'.format(company.name))
        elif form.delete.data:
            db.session.delete(company)
            db.session.commit()
            flash('Compania {} a fost stearsa.'.format(company.name))
        return redirect(url_for("admin.list_companies"))
    return render_template("admin/detail_company.html", form=form)