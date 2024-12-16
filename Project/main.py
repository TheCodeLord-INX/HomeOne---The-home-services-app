import os
from flask import Blueprint, render_template, request, redirect, url_for, Flask, abort, flash, current_app, jsonify
from . import db
from .models import User, Services, ServiceRemarks, ServiceRequests  # Import ServiceRequests model
from flask_login import login_required, current_user
from datetime import datetime

main = Blueprint('main', __name__)



# 
# 
# Step 2: Configure upload folder and allowed extensions
# @main.before_app_first_request
# def configure_upload():
#     upload_folder = os.path.join(current_app.root_path, 'submittedPDFs')
#     allowed_extensions = {'pdf'}
#     current_app.config['UPLOAD_FOLDER'] = upload_folder
# 
# 


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user_home', methods=['GET', 'POST'])
@login_required
def user_home():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        action = request.form.get('action')
        service_request = ServiceRequests.query.get(service_id)
        if service_request:
            if action == 'close':
                service_request.status = 'closed'
                flash('Service closed successfully!', 'success')
            elif action == 'cancel':
                db.session.delete(service_request)
                flash('Service cancelled successfully!', 'success')
            db.session.commit()
        else:
            flash('Service request not found', 'error')
    booked_services = ServiceRequests.query.filter(ServiceRequests.status != 'none').all()
    services = Services.query.all()
    return render_template('user_home.html', booked_services=booked_services, services=services)


@main.route('/find_service', methods=['GET', 'POST'])
@login_required
def find_service():
    search_query = request.args.get('search_query')
    if request.method == 'POST':
        if 'service_id' in request.form:
            service_id = request.form.get('service_id')
            service = Services.query.get(service_id)
            if service:
                existing_request = ServiceRequests.query.filter_by(user_id=current_user.id, name=service.name, status='requested').first()
                if existing_request:
                    flash('You have already requested this service!', 'error')
                else:
                    service_request = ServiceRequests(
                        name=service.name,
                        bp=service.bp,
                        desc=service.desc,
                        user_id=current_user.id,
                        status='requested',
                        location=current_user.address
                    )
                    db.session.add(service_request)
                    db.session.commit()
                    flash('Your service is booked successfully!', 'success')
            else:
                flash('Service not found', 'error')
        else:
            search_query = request.form.get('search_query')
    
    if search_query:
        services = Services.query.filter(   
            (Services.name.ilike(f'%{search_query}%')) |
            (Services.bp.ilike(f'%{search_query}%')) |
            (Services.desc.ilike(f'%{search_query}%')) |
            (Services.pin.ilike(f'%{search_query}%')) |
            (Services.location.ilike(f'%{search_query}%')) |
            (Services.rating.ilike(f'%{search_query}%'))
        ).all()
        return render_template('customer_search.html', services=services, search_query=search_query)
    
    services = Services.query.all()
    return render_template('customer_search.html', services=services)

def booked_service():
    service_id = request.form.get('service_id')
    service = Services.query.get(service_id)
    if service:
        service.status = 'requested'
        db.session.commit()
        flash('Your service is booked successfully!', 'success')
    else:
        flash('Service not found', 'error')
    return redirect(url_for('main.find_service'))

