-- AGRO-BOT & AUTOMATION Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Users table (Firebase UID integration)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    firebase_uid VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'farmer' CHECK (role IN ('farmer', 'admin', 'agriculture_officer', 'expert')),
    profile_image_url TEXT,
    language_preference VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Farmers profile table
CREATE TABLE farmers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    farmer_id VARCHAR(50) UNIQUE, -- Government farmer ID
    address TEXT,
    district VARCHAR(100),
    state VARCHAR(100),
    pincode VARCHAR(10),
    total_land_area DECIMAL(10,2), -- in acres
    experience_years INTEGER,
    education_level VARCHAR(50),
    annual_income DECIMAL(12,2),
    bank_account_number VARCHAR(50),
    ifsc_code VARCHAR(20),
    aadhaar_number VARCHAR(12),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Farms table
CREATE TABLE farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    location GEOGRAPHY(POINT, 4326), -- PostGIS for GPS coordinates
    address TEXT,
    total_area DECIMAL(10,2), -- in acres
    soil_type VARCHAR(100),
    irrigation_type VARCHAR(100),
    elevation DECIMAL(8,2), -- in meters
    farm_type VARCHAR(50) CHECK (farm_type IN ('organic', 'conventional', 'hydroponic', 'greenhouse')),
    ownership_type VARCHAR(50) CHECK (ownership_type IN ('owned', 'leased', 'sharecrop')),
    registration_number VARCHAR(100),
    images JSONB, -- Array of image URLs
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Farm plots/sections
CREATE TABLE plots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    area DECIMAL(8,2), -- in acres
    soil_ph DECIMAL(3,1),
    soil_ec DECIMAL(5,2), -- Electrical conductivity
    organic_matter DECIMAL(5,2), -- percentage
    nitrogen_level DECIMAL(5,2),
    phosphorus_level DECIMAL(5,2),
    potassium_level DECIMAL(5,2),
    last_soil_test DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crops master data
CREATE TABLE crop_varieties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    scientific_name VARCHAR(200),
    category VARCHAR(100), -- cereals, vegetables, fruits, etc.
    variety VARCHAR(200),
    season VARCHAR(50) CHECK (season IN ('kharif', 'rabi', 'summer', 'year_round')),
    growth_duration_days INTEGER, -- Average days from planting to harvest
    water_requirement VARCHAR(50), -- low, medium, high
    soil_type_preference TEXT,
    temperature_range VARCHAR(50),
    spacing_cm INTEGER,
    seed_rate_per_acre DECIMAL(8,2),
    expected_yield_per_acre DECIMAL(8,2),
    market_price_per_kg DECIMAL(8,2),
    image_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Current crops in farms
CREATE TABLE crops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plot_id UUID REFERENCES plots(id) ON DELETE CASCADE,
    crop_variety_id UUID REFERENCES crop_varieties(id),
    planting_date DATE NOT NULL,
    expected_harvest_date DATE,
    actual_harvest_date DATE,
    area_planted DECIMAL(8,2), -- in acres
    seed_quantity DECIMAL(8,2),
    seed_cost DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'growing' CHECK (status IN ('planning', 'planted', 'growing', 'flowering', 'harvested', 'failed')),
    growth_stage VARCHAR(100),
    expected_yield DECIMAL(8,2),
    actual_yield DECIMAL(8,2),
    notes TEXT,
    images JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- IoT Devices
