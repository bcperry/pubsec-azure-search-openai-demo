import os
import json
import logging

# Configure logging to show info logs on command line
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # This will output to console
    ]
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class CloudConfiguration():
    def __init__(self):
        self.config = self.load_cloud_config()
        self.name = self.config.get("name", "Unknown")

    def load_cloud_config(self):
        """Load cloud configuration based on environment variable."""
        azure_cloud_env = os.getenv("AZURE_CLOUD_ENVIRONMENT")
        cloud_config_path = os.path.join(os.path.dirname(__file__), "..", "clouds", "cloudConfig.json")
        with open(cloud_config_path, 'r') as f:
            cloud_configs = json.load(f)
            
        if azure_cloud_env in cloud_configs.get("environments", {}):
            config = cloud_configs["environments"][azure_cloud_env]
            logger.info(f"Using Azure cloud configuration for environment: {config['name']}")
        elif azure_cloud_env is None:
            # Default to Azure Public if no environment is set
            config = cloud_configs["environments"]["AzurePublic"]
            logger.info("No AZURE_CLOUD_ENVIRONMENT set, using Azure Public configuration.")
        else:
            available_envs = list(cloud_configs.get('environments', {}).keys())
            logger.error(f"Invalid Azure cloud environment: '{azure_cloud_env}'. Available environments: {available_envs}")
            raise ValueError(f"Invalid Azure cloud environment: '{azure_cloud_env}'. Available environments: {available_envs}")
        
        return config

if __name__ == "__main__":
    cloud_config = CloudConfiguration()
    logger.info(f"Current cloud configuration: {cloud_config.name}")