@main.route('/admin/manage_cat', methods=['GET', 'POST'])
@login_required
def manage_cat():
    if request.method == 'POST':
        if 'create_service' in request.form:
            service_name = request.form.get('create_service')
            service_bp = request.form.get('create_bp')
            service_desc = request.form.get('create_desc')
            service_pin = request.form.get('create_pin')
            service_location = request.form.get('create_location')
            service_rating = request.form.get('create_rating')
            service_status = request.form.get('create_status')
            

            existing_service = Services.query.filter_by(name=service_name).first()

            if existing_service:
                flash('Service already exists', category='error')
            else:
                try:
                    service_bp = float(service_bp)
                except ValueError:
                    flash('Invalid Base Price. Please enter a valid number.', category='error')
                    return redirect(url_for('main.manage_cat'))

                new_service = Services(name=service_name, bp=service_bp, desc=service_desc, pin=service_pin,location=service_location, rating=service_rating , status=service_status)

                db.session.add(new_service)
                db.session.commit()
                
                flash('Service created successfully', category='success')
        elif 'remove_service' in request.form:
            service_id = request.form.get('service_id')

            service = Services.query.get(service_id)

            if service:
                db.session.delete(service)
                db.session.commit()

                flash('Service removed successfully', category='success')
            else:
                flash('Service not found', category='error')
        elif 'edit_service' in request.form:
            service_id = request.form.get('service_id')
            new_service_name = request.form.get('new_service_name')
            new_bp_name = request.form.get('new_bp_name')
            new_desc_name = request.form.get('new_desc_name')
            new_pin_name = request.form.get('new_pincode_name')
            new_location_name = request.form.get('new_location_name')
            new_rating_name = request.form.get('new_rating_name')
            
            service = Services.query.get(service_id)

            if service:
                service.name = new_service_name
                try:
                    service.bp = float(new_bp_name)  # Convert to float
                except ValueError:
                    flash('Invalid Base Price. Please enter a valid number.', category='error')
                    return redirect(url_for('main.manage_cat'))
                service.desc = new_desc_name
                service.pin = new_pin_name
                service.location = new_location_name
                try:
                    service.rating = float(new_rating_name)  # Convert to float
                except ValueError:
                    flash('Invalid Rating. Please enter a valid number.', category='error')
                    return redirect(url_for('main.manage_cat'))
                db.session.commit()

                flash('Service updated successfully', category='success')
            else:
                flash('Service not found', category='error')
        return redirect(url_for('main.manage_cat'))
    
    if not current_user.role == 0:
        abort(403)
    services = Services.query.all()

    return render_template('manage_cat.html', services=services)

@main.route('/admin_home', methods=['GET', 'POST'])
@login_required
def admin_home():
    services = Services.query.all()
    requested_services = ServiceRequests.query.all()
    profs = User.query.filter_by(role=1).all()
    return render_template('admin_home.html', req_services=requested_services, service_details = services, profs = profs)

@main.route('/admin_search', methods=['GET', 'POST'])
@login_required
def admin_search():
    return render_template('search_admin.html')

@main.route('/admin_manage_profs', methods=['GET', 'POST'])
@login_required
def admin_manage_profs():
    if request.method == 'POST':
        prof_id = request.form.get('prof_id')
        action = request.form.get('action')
        user = User.query.filter_by(id=prof_id, role=1).first()
        if user:
            if action == 'approve':
                user.status = 'approved'
                db.session.commit()
                flash(f'Professional {user.name} approved successfully!', 'success')
            elif action == 'reject':
                user.status = 'rejected'
                db.session.commit()
                flash(f'Professional {user.name} rejected successfully!', 'success')
            elif action == 'block':
                user.status = 'blocked'
                db.session.commit()
                flash(f'Professional {user.name} blocked successfully!', 'success')
            elif action == 'unblock':
                user.status = 'unblocked'
                db.session.commit()
                flash(f'Professional {user.name} unblocked successfully!', 'success')
        else:
            flash('Professional not found', 'error')
        return redirect(url_for('main.admin_manage_profs'))

    search_query = request.args.get('search_query')
    if search_query:
        new_prof = User.query.filter(
            (User.role == 1) &
            ((User.name.ilike(f'%{search_query}%')) |
             (User.expy.ilike(f'%{search_query}%')) |
             (User.service.ilike(f'%{search_query}%')))
        ).all()
    else:
        new_prof = User.query.filter_by(role=1).all()
    return render_template('admin_manage_profs.html', new_prof=new_prof)

@main.route('/professional_home', methods=['GET', 'POST'])
@login_required
def professional_home():
    if request.method == 'POST':
        service_id = request.form.get('service_id')
        action = request.form.get('action')
        service_request = ServiceRequests.query.get(service_id)
        if service_request:
            if action == 'accept' and service_request.status == 'requested':
                service_request.status = 'accepted'
                service_request.assigned_prof = current_user.name
            elif action == 'reject' and service_request.status == 'requested':
                db.session.delete(service_request)
            elif action == 'close' and service_request.status == 'accepted':
                service_request.status = 'closed'
            db.session.commit()
        return redirect(url_for('main.professional_home'))

    requested_services = db.session.query(ServiceRequests.id, User.name, User.address, ServiceRequests.desc, ServiceRequests.status).filter(ServiceRequests.status.in_(['requested', 'accepted'])).join(User, ServiceRequests.user_id == User.id).all()
    
    closed_services = db.session.query(ServiceRequests.id, User.name, ServiceRequests.location, ServiceRequests.reqDate, ServiceRequests.rating).filter(ServiceRequests.status == 'closed').join(User, ServiceRequests.user_id == User.id).all()
    
    return render_template('professional_home.html', requested_services=requested_services, closed_services=closed_services, enumerate=enumerate)


