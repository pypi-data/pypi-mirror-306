import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ErrorHandler:
    async def handle_error(self, error: Exception, context: Dict[str, Any]):
        error_type = type(error).__name__
        error_message = str(error)
        
        logger.error(f"Error occurred: {error_type} - {error_message}")
        logger.error(f"Context: {context}")
        
        if isinstance(error, ValueError):
            # Handle value errors
            logger.info("Attempting to recover from ValueError...")
            # Implement recovery logic here
        elif isinstance(error, TimeoutError):
            # Handle timeout errors
            logger.info("Attempting to retry after TimeoutError...")
            # Implement retry logic here
        else:
            # Handle other types of errors
            logger.warning("Unhandled error type. Propagating error...")
            raise error