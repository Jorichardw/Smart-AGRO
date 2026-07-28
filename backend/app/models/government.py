"""Government Scheme models for AGRO-BOT & AUTOMATION"""
from sqlalchemy import Column, String, Text, DECIMAL, ForeignKey, DateTime, Enum, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base

class SchemeType(str, enum.Enum):
    SUBSIDY = "subsidy"
    LOAN = "loan"
    INSURANCE = "insurance"
    GRANT = "grant"
    TRAINING = "training"

class ApplicationStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    DISBURSED = "disbursed"

class GovernmentScheme(Base):
    __tablename__ = "government_schemes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scheme_name = Column(String(300), nullable=False)
    scheme_type = Column(Enum(SchemeType))
    description = Column(Text)
    benefits = Column(Text)
    eligibility_criteria = Column(Text)
    required_documents = Column(Text)
    application_process = Column(Text)
    application_deadline = Column(Date)
    scheme_amount = Column(DECIMAL(12, 2))
    percentage_subsidy = Column(DECIMAL(5, 2))
    implementing_agency = Column(String(200))
    contact_details = Column(Text)
    website_url = Column(Text)
    state = Column(String(100))
    district = Column(String(100))
    is_active = Column(Boolean, default=True)
    launch_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    applications = relationship("SchemeApplication", back_populates="scheme")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'scheme_name': self.scheme_name, 'scheme_type': self.scheme_type.value if self.scheme_type else None,
            'description': self.description, 'benefits': self.benefits, 'eligibility_criteria': self.eligibility_criteria,
            'required_documents': self.required_documents, 'application_process': self.application_process,
            'application_deadline': self.application_deadline.isoformat() if self.application_deadline else None,
            'scheme_amount': float(self.scheme_amount) if self.scheme_amount else None,
            'percentage_subsidy': float(self.percentage_subsidy) if self.percentage_subsidy else None,
            'implementing_agency': self.implementing_agency, 'contact_details': self.contact_details,
            'website_url': self.website_url, 'state': self.state, 'district': self.district, 'is_active': self.is_active,
            'launch_date': self.launch_date.isoformat() if self.launch_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class SchemeApplication(Base):
    __tablename__ = "scheme_applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("farmers.id", ondelete="CASCADE"), nullable=False)
    scheme_id = Column(UUID(as_uuid=True), ForeignKey("government_schemes.id"), nullable=False)
    application_number = Column(String(100), unique=True)
    application_date = Column(Date)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.SUBMITTED)
    applied_amount = Column(DECIMAL(12, 2))
    approved_amount = Column(DECIMAL(12, 2))
    disbursed_amount = Column(DECIMAL(12, 2))
    rejection_reason = Column(Text)
    documents_submitted = Column(JSONB)
    officer_remarks = Column(Text)
    disbursement_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="scheme_applications")
    scheme = relationship("GovernmentScheme", back_populates="applications")
    
    def to_dict(self):
        return {
            'id': str(self.id), 'farmer_id': str(self.farmer_id), 'scheme_id': str(self.scheme_id),
            'application_number': self.application_number, 'application_date': self.application_date.isoformat() if self.application_date else None,
            'status': self.status.value if self.status else None, 'applied_amount': float(self.applied_amount) if self.applied_amount else None,
            'approved_amount': float(self.approved_amount) if self.approved_amount else None,
            'disbursed_amount': float(self.disbursed_amount) if self.disbursed_amount else None,
            'rejection_reason': self.rejection_reason, 'documents_submitted': self.documents_submitted,
            'officer_remarks': self.officer_remarks, 'disbursement_date': self.disbursement_date.isoformat() if self.disbursement_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }