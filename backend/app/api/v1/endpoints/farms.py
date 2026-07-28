"""
Farm endpoints for AGRO-BOT & AUTOMATION
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user, get_farmer_user
from app.models.user import User
from app.models.farm import Farm, Plot
from app.services.farm_service import FarmService, PlotService
from app.services.farmer_service import FarmerService
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


# Farm schemas (inline for now)
from pydantic import BaseModel, validator
from typing import Optional


class FarmCreate(BaseModel):
    name: str
    address: Optional[str] = None
    total_area: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    elevation: Optional[float] = None
    farm_type: Optional[str] = None
    ownership_type: Optional[str] = None
    registration_number: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    @validator('total_area')
    def validate_area(cls, v):
        if v is not None and v < 0:
            raise ValueError('Area cannot be negative')
        return v


class FarmUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    total_area: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    elevation: Optional[float] = None
    farm_type: Optional[str] = None
    ownership_type: Optional[str] = None
    registration_number: Optional[str] = None


class PlotCreate(BaseModel):
    name: str
    area: Optional[float] = None
    soil_ph: Optional[float] = None
    soil_ec: Optional[float] = None
    organic_matter: Optional[float] = None
    nitrogen_level: Optional[float] = None
    phosphorus_level: Optional[float] = None
    potassium_level: Optional[float] = None
    
    @validator('area')
    def validate_area(cls, v):
        if v is not None and v < 0:
            raise ValueError('Area cannot be negative')
        return v
    
    @validator('soil_ph')
    def validate_ph(cls, v):
        if v is not None and (v < 0 or v > 14):
            raise ValueError('pH must be between 0 and 14')
        return v


class PlotUpdate(BaseModel):
    name: Optional[str] = None
    area: Optional[float] = None
    soil_ph: Optional[float] = None
    soil_ec: Optional[float] = None
    organic_matter: Optional[float] = None
    nitrogen_level: Optional[float] = None
    phosphorus_level: Optional[float] = None
    potassium_level: Optional[float] = None


class FarmResponse(BaseModel):
    id: UUID
    name: str
    address: Optional[str] = None
    total_area: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    elevation: Optional[float] = None
    farm_type: Optional[str] = None
    ownership_type: Optional[str] = None
    registration_number: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


class PlotResponse(BaseModel):
    id: UUID
    name: str
    area: Optional[float] = None
    soil_ph: Optional[float] = None
    soil_ec: Optional[float] = None
    organic_matter: Optional[float] = None
    nitrogen_level: Optional[float] = None
    phosphorus_level: Optional[float] = None
    potassium_level: Optional[float] = None
    created_at: str
    updated_at: Optional[str] = None
    
    class Config:
        from_attributes = True


# Farm endpoints
@router.get("/", response_model=List[FarmResponse])
async def get_my_farms(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Get current user's farms"""
    try:
        # Get farmer profile
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farmer profile not found"
            )
        
        # Get farms
        farm_service = FarmService(db)
        farms = farm_service.get_by_farmer_id(farmer.id, skip=skip, limit=limit)
        
        return [FarmResponse.from_attributes(farm) for farm in farms]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting farms for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving farms"
        )


@router.post("/", response_model=FarmResponse)
async def create_farm(
    farm_data: FarmCreate,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Create new farm"""
    try:
        # Get farmer profile
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farmer profile not found"
            )
        
        # Prepare farm data
        farm_dict = farm_data.dict(exclude_unset=True)
        farm_dict['farmer_id'] = farmer.id
        
        # Handle location data
        if farm_data.latitude and farm_data.longitude:
            # Convert to PostGIS POINT (longitude, latitude)
            from sqlalchemy import text
            farm_dict['location'] = text(f"ST_SetSRID(ST_MakePoint({farm_data.longitude}, {farm_data.latitude}), 4326)")
            del farm_dict['latitude']
            del farm_dict['longitude']
        
        # Create farm
        farm_service = FarmService(db)
        farm = farm_service.create(farm_dict)
        
        logger.info(f"Farm created: {farm.id} for user {current_user.id}")
        return FarmResponse.from_attributes(farm)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating farm for user {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating farm"
        )


@router.get("/{farm_id}", response_model=FarmResponse)
async def get_farm(
    farm_id: UUID,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Get specific farm"""
    try:
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(farm_id)
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        # Check ownership
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this farm"
            )
        
        return FarmResponse.from_attributes(farm)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting farm {farm_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving farm"
        )