CREATE TABLE devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID REFERENCES farms(id) ON DELETE CASCADE,
    device_id VARCHAR(100) UNIQUE NOT NULL, -- Physical device identifier
    name VARCHAR(200),
    device_type VARCHAR(50) CHECK (device_type IN ('sensor_node', 'weather_station', 'irrigation_controller', 'camera', 'gateway')),
    model VARCHAR(100),
    manufacturer VARCHAR(100),
    location GEOGRAPHY(POINT, 4326),
    installation_date DATE,
    last_maintenance DATE,
    battery_level INTEGER, -- 0-100%
    signal_strength INTEGER, -- RSSI or similar
    firmware_version VARCHAR(50),
    configuration JSONB,
    is_active BOOLEAN DEFAULT true,
    status VARCHAR(50) DEFAULT 'online' CHECK (status IN ('online', 'offline', 'maintenance', 'error')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Sensor data readings
CREATE TABLE sensor_readings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    device_id UUID REFERENCES devices(id) ON DELETE CASCADE,
    sensor_type VARCHAR(100) NOT NULL, -- temperature, humidity, soil_moisture, ph, etc.
    value DECIMAL(10,4) NOT NULL,
    unit VARCHAR(20),
    quality_score INTEGER, -- Data quality 0-100
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create index for time-series queries
CREATE INDEX idx_sensor_readings_device_time ON sensor_readings(device_id, timestamp DESC);
CREATE INDEX idx_sensor_readings_type_time ON sensor_readings(sensor_type, timestamp DESC);

-- Weather data
CREATE TABLE weather_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    temperature DECIMAL(5,2), -- Celsius
    humidity DECIMAL(5,2), -- percentage
    pressure DECIMAL(7,2), -- hPa
    wind_speed DECIMAL(5,2), -- km/h
    wind_direction INTEGER, -- degrees
    rainfall DECIMAL(6,2), -- mm
    solar_radiation DECIMAL(8,2), -- W/m²
    uv_index DECIMAL(3,1),
    visibility DECIMAL(5,2), -- km
    weather_condition VARCHAR(100),
    source VARCHAR(50) DEFAULT 'api', -- api, local_sensor
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_weather_location_time ON weather_data USING GIST(location, timestamp);

-- Weather forecasts
CREATE TABLE weather_forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location GEOGRAPHY(POINT, 4326) NOT NULL,
    forecast_date DATE NOT NULL,
    min_temperature DECIMAL(5,2),
    max_temperature DECIMAL(5,2),
    humidity DECIMAL(5,2),
    wind_speed DECIMAL(5,2),
    rainfall_probability DECIMAL(5,2), -- percentage
    expected_rainfall DECIMAL(6,2), -- mm
    weather_condition VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Disease detection results
CREATE TABLE disease_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    image_url TEXT NOT NULL,
    detected_disease VARCHAR(200),
    confidence_score DECIMAL(5,4), -- 0-1
    severity VARCHAR(50) CHECK (severity IN ('mild', 'moderate', 'severe')),
    affected_area_percentage DECIMAL(5,2),
    symptoms TEXT,
    causes TEXT,
    treatment_recommendations TEXT,
    organic_treatments TEXT,
    chemical_treatments TEXT,
    prevention_tips TEXT,
    detection_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ai_model_version VARCHAR(50),
    is_verified BOOLEAN DEFAULT false,
    verified_by UUID REFERENCES users(id),
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Pest detection results
CREATE TABLE pest_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    image_url TEXT NOT NULL,
    detected_pest VARCHAR(200),
    confidence_score DECIMAL(5,4),
    severity VARCHAR(50) CHECK (severity IN ('low', 'medium', 'high')),
    pest_count INTEGER,
    life_stage VARCHAR(50), -- egg, larva, adult, etc.
    damage_description TEXT,
    treatment_recommendations TEXT,
    organic_treatments TEXT,
    chemical_treatments TEXT,
    prevention_measures TEXT,
    detection_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ai_model_version VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Irrigation schedules and logs
CREATE TABLE irrigation_schedules (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    plot_id UUID REFERENCES plots(id) ON DELETE CASCADE,
    crop_id UUID REFERENCES crops(id),
    schedule_name VARCHAR(200),
    irrigation_method VARCHAR(100), -- drip, sprinkler, flood, furrow
    frequency_days INTEGER, -- Every X days
    duration_minutes INTEGER,
    water_amount_liters DECIMAL(10,2),
    start_date DATE,
    end_date DATE,
    time_of_day TIME,
    is_active BOOLEAN DEFAULT true,
    auto_adjustment BOOLEAN DEFAULT true, -- AI-based adjustment
    weather_dependent BOOLEAN DEFAULT true,
    soil_moisture_threshold DECIMAL(5,2), -- trigger threshold
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Irrigation execution logs
CREATE TABLE irrigation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    schedule_id UUID REFERENCES irrigation_schedules(id),
    plot_id UUID REFERENCES plots(id) ON DELETE CASCADE,
    device_id UUID REFERENCES devices(id),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    planned_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    water_used_liters DECIMAL(10,2),
    trigger_reason VARCHAR(100), -- scheduled, manual, soil_moisture, weather
    soil_moisture_before DECIMAL(5,2),
    soil_moisture_after DECIMAL(5,2),
    status VARCHAR(50) CHECK (status IN ('completed', 'interrupted', 'failed', 'in_progress')),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fertilizer recommendations and applications
CREATE TABLE fertilizer_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    recommended_by VARCHAR(50) DEFAULT 'ai', -- ai, expert, farmer
    fertilizer_type VARCHAR(100), -- NPK, urea, compost, etc.
    npk_ratio VARCHAR(20), -- e.g., "10-26-26"
    quantity_per_acre DECIMAL(8,2), -- kg per acre
    application_method VARCHAR(100), -- broadcast, band, foliar
    application_timing VARCHAR(200), -- growth stage or days after planting
    frequency INTEGER, -- times per season
    cost_per_kg DECIMAL(8,2),
    total_cost DECIMAL(10,2),
    benefits TEXT,
    application_instructions TEXT,
    precautions TEXT,
    is_organic BOOLEAN DEFAULT false,
    recommendation_date DATE,
    valid_until DATE,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'applied', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fertilizer application logs
CREATE TABLE fertilizer_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recommendation_id UUID REFERENCES fertilizer_recommendations(id),
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    applied_by UUID REFERENCES users(id),
    fertilizer_name VARCHAR(200),
    quantity_applied DECIMAL(8,2),
    application_method VARCHAR(100),
    application_date DATE,
    weather_conditions TEXT,
    soil_conditions TEXT,
    cost DECIMAL(10,2),
    notes TEXT,
    images JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Yield predictions
CREATE TABLE yield_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_id UUID REFERENCES crops(id) ON DELETE CASCADE,
    prediction_date DATE,
    predicted_yield DECIMAL(8,2), -- kg per acre
    confidence_interval_lower DECIMAL(8,2),
    confidence_interval_upper DECIMAL(8,2),
    prediction_accuracy DECIMAL(5,4), -- 0-1
    factors_considered JSONB, -- weather, soil, crop stage, etc.
    ai_model_version VARCHAR(50),
    market_price_prediction DECIMAL(8,2),
    revenue_prediction DECIMAL(12,2),
    harvest_window_start DATE,
    harvest_window_end DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Marketplace categories
CREATE TABLE marketplace_categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    parent_category_id UUID REFERENCES marketplace_categories(id),
    description TEXT,
    image_url TEXT,
    is_active BOOLEAN DEFAULT true,
    sort_order INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Marketplace products
CREATE TABLE marketplace_products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    seller_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    category_id UUID REFERENCES marketplace_categories(id),
    name VARCHAR(300) NOT NULL,
    description TEXT,
    product_type VARCHAR(50) CHECK (product_type IN ('produce', 'seeds', 'fertilizer', 'equipment', 'services')),
    variety VARCHAR(200),
    quantity DECIMAL(10,2),
    unit VARCHAR(20), -- kg, tons, pieces, etc.
    price_per_unit DECIMAL(10,2),
    min_order_quantity DECIMAL(8,2),
    harvest_date DATE,
    expiry_date DATE,
    quality_grade VARCHAR(50),
    organic_certified BOOLEAN DEFAULT false,
    certification_details TEXT,
    location GEOGRAPHY(POINT, 4326),
    pickup_available BOOLEAN DEFAULT true,
    delivery_available BOOLEAN DEFAULT false,
    delivery_radius_km INTEGER,
    images JSONB,
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'sold', 'expired', 'inactive')),
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Marketplace orders
CREATE TABLE marketplace_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    buyer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    seller_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    product_id UUID REFERENCES marketplace_products(id),
    quantity DECIMAL(10,2),
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(12,2),
    delivery_address TEXT,
    delivery_type VARCHAR(50) CHECK (delivery_type IN ('pickup', 'delivery')),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    order_status VARCHAR(50) DEFAULT 'placed' CHECK (order_status IN ('placed', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled')),
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    notes TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Government schemes
CREATE TABLE government_schemes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scheme_name VARCHAR(300) NOT NULL,
    scheme_type VARCHAR(100) CHECK (scheme_type IN ('subsidy', 'loan', 'insurance', 'grant', 'training')),
    description TEXT,
    benefits TEXT,
    eligibility_criteria TEXT,
    required_documents TEXT,
    application_process TEXT,
    application_deadline DATE,
    scheme_amount DECIMAL(12,2),
    percentage_subsidy DECIMAL(5,2),
    implementing_agency VARCHAR(200),
    contact_details TEXT,
    website_url TEXT,
    state VARCHAR(100),
    district VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    launch_date DATE,
    end_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Scheme applications by farmers
CREATE TABLE scheme_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id UUID REFERENCES farmers(id) ON DELETE CASCADE,
    scheme_id UUID REFERENCES government_schemes(id),
    application_number VARCHAR(100) UNIQUE,
    application_date DATE,
    status VARCHAR(50) DEFAULT 'submitted' CHECK (status IN ('draft', 'submitted', 'under_review', 'approved', 'rejected', 'disbursed')),
    applied_amount DECIMAL(12,2),
    approved_amount DECIMAL(12,2),
    disbursed_amount DECIMAL(12,2),
    rejection_reason TEXT,
    documents_submitted JSONB,
    officer_remarks TEXT,
    disbursement_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- AI Chat conversations
CREATE TABLE chat_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    conversation_title VARCHAR(300),
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES chat_conversations(id) ON DELETE CASCADE,
    message_type VARCHAR(20) CHECK (message_type IN ('user', 'assistant')),
    message_text TEXT NOT NULL,
    message_audio_url TEXT, -- for voice messages
    attachments JSONB, -- images, documents
    context_data JSONB, -- farm, crop context for AI
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(300) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(100) CHECK (
        notification_type IN (
            'weather_alert', 'irrigation_reminder', 'disease_detected', 
            'pest_detected', 'harvest_reminder', 'fertilizer_reminder',
            'scheme_update', 'market_price', 'order_update', 'system'
        )
    ),
    priority VARCHAR(20) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    data JSONB, -- Additional notification data
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP WITH TIME ZONE,
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    action_url TEXT, -- Deep link or web URL
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- System alerts and warnings
CREATE TABLE system_alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) CHECK (severity IN ('info', 'warning', 'error', 'critical')),
    title VARCHAR(300) NOT NULL,
    description TEXT,
    affected_area GEOGRAPHY(POLYGON, 4326), -- Geographic area
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    source VARCHAR(100), -- weather_service, iot_sensor, manual
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Analytics and reports
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL, -- login, crop_added, disease_scan, etc.
    event_data JSONB,
    session_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL, -- CREATE, UPDATE, DELETE, LOGIN, etc.
    table_name VARCHAR(100),
    record_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- API usage tracking
CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    endpoint VARCHAR(200),
    method VARCHAR(10),
    status_code INTEGER,
    response_time_ms INTEGER,
    request_size_bytes INTEGER,
    response_size_bytes INTEGER,
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_users_firebase_uid ON users(firebase_uid);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_farmers_user_id ON farmers(user_id);
CREATE INDEX idx_farms_farmer_id ON farms(farmer_id);
CREATE INDEX idx_farms_location ON farms USING GIST(location);
CREATE INDEX idx_crops_plot_id ON crops(plot_id);
CREATE INDEX idx_crops_status ON crops(status);
CREATE INDEX idx_devices_farm_id ON devices(farm_id);
CREATE INDEX idx_devices_status ON devices(status);
CREATE INDEX idx_marketplace_products_seller_id ON marketplace_products(seller_id);
CREATE INDEX idx_marketplace_products_category ON marketplace_products(category_id);
CREATE INDEX idx_marketplace_products_status ON marketplace_products(status);
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id) WHERE is_read = false;

-- Create triggers for updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_farmers_updated_at BEFORE UPDATE ON farmers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_farms_updated_at BEFORE UPDATE ON farms FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_plots_updated_at BEFORE UPDATE ON plots FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_crops_updated_at BEFORE UPDATE ON crops FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_devices_updated_at BEFORE UPDATE ON devices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();