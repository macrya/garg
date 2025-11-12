from app import app, db, User, Customer, Vehicle, Service, InventoryPart, ServicePart, Sale
from datetime import datetime, timedelta
import random

def init_database():
    """Initialize database with sample data"""
    
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("Creating users...")
        admin = User(username='admin', email='admin@garage.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create staff user
        staff = User(username='staff', email='staff@garage.com', role='staff')
        staff.set_password('staff123')
        db.session.add(staff)
        
        db.session.commit()
        print(f"Created users: admin/admin123, staff/staff123")
        
        # Create customers
        print("Creating customers...")
        customers_data = [
            {'name': 'John Smith', 'email': 'john.smith@email.com', 'phone': '+1-555-0101', 'address': '123 Main St, New York, NY 10001'},
            {'name': 'Sarah Johnson', 'email': 'sarah.j@email.com', 'phone': '+1-555-0102', 'address': '456 Oak Ave, Los Angeles, CA 90001'},
            {'name': 'Michael Brown', 'email': 'mbrown@email.com', 'phone': '+1-555-0103', 'address': '789 Pine Rd, Chicago, IL 60601'},
            {'name': 'Emily Davis', 'email': 'emily.davis@email.com', 'phone': '+1-555-0104', 'address': '321 Elm St, Houston, TX 77001'},
            {'name': 'David Wilson', 'email': 'dwilson@email.com', 'phone': '+1-555-0105', 'address': '654 Maple Dr, Phoenix, AZ 85001'},
            {'name': 'Lisa Anderson', 'email': 'landerson@email.com', 'phone': '+1-555-0106', 'address': '987 Birch Ln, Philadelphia, PA 19101'},
            {'name': 'James Martinez', 'email': 'jmartinez@email.com', 'phone': '+1-555-0107', 'address': '147 Cedar Ct, San Antonio, TX 78201'},
            {'name': 'Jennifer Taylor', 'email': 'jtaylor@email.com', 'phone': '+1-555-0108', 'address': '258 Spruce Way, San Diego, CA 92101'},
            {'name': 'Robert Thomas', 'email': 'rthomas@email.com', 'phone': '+1-555-0109', 'address': '369 Walnut Blvd, Dallas, TX 75201'},
            {'name': 'Maria Garcia', 'email': 'mgarcia@email.com', 'phone': '+1-555-0110', 'address': '741 Ash Ave, San Jose, CA 95101'},
        ]
        
        customers = []
        for data in customers_data:
            customer = Customer(**data)
            customers.append(customer)
            db.session.add(customer)
        
        db.session.commit()
        print(f"Created {len(customers)} customers")
        
        # Create vehicles
        print("Creating vehicles...")
        vehicles_data = [
            {'make': 'Toyota', 'model': 'Camry', 'year': 2020, 'license_plate': 'ABC-1234', 'vin': '1HGCM82633A123456', 'color': 'Silver'},
            {'make': 'Honda', 'model': 'Accord', 'year': 2019, 'license_plate': 'XYZ-5678', 'vin': '1HGCM82633A789012', 'color': 'Black'},
            {'make': 'Ford', 'model': 'F-150', 'year': 2021, 'license_plate': 'DEF-9012', 'vin': '1FTFW1ET5DFC10312', 'color': 'Blue'},
            {'make': 'Chevrolet', 'model': 'Silverado', 'year': 2018, 'license_plate': 'GHI-3456', 'vin': '1GCVKREC0JZ123456', 'color': 'Red'},
            {'make': 'BMW', 'model': '3 Series', 'year': 2022, 'license_plate': 'JKL-7890', 'vin': 'WBA8E9G51HNU12345', 'color': 'White'},
            {'make': 'Mercedes-Benz', 'model': 'C-Class', 'year': 2020, 'license_plate': 'MNO-2345', 'vin': 'WDDWF8EB0KA123456', 'color': 'Gray'},
            {'make': 'Nissan', 'model': 'Altima', 'year': 2019, 'license_plate': 'PQR-6789', 'vin': '1N4AL3AP9JC123456', 'color': 'Blue'},
            {'make': 'Hyundai', 'model': 'Elantra', 'year': 2021, 'license_plate': 'STU-0123', 'vin': '5NPD84LF9MH123456', 'color': 'White'},
            {'make': 'Mazda', 'model': 'CX-5', 'year': 2020, 'license_plate': 'VWX-4567', 'vin': 'JM3KFBCM5L0123456', 'color': 'Black'},
            {'make': 'Volkswagen', 'model': 'Jetta', 'year': 2019, 'license_plate': 'YZA-8901', 'vin': '3VW5T7AJ0KM123456', 'color': 'Silver'},
            {'make': 'Subaru', 'model': 'Outback', 'year': 2021, 'license_plate': 'BCD-2345', 'vin': '4S4BTANC6M3123456', 'color': 'Green'},
            {'make': 'Audi', 'model': 'A4', 'year': 2020, 'license_plate': 'EFG-6789', 'vin': 'WAUENAF46LN123456', 'color': 'Gray'},
            {'make': 'Tesla', 'model': 'Model 3', 'year': 2022, 'license_plate': 'HIJ-0123', 'vin': '5YJ3E1EA5MF123456', 'color': 'Red'},
            {'make': 'Kia', 'model': 'Forte', 'year': 2019, 'license_plate': 'KLM-4567', 'vin': '3KPF24AD8KE123456', 'color': 'Blue'},
            {'make': 'Jeep', 'model': 'Wrangler', 'year': 2021, 'license_plate': 'NOP-8901', 'vin': '1C4HJXDG2MW123456', 'color': 'Yellow'},
        ]
        
        vehicles = []
        for i, data in enumerate(vehicles_data):
            data['customer_id'] = customers[i % len(customers)].id
            vehicle = Vehicle(**data)
            vehicles.append(vehicle)
            db.session.add(vehicle)
        
        db.session.commit()
        print(f"Created {len(vehicles)} vehicles")
        
        # Create inventory parts
        print("Creating inventory parts...")
        parts_data = [
            {'part_name': 'Engine Oil Filter', 'part_number': 'EOF-001', 'description': 'Standard oil filter', 'quantity': 50, 'unit_price': 8.99, 'reorder_level': 10, 'supplier': 'AutoParts Co'},
            {'part_name': 'Air Filter', 'part_number': 'AF-002', 'description': 'Cabin air filter', 'quantity': 35, 'unit_price': 12.50, 'reorder_level': 10, 'supplier': 'AutoParts Co'},
            {'part_name': 'Brake Pads (Front)', 'part_number': 'BP-F-003', 'description': 'Front brake pads set', 'quantity': 20, 'unit_price': 45.00, 'reorder_level': 5, 'supplier': 'Brake Masters'},
            {'part_name': 'Brake Pads (Rear)', 'part_number': 'BP-R-004', 'description': 'Rear brake pads set', 'quantity': 18, 'unit_price': 40.00, 'reorder_level': 5, 'supplier': 'Brake Masters'},
            {'part_name': 'Spark Plugs', 'part_number': 'SP-005', 'description': 'Iridium spark plugs (set of 4)', 'quantity': 40, 'unit_price': 28.00, 'reorder_level': 8, 'supplier': 'Engine Parts Ltd'},
            {'part_name': 'Wiper Blades', 'part_number': 'WB-006', 'description': 'All-season wiper blades', 'quantity': 30, 'unit_price': 15.99, 'reorder_level': 10, 'supplier': 'AutoParts Co'},
            {'part_name': 'Battery', 'part_number': 'BAT-007', 'description': '12V car battery', 'quantity': 8, 'unit_price': 120.00, 'reorder_level': 3, 'supplier': 'Power Source'},
            {'part_name': 'Transmission Fluid', 'part_number': 'TF-008', 'description': 'Automatic transmission fluid (1L)', 'quantity': 25, 'unit_price': 18.50, 'reorder_level': 5, 'supplier': 'Fluid Dynamics'},
            {'part_name': 'Coolant', 'part_number': 'CL-009', 'description': 'Engine coolant (1L)', 'quantity': 30, 'unit_price': 12.00, 'reorder_level': 8, 'supplier': 'Fluid Dynamics'},
            {'part_name': 'Tire (All-Season)', 'part_number': 'TIRE-010', 'description': '205/55R16 all-season tire', 'quantity': 16, 'unit_price': 95.00, 'reorder_level': 4, 'supplier': 'Tire World'},
            {'part_name': 'Headlight Bulb', 'part_number': 'HB-011', 'description': 'LED headlight bulb', 'quantity': 24, 'unit_price': 22.00, 'reorder_level': 6, 'supplier': 'Lighting Pro'},
            {'part_name': 'Serpentine Belt', 'part_number': 'SB-012', 'description': 'Engine serpentine belt', 'quantity': 12, 'unit_price': 32.00, 'reorder_level': 3, 'supplier': 'Engine Parts Ltd'},
            {'part_name': 'Fuel Filter', 'part_number': 'FF-013', 'description': 'Inline fuel filter', 'quantity': 28, 'unit_price': 14.50, 'reorder_level': 8, 'supplier': 'AutoParts Co'},
            {'part_name': 'Cabin Air Filter', 'part_number': 'CAF-014', 'description': 'Activated carbon cabin filter', 'quantity': 22, 'unit_price': 16.99, 'reorder_level': 6, 'supplier': 'AutoParts Co'},
            {'part_name': 'Alternator', 'part_number': 'ALT-015', 'description': '12V alternator', 'quantity': 5, 'unit_price': 185.00, 'reorder_level': 2, 'supplier': 'Engine Parts Ltd'},
        ]
        
        parts = []
        for data in parts_data:
            part = InventoryPart(**data)
            parts.append(part)
            db.session.add(part)
        
        db.session.commit()
        print(f"Created {len(parts)} inventory parts")
        
        # Create services
        print("Creating services...")
        service_types = [
            'Oil Change',
            'Brake Service',
            'Tire Rotation',
            'Engine Diagnostic',
            'Transmission Service',
            'Battery Replacement',
            'Air Filter Replacement',
            'Coolant Flush',
            'Brake Pad Replacement',
            'Wheel Alignment'
        ]
        
        statuses = ['pending', 'in_progress', 'completed', 'completed', 'completed']  # More completed for realism
        
        services = []
        for i in range(30):
            days_offset = random.randint(-30, 30)
            scheduled_date = datetime.utcnow() + timedelta(days=days_offset)
            status = random.choice(statuses)
            
            service = Service(
                vehicle_id=random.choice(vehicles).id,
                service_type=random.choice(service_types),
                description=f"Service description for {random.choice(service_types).lower()}",
                status=status,
                cost=random.uniform(50, 500),
                scheduled_date=scheduled_date,
                completed_date=scheduled_date + timedelta(hours=random.randint(2, 8)) if status == 'completed' else None,
                created_by=admin.id
            )
            services.append(service)
            db.session.add(service)
        
        db.session.commit()
        print(f"Created {len(services)} services")
        
        # Add parts to some services
        print("Adding parts to services...")
        for service in random.sample(services, 15):
            num_parts = random.randint(1, 3)
            for _ in range(num_parts):
                part = random.choice(parts)
                quantity = random.randint(1, 3)
                
                if part.quantity >= quantity:
                    service_part = ServicePart(
                        service_id=service.id,
                        part_id=part.id,
                        quantity=quantity,
                        unit_price=part.unit_price
                    )
                    part.quantity -= quantity
                    service.cost += (part.unit_price * quantity)
                    db.session.add(service_part)
        
        db.session.commit()
        
        # Create sales for completed services
        print("Creating sales records...")
        completed_services = [s for s in services if s.status == 'completed']
        payment_methods = ['cash', 'card', 'transfer']
        
        for service in completed_services:
            sale = Sale(
                service_id=service.id,
                total_amount=service.cost,
                payment_method=random.choice(payment_methods),
                payment_status='paid' if random.random() > 0.1 else 'partial',
                created_by=admin.id
            )
            db.session.add(sale)
        
        db.session.commit()
        print(f"Created {len(completed_services)} sales records")
        
        print("\n" + "="*50)
        print("Database initialized successfully!")
        print("="*50)
        print("\nLogin Credentials:")
        print("-" * 50)
        print("Admin: username='admin', password='admin123'")
        print("Staff: username='staff', password='staff123'")
        print("-" * 50)
        print(f"\nSummary:")
        print(f"  - {len(customers)} customers")
        print(f"  - {len(vehicles)} vehicles")
        print(f"  - {len(services)} services")
        print(f"  - {len(parts)} inventory parts")
        print(f"  - {len(completed_services)} sales records")
        print("\nRun 'python app.py' to start the application!")
        print("="*50)

if __name__ == '__main__':
    init_database()
