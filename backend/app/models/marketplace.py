"""Marketplace models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, Text, Integer, DECIMAL, ForeignKey, DateTime, Enum, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from geoalchemy2 import Geography
import uuid
import enum
from app.core.database import Base

class ProductType(str, enum.Enum):
    PRODUCE = "produce"
    SEEDS = "seeds"
    FERTILIZER = "fertilizer"
    EQUIPMENT = "equipment"
    SERVICES = "services"

class ProductStatus(str, enum.Enum):
    ACTIVE = "active"
    SOLD = "sold"
    EXPIRED = "expired"
    INACTIVE = "inactive"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class OrderStatus(str, enum.Enum):
    PLACED = "placed"
    CONFIRMED = "confirmed"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class DeliveryType(str, enum.Enum):
    PICKUP = "pickup"
    DELIVERY = "delivery"

class MarketplaceCategory(Base):
    __tablename__ = "marketplace_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    parent_category_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_categories.id"))
    description = Column(Text)
    image_url = Column(Text)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    products = relationship("MarketplaceProduct", back_populates="category")
    parent_category = relationship("MarketplaceCategory", remote_side=[id])
    
    def to_dict(self):
        return {
            'id': str(self.id), 'name': self.name, 'parent_category_id': str(self.parent_category_id) if self.parent_category_id else None,
            'description': self.description, 'image_url': self.image_url, 'is_active': self.is_active,
            'sort_order': self.sort_order, 'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MarketplaceProduct(Base):
    __tablename__ = "marketplace_products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_categories.id"))
    name = Column(String(300), nullable=False)
    description = Column(Text)
    product_type = Column(Enum(ProductType))
    variety = Column(String(200))
    quantity = Column(DECIMAL(10, 2))
    unit = Column(String(20))
    price_per_unit = Column(DECIMAL(10, 2))
    min_order_quantity = Column(DECIMAL(8, 2))
    harvest_date = Column(Date)
    expiry_date = Column(Date)
    quality_grade = Column(String(50))
    organic_certified = Column(Boolean, default=False)
    certification_details = Column(Text)
    location = Column(Geography(geometry_type='POINT', srid=4326))
    pickup_available = Column(Boolean, default=True)
    delivery_available = Column(Boolean, default=False)
    delivery_radius_km = Column(Integer)
    images = Column(JSONB)
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    views_count = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    seller = relationship("Farmer", back_populates="marketplace_products")
    category = relationship("MarketplaceCategory", back_populates="products")
    orders = relationship("MarketplaceOrder", back_populates="product")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'seller_id': str(self.seller_id), 'category_id': str(self.category_id) if self.category_id else None,
            'name': self.name, 'description': self.description, 'product_type': self.product_type.value if self.product_type else None,
            'variety': self.variety, 'quantity': float(self.quantity) if self.quantity else None, 'unit': self.unit,
            'price_per_unit': float(self.price_per_unit) if self.price_per_unit else None,
            'min_order_quantity': float(self.min_order_quantity) if self.min_order_quantity else None,
            'harvest_date': self.harvest_date.isoformat() if self.harvest_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'quality_grade': self.quality_grade, 'organic_certified': self.organic_certified,
            'certification_details': self.certification_details, 'pickup_available': self.pickup_available,
            'delivery_available': self.delivery_available, 'delivery_radius_km': self.delivery_radius_km,
            'images': self.images, 'status': self.status.value if self.status else None,
            'views_count': self.views_count, 'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class MarketplaceOrder(Base):
    __tablename__ = "marketplace_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(String(50), unique=True, nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_products.id"))
    quantity = Column(DECIMAL(10, 2))
    unit_price = Column(DECIMAL(10, 2))
    total_amount = Column(DECIMAL(12, 2))
    delivery_address = Column(Text)
    delivery_type = Column(Enum(DeliveryType))
    payment_method = Column(String(50))
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.PLACED)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_delivery_date = Column(Date)
    actual_delivery_date = Column(Date)
    notes = Column(Text)
    rating = Column(Integer)
    review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    buyer = relationship("Farmer", foreign_keys=[buyer_id])
    seller = relationship("Farmer", foreign_keys=[seller_id])
    product = relationship("MarketplaceProduct", back_populates="orders")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'order_number': self.order_number, 'buyer_id': str(self.buyer_id),
            'seller_id': str(self.seller_id), 'product_id': str(self.product_id),
            'quantity': float(self.quantity) if self.quantity else None,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'delivery_address': self.delivery_address, 'delivery_type': self.delivery_type.value if self.delivery_type else None,
            'payment_method': self.payment_method, 'payment_status': self.payment_status.value if self.payment_status else None,
            'order_status': self.order_status.value if self.order_status else None,
            'order_date': self.order_date.isoformat(), 'expected_delivery_date': self.expected_delivery_date.isoformat() if self.expected_delivery_date else None,
            'actual_delivery_date': self.actual_delivery_date.isoformat() if self.actual_delivery_date else None,
            'notes': self.notes, 'rating': self.rating, 'review': self.review,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }