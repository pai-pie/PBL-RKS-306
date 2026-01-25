from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import re
from werkzeug.security import generate_password_hash, check_password_hash

@dataclass
class User:
    id: int
    username: str
    email: str
    password_hash: str
    role: str
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validasi setelah inisialisasi"""
        self._validate_username()
        self._validate_email()
    
    def _validate_username(self):
        if not self.username or len(self.username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if not re.match(r'^[a-zA-Z0-9_]+$', self.username):
            raise ValueError("Username can only contain letters, numbers and underscores")
    
    def _validate_email(self):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, self.email):
            raise ValueError("Invalid email format")
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validasi password untuk registration - MINIMAL 12 KARAKTER"""
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters long")
        return True
    
    @classmethod
    def create(cls, username: str, email: str, password: str, role: str = 'user') -> 'User':
        # Validasi password
        cls.validate_password(password)
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        return cls(
            id=0,  # ID akan di-set oleh database
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=datetime.now()
        )
    
    def check_password(self, password: str) -> bool:
        """Cek apakah password cocok dengan hash"""
        return check_password_hash(self.password_hash, password)

@dataclass
class Event:
    id: int
    name: str
    event_date: datetime
    location: str
    status: str
    
    def __post_init__(self):
        """Validasi event"""
        if not self.name or len(self.name.strip()) < 3:
            raise ValueError("Event name must be at least 3 characters long")
        if self.event_date < datetime.now():
            # Ini warning saja, tidak error
            print("⚠️ Warning: Event date is in the past")
        if self.status not in ['Active', 'Upcoming', 'Completed', 'Cancelled']:
            raise ValueError("Invalid event status")

@dataclass
class Ticket:
    id: int
    event_id: int
    type_name: str
    price: float
    quota: int
    sold: int
    
    def __post_init__(self):
        """Validasi ticket"""
        if self.price <= 0:
            raise ValueError("Ticket price must be positive")
        if self.quota <= 0:
            raise ValueError("Ticket quota must be positive")
        if self.sold < 0:
            raise ValueError("Sold tickets cannot be negative")
        if self.sold > self.quota:
            raise ValueError("Sold tickets cannot exceed quota")
    
    @property
    def available(self) -> int:
        """Jumlah tiket yang tersedia"""
        return self.quota - self.sold
    
    @property
    def is_sold_out(self) -> bool:
        """Apakah tiket sudah habis?"""
        return self.available <= 0

@dataclass
class Payment:
    id: int
    user_id: int
    event_id: int
    amount: float
    status: str
    va_number: str
    created_at: datetime
    
    def __post_init__(self):
        """Validasi payment"""
        if self.amount <= 0:
            raise ValueError("Payment amount must be positive")
        if self.status not in ['pending', 'paid', 'failed', 'expired']:
            raise ValueError("Invalid payment status")
        if not self.va_number or len(self.va_number) < 10:
            raise ValueError("Invalid VA number")
    
    @property
    def is_paid(self) -> bool:
        """Apakah pembayaran sudah lunas?"""
        return self.status == 'paid'

@dataclass
class Order:
    id: int
    user_id: int
    event_id: int
    total_amount: float
    payment_status: str
    ticket_details: str
    order_date: Optional[datetime] = None
    
    def __post_init__(self):
        """Validasi order"""
        if self.total_amount <= 0:
            raise ValueError("Order amount must be positive")
        if self.payment_status not in ['pending', 'paid', 'cancelled', 'refunded']:
            raise ValueError("Invalid payment status")
    
    @property
    def is_paid(self) -> bool:
        """Apakah order sudah dibayar?"""
        return self.payment_status == 'paid'

@dataclass
class UserProfile:
    id: int
    username: str
    email: str
    role: str
    status: str
    created_at: datetime
    total_tickets: int = 0
    upcoming_events: int = 0
    total_spent: float = 0.0
    
    @property
    def is_premium(self) -> bool:
        """Apakah user premium?"""
        return self.status.lower() == 'premium'
    
    @property
    def is_admin(self) -> bool:
        """Apakah user admin?"""
        return self.role.lower() == 'admin'

@dataclass
class UserTicket:
    order_id: int
    event_name: str
    event_date: datetime
    location: str
    ticket_details: str
    total_amount: float
    payment_status: str
    order_date: datetime
    va_number: str = ""
    
    @property
    def is_paid(self) -> bool:
        """Apakah tiket sudah dibayar?"""
        return self.payment_status.lower() == 'paid'
    
    @property
    def is_upcoming(self) -> bool:
        """Apakah event masih upcoming?"""
        return self.event_date > datetime.now()