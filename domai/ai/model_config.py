"""
Model Configuration for DōmAI
Manages AI model configurations for dual-stream processing
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

class ModelProvider(Enum):
    """Supported AI model providers"""
    OPENAI = "openai"
    GOOGLE = "google"
    MISTRAL = "mistral"
    LOCAL = "local"

@dataclass
class ModelParameters:
    """AI model parameters"""
    temperature: float = 0.7
    top_p: float = 1.0
    max_tokens: Optional[int] = None
    stop_sequences: Optional[list[str]] = None
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0

@dataclass
class StreamConfig:
    """Configuration for dual-stream processing"""
    crisis_temperature: float = 0.3  # Lower temperature for more focused crisis responses
    knowledge_temperature: float = 0.7  # Higher temperature for more creative educational content
    crisis_max_tokens: int = 1000  # Shorter responses for crisis stream
    knowledge_max_tokens: int = 2000  # Longer responses for educational content

@dataclass
class ModelConfig:
    """AI model configuration with dual-stream support"""
    provider: ModelProvider
    model_id: str
    api_key: str
    api_base: Optional[str] = None
    parameters: ModelParameters = field(default_factory=ModelParameters)
    stream_config: StreamConfig = field(default_factory=StreamConfig)

class ModelConfigManager:
    """Manages AI model configurations for dual-stream processing"""
    
    def __init__(self):
        self.default_configs = self._get_default_configs()
        
    def _get_default_configs(self) -> Dict[str, ModelConfig]:
        """Get default configurations for each provider"""
        return {
            ModelProvider.OPENAI.value: ModelConfig(
                provider=ModelProvider.OPENAI,
                model_id="gpt-4",
                api_key="",
                parameters=ModelParameters(
                    temperature=0.7,
                    max_tokens=2000
                ),
                stream_config=StreamConfig()
            ),
            ModelProvider.GOOGLE.value: ModelConfig(
                provider=ModelProvider.GOOGLE,
                model_id="gemini-pro",
                api_key="",
                parameters=ModelParameters(
                    temperature=0.7,
                    max_tokens=2000
                ),
                stream_config=StreamConfig()
            ),
            ModelProvider.MISTRAL.value: ModelConfig(
                provider=ModelProvider.MISTRAL,
                model_id="mistral-medium",
                api_key="",
                parameters=ModelParameters(
                    temperature=0.7,
                    max_tokens=2000
                ),
                stream_config=StreamConfig()
            ),
            ModelProvider.LOCAL.value: ModelConfig(
                provider=ModelProvider.LOCAL,
                model_id="local",
                api_key="",
                parameters=ModelParameters(
                    temperature=0.7,
                    max_tokens=2000
                ),
                stream_config=StreamConfig()
            )
        }
        
    def get_config(self, provider: ModelProvider) -> ModelConfig:
        """Get configuration for specified provider"""
        return self.default_configs.get(provider.value)
        
    def get_crisis_config(self, provider: ModelProvider) -> ModelConfig:
        """Get configuration optimized for crisis stream"""
        config = self.get_config(provider)
        if config:
            config.parameters.temperature = config.stream_config.crisis_temperature
            config.parameters.max_tokens = config.stream_config.crisis_max_tokens
        return config
        
    def get_knowledge_config(self, provider: ModelProvider) -> ModelConfig:
        """Get configuration optimized for knowledge stream"""
        config = self.get_config(provider)
        if config:
            config.parameters.temperature = config.stream_config.knowledge_temperature
            config.parameters.max_tokens = config.stream_config.knowledge_max_tokens
        return config
        
    def update_config(self, provider: ModelProvider, **kwargs) -> None:
        """Update configuration for specified provider"""
        if provider.value in self.default_configs:
            config = self.default_configs[provider.value]
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
                elif hasattr(config.parameters, key):
                    setattr(config.parameters, key, value)
                elif hasattr(config.stream_config, key):
                    setattr(config.stream_config, key, value)
                    
    def validate_config(self, config: ModelConfig) -> bool:
        """Validate model configuration"""
        if not config.api_key and config.provider != ModelProvider.LOCAL:
            return False
            
        if not config.model_id:
            return False
            
        if config.parameters.temperature < 0 or config.parameters.temperature > 1:
            return False
            
        if config.parameters.top_p < 0 or config.parameters.top_p > 1:
            return False
            
        return True