@main.route('/professional_search', methods=['GET', 'POST'])
@login_required
def professional_search():
    return render_template('professional_search.html')


# @main.route('/user-chart')
# def user_chart():
#     users = User.query.all()
    
#     role_count = {}
    
#     for user in users:
#         role = str(user.role)
#         role_count[role] = role_count.get(role, 0) + 1
        
#     roles = list(role_count.keys())
#     counts = list(role_count.values())
    
#     plt.figure(figsize=(10,5))
#     plt.bar(roles, counts, color='blue', alpha=0.7)
#     plt.xlabel('Roles')
#     plt.ylabel('No. of Users')
#     plt.title('Users by Roles')
#     plt.tight_layout()
    
#     chart_path = 'static/images/chart.png'
    
#     plt.close()
    
#     return render_template('user_chart.html', chart_path=chart_path)




@main.route('/admin/accept_prof', methods=['POST'])
@login_required
def accept_prof():
    if current_user.role != 0:
        abort(403)
    data = request.get_json()
    prof_id = data.get('id')
    user = User.query.filter_by(id=prof_id, role=1).first()
    if user:
        user.role = 1  # Keep as professional
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@main.route('/admin/reject_prof', methods=['POST'])
@login_required
def reject_prof():
    if current_user.role != 0:
        abort(403)
    data = request.get_json()
    prof_id = data.get('id')
    user = User.query.filter_by(id=prof_id, role=1).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400


@main.route('/service_remarks', methods=['GET', 'POST'])
@login_required
def service_remarks():
    service_id = request.args.get('service_id')
    service_request = ServiceRequests.query.get(service_id)
    if not service_request:
        flash('Service request not found', 'error')
        return redirect(url_for('main.user_home'))
    
    if request.method == 'POST':
        service_name = request.form.get('serviceName')
        description = request.form.get('description')
        date = request.form.get('date')
        contact_no = request.form.get('contactNo')
        prof_uname = request.form.get('professionalUname')
        prof_name = request.form.get('professionalName')
        service_rating = request.form.get('rating')
        remarks = request.form.get('remarks')

        existing_remarks = ServiceRemarks.query.filter_by(service_request_id=service_id).first()
        if existing_remarks:
            existing_remarks.service_name = service_name
            existing_remarks.description = description
            existing_remarks.date = datetime.strptime(date, '%Y-%m-%d')
            existing_remarks.contact_no = contact_no
            existing_remarks.prof_uname = prof_uname
            existing_remarks.prof_name = prof_name
            existing_remarks.service_rating = float(service_rating)
            existing_remarks.remarks = remarks
        else:
            new_service_remarks = ServiceRemarks(
                service_name=service_name,
                description=description,
                date=datetime.strptime(date, '%Y-%m-%d'),
                contact_no=contact_no,
                prof_uname=prof_uname,
                prof_name=prof_name,
                service_rating=float(service_rating),
                remarks=remarks,
                service_request_id=service_id
            )
            db.session.add(new_service_remarks)

        db.session.commit()

        # Update the service request status to "closed"
        service_request.status = 'closed'
        service_request.rating = float(service_rating)  # Update the rating in ServiceRequests
        db.session.commit()

        flash('Remarks added/updated successfully', 'success')
        return redirect(url_for('main.user_home'))
    
    return render_template('service_remarks.html', service_request=service_request)

@main.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@main.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        field = request.form.get('field')
        value = request.form.get('value')
        
        if field and value:
            print(f"Updating {field} to {value}")  # Debug statement
            if field == 'username':
                current_user.username = value
            elif field == 'name':
                current_user.name = value  # Corrected field name
            elif field == 'email':
                current_user.email = value
            elif field == 'address':
                current_user.address = value
            db.session.commit()
            print(f"Updated {field} to {value} in the database")  # Debug statement after commit
    
    user_details = User.query.filter_by(id=current_user.id).first()
    return render_template('profile.html', user_details=user_details)

def book_service():
    service_id = request.form.get('service_id')
    service = Services.query.get(service_id)
    if service:
        service.status = 'requested'
        db.session.commit()
        flash('Your service is booked successfully!', 'success')
    else:
        flash('Service not found', 'error')
    return redirect(url_for('main.find_service'))


