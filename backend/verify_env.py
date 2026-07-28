#!/usr/bin/env python3
"""
Environment Configuration Verification Script
Checks if all required environment variables are properly configured
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    print("❌ ERROR: .env file not found!")
    print(f"   Expected at: {env_path}")
    exit(1)

load_dotenv(env_path)

# Color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

print(f"\n{BOLD}🔍 Environment Configuration Verification{RESET}\n")
print("=" * 60)

# Check categories
checks = {
    "✅ CRITICAL - Must Have": {
        "DATABASE_URL": {
            "required": True,
            "description": "PostgreSQL connection string"
        },
        "SECRET_KEY": {
            "required": True,
            "description": "API security key"
        },
    },
    "⚡ IMPORTANT - Recommended": {
        "WEATHER_API_KEY": {
            "required": False,
            "description": "OpenWeatherMap API (for weather features)"
        },
        "REDIS_URL": {
            "required": False,
            "description": "Redis cache URL (for background tasks)"
        },
    },
    "📦 OPTIONAL - Set Later": {
        "FIREBASE_PROJECT_ID": {
            "required": False,
            "description": "Firebase project ID (for authentication)"
        },
        "TWILIO_ACCOUNT_SID": {
            "required": False,
            "description": "Twilio SMS service"
        },
        "STRIPE_SECRET_KEY": {
            "required": False,
            "description": "Stripe payment service"
        },
        "AWS_ACCESS_KEY_ID": {
            "required": False,
            "description": "AWS S3 file storage"
        },
    }
}

total_checks = 0
passed_checks = 0
failed_checks = 0
missing_important = []

for category, variables in checks.items():
    print(f"\n{category}")
    print("-" * 60)
    
    for var_name, var_info in variables.items():
        total_checks += 1
        value = os.getenv(var_name, "")
        is_required = var_info["required"]
        description = var_info["description"]
        
        # Check if variable is set
        if value and value != "" and "your-" not in value.lower():
            status = f"{GREEN}✓ SET{RESET}"
            passed_checks += 1
            # Show masked value for security
            if len(value) > 30:
                display_value = value[:20] + "..." + value[-7:]
            else:
                display_value = value
            print(f"{status} {var_name}")
            print(f"     └─ {description}")
            print(f"     └─ Value: {display_value}\n")
        else:
            if is_required or value == "":
                status = f"{RED}✗ NOT SET{RESET}"
                failed_checks += 1
                if "IMPORTANT" in category or "CRITICAL" in category:
                    missing_important.append(var_name)
            else:
                status = f"{YELLOW}○ OPTIONAL{RESET}"
            print(f"{status} {var_name}")
            print(f"     └─ {description}\n")

# Summary
print("=" * 60)
print(f"\n{BOLD}📊 Summary{RESET}")
print(f"Total Checks: {total_checks}")
print(f"{GREEN}Passed: {passed_checks}{RESET}")
print(f"{RED}Failed/Missing: {failed_checks}{RESET}")

# Details based on results
print(f"\n{BOLD}Status:{RESET}")

if missing_important:
    print(f"\n{RED}⚠️  IMPORTANT - These variables are missing:{RESET}")
    for var in missing_important:
        print(f"   • {var}")
    print(f"\n📖 See ENV_SETUP_GUIDE.md for instructions on how to set these up.")
else:
    print(f"\n{GREEN}✅ All critical variables are configured!{RESET}")

# Database connection check
print(f"\n{BOLD}🗄️  Database Connection Test{RESET}")
print("-" * 60)
try:
    db_url = os.getenv("DATABASE_URL", "")
    if db_url and db_url != "":
        # Parse connection string
        if "postgresql://" in db_url:
            parts = db_url.replace("postgresql://", "").split("@")
            if len(parts) == 2:
                creds = parts[0].split(":")
                host_port = parts[1].split("/")
                
                user = creds[0] if len(creds) > 0 else "unknown"
                db_name = host_port[1] if len(host_port) > 1 else "unknown"
                host = host_port[0].split(":")[0]
                
                print(f"{GREEN}✓ Connection string parsed successfully{RESET}")
                print(f"  Host: {host}")
                print(f"  User: {user}")
                print(f"  Database: {db_name}")
                
                # Try to connect (requires psycopg2)
                try:
                    import psycopg2
                    try:
                        conn = psycopg2.connect(db_url)
                        print(f"{GREEN}✓ Database connection successful!{RESET}")
                        conn.close()
                    except Exception as e:
                        print(f"{YELLOW}⚠️  Could not connect to database{RESET}")
                        print(f"   Error: {str(e)}")
                        print(f"   Make sure PostgreSQL is running on {host}")
                except ImportError:
                    print(f"{YELLOW}⚠️  psycopg2 not installed (run: pip install psycopg2-binary){RESET}")
            else:
                print(f"{YELLOW}⚠️  Could not parse DATABASE_URL{RESET}")
        else:
            print(f"{RED}✗ Invalid database URL format{RESET}")
    else:
        print(f"{RED}✗ DATABASE_URL not set{RESET}")
except Exception as e:
    print(f"{RED}✗ Error during database check: {e}{RESET}")

# Secret key validation
print(f"\n{BOLD}🔐 Secret Key Validation{RESET}")
print("-" * 60)
secret_key = os.getenv("SECRET_KEY", "")
if secret_key:
    if len(secret_key) >= 32:
        print(f"{GREEN}✓ SECRET_KEY is strong{RESET}")
        print(f"  Length: {len(secret_key)} characters")
    else:
        print(f"{YELLOW}⚠️  SECRET_KEY is too short{RESET}")
        print(f"  Current: {len(secret_key)} characters")
        print(f"  Recommended: 32+ characters")
else:
    print(f"{RED}✗ SECRET_KEY not set{RESET}")

# Final recommendation
print(f"\n{BOLD}📝 Next Steps:{RESET}")
if missing_important:
    print(f"1. Open ENV_SETUP_GUIDE.md for detailed setup instructions")
    print(f"2. Configure missing variables in .env file")
    print(f"3. Run this script again to verify")
else:
    print(f"✅ Your environment is configured!")
    print(f"1. Start the backend: uvicorn app.main:app --reload")
    print(f"2. Start the frontend: npm run dev")
    print(f"3. Visit http://localhost:3000")

print("\n" + "=" * 60 + "\n")
