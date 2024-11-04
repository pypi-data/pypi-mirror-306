import os
import json
from pathlib import Path
from typing import Dict, List, Optional

class ConfigManager:
    def __init__(self):
        self.home = Path.home()
        self.config_dir = self.home / '.jupyter_whisper'
        self.config_file = self.config_dir / 'config.json'
        self.ensure_config_dir()

    def ensure_config_dir(self) -> None:
        """Ensure configuration directory exists"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.save_config({})

    def load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_config(self, config: Dict) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    def set_api_key(self, key: str, value: str) -> None:
        """Set an API key in the configuration"""
        config = self.load_config()
        config[key] = value
        self.save_config(config)
        os.environ[key] = value

    def get_api_key(self, key: str) -> Optional[str]:
        """Get an API key from config or environment"""
        # Environment variables take precedence
        env_value = os.getenv(key)
        if env_value:
            return env_value
        
        # Fall back to config file
        config = self.load_config()
        return config.get(key)

    def ensure_api_keys(self) -> List[str]:
        """Ensure all required API keys are available"""
        required_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'PERPLEXITY_API_KEY']
        missing_keys = []
        
        for key in required_keys:
            value = self.get_api_key(key)
            if value:
                os.environ[key] = value
            else:
                missing_keys.append(key)
        
        return missing_keys

# Singleton instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get or create config manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager
