#!/bin/bash

# AGRO-BOT & AUTOMATION - Production Deployment Script
# This script automates the deployment process

set -e

echo "🚀 AGRO-BOT & AUTOMATION - Production Deployment"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_DIR="/opt/agro-bot"
BACKUP_DIR="/opt/agro-bot-backups"
COMPOSE_FILE="docker-compose.prod.yml"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    log_error "Please run as root or with sudo"
    exit 1
fi

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup current deployment
backup_deployment() {
    log_info "Creating backup of current deployment..."
    
    if [ -d "$DEPLOY_DIR" ]; then
        tar -czf "$BACKUP_DIR/agro-bot-backup-$TIMESTAMP.tar.gz" -C "$DEPLOY_DIR" .
        log_info "Backup created: $BACKUP_DIR/agro-bot-backup-$TIMESTAMP.tar.gz"
    fi
}

# Backup database
backup_database() {
    log_info "Backing up database..."
    
    docker exec agro_postgres_prod pg_dump -U agro_user agro_bot_db > \
        "$BACKUP_DIR/database-backup-$TIMESTAMP.sql"
    
    log_info "Database backup created"
}

# Pull latest changes
pull_changes() {
    log_info "Pulling latest changes from repository..."
    
    cd "$DEPLOY_DIR"
    git fetch origin
    git pull origin main
    
    log_info "Code updated successfully"
}

# Build and deploy
deploy() {
    log_info "Building and deploying services..."
    
    cd "$DEPLOY_DIR"
    
    # Pull latest images
    docker-compose -f "$COMPOSE_FILE" pull
    
    # Build custom images
    docker-compose -f "$COMPOSE_FILE" build --no-cache
    
    # Stop existing services
    log_info "Stopping existing services..."
    docker-compose -f "$COMPOSE_FILE" down
    
    # Start services
    log_info "Starting services..."
    docker-compose -f "$COMPOSE_FILE" up -d
    
    log_info "Services started successfully"
}

# Run database migrations
run_migrations() {
    log_info "Running database migrations..."
    
    docker exec agro_backend_prod python -c \
        "from app.core.database import create_tables; create_tables()"
    
    log_info "Migrations completed"
}

# Health check
health_check() {
    log_info "Performing health check..."
    
    sleep 30  # Wait for services to start
    
    # Check backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        log_info "✓ Backend is healthy"
    else
        log_error "✗ Backend health check failed"
        return 1
    fi
    
    # Check frontend
    if curl -f http://localhost:3000/ > /dev/null 2>&1; then
        log_info "✓ Frontend is healthy"
    else
        log_error "✗ Frontend health check failed"
        return 1
    fi
    
    # Check database
    if docker exec agro_postgres_prod pg_isready -U agro_user > /dev/null 2>&1; then
        log_info "✓ Database is healthy"
    else
        log_error "✗ Database health check failed"
        return 1
    fi
    
    log_info "All health checks passed ✓"
    return 0
}

# Cleanup old images
cleanup() {
    log_info "Cleaning up old Docker images..."
    
    docker system prune -af --volumes
    
    # Keep only last 5 backups
    cd "$BACKUP_DIR"
    ls -t agro-bot-backup-*.tar.gz | tail -n +6 | xargs -r rm
    ls -t database-backup-*.sql | tail -n +6 | xargs -r rm
    
    log_info "Cleanup completed"
}

# Rollback
rollback() {
    log_error "Deployment failed. Rolling back..."
    
    # Find latest backup
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/agro-bot-backup-*.tar.gz | head -1)
    
    if [ -n "$LATEST_BACKUP" ]; then
        log_info "Restoring from backup: $LATEST_BACKUP"
        
        cd "$DEPLOY_DIR"
        docker-compose -f "$COMPOSE_FILE" down
        
        rm -rf "$DEPLOY_DIR"/*
        tar -xzf "$LATEST_BACKUP" -C "$DEPLOY_DIR"
        
        docker-compose -f "$COMPOSE_FILE" up -d
        
        log_info "Rollback completed"
    else
        log_error "No backup found for rollback"
    fi
}

# Main deployment flow
main() {
    log_info "Starting deployment process..."
    
    # Pre-deployment
    backup_deployment
    backup_database
    
    # Deployment
    if pull_changes && deploy && run_migrations; then
        if health_check; then
            log_info "✓ Deployment successful!"
            cleanup
        else
            log_error "Health check failed"
            rollback
            exit 1
        fi
    else
        log_error "Deployment failed"
        rollback
        exit 1
    fi
    
    # Post-deployment
    log_info "Deployment completed successfully! 🎉"
    log_info "Backup location: $BACKUP_DIR/agro-bot-backup-$TIMESTAMP.tar.gz"
    
    # Display service status
    echo ""
    log_info "Service Status:"
    docker-compose -f "$COMPOSE_FILE" ps
}

# Handle interruptions
trap 'log_error "Deployment interrupted"; rollback; exit 1' INT TERM

# Run main deployment
main "$@"