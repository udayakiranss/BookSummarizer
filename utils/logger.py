import logging
import sys
import json
import inspect
from typing import Optional, Dict, Any
from config.config import settings

class Logger:
    """Centralized logging utility for the application with detailed flow tracking."""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Setup the logger with appropriate configuration."""
        self._logger = logging.getLogger("book_insight")
        self._logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self._logger.handlers.clear()
        
        # Create custom formatter that captures the actual calling file
        class CallingFileFormatter(logging.Formatter):
            def format(self, record):
                # Get the actual calling file from the stack
                frame = inspect.currentframe()
                try:
                    # Walk up the stack to find the calling file (skip logger.py and formatter methods)
                    calling_file = record.filename
                    calling_function = record.funcName
                    calling_line = record.lineno
                    
                    while frame:
                        frame = frame.f_back
                        if frame:
                            filename = frame.f_code.co_filename
                            # Skip logger.py and formatter files
                            if (not filename.endswith('logger.py') and 
                                not filename.endswith('__init__.py') and
                                not 'logging' in filename and
                                not 'formatter' in filename.lower()):
                                # Found the calling file
                                calling_file = filename.split('/')[-1]  # Get just the filename
                                calling_function = frame.f_code.co_name
                                calling_line = frame.f_lineno
                                break
                finally:
                    del frame
                
                # Update the record with actual calling info
                record.filename = calling_file
                record.funcName = calling_function
                record.lineno = calling_line
                
                return super().format(record)
        
        formatter = CallingFileFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)
        
        # File handler for all logs
        try:
            file_handler = logging.FileHandler('logs/app.log')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
        except FileNotFoundError:
            # Create logs directory if it doesn't exist
            import os
            os.makedirs('logs', exist_ok=True)
            file_handler = logging.FileHandler('logs/app.log')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._logger.error(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._logger.debug(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._logger.critical(message, extra=kwargs)
    
    def api_request(self, endpoint: str, method: str, params: Dict[str, Any] = None):
        """Log API request details."""
        self._logger.info(f"🌐 API REQUEST: {method} {endpoint}")
        if params:
            self._logger.info(f"📝 Request params: {json.dumps(params, indent=2)}")
    
    def api_response(self, endpoint: str, status_code: int, response_data: Dict[str, Any] = None):
        """Log API response details."""
        self._logger.info(f"📤 API RESPONSE: {endpoint} -> Status: {status_code}")
        if response_data:
            # Log response summary, not full data to avoid log spam
            if isinstance(response_data, dict):
                summary = {
                    "total_items": response_data.get("total_count", 0),
                    "source": response_data.get("source", "unknown"),
                    "generated_at": response_data.get("generated_at", "unknown")
                }
                self._logger.info(f"📊 Response summary: {json.dumps(summary, indent=2)}")
    
    def openai_request(self, model: str, prompt: str, max_tokens: int, temperature: float, messages: list = None):
        """Log OpenAI API request details with full content."""
        self._logger.info(f"🤖 OPENAI REQUEST: Model={model}, MaxTokens={max_tokens}, Temp={temperature}")
        
        if messages:
            self._logger.info(f"📝 Full Request Messages:")
            for i, message in enumerate(messages):
                role = message.get("role", "unknown")
                content = message.get("content", "")
                self._logger.info(f"   Message {i+1} ({role}): {content}")
        else:
            self._logger.info(f"📝 Prompt: {prompt}")
    
    def openai_response(self, model: str, response_length: int, usage: Dict[str, Any] = None, full_response: str = None):
        """Log OpenAI API response details with full content."""
        self._logger.info(f"🤖 OPENAI RESPONSE: Model={model}, Length={response_length}")
        
        if full_response:
            self._logger.info(f"📤 Full OpenAI Response:")
            self._logger.info(f"   {full_response}")
        
        if usage:
            self._logger.info(f"💰 Token usage: {json.dumps(usage, indent=2)}")
    
    def service_flow(self, service: str, method: str, input_data: Dict[str, Any] = None, output_data: Dict[str, Any] = None):
        """Log service layer flow."""
        self._logger.info(f"⚙️  SERVICE FLOW: {service}.{method}")
        if input_data:
            self._logger.info(f"📥 Input: {json.dumps(input_data, indent=2)}")
        if output_data:
            # Log output summary
            if isinstance(output_data, dict) and "news_items" in output_data:
                summary = {
                    "total_items": len(output_data.get("news_items", [])),
                    "source": output_data.get("source", "unknown")
                }
                self._logger.info(f"📤 Output summary: {json.dumps(summary, indent=2)}")
    
    def integration_flow(self, integration: str, method: str, request_data: Dict[str, Any] = None, response_data: Dict[str, Any] = None):
        """Log integration layer flow."""
        self._logger.info(f"🔌 INTEGRATION FLOW: {integration}.{method}")
        if request_data:
            self._logger.info(f"📤 Request: {json.dumps(request_data, indent=2)}")
        if response_data:
            self._logger.info(f"📥 Response: {json.dumps(response_data, indent=2)}")

# Global logger instance
logger = Logger()