@router.put("/{farm_id}", response_model=FarmResponse)
async def update_farm(
    farm_id: UUID,
    farm_data: FarmUpdate,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Update farm"""
    try:
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(farm_id)
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        # Check ownership
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this farm"
            )
        
        # Update farm
        updated_farm = farm_service.update(farm_id, farm_data.dict(exclude_unset=True))
        
        logger.info(f"Farm updated: {farm_id} by user {current_user.id}")
        return FarmResponse.from_attributes(updated_farm)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating farm {farm_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating farm"
        )


@router.delete("/{farm_id}")
async def delete_farm(
    farm_id: UUID,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Delete farm"""
    try:
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(farm_id)
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        # Check ownership
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this farm"
            )
        
        # Delete farm
        success = farm_service.delete(farm_id)
        
        if success:
            logger.info(f"Farm deleted: {farm_id} by user {current_user.id}")
            return {"message": "Farm deleted successfully", "farm_id": str(farm_id)}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting farm"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting farm {farm_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting farm"
        )


# Plot endpoints
@router.get("/{farm_id}/plots", response_model=List[PlotResponse])
async def get_farm_plots(
    farm_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Get plots for a farm"""
    try:
        # Check farm ownership first
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(farm_id)
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this farm"
            )
        
        # Get plots
        plot_service = PlotService(db)
        plots = plot_service.get_by_farm_id(farm_id, skip=skip, limit=limit)
        
        return [PlotResponse.from_attributes(plot) for plot in plots]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting plots for farm {farm_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving plots"
        )


@router.post("/{farm_id}/plots", response_model=PlotResponse)
async def create_plot(
    farm_id: UUID,
    plot_data: PlotCreate,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Create new plot in farm"""
    try:
        # Check farm ownership
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(farm_id)
        
        if not farm:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Farm not found"
            )
        
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this farm"
            )
        
        # Create plot
        plot_dict = plot_data.dict(exclude_unset=True)
        plot_dict['farm_id'] = farm_id
        
        plot_service = PlotService(db)
        plot = plot_service.create(plot_dict)
        
        logger.info(f"Plot created: {plot.id} in farm {farm_id}")
        return PlotResponse.from_attributes(plot)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating plot in farm {farm_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating plot"
        )


@router.get("/plots/{plot_id}", response_model=PlotResponse)
async def get_plot(
    plot_id: UUID,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Get specific plot"""
    try:
        plot_service = PlotService(db)
        plot = plot_service.get_by_id(plot_id)
        
        if not plot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plot not found"
            )
        
        # Check ownership via farm
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(plot.farm_id)
        
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or not farm or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this plot"
            )
        
        return PlotResponse.from_attributes(plot)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting plot {plot_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving plot"
        )


@router.put("/plots/{plot_id}", response_model=PlotResponse)
async def update_plot(
    plot_id: UUID,
    plot_data: PlotUpdate,
    current_user: User = Depends(get_farmer_user),
    db: Session = Depends(get_db)
):
    """Update plot"""
    try:
        plot_service = PlotService(db)
        plot = plot_service.get_by_id(plot_id)
        
        if not plot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plot not found"
            )
        
        # Check ownership
        farm_service = FarmService(db)
        farm = farm_service.get_by_id(plot.farm_id)
        
        farmer_service = FarmerService(db)
        farmer = farmer_service.get_by_user_id(current_user.id)
        
        if not farmer or not farm or farm.farmer_id != farmer.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this plot"
            )
        
        # Update plot
        updated_plot = plot_service.update(plot_id, plot_data.dict(exclude_unset=True))
        
        logger.info(f"Plot updated: {plot_id}")
        return PlotResponse.from_attributes(updated_plot)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating plot {plot_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating plot"
        )