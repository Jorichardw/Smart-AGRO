"""
Logging utilities for AGRO-BOT & AUTOMATION
"""

import logging
import logging.handlers
import os
from datetime import datetime
from typing import Optional

from app.core.config import settings


def setup_logger(
    logger_name: Optional[str] = None,
    log_level: Optional[str] = None
) -> logging.Logger:
    """
    Setup application logger with file and console handlers
    
    Args:
        logger_name: Name of the logger
        log_level: Logging level
        
    Returns:
        logging.Logger: Configured logger
    """
    # Create logger
    if logger_name is None:
        logger_name = "agro_bot"
    
    logger = logging.getLogger(logger_name)
    
    # Set log level
    if log_level is None:
        log_level = settings.LOG_LEVEL
    
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    simple_formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    try:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(settings.LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Rotating file handler
        file_handler = logging.handlers.RotatingFileHandler(
            settings.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
    except Exception as e:
        logger.warning(f"Could not setup file logging: {e}")
    
    # Error file handler for errors only
    try:
        error_log_file = settings.LOG_FILE.replace('.log', '_errors.log')
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        logger.addHandler(error_handler)
        
    except Exception as e:
        logger.warning(f"Could not setup error file logging: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger instance
    
    Args:
        name: Logger name
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


class APILogger:
    """
    Specialized logger for API requests and responses
    """
    
    def __init__(self):
        self.logger = get_logger("agro_bot.api")
    
    def log_request(self, method: str, url: str, user_id: Optional[str] = None, **kwargs):
        """Log API request"""
        extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.info(f"Request: {method} {url} | User: {user_id} | {extra_info}")
    
    def log_response(self, status_code: int, response_time: float, **kwargs):
        """Log API response"""
        extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.info(f"Response: {status_code} | Time: {response_time:.4f}s | {extra_info}")
    
    def log_error(self, error: Exception, context: str = "", **kwargs):
        """Log API error"""
        extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.error(f"Error: {context} | {str(error)} | {extra_info}", exc_info=True)


class SecurityLogger:
    """
    Specialized logger for security events
    """
    
    def __init__(self):
        self.logger = get_logger("agro_bot.security")
    
    def log_login_attempt(self, email: str, success: bool, ip_address: str = ""):
        """Log login attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Login {status}: {email} | IP: {ip_address}")
    
    def log_auth_failure(self, reason: str, ip_address: str = "", **kwargs):
        """Log authentication failure"""
        extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        self.logger.warning(f"Auth Failure: {reason} | IP: {ip_address} | {extra_info}")
    
    def log_permission_denied(self, user_id: str, action: str, resource: str = ""):
        """Log permission denied event"""
        self.logger.warning(f"Permission Denied: User {user_id} | Action: {action} | Resource: {resource}")


class BusinessLogger:
    """
    Specialized logger for business logic events
    """
    
    def __init__(self):
        self.logger = get_logger("agro_bot.business")
    
    def log_disease_detection(self, user_id: str, crop_id: str, disease: str, confidence: float):
        """Log disease detection event"""
        self.logger.info(f"Disease Detection: User {user_id} | Crop {crop_id} | Disease: {disease} | Confidence: {confidence}")
    
    def log_irrigation_event(self, plot_id: str, duration: int, trigger: str):
        """Log irrigation event"""
        self.logger.info(f"Irrigation: Plot {plot_id} | Duration: {duration}min | Trigger: {trigger}")
    
    def log_marketplace_order(self, buyer_id: str, seller_id: str, product_id: str, amount: float):
        """Log marketplace order"""
        self.logger.info(f"Marketplace Order: Buyer {buyer_id} | Seller {seller_id} | Product {product_id} | Amount: {amount}")


# Global logger instances
api_logger = APILogger()
security_logger = SecurityLogger()
business_logger = BusinessLogger()