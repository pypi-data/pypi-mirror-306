import os
from pathlib import Path

class Config:
    def __init__(self):
        self._init_defaults()

    def _init_defaults(self):
        """Initialize default configurations"""
        # Node settings
        self.node_host = '127.0.0.1'
        self.node_port = 8468
        
        # Vector DB settings
        self.default_dim = 1024
        self.default_max_elements = 10000
        
        # Network settings
        self.replication_factor = 3
        self.bootstrap_host = None
        self.bootstrap_port = 8468

    def update_config(self, **kwargs):
        """Update configuration with user provided values"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration parameter: {key}")

config = Config()  # Single instance to be imported