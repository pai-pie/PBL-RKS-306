import mysql.connector
import os
import time
from datetime import datetime

class Database:
    def __init__(self):
        self.db_config = {
            'host': os.environ.get('DATABASE_HOST', 'localhost'),
            'user': os.environ.get('DATABASE_USER', 'root'),
            'password': os.environ.get('DATABASE_PASSWORD', 'pulupulu'),
            'database': 'db_konser',
            'port': os.environ.get('DATABASE_PORT', '3306'),
            'auth_plugin': 'mysql_native_password'
        }
    
    def get_connection(self):
        max_retries = 5
        for attempt in range(max_retries):
            try:
                connection = mysql.connector.connect(**self.db_config)
                print(f"✅ Database connection successful (attempt {attempt + 1})")
                return connection
            except Exception as e:
                print(f"❌ Database connection error (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    return None

    def execute_query(self, query, params=None, fetch=False, fetch_one=False):
        """Eksekusi query dengan error handling"""
        conn = None
        try:
            conn = self.get_connection()
            if not conn:
                return None
                
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            elif fetch_one:
                result = cursor.fetchone()
            else:
                conn.commit()
                result = cursor.lastrowid
            
            return result
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            if conn:
                conn.rollback()
            return None
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==========================
    #   USER OPERATIONS
    # ==========================
    
    def get_user_by_email(self, email):
        return self.execute_query(
            "SELECT * FROM users WHERE email = %s", 
            (email,), 
            fetch_one=True
        )

    def get_user_by_id(self, user_id):
        return self.execute_query(
            "SELECT * FROM users WHERE id = %s", 
            (user_id,), 
            fetch_one=True
        )

    def create_user(self, username, email, password_hash, role='user'):
        """Create a new user in database"""
        # =============================================
        # ✅ Catatan: Validasi panjang password sudah dilakukan di app.py
        # sebelum password di-hash. Fungsi ini hanya menerima password_hash
        # yang sudah di-hash oleh werkzeug.security.generate_password_hash()
        # =============================================
        
        try:
            query = "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)"
            result = self.execute_query(query, (username, email, password_hash, role))
            
            if result:
                print(f"✅ User created successfully: {username} ({email})")
                return True
            else:
                print(f"❌ Failed to create user: {username}")
                return False
        except Exception as e:
            print(f"❌ Database error creating user: {e}")
            import traceback
            traceback.print_exc()
            return False

    # ==========================
    #   EVENT OPERATIONS
    # ==========================
    
    def get_events_with_tickets(self):
        """Ambil events dengan data tickets"""
        events = self.execute_query(
            "SELECT * FROM events WHERE status IN ('Active', 'Upcoming') ORDER BY event_date ASC",
            fetch=True
        ) or []
        
        events_with_tickets = []
        for event in events:
            tickets = self.execute_query(
                """SELECT type_name, price, quota, sold, (quota - sold) as available 
                   FROM tickets WHERE event_id = %s ORDER BY price DESC""",
                (event['id'],), 
                fetch=True
            ) or []
            
            events_with_tickets.append({
                'id': event['id'],
                'name': event['name'],
                'location': event['location'],
                'event_date': event['event_date'],
                'status': event['status'],
                'tickets': tickets
            })
            
        return events_with_tickets

    def get_event_by_id(self, event_id):
        return self.execute_query(
            "SELECT * FROM events WHERE id = %s", 
            (event_id,), 
            fetch_one=True
        )

    def create_event(self, name, event_date, location, status):
        return self.execute_query(
            "INSERT INTO events (name, event_date, location, status) VALUES (%s, %s, %s, %s)",
            (name, event_date, location, status)
        )

    def update_event(self, event_id, name, event_date, location, status):
        return self.execute_query(
            "UPDATE events SET name=%s, event_date=%s, location=%s, status=%s WHERE id=%s",
            (name, event_date, location, status, event_id)
        )

    def delete_event(self, event_id):
        """Delete event dengan disable foreign key checks sementara"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            print(f"🔍 Attempting to delete event {event_id}")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            cursor.execute("DELETE FROM orders WHERE event_id = %s", (event_id,))
            print(f"📦 Deleted {cursor.rowcount} orders")
            
            cursor.execute("DELETE FROM payments WHERE event_id = %s", (event_id,))
            print(f"💰 Deleted {cursor.rowcount} payments")
            
            cursor.execute("DELETE FROM tickets WHERE event_id = %s", (event_id,))
            print(f"🎫 Deleted {cursor.rowcount} tickets")
            
            cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
            deleted_rows = cursor.rowcount
            print(f"🗑️ Deleted {deleted_rows} events")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            print(f"🎉 Event {event_id} deleted successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error deleting event {event_id}: {str(e)}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==========================
    #   TICKET OPERATIONS  
    # ==========================
    
    def get_tickets_by_event(self, event_id):
        return self.execute_query(
            "SELECT *, (quota - sold) as available FROM tickets WHERE event_id = %s ORDER BY price ASC",
            (event_id,), 
            fetch=True
        )

    def get_ticket_by_id(self, ticket_id):
        return self.execute_query(
            "SELECT * FROM tickets WHERE id = %s", 
            (ticket_id,), 
            fetch_one=True
        )

    def get_ticket_with_event(self, ticket_id):
        return self.execute_query(
            """SELECT t.*, e.name as event_name 
               FROM tickets t JOIN events e ON t.event_id = e.id 
               WHERE t.id = %s""",
            (ticket_id,), 
            fetch_one=True
        )

    def create_ticket(self, event_id, type_name, price, quota, sold=0):
        return self.execute_query(
            "INSERT INTO tickets (event_id, type_name, price, quota, sold) VALUES (%s, %s, %s, %s, %s)",
            (event_id, type_name, price, quota, sold)
        )

    def update_ticket(self, ticket_id, type_name, price, quota):
        return self.execute_query(
            "UPDATE tickets SET type_name=%s, price=%s, quota=%s WHERE id=%s",
            (type_name, price, quota, ticket_id)
        )

    def delete_ticket(self, ticket_id):
        return self.execute_query(
            "DELETE FROM tickets WHERE id = %s", 
            (ticket_id,)
        )

    # ==========================
    #   PAYMENT & ORDER OPERATIONS - ✅ DEBUG EXTENSIF
    # ==========================
    
    def process_checkout(self, user_id, event_id, tickets, username, email, payment_method='VA'):
        """Process checkout dengan transaction - ULTRA DEBUG"""
        conn = None
        try:
            print(f"🔍 [CHECKOUT] START: user_id={user_id}, event_id={event_id}, tickets={tickets}")
        
            conn = self.get_connection()
            if not conn:
                print("❌ [CHECKOUT] Database connection failed")
                return {'success': False, 'error': 'Database connection failed'}
            
            cursor = conn.cursor(dictionary=True)
            print("✅ [CHECKOUT] Database connection successful")
        
            # Hitung total & validasi stok
            total_amount = 0
            ticket_details = []
        
            for ticket_type, quantity in tickets.items():
                if quantity <= 0:
                    continue
                
                print(f"🔍 [CHECKOUT] Processing ticket: {ticket_type} x{quantity}")
                cursor.execute(
                    "SELECT id, quota, sold, price FROM tickets WHERE event_id = %s AND type_name = %s",
                    (event_id, ticket_type)
                )
                ticket = cursor.fetchone()
            
                if not ticket:
                    print(f"❌ [CHECKOUT] Ticket type {ticket_type} not found")
                    return {'success': False, 'error': f'Ticket type {ticket_type} not found'}
            
                available = ticket['quota'] - ticket['sold']
                print(f"🔍 [CHECKOUT] Ticket {ticket_type}: quota={ticket['quota']}, sold={ticket['sold']}, available={available}")
            
                if quantity > available:
                    print(f"❌ [CHECKOUT] Not enough {ticket_type} tickets")
                    return {'success': False, 'error': f'Only {available} {ticket_type} tickets available'}
            
                total_amount += quantity * ticket['price']
                ticket_details.append(f"{ticket_type} x{quantity}")
            
                # Update ticket quota
                cursor.execute(
                    "UPDATE tickets SET sold = sold + %s WHERE event_id = %s AND type_name = %s",
                    (quantity, event_id, ticket_type)
                )
                print(f"✅ [CHECKOUT] Updated ticket {ticket_type}: +{quantity} sold")
        
            # Generate VA Number
            va_number = f"88{user_id:06d}{int(time.time()) % 10000:04d}"
            print(f"💰 [CHECKOUT] Total amount: {total_amount}, VA: {va_number}")
        
            # Convert untuk payments table
            payment_amount = int(total_amount)
            print(f"🔧 [CHECKOUT] Payment amount (int): {payment_amount}")
        
            # Insert ke payments
            print(f"🔧 [CHECKOUT] Inserting into payments...")
            cursor.execute(
                """INSERT INTO payments 
                (user_id, event_id, payment_method, va_number, amount, status, expires_at) 
                VALUES (%s, %s, %s, %s, %s, 'paid', DATE_ADD(NOW(), INTERVAL 24 HOUR))""",
                (user_id, event_id, payment_method, va_number, payment_amount)
            )
            payment_id = cursor.lastrowid
            print(f"✅ [CHECKOUT] Created payment: ID {payment_id}")
        
            # Insert ke orders
            print(f"🔧 [CHECKOUT] Inserting into orders...")
            cursor.execute(
                """INSERT INTO orders 
                (user_id, event_id, customer_name, customer_email, total_amount, payment_status, payment_id, ticket_details, order_date) 
                VALUES (%s, %s, %s, %s, %s, 'paid', %s, %s, NOW())""",
                (user_id, event_id, username, email, total_amount, payment_id, ', '.join(ticket_details))
            )
            order_id = cursor.lastrowid
            print(f"✅ [CHECKOUT] Created order: ID {order_id}")
        
            # VERIFY DATA SEBELUM COMMIT - DETAILED
            print(f"🔄 [CHECKOUT] Verifying data before commit...")
        
            cursor.execute("SELECT * FROM payments WHERE id = %s", (payment_id,))
            payment_check = cursor.fetchone()
            print(f"🔄 [CHECKOUT] Payment verification: {payment_check}")
        
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order_check = cursor.fetchone()
            print(f"🔄 [CHECKOUT] Order verification: {order_check}")
        
            # COMMIT dengan error handling detail
            print(f"🔄 [CHECKOUT] COMMITTING transaction...")
            try:
                conn.commit()
                print(f"✅ [CHECKOUT] AFTER COMMIT - Transaction SUCCESS!")
            
                # VERIFY SETELAH COMMIT
                print(f"🔍 [CHECKOUT] Verifying data AFTER commit...")
                cursor.execute("SELECT * FROM payments WHERE id = %s", (payment_id,))
                payment_after = cursor.fetchone()
                print(f"🔍 [CHECKOUT] Payment after commit: {payment_after}")
            
                cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
                order_after = cursor.fetchone()
                print(f"🔍 [CHECKOUT] Order after commit: {order_after}")
            
            except Exception as commit_error:
                print(f"❌ [CHECKOUT] COMMIT ERROR: {commit_error}")
                raise commit_error
        
            print(f"🎉 [CHECKOUT] FINAL SUCCESS: user={user_id}, order={order_id}, payment={payment_id}")
        
            return {
                'success': True,
                'payment_id': payment_id,
                'va_number': va_number,
                'total_amount': total_amount
            }
        
        except Exception as e:
            print(f"❌ [CHECKOUT] CRITICAL ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            if conn:
                conn.rollback()
                print("🔄 [CHECKOUT] Transaction ROLLED BACK")
            return {'success': False, 'error': f'Checkout failed: {str(e)}'}
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                print("🔒 [CHECKOUT] Database connection closed")

    # ==========================
    #   PAYMENT OPERATIONS
    # ==========================

    def get_payment_with_details(self, payment_id):
        return self.execute_query(
            """SELECT p.*, e.name as event_name, u.username 
               FROM payments p
               JOIN events e ON p.event_id = e.id
               JOIN users u ON p.user_id = u.id
               WHERE p.id = %s""",
            (payment_id,), 
            fetch_one=True
        )

    def mark_payment_as_paid(self, payment_id):
        """Mark payment as paid dengan transaction"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT p.*, o.ticket_details, o.id as order_id 
                FROM payments p 
                LEFT JOIN orders o ON p.id = o.payment_id 
                WHERE p.id = %s
            """, (payment_id,))
            payment = cursor.fetchone()
            
            if not payment:
                return {'success': False, 'error': 'Payment not found'}
            
            if payment['status'] == 'paid':
                return {'success': False, 'error': 'Payment already completed'}
            
            cursor.execute("UPDATE payments SET status = 'paid' WHERE id = %s", (payment_id,))
            
            if payment['order_id']:
                cursor.execute("UPDATE orders SET payment_status = 'paid' WHERE payment_id = %s", (payment_id,))
            
            conn.commit()
            return {'success': True}
            
        except Exception as e:
            if conn:
                conn.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==========================
    #   ORDER OPERATIONS
    # ==========================
    
    def get_orders_by_user(self, user_id):
        return self.execute_query(
            """SELECT o.*, e.name as event_name, e.event_date, e.location
               FROM orders o 
               JOIN events e ON o.event_id = e.id 
               WHERE o.user_id = %s 
               ORDER BY o.order_date DESC""",
            (user_id,), 
            fetch=True
        )

    def get_all_orders(self):
        return self.execute_query(
            """SELECT o.*, e.name as event_name, u.username, e.event_date
               FROM orders o 
               JOIN events e ON o.event_id = e.id 
               JOIN users u ON o.user_id = u.id 
               ORDER BY o.order_date DESC""",
            fetch=True
        )

    # ==========================
    #   ADMIN DASHBOARD DATA - ✅ DIPERBAIKI
    # ==========================
    
    def get_admin_dashboard_data(self):
        """Ambil semua data untuk admin dashboard - SIMPLE FIX"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            print("🔍 [ADMIN] Getting dashboard data...")
            
            # 1. Get events - PASTI WORK
            cursor.execute("SELECT * FROM events ORDER BY event_date DESC")
            events = cursor.fetchall() or []
            print(f"✅ [ADMIN] Found {len(events)} events")
            
            # 2. Get tickets - PASTI WORK  
            cursor.execute("""
                SELECT t.*, (t.quota - t.sold) as available, e.name as event_name
                FROM tickets t JOIN events e ON t.event_id = e.id
                ORDER BY e.name, t.price ASC
            """)
            all_tickets = cursor.fetchall() or []
            print(f"✅ [ADMIN] Found {len(all_tickets)} tickets")
            
            # 3. ✅ PERBAIKAN KRITIS: Get users dengan query SANGAT SEDERHANA
            cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY created_at DESC")
            users_raw = cursor.fetchall() or []
            print(f"✅ [ADMIN] Found {len(users_raw)} raw users")
            
            # Process users data - hitung manual total_orders dan total_spent
            users = []
            for user in users_raw:
                # Get total orders untuk user ini
                cursor.execute("SELECT COUNT(*) as total_orders FROM orders WHERE user_id = %s", (user['id'],))
                orders_result = cursor.fetchone()
                total_orders = orders_result['total_orders'] if orders_result else 0
                
                # Get total spent untuk user ini  
                cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total_spent FROM orders WHERE user_id = %s AND payment_status = 'paid'", (user['id'],))
                spent_result = cursor.fetchone()
                total_spent = spent_result['total_spent'] if spent_result else 0
                
                users.append({
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'role': user['role'],
                    'status': 'Regular Member',  # Default value
                    'created_at': user['created_at'],
                    'total_orders': total_orders,
                    'total_spent': total_spent
                })
            
            print(f"✅ [ADMIN] Processed {len(users)} users")
            
            # 4. Get transactions
            cursor.execute("""
                SELECT p.*, e.name as event_name, u.username as customer_name,
                       o.ticket_details, p.created_at as transaction_date
                FROM payments p
                JOIN events e ON p.event_id = e.id
                JOIN users u ON p.user_id = u.id
                LEFT JOIN orders o ON p.id = o.payment_id
                ORDER BY p.created_at DESC LIMIT 10
            """)
            transactions = cursor.fetchall() or []
            print(f"✅ [ADMIN] Found {len(transactions)} transactions")
            
            # 5. Get stats
            cursor.execute("SELECT COUNT(*) as total FROM payments")
            total_transactions = cursor.fetchone()['total'] or 0
            
            cursor.execute("SELECT COUNT(*) as paid FROM payments WHERE status = 'paid'")
            paid_transactions = cursor.fetchone()['paid'] or 0
            
            cursor.execute("SELECT SUM(amount) as revenue FROM payments WHERE status = 'paid'")
            revenue_result = cursor.fetchone()
            revenue = revenue_result['revenue'] if revenue_result and revenue_result['revenue'] else 0
            
            print(f"📊 [ADMIN] Final stats: transactions={total_transactions}, paid={paid_transactions}, revenue={revenue}")
            
            return {
                'events': events,
                'all_tickets': all_tickets,
                'users': users,
                'transactions': transactions,
                'total_transactions': total_transactions,
                'paid_transactions': paid_transactions,
                'revenue': revenue
            }
            
        except Exception as e:
            print(f"❌ [ADMIN] CRITICAL ERROR in dashboard: {str(e)}")
            import traceback
            traceback.print_exc()
            # Return empty data rather than crashing
            return {
                'events': [],
                'all_tickets': [],
                'users': [],
                'transactions': [],
                'total_transactions': 0,
                'paid_transactions': 0,
                'revenue': 0
            }
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==========================
    #   ADDITIONAL METHODS
    # ==========================
    
    def get_event_stats(self):
        """Get statistics for events"""
        return self.execute_query(
            """SELECT 
                   COUNT(*) as total_events,
                   SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_events,
                   SUM(CASE WHEN status = 'Upcoming' THEN 1 ELSE 0 END) as upcoming_events,
                   SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed_events
               FROM events""",
            fetch_one=True
        )

    def get_user_stats(self):
        """Get statistics for users"""
        return self.execute_query(
            """SELECT 
                   COUNT(*) as total_users,
                   SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) as admin_users,
                   SUM(CASE WHEN role = 'user' THEN 1 ELSE 0 END) as regular_users
               FROM users""",
            fetch_one=True
        )

    # ==========================
    #   USER PROFILE OPERATIONS
    # ==========================
    
    def update_user_profile(self, user_id, name, email, status):
        """Update user profile information"""
        try:
            print(f"🔧 DATABASE: Updating profile for user {user_id}")
            print(f"🔧 DATABASE: name={name}, email={email}, status={status}")
            
            result = self.execute_query(
                "UPDATE users SET username = %s, email = %s, status = %s WHERE id = %s",
                (name, email, status, user_id)
            )
            
            print(f"🔧 DATABASE: Update result = {result}")
            
            return result is not None
        except Exception as e:
            print(f"❌ DATABASE Error: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_user_tickets(self, user_id):
        """Get all tickets for a user"""
        return self.execute_query(
            """SELECT 
                   o.id as order_id,
                   o.ticket_details,
                   o.total_amount,
                   o.payment_status,
                   o.order_date,
                   e.name as event_name,
                   e.event_date,
                   e.location,
                   p.va_number,
                   p.status as payment_status
               FROM orders o
               JOIN events e ON o.event_id = e.id
               LEFT JOIN payments p ON o.payment_id = p.id
               WHERE o.user_id = %s
               ORDER BY o.order_date DESC""",
            (user_id,), 
            fetch=True
        ) or []

    def get_user_detailed_stats(self, user_id):
        """Get detailed statistics for a user"""
        total_tickets = self.execute_query(
            "SELECT COUNT(*) as count FROM orders WHERE user_id = %s",
            (user_id,), 
            fetch_one=True
        ) or {'count': 0}
        
        upcoming_events = self.execute_query(
            """SELECT COUNT(DISTINCT o.event_id) as count 
               FROM orders o 
               JOIN events e ON o.event_id = e.id 
               WHERE o.user_id = %s AND e.event_date >= CURDATE()""",
            (user_id,), 
            fetch_one=True
        ) or {'count': 0}
        
        total_spent = self.execute_query(
            "SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE user_id = %s AND payment_status = 'paid'",
            (user_id,), 
            fetch_one=True
        ) or {'total': 0}
        
        user_info = self.get_user_by_id(user_id)
        
        return {
            'total_tickets': total_tickets['count'],
            'upcoming_events': upcoming_events['count'],
            'total_spent': total_spent['total'],
            'member_since': user_info.get('created_at') if user_info else None,
            'status': user_info.get('status', 'Regular Member') if user_info else 'Regular Member'
        }

    def cancel_user_ticket(self, user_id, ticket_id):
        """Cancel a user's ticket"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM orders WHERE id = %s AND user_id = %s",
                (ticket_id, user_id)
            )
            order = cursor.fetchone()
            
            if not order:
                return {'success': False, 'error': 'Ticket not found'}
            
            cursor.execute(
                "UPDATE orders SET payment_status = 'cancelled' WHERE id = %s",
                (ticket_id,)
            )
            
            conn.commit()
            return {'success': True}
            
        except Exception as e:
            if conn:
                conn.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    # ==========================
    #   ADMIN USER MANAGEMENT
    # ==========================
    
    def update_user_role(self, user_id, role):
        """Update user role (admin function)"""
        return self.execute_query(
            "UPDATE users SET role = %s WHERE id = %s",
            (role, user_id)
        )

    def get_all_users_detailed(self):
        """Get all users with detailed information"""
        return self.execute_query(
            """SELECT 
                   u.id, u.username, u.email, u.role, 
                   u.created_at, 
                   COUNT(o.id) as total_orders,
                   COALESCE(SUM(CASE WHEN o.payment_status = 'paid' THEN o.total_amount ELSE 0 END), 0) as total_spent
               FROM users u
               LEFT JOIN orders o ON u.id = o.user_id
               GROUP BY u.id, u.username, u.email, u.role, u.created_at
               ORDER BY u.created_at DESC""",
            fetch=True
        ) or []

    # ==========================
    #   DELETE USER ACCOUNT
    # ==========================
    
    def delete_user_account(self, user_id):
        """Delete user account and all associated data"""
        conn = None
        try:
            conn = self.get_connection()
            if not conn:
                return {'success': False, 'error': 'Database connection failed'}
                
            cursor = conn.cursor(dictionary=True)
            
            print(f"🔍 Starting account deletion for user {user_id}")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            
            cursor.execute("DELETE FROM payments WHERE user_id = %s", (user_id,))
            payments_deleted = cursor.rowcount
            print(f"💰 Deleted {payments_deleted} payments")
            
            cursor.execute("DELETE FROM orders WHERE user_id = %s", (user_id,))
            orders_deleted = cursor.rowcount
            print(f"📦 Deleted {orders_deleted} orders")
            
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            user_deleted = cursor.rowcount
            print(f"👤 Deleted {user_deleted} users")
            
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            
            if user_deleted > 0:
                print(f"🎉 Account {user_id} deleted successfully!")
                return {'success': True}
            else:
                print(f"❌ User {user_id} not found for deletion")
                return {'success': False, 'error': 'User not found'}
                
        except Exception as e:
            print(f"❌ Error deleting account {user_id}: {str(e)}")
            if conn:
                conn.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()