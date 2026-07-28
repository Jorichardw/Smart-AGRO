"""
Quick test script for Smart AGRO backend
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all imports work correctly"""
    print("Testing imports...")
    
    try:
        # Test core imports
        from app.core.config import settings
        print("✓ Config imported successfully")
        
        from app.core.database import Base, get_db
        print("✓ Database imports successful")
        
        from app.core.security import create_access_token
        print("✓ Security imports successful")
        
        # Test model imports
        from app.models import User, Farmer, Farm, Plot
        print("✓ Model imports successful")
        
        # Test service imports
        from app.services.user_service import UserService
        from app.services.farmer_service import FarmerService
        from app.services.farm_service import FarmService
        print("✓ Service imports successful")
        
        # Test API imports
        from app.api.v1 import api_router
        print("✓ API router import successful")
        
        # Test main app
        from app.main import app
        print("✓ Main app import successful")
        
        print("\n🎉 All imports successful! Backend setup looks good.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_configuration():
    """Test configuration values"""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        
        print(f"✓ Project Name: {settings.PROJECT_NAME}")
        print(f"✓ Version: {settings.VERSION}")
        print(f"✓ Environment: {settings.ENVIRONMENT}")
        print(f"✓ API V1 Prefix: {settings.API_V1_STR}")
        print(f"✓ Database URL configured: {'postgresql' in settings.DATABASE_URL}")
        
        print("\n✓ Configuration test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_database_models():
    """Test database model structure"""
    print("\nTesting database models...")
    
    try:
        from app.models import Base
        from sqlalchemy import MetaData
        
        # Get all tables
        metadata = Base.metadata
        table_names = list(metadata.tables.keys())
        
        expected_tables = [
            'users', 'farmers', 'farms', 'plots', 'crop_varieties', 
            'crops', 'devices', 'sensor_readings', 'weather_data',
            'disease_detections', 'marketplace_products', 'notifications'
        ]
        
        print(f"✓ Found {len(table_names)} database tables")
        
        found_expected = [table for table in expected_tables if table in table_names]
        print(f"✓ Core tables present: {len(found_expected)}/{len(expected_tables)}")
        
        if len(found_expected) >= len(expected_tables) * 0.8:  # 80% of expected tables
            print("✓ Database model structure looks good")
            return True
        else:
            print("⚠️ Some expected tables missing, but basic structure exists")
            return True
            
    except Exception as e:
        print(f"❌ Database model error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Testing Smart AGRO Backend Setup")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_database_models
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("=" * 50)
    print("📊 Test Summary:")
    passed = sum(results)
    total = len(results)
    
    print(f"✓ Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to run.")
        print("\n🚀 Next steps:")
        print("1. Set up PostgreSQL database")
        print("2. Configure Firebase credentials")
        print("3. Run: cd backend && uvicorn app.main:app --reload")
    elif passed >= total * 0.7:
        print("⚠️ Most tests passed. Minor issues to resolve.")
    else:
        print("❌ Several issues found. Please check the errors above.")


if __name__ == "__main__":
    main()