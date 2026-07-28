-- Create required PostgreSQL extensions for AGRO-BOT & AUTOMATION

-- UUID extension for generating UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- PostGIS extension for geographic data
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Additional extensions for full-text search
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Extension for case-insensitive text operations
CREATE EXTENSION IF NOT EXISTS "citext";

-- Extension for additional aggregate functions
CREATE EXTENSION IF NOT EXISTS "tablefunc";

-- Extension for cryptographic functions
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Log the successful creation of extensions
DO $$
BEGIN
    RAISE NOTICE 'All required PostgreSQL extensions have been created successfully for AGRO-BOT & AUTOMATION database.';
END
$$;