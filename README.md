# Garage Management System

A comprehensive, production-ready Garage Management System built with Flask, SQLite, and Bootstrap 5.

## Features

✅ **User Authentication** - Secure login/logout with role-based access (admin/staff)
✅ **Customer Management** - Complete CRUD operations for customer records
✅ **Vehicle Management** - Track vehicles with customer associations
✅ **Service Booking** - Schedule and manage service appointments
✅ **Inventory Management** - Track parts with low-stock alerts
✅ **Sales Tracking** - Record and view sales with receipt generation
✅ **Dashboard** - Real-time metrics and statistics
✅ **Responsive UI** - Mobile-friendly Bootstrap 5 design
✅ **Sample Data** - Pre-loaded demo data for testing

## Technology Stack

- **Backend**: Python 3.8+, Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Icons**: Bootstrap Icons

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Installation

```bash
# Clone or download the project
cd garage_system

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
# Initialize database with sample data
python init_db.py
```

This will create:
- 2 user accounts (admin and staff)
- 10 sample customers
- 15 sample vehicles
- 15 sample inventory parts
- 30 sample services
- Sample sales records

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### 5. Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Staff Account:**
- Username: `staff`
- Password: `staff123`

## Project Structure

```
garage_system/
├── app.py                      # Main application file
├── init_db.py                  # Database initialization script
├── requirements.txt            # Python dependencies
├── garage.db                   # SQLite database (created after init)
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # Main dashboard
│   ├── customers.html         # Customer listing
│   ├── customer_form.html     # Customer add/edit form
│   ├── customer_view.html     # Customer details
│   ├── vehicles.html          # Vehicle listing
│   ├── vehicle_form.html      # Vehicle add/edit form
│   ├── services.html          # Service listing
│   ├── service_form.html      # Service add/edit form
│   ├── service_view.html      # Service details
│   ├── inventory.html         # Inventory listing
│   ├── part_form.html         # Part add/edit form
│   ├── sales.html             # Sales listing
│   ├── sale_form.html         # Sale creation form
│   ├── sale_view.html         # Sale receipt
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
└── README.md                   # This file
```

## Features Guide

### Dashboard
- View key metrics: total customers, vehicles, pending services, completed services
- Monitor revenue (total and today's)
- Track upcoming appointments
- View recent services
- Low stock alerts for inventory

### Customer Management
- Add new customers with contact information
- Edit customer details
- View customer profile with all vehicles and service history
- Delete customers (with cascade delete for associated data)

### Vehicle Management
- Register vehicles with make, model, year, license plate, VIN
- Associate vehicles with customers
- Track vehicle service history
- Edit and delete vehicles

### Service Management
- Book service appointments
- Select from predefined service types
- Track service status (pending, in progress, completed, cancelled)
- Add parts to services
- Automatic cost calculation
- Create sales records for completed services

### Inventory Management
- Add and manage inventory parts
- Track stock levels
- Set reorder levels for low-stock alerts
- View supplier information
- Automatic stock deduction when parts are used

### Sales Tracking
- Create sales records for completed services
- Multiple payment methods (cash, card, transfer)
- Payment status tracking (paid, partial, pending)
- Generate printable receipts
- View sales history and revenue statistics

## Database Schema

### Users
- id, username, email, password_hash, role, created_at

### Customers
- id, name, email, phone, address, created_at

### Vehicles
- id, customer_id (FK), make, model, year, license_plate, vin, color, created_at

### Services
- id, vehicle_id (FK), service_type, description, status, cost, scheduled_date, completed_date, created_by (FK), created_at

### InventoryPart
- id, part_name, part_number, description, quantity, unit_price, reorder_level, supplier, created_at

### ServicePart
- id, service_id (FK), part_id (FK), quantity, unit_price

### Sale
- id, service_id (FK), total_amount, payment_method, payment_status, created_by (FK), created_at

## Security Features

- Password hashing using Werkzeug security
- Login required decorators on all protected routes
- Session-based authentication
- CSRF protection (built into Flask)
- SQL injection protection (SQLAlchemy ORM)

## Customization

### Change Secret Key
In `app.py`, update the SECRET_KEY:
```python
app.config['SECRET_KEY'] = 'your-secure-secret-key-here'
```

### Add More Service Types
Edit the service_type select options in `templates/service_form.html`

### Modify UI Colors
Update the gradient colors in `templates/base.html` in the `<style>` section

### Change Database Location
In `app.py`, update the database URI:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
```

## API Endpoints

The application includes a RESTful API endpoint:

**GET** `/api/vehicles/customer/<customer_id>` - Get all vehicles for a specific customer

## Troubleshooting

### Database Issues
```bash
# Delete the database and reinitialize
rm garage.db
python init_db.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## Production Deployment

### Important Security Changes

1. **Change SECRET_KEY**: Generate a secure random key
   ```python
   import secrets
   secrets.token_hex(16)
   ```

2. **Disable DEBUG mode**: In `app.py`, change:
   ```python
   app.run(debug=False)
   ```

3. **Use Production Database**: Consider PostgreSQL or MySQL instead of SQLite

4. **Use WSGI Server**: Deploy with Gunicorn, uWSGI, or Waitress
   ```bash
   pip install gunicorn
   gunicorn -w 4 app:app
   ```

5. **Set Environment Variables**:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   ```

6. **Enable HTTPS**: Use a reverse proxy like Nginx with SSL certificates

## Support and Contribution

For issues, questions, or contributions:
- Review the code comments for detailed explanations
- All functions include error handling
- Database transactions use try-except blocks
- Forms include client-side validation

## License

This project is provided as-is for educational and commercial use.

## Version History

- **v1.0.0** (2024) - Initial release
  - Complete CRUD operations for all entities
  - User authentication and authorization
  - Dashboard with statistics
  - Responsive UI with Bootstrap 5
  - Sample data for testing
  - Production-ready error handling

---
