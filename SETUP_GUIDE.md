# COMPLETE SETUP AND USAGE GUIDE

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Database Setup](#database-setup)
4. [Running the Application](#running-the-application)
5. [User Guide](#user-guide)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python**: Version 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 100MB free space
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)

### Check Python Installation
Open terminal/command prompt and run:
```bash
python --version
# or
python3 --version
```

If Python is not installed, download from: https://www.python.org/downloads/

---

## Installation Steps

### Method 1: Automated Setup (Recommended)

#### On Windows:
1. Open Command Prompt in the project folder
2. Run the setup script:
   ```cmd
   setup.bat
   ```
3. Wait for installation to complete
4. Follow the on-screen instructions

#### On macOS/Linux:
1. Open Terminal in the project folder
2. Make the script executable:
   ```bash
   chmod +x setup.sh
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```
4. Follow the on-screen instructions

### Method 2: Manual Setup

#### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

If you encounter errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Initialize Database
```bash
python init_db.py
```

You should see output confirming:
- Database tables created
- Users created
- Sample data loaded

---

## Database Setup

### Understanding the Database

The system uses SQLite, a file-based database that requires no separate server installation. The database file (`garage.db`) is created automatically.

### Sample Data Includes:

- **2 Users**: admin and staff accounts
- **10 Customers**: With contact information
- **15 Vehicles**: Associated with customers
- **30 Services**: In various states
- **15 Inventory Parts**: With stock levels
- **Sales Records**: For completed services

### Resetting the Database

To start fresh:
```bash
# Delete the database file
rm garage.db  # macOS/Linux
del garage.db  # Windows

# Reinitialize
python init_db.py
```

---

## Running the Application

### Start the Server

```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the application
python app.py
```

### Access the Application

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You should see the login page

### Default Login Credentials

**Administrator Account:**
- Username: `admin`
- Password: `admin123`
- Access: Full system access

**Staff Account:**
- Username: `staff`
- Password: `staff123`
- Access: Standard operations

### Stopping the Server

Press `Ctrl+C` in the terminal/command prompt

---

## User Guide

### 1. Dashboard Overview

After logging in, you'll see:

**Statistics Cards:**
- Total Customers
- Total Vehicles
- Pending Services
- Completed Today
- Total Revenue
- Today's Revenue

**Information Panels:**
- Upcoming Appointments
- Recent Services
- Low Stock Alerts

### 2. Customer Management

#### Adding a Customer
1. Click "Customers" in sidebar
2. Click "Add New Customer"
3. Fill in required fields:
   - Full Name (required)
   - Phone (required)
   - Email (optional)
   - Address (optional)
4. Click "Add Customer"

#### Viewing Customer Details
1. Go to Customers list
2. Click the eye icon or customer name
3. View customer info, vehicles, and service history

#### Editing a Customer
1. Find customer in list
2. Click pencil icon
3. Modify details
4. Click "Update Customer"

#### Deleting a Customer
1. Find customer in list
2. Click trash icon
3. Confirm deletion
**Note**: This will also delete associated vehicles and services

### 3. Vehicle Management

#### Adding a Vehicle
1. Click "Vehicles" in sidebar
2. Click "Add New Vehicle"
3. Fill in required fields:
   - Owner (select from dropdown)
   - Make (e.g., Toyota)
   - Model (e.g., Camry)
   - Year (e.g., 2020)
   - License Plate (required)
   - Color (optional)
   - VIN (optional)
4. Click "Add Vehicle"

#### Quick Add from Customer Page
1. View a customer's profile
2. Click "Add Vehicle" button
3. Owner is pre-selected

### 4. Service Management

#### Booking a Service
1. Click "Services" in sidebar
2. Click "Book New Service"
3. Select:
   - Vehicle (from dropdown)
   - Service Type (Oil Change, Brake Service, etc.)
   - Description (optional details)
   - Scheduled Date & Time
   - Estimated Cost
4. Click "Book Service"

#### Service Status Flow
- **Pending**: Newly booked
- **In Progress**: Service is being performed
- **Completed**: Service finished
- **Cancelled**: Service cancelled

#### Adding Parts to Service
1. Open service details
2. Click "Add Part" button
3. Select part from inventory
4. Enter quantity
5. Click "Add Part"
- Cost automatically updates
- Inventory automatically decreases

#### Completing a Service
1. Edit the service
2. Change status to "Completed"
3. Update service
4. Create a sale record

### 5. Inventory Management

#### Adding Inventory Parts
1. Click "Inventory" in sidebar
2. Click "Add New Part"
3. Fill in:
   - Part Name (e.g., Oil Filter)
   - Part Number (unique identifier)
   - Description
   - Quantity (stock level)
   - Unit Price
   - Reorder Level (alert threshold)
   - Supplier
4. Click "Add Part"

#### Managing Stock Levels
- Yellow row = Low stock warning
- Red badge = Critical stock level
- Edit part to update quantity

#### Understanding Reorder Level
- System alerts when quantity ≤ reorder level
- Displays on dashboard
- Helps prevent stockouts

### 6. Sales Management

#### Creating a Sale
1. Complete a service first
2. Go to service details
3. Click "Create Sale Record"
4. Set:
   - Total Amount (pre-filled with service cost)
   - Payment Method (cash/card/transfer)
   - Payment Status (paid/partial/pending)
5. Click "Create Sale"

#### Viewing Sales
- Click "Sales" in sidebar
- See all sales with:
  - Customer info
  - Vehicle details
  - Amount
  - Payment status
  - Date

#### Printing Receipt
1. Click on a sale
2. Review receipt details
3. Click "Print Receipt"
4. Use browser's print function

### 7. User Management

#### Creating New Users
1. Logout
2. Click "Register here"
3. Fill in:
   - Username (unique)
   - Email
   - Password
   - Confirm Password
4. Click "Register"
5. New users are created as "staff" role

#### Changing Role (Database Level)
```bash
# Access database
sqlite3 garage.db

# Update user role
UPDATE user SET role='admin' WHERE username='staffname';

# Exit
.quit
```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. "Command not found: python"
**Solution**: Try `python3` instead of `python`
```bash
python3 app.py
```

#### 2. "Module not found" errors
**Solution**: Ensure virtual environment is activated and dependencies installed
```bash
# Activate venv first
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. "Address already in use"
**Solution**: Port 5000 is occupied. Change port in app.py:
```python
# In app.py, last line:
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### 4. "Database is locked"
**Solution**: Close any other processes accessing the database
```bash
# Kill Python processes
# Windows: Task Manager > End Python tasks
# macOS/Linux: killall python3
```

#### 5. Login Not Working
**Solution**: Reinitialize database
```bash
rm garage.db
python init_db.py
```

#### 6. Blank Page After Login
**Solution**: Clear browser cache or try incognito mode

#### 7. Parts Not Deducting from Inventory
**Solution**: Check stock levels before adding to service
- Ensure quantity available ≥ quantity needed

#### 8. CSS Not Loading
**Solution**: Hard refresh browser
- Chrome/Firefox: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Clear browser cache

---

## Production Deployment

### Security Checklist

#### 1. Change Secret Key
```python
# In app.py
import secrets
app.config['SECRET_KEY'] = secrets.token_hex(32)
```

#### 2. Disable Debug Mode
```python
# In app.py
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

#### 3. Use Production Database
Replace SQLite with PostgreSQL or MySQL:
```python
# Example for PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/garage_db'
```

#### 4. Environment Variables
```bash
# Create .env file
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://...
FLASK_ENV=production

# Install python-dotenv
pip install python-dotenv

# Load in app.py
from dotenv import load_dotenv
load_dotenv()
```

#### 5. Use Production Server
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### 6. Setup Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 7. Enable HTTPS
```bash
# Using Let's Encrypt
sudo certbot --nginx -d yourdomain.com
```

### Backup Strategy

#### Backup Database
```bash
# Copy database file
cp garage.db garage_backup_$(date +%Y%m%d).db

# Or create automated backup script
```

#### Restore Database
```bash
cp garage_backup_YYYYMMDD.db garage.db
```

---

## Performance Optimization

### Tips for Better Performance

1. **Add Database Indexes**
   ```python
   # In models, add index=True
   license_plate = db.Column(db.String(20), unique=True, nullable=False, index=True)
   ```

2. **Enable Query Caching**
   - Use Flask-Caching for frequently accessed data

3. **Optimize Images**
   - Compress images if adding image support

4. **Use CDN**
   - Serve Bootstrap/jQuery from CDN (already implemented)

---

## Additional Features to Consider

### Future Enhancements
- Email notifications for appointments
- SMS reminders
- PDF invoice generation
- Advanced reporting and analytics
- Multi-language support
- Mobile app integration
- Calendar integration
- Parts ordering system
- Employee time tracking
- Customer portal

---

## Support and Resources

### Getting Help
- Check README.md for quick reference
- Review code comments in app.py
- Test with sample data first

### Best Practices
- Regular database backups
- Keep dependencies updated
- Monitor error logs
- Use staging environment for testing
- Document any customizations

---

## System Architecture

### Technology Stack
```
Frontend:
- HTML5, CSS3, JavaScript
- Bootstrap 5.3
- Bootstrap Icons
- jQuery 3.6

Backend:
- Python 3.8+
- Flask 3.0 (Web Framework)
- SQLAlchemy 2.0 (ORM)
- Flask-Login 0.6 (Authentication)

Database:
- SQLite (Development)
- PostgreSQL/MySQL (Production Recommended)

Server:
- Flask Development Server (Development)
- Gunicorn/uWSGI (Production)
```

### File Structure Explained
```
garage_system/
├── app.py                 # Main application + routes + models
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── SETUP_GUIDE.md        # This file
├── setup.sh/.bat         # Automated setup scripts
└── templates/            # Jinja2 HTML templates
    ├── base.html         # Base template with navigation
    ├── *.html            # Feature-specific templates
```

---

**Last Updated**: 2024
**Version**: 1.0.0
**Author**: Claude

For questions or issues, review the troubleshooting section or check the code comments in app.py.
