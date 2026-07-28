# 🚀 AGRO-BOT & AUTOMATION - Production Deployment Guide

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Server Setup](#server-setup)
- [SSL/TLS Configuration](#ssltls-configuration)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Deployment Steps](#deployment-steps)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Backup & Recovery](#backup--recovery)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Minimum Server Requirements
```
Production Environment:
- CPU: 8 cores (16 recommended)
- RAM: 16 GB (32 GB recommended)
- Storage: 200 GB SSD (500 GB recommended)
- OS: Ubuntu 22.04 LTS or CentOS 8+
- Network: 1 Gbps

Staging Environment:
- CPU: 4 cores
- RAM: 8 GB
- Storage: 100 GB SSD
```

### Required Software
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install additional tools
sudo apt install -y git nginx certbot python3-certbot-nginx ufw fail2ban

# Verify installations
docker --version
docker-compose --version
git --version
```

---

## 🖥️ Server Setup

### 1. Create Deployment User
```bash
# Create deployment user
sudo useradd -m -s /bin/bash deploy
sudo usermod -aG docker deploy
sudo mkdir -p /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh

# Add SSH key
echo "your-public-ssh-key" | sudo tee /home/deploy/.ssh/authorized_keys
sudo chmod 600 /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
```

### 2. Configure Firewall
```bash
# Enable UFW
sudo ufw --force enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow PostgreSQL (internal only)
sudo ufw allow from 172.20.0.0/16 to any port 5432

# Check status
sudo ufw status
```

### 3. Configure Fail2Ban
```bash
# Install and configure
sudo apt install fail2ban -y

# Create jail configuration
sudo tee /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = 22

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
EOF

# Restart fail2ban
sudo systemctl restart fail2ban
sudo systemctl enable fail2ban
```

---

## 🔒 SSL/TLS Configuration

### Option 1: Let's Encrypt (Recommended for Production)
```bash
# Stop nginx if running
sudo systemctl stop nginx

# Obtain SSL certificate
sudo certbot certonly --standalone \
    -d yourdomain.com \
    -d www.yourdomain.com \
    -d api.yourdomain.com \
    --email your-email@domain.com \
    --agree-tos \
    --no-eff-email

# Copy certificates to nginx directory
sudo mkdir -p /opt/agro-bot/nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/agro-bot/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/agro-bot/nginx/ssl/key.pem

# Set up auto-renewal
sudo crontab -e
# Add line: 0 0 * * * certbot renew --quiet --deploy-hook "docker restart agro_nginx_prod"
```

### Option 2: Self-Signed Certificate (Development/Staging)
```bash
# Generate self-signed certificate
sudo mkdir -p /opt/agro-bot/nginx/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /opt/agro-bot/nginx/ssl/key.pem \
    -out /opt/agro-bot/nginx/ssl/cert.pem \
    -subj "/C=IN/ST=State/L=City/O=Organization/CN=yourdomain.com"
```

---

## ⚙️ Environment Configuration

### 1. Clone Repository
```bash
# Create application directory
sudo mkdir -p /opt/agro-bot
sudo chown deploy:deploy /opt/agro-bot

# Clone repository
cd /opt/agro-bot
git clone https://github.com/your-org/agro-bot-automation.git .
```

### 2. Configure Backend Environment
```bash
# Copy production environment file
cd /opt/agro-bot/backend
cp .env.production .env

# Edit environment variables
nano .env

# Required changes:
# - SECRET_KEY: Generate with `openssl rand -hex 32`
# - DATABASE_URL: Update with production database credentials
# - REDIS_PASSWORD: Set strong password
# - FIREBASE_* : Add Firebase credentials
# - WEATHER_API_KEY: Add OpenWeatherMap API key
# - All other API keys and passwords
```

### 3. Configure Frontend Environment
```bash
# Copy production environment file
cd /opt/agro-bot/frontend
cp .env.production .env

# Edit environment variables
nano .env

# Required changes:
# - NEXT_PUBLIC_API_URL: https://api.yourdomain.com
# - NEXT_PUBLIC_FIREBASE_*: Add Firebase configuration
# - Update all domain references
```

### 4. Configure Nginx
```bash
# Update nginx configuration with your domain
cd /opt/agro-bot/nginx
nano nginx.conf

# Replace all instances of 'yourdomain.com' with your actual domain
```

---

## 🗄️ Database Setup

### 1. Initialize Database
```bash
# Start PostgreSQL container
docker-compose -f docker-compose.prod.yml up -d postgres

# Wait for database to be ready
sleep 10

# Create database extensions
docker exec -i agro_postgres_prod psql -U agro_user -d agro_bot_db << EOF
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
EOF
```

### 2. Run Initial Schema
```bash
# Apply database schema
docker exec -i agro_postgres_prod psql -U agro_user -d agro_bot_db < database/schema.sql

# Run seed data
docker exec -i agro_postgres_prod psql -U agro_user -d agro_bot_db < database/init/02-seed-data.sql
```

### 3. Create Database Backup Strategy
```bash
# Create backup script
sudo tee /opt/agro-bot/scripts/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/agro-bot-backups/database"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
mkdir -p "$BACKUP_DIR"

docker exec agro_postgres_prod pg_dump -U agro_user agro_bot_db | \
    gzip > "$BACKUP_DIR/db-backup-$TIMESTAMP.sql.gz"

# Keep only last 30 days
find "$BACKUP_DIR" -name "db-backup-*.sql.gz" -mtime +30 -delete
EOF

sudo chmod +x /opt/agro-bot/scripts/backup-db.sh

# Schedule daily backups
sudo crontab -e
# Add line: 0 2 * * * /opt/agro-bot/scripts/backup-db.sh
```

---

## 🚀 Deployment Steps

### Initial Deployment

```bash
# 1. Navigate to deployment directory
cd /opt/agro-bot

# 2. Build and start services
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# 3. Check service status
docker-compose -f docker-compose.prod.yml ps

# 4. View logs
docker-compose -f docker-compose.prod.yml logs -f

# 5. Verify health
curl https://api.yourdomain.com/health
curl https://yourdomain.com/
```

### Using Deployment Script

```bash
# Make script executable
chmod +x deployment/deploy.sh

# Run deployment
sudo ./deployment/deploy.sh
```

### Zero-Downtime Deployment

```bash
# 1. Build new images
docker-compose -f docker-compose.prod.yml build

# 2. Scale up with new version
docker-compose -f docker-compose.prod.yml up -d --scale backend=4 --no-recreate

# 3. Wait for health checks
sleep 30

# 4. Scale down old containers
docker-compose -f docker-compose.prod.yml up -d --scale backend=2

# 5. Remove old containers
docker-compose -f docker-compose.prod.yml up -d --remove-orphans
```

---

## 📊 Monitoring & Maintenance

### 1. Setup Monitoring Stack

```bash
# Add monitoring to docker-compose
cat >> docker-compose.prod.yml << 'EOF'
  prometheus:
    image: prom/prometheus:latest
    container_name: agro_prometheus
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - agro_network

  grafana:
    image: grafana/grafana:latest
    container_name: agro_grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - agro_network
EOF
```

### 2. Log Management

```bash
# Configure log rotation
sudo tee /etc/logrotate.d/agro-bot << EOF
/opt/agro-bot/backend/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 deploy deploy
    sharedscripts
    postrotate
        docker kill -s USR1 agro_backend_prod
    endscript
}
EOF
```

### 3. Health Check Monitoring

```bash
# Create health check script
cat > /opt/agro-bot/scripts/health-check.sh << 'EOF'
#!/bin/bash
SERVICES=("https://api.yourdomain.com/health" "https://yourdomain.com/")

for service in "${SERVICES[@]}"; do
    if ! curl -f "$service" > /dev/null 2>&1; then
        echo "Service $service is down!"
        # Send alert (email, Slack, etc.)
    fi
done
EOF

chmod +x /opt/agro-bot/scripts/health-check.sh

# Run every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /opt/agro-bot/scripts/health-check.sh") | crontab -
```

---

## 💾 Backup & Recovery

### Automated Backup Strategy

```bash
# Full system backup script
cat > /opt/agro-bot/scripts/full-backup.sh << 'EOF'
#!/bin/bash
BACKUP_ROOT="/opt/agro-bot-backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Database backup
docker exec agro_postgres_prod pg_dump -U agro_user agro_bot_db | \
    gzip > "$BACKUP_ROOT/database/db-$TIMESTAMP.sql.gz"

# Uploads backup
tar -czf "$BACKUP_ROOT/uploads/uploads-$TIMESTAMP.tar.gz" \
    /opt/agro-bot/backend/uploads

# Configuration backup
tar -czf "$BACKUP_ROOT/config/config-$TIMESTAMP.tar.gz" \
    /opt/agro-bot/backend/.env \
    /opt/agro-bot/frontend/.env \
    /opt/agro-bot/nginx/nginx.conf

# Upload to S3 (optional)
aws s3 sync "$BACKUP_ROOT" s3://your-backup-bucket/agro-bot/

echo "Backup completed: $TIMESTAMP"
EOF

chmod +x /opt/agro-bot/scripts/full-backup.sh
```

### Disaster Recovery

```bash
# Restore from backup
cd /opt/agro-bot

# 1. Stop services
docker-compose -f docker-compose.prod.yml down

# 2. Restore database
gunzip < /opt/agro-bot-backups/database/db-TIMESTAMP.sql.gz | \
    docker exec -i agro_postgres_prod psql -U agro_user agro_bot_db

# 3. Restore uploads
tar -xzf /opt/agro-bot-backups/uploads/uploads-TIMESTAMP.tar.gz -C /

# 4. Restart services
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔍 Troubleshooting

### Common Issues

#### Services Not Starting
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check specific service
docker logs agro_backend_prod

# Restart service
docker-compose -f docker-compose.prod.yml restart backend
```

#### Database Connection Issues
```bash
# Check database is running
docker exec agro_postgres_prod pg_isready -U agro_user

# Check connections
docker exec agro_postgres_prod psql -U agro_user -d agro_bot_db -c \
    "SELECT count(*) FROM pg_stat_activity;"

# Reset connections
docker-compose -f docker-compose.prod.yml restart postgres
```

#### High Memory Usage
```bash
# Check container stats
docker stats

# Restart containers with memory limits
docker-compose -f docker-compose.prod.yml up -d --force-recreate

# Clear Docker cache
docker system prune -af
```

#### SSL Certificate Issues
```bash
# Renew certificate
sudo certbot renew --force-renewal

# Copy new certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/agro-bot/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/agro-bot/nginx/ssl/key.pem

# Restart nginx
docker restart agro_nginx_prod
```

---

## 📞 Support & Maintenance

### Regular Maintenance Tasks

**Daily:**
- Check service health
- Monitor error logs
- Review resource usage

**Weekly:**
- Update security patches
- Review backup integrity
- Check SSL certificate expiry
- Analyze performance metrics

**Monthly:**
- Update dependencies
- Review and optimize database
- Audit security logs
- Test disaster recovery

### Performance Optimization

```bash
# Database optimization
docker exec agro_postgres_prod psql -U agro_user -d agro_bot_db -c "VACUUM ANALYZE;"

# Docker image cleanup
docker image prune -a -f

# Log cleanup
find /opt/agro-bot/backend/logs -name "*.log" -mtime +7 -delete
```

---

## 🎉 Post-Deployment Checklist

- [ ] All services are running and healthy
- [ ] SSL certificates are properly configured
- [ ] Database backups are scheduled
- [ ] Monitoring and alerts are configured
- [ ] Logs are being collected and rotated
- [ ] Firewall rules are in place
- [ ] Domain DNS is properly configured
- [ ] Email delivery is working
- [ ] SMS notifications are working
- [ ] Payment gateway is configured
- [ ] Firebase integration is working
- [ ] Weather API is responding
- [ ] AI services are functional
- [ ] Load testing completed
- [ ] Security audit completed
- [ ] Documentation is updated

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

**Deployment Version:** 1.0.0  
**Last Updated:** 2024  
**Contact:** support@yourdomain.com