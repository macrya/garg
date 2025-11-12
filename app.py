from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy import func
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='staff')  # admin, staff
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True, cascade='all, delete-orphan')

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    vin = db.Column(db.String(50))
    color = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    services = db.relationship('Service', backref='vehicle', lazy=True)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, cancelled
    cost = db.Column(db.Float, default=0.0)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    completed_date = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parts_used = db.relationship('ServicePart', backref='service', lazy=True, cascade='all, delete-orphan')

class InventoryPart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_name = db.Column(db.String(100), nullable=False)
    part_number = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, nullable=False)
    reorder_level = db.Column(db.Integer, default=10)
    supplier = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ServicePart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('inventory_part.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    part = db.relationship('InventoryPart', backref='service_parts')

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # cash, card, transfer
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, partial
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    service = db.relationship('Service', backref='sale')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        user = User(username=username, email=email, role='staff')
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration', 'danger')
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_customers = Customer.query.count()
    total_vehicles = Vehicle.query.count()
    pending_services = Service.query.filter_by(status='pending').count()
    completed_today = Service.query.filter(
        Service.status == 'completed',
        func.date(Service.completed_date) == datetime.utcnow().date()
    ).count()
    
    # Revenue statistics
    total_revenue = db.session.query(func.sum(Sale.total_amount)).filter_by(payment_status='paid').scalar() or 0
    today_revenue = db.session.query(func.sum(Sale.total_amount)).filter(
        Sale.payment_status == 'paid',
        func.date(Sale.created_at) == datetime.utcnow().date()
    ).scalar() or 0
    
    # Low stock items
    low_stock_parts = InventoryPart.query.filter(
        InventoryPart.quantity <= InventoryPart.reorder_level
    ).limit(5).all()
    
    # Recent services
    recent_services = Service.query.order_by(Service.created_at.desc()).limit(5).all()
    
    # Upcoming appointments
    upcoming_services = Service.query.filter(
        Service.status.in_(['pending', 'in_progress']),
        Service.scheduled_date >= datetime.utcnow()
    ).order_by(Service.scheduled_date).limit(5).all()
    
    return render_template('dashboard.html',
                         total_customers=total_customers,
                         total_vehicles=total_vehicles,
                         pending_services=pending_services,
                         completed_today=completed_today,
                         total_revenue=total_revenue,
                         today_revenue=today_revenue,
                         low_stock_parts=low_stock_parts,
                         recent_services=recent_services,
                         upcoming_services=upcoming_services)

# Customer Routes
@app.route('/customers')
@login_required
def customers():
    customers_list = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template('customers.html', customers=customers_list)

@app.route('/customers/add', methods=['GET', 'POST'])
@login_required
def add_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        customer = Customer(name=name, email=email, phone=phone, address=address)
        
        try:
            db.session.add(customer)
            db.session.commit()
            flash('Customer added successfully', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding customer', 'danger')
    
    return render_template('customer_form.html', customer=None)

@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    
    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.email = request.form.get('email')
        customer.phone = request.form.get('phone')
        customer.address = request.form.get('address')
        
        try:
            db.session.commit()
            flash('Customer updated successfully', 'success')
            return redirect(url_for('customers'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating customer', 'danger')
    
    return render_template('customer_form.html', customer=customer)

@app.route('/customers/delete/<int:id>', methods=['POST'])
@login_required
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    
    try:
        db.session.delete(customer)
        db.session.commit()
        flash('Customer deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting customer', 'danger')
    
    return redirect(url_for('customers'))

@app.route('/customers/view/<int:id>')
@login_required
def view_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customer_view.html', customer=customer)

# Vehicle Routes
@app.route('/vehicles')
@login_required
def vehicles():
    vehicles_list = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return render_template('vehicles.html', vehicles=vehicles_list)

@app.route('/vehicles/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        make = request.form.get('make')
        model = request.form.get('model')
        year = request.form.get('year')
        license_plate = request.form.get('license_plate')
        vin = request.form.get('vin')
        color = request.form.get('color')
        
        vehicle = Vehicle(
            customer_id=customer_id,
            make=make,
            model=model,
            year=year,
            license_plate=license_plate,
            vin=vin,
            color=color
        )
        
        try:
            db.session.add(vehicle)
            db.session.commit()
            flash('Vehicle added successfully', 'success')
            return redirect(url_for('vehicles'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding vehicle', 'danger')
    
    customers = Customer.query.order_by(Customer.name).all()
    return render_template('vehicle_form.html', vehicle=None, customers=customers)

@app.route('/vehicles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    
    if request.method == 'POST':
        vehicle.customer_id = request.form.get('customer_id')
        vehicle.make = request.form.get('make')
        vehicle.model = request.form.get('model')
        vehicle.year = request.form.get('year')
        vehicle.license_plate = request.form.get('license_plate')
        vehicle.vin = request.form.get('vin')
        vehicle.color = request.form.get('color')
        
        try:
            db.session.commit()
            flash('Vehicle updated successfully', 'success')
            return redirect(url_for('vehicles'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating vehicle', 'danger')
    
    customers = Customer.query.order_by(Customer.name).all()
    return render_template('vehicle_form.html', vehicle=vehicle, customers=customers)

@app.route('/vehicles/delete/<int:id>', methods=['POST'])
@login_required
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    
    try:
        db.session.delete(vehicle)
        db.session.commit()
        flash('Vehicle deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting vehicle', 'danger')
    
    return redirect(url_for('vehicles'))

# Service Routes
@app.route('/services')
@login_required
def services():
    services_list = Service.query.order_by(Service.scheduled_date.desc()).all()
    return render_template('services.html', services=services_list)

@app.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        vehicle_id = request.form.get('vehicle_id')
        service_type = request.form.get('service_type')
        description = request.form.get('description')
        scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%dT%H:%M')
        cost = float(request.form.get('cost', 0))
        
        service = Service(
            vehicle_id=vehicle_id,
            service_type=service_type,
            description=description,
            scheduled_date=scheduled_date,
            cost=cost,
            created_by=current_user.id
        )
        
        try:
            db.session.add(service)
            db.session.commit()
            flash('Service booking created successfully', 'success')
            return redirect(url_for('services'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating service booking', 'danger')
    
    vehicles = Vehicle.query.order_by(Vehicle.license_plate).all()
    return render_template('service_form.html', service=None, vehicles=vehicles)

@app.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.vehicle_id = request.form.get('vehicle_id')
        service.service_type = request.form.get('service_type')
        service.description = request.form.get('description')
        service.scheduled_date = datetime.strptime(request.form.get('scheduled_date'), '%Y-%m-%dT%H:%M')
        service.cost = float(request.form.get('cost', 0))
        service.status = request.form.get('status')
        
        if service.status == 'completed' and not service.completed_date:
            service.completed_date = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Service updated successfully', 'success')
            return redirect(url_for('services'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating service', 'danger')
    
    vehicles = Vehicle.query.order_by(Vehicle.license_plate).all()
    return render_template('service_form.html', service=service, vehicles=vehicles)

@app.route('/services/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    
    try:
        db.session.delete(service)
        db.session.commit()
        flash('Service deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting service', 'danger')
    
    return redirect(url_for('services'))

@app.route('/services/view/<int:id>')
@login_required
def view_service(id):
    service = Service.query.get_or_404(id)
    parts = InventoryPart.query.all()
    return render_template('service_view.html', service=service, parts=parts)

@app.route('/services/<int:id>/add_part', methods=['POST'])
@login_required
def add_service_part(id):
    service = Service.query.get_or_404(id)
    part_id = request.form.get('part_id')
    quantity = int(request.form.get('quantity', 1))
    
    part = InventoryPart.query.get_or_404(part_id)
    
    if part.quantity < quantity:
        flash('Insufficient stock', 'danger')
        return redirect(url_for('view_service', id=id))
    
    service_part = ServicePart(
        service_id=id,
        part_id=part_id,
        quantity=quantity,
        unit_price=part.unit_price
    )
    
    part.quantity -= quantity
    service.cost += (part.unit_price * quantity)
    
    try:
        db.session.add(service_part)
        db.session.commit()
        flash('Part added to service', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error adding part', 'danger')
    
    return redirect(url_for('view_service', id=id))

# Inventory Routes
@app.route('/inventory')
@login_required
def inventory():
    parts = InventoryPart.query.order_by(InventoryPart.part_name).all()
    return render_template('inventory.html', parts=parts)

@app.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_part():
    if request.method == 'POST':
        part_name = request.form.get('part_name')
        part_number = request.form.get('part_number')
        description = request.form.get('description')
        quantity = int(request.form.get('quantity', 0))
        unit_price = float(request.form.get('unit_price'))
        reorder_level = int(request.form.get('reorder_level', 10))
        supplier = request.form.get('supplier')
        
        part = InventoryPart(
            part_name=part_name,
            part_number=part_number,
            description=description,
            quantity=quantity,
            unit_price=unit_price,
            reorder_level=reorder_level,
            supplier=supplier
        )
        
        try:
            db.session.add(part)
            db.session.commit()
            flash('Part added successfully', 'success')
            return redirect(url_for('inventory'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding part', 'danger')
    
    return render_template('part_form.html', part=None)

@app.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_part(id):
    part = InventoryPart.query.get_or_404(id)
    
    if request.method == 'POST':
        part.part_name = request.form.get('part_name')
        part.part_number = request.form.get('part_number')
        part.description = request.form.get('description')
        part.quantity = int(request.form.get('quantity', 0))
        part.unit_price = float(request.form.get('unit_price'))
        part.reorder_level = int(request.form.get('reorder_level', 10))
        part.supplier = request.form.get('supplier')
        
        try:
            db.session.commit()
            flash('Part updated successfully', 'success')
            return redirect(url_for('inventory'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating part', 'danger')
    
    return render_template('part_form.html', part=part)

@app.route('/inventory/delete/<int:id>', methods=['POST'])
@login_required
def delete_part(id):
    part = InventoryPart.query.get_or_404(id)
    
    try:
        db.session.delete(part)
        db.session.commit()
        flash('Part deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting part', 'danger')
    
    return redirect(url_for('inventory'))

# Sales Routes
@app.route('/sales')
@login_required
def sales():
    sales_list = Sale.query.order_by(Sale.created_at.desc()).all()
    return render_template('sales.html', sales=sales_list)

@app.route('/sales/add/<int:service_id>', methods=['GET', 'POST'])
@login_required
def add_sale(service_id):
    service = Service.query.get_or_404(service_id)
    
    if request.method == 'POST':
        total_amount = float(request.form.get('total_amount'))
        payment_method = request.form.get('payment_method')
        payment_status = request.form.get('payment_status')
        
        sale = Sale(
            service_id=service_id,
            total_amount=total_amount,
            payment_method=payment_method,
            payment_status=payment_status,
            created_by=current_user.id
        )
        
        try:
            db.session.add(sale)
            db.session.commit()
            flash('Sale recorded successfully', 'success')
            return redirect(url_for('sales'))
        except Exception as e:
            db.session.rollback()
            flash('Error recording sale', 'danger')
    
    return render_template('sale_form.html', service=service)

@app.route('/sales/view/<int:id>')
@login_required
def view_sale(id):
    sale = Sale.query.get_or_404(id)
    return render_template('sale_view.html', sale=sale)

# API Endpoints for AJAX
@app.route('/api/vehicles/customer/<int:customer_id>')
@login_required
def get_customer_vehicles(customer_id):
    vehicles = Vehicle.query.filter_by(customer_id=customer_id).all()
    return jsonify([{
        'id': v.id,
        'display': f"{v.year} {v.make} {v.model} ({v.license_plate})"
    } for v in vehicles])

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
