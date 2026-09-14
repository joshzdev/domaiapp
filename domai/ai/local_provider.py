"""
Local LLM Provider for DōmAI
Manages local AI models for MacOS security assistance
"""

import logging
from typing import Dict, Any, Optional, AsyncGenerator
from enum import Enum
from dataclasses import dataclass
import aiohttp
import json

from .model_config import ModelConfig

class LocalModelFormat(Enum):
    """Supported local model formats"""
    LLAMA_CPP = "llama.cpp"
    GGML = "ggml"
    ONNX = "onnx"
    PYTORCH = "pytorch"

@dataclass
class LocalModelInfo:
    """Local model information"""
    name: str
    format: LocalModelFormat
    path: Optional[str] = None
    api_base: Optional[str] = None
    template: Optional[str] = None
    context_size: int = 2048
    parameters: Dict[str, Any] = None

class LocalProvider:
    """Local model provider"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.local")
        self.models: Dict[str, LocalModelInfo] = {}
        
    def add_model(self, model_id: str, info: LocalModelInfo) -> None:
        """Add local model configuration"""
        self.models[model_id] = info
        
    def get_model(self, model_id: str) -> Optional[LocalModelInfo]:
        """Get local model configuration"""
        return self.models.get(model_id)
        
    async def generate(self, prompt: str, config: ModelConfig) -> str:
        """Generate response using local model"""
        try:
            model_info = self.get_model(config.model_id)
            if not model_info:
                raise ValueError(f"Model not found: {config.model_id}")
                
            if model_info.api_base:
                return await self._generate_api(prompt, config, model_info)
            else:
                return await self._generate_local(prompt, config, model_info)
                
        except Exception as e:
            self.logger.error(f"Local generation failed: {str(e)}")
            raise
            
    async def stream(self, prompt: str, config: ModelConfig) -> AsyncGenerator[str, None]:
        """Stream response using local model"""
        try:
            model_info = self.get_model(config.model_id)
            if not model_info:
                raise ValueError(f"Model not found: {config.model_id}")
                
            if model_info.api_base:
                async for chunk in self._stream_api(prompt, config, model_info):
                    yield chunk
            else:
                async for chunk in self._stream_local(prompt, config, model_info):
                    yield chunk
                    
        except Exception as e:
            self.logger.error(f"Local streaming failed: {str(e)}")
            raise
            
    async def _generate_api(self, prompt: str, config: ModelConfig, model_info: LocalModelInfo) -> str:
        """Generate response using local API endpoint"""
        try:
            headers = {"Content-Type": "application/json"}
            
            # Format prompt using template if provided
            if model_info.template:
                formatted_prompt = model_info.template.format(prompt=prompt)
            else:
                formatted_prompt = prompt
                
            data = {
                "prompt": formatted_prompt,
                "temperature": config.parameters.temperature,
                "top_p": config.parameters.top_p,
                "max_tokens": config.parameters.max_tokens or model_info.context_size
            }
            
            if model_info.parameters:
                data.update(model_info.parameters)
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{model_info.api_base}/v1/completions",
                    headers=headers,
                    json=data
                ) as response:
                    result = await response.json()
                    return result["choices"][0]["text"]
                    
        except Exception as e:
            self.logger.error(f"API generation failed: {str(e)}")
            raise
            
    async def _generate_local(self, prompt: str, config: ModelConfig, model_info: LocalModelInfo) -> str:
        """Generate response using local model file"""
        try:
            if model_info.format == LocalModelFormat.LLAMA_CPP:
                from llama_cpp import Llama
                
                llm = Llama(
                    model_path=model_info.path,
                    n_ctx=model_info.context_size,
                    n_threads=4
                )
                
                output = llm(
                    prompt,
                    max_tokens=config.parameters.max_tokens or model_info.context_size,
                    temperature=config.parameters.temperature,
                    top_p=config.parameters.top_p,
                    echo=False
                )
                
                return output["choices"][0]["text"]
                
            else:
                raise ValueError(f"Unsupported local format: {model_info.format}")
                
        except Exception as e:
            self.logger.error(f"Local generation failed: {str(e)}")
            raise
            
    async def _stream_api(self, prompt: str, config: ModelConfig, model_info: LocalModelInfo) -> AsyncGenerator[str, None]:
        """Stream response using local API endpoint"""
        try:
            headers = {"Content-Type": "application/json"}
            
            # Format prompt using template if provided
            if model_info.template:
                formatted_prompt = model_info.template.format(prompt=prompt)
            else:
                formatted_prompt = prompt
                
            data = {
                "prompt": formatted_prompt,
                "temperature": config.parameters.temperature,
                "top_p": config.parameters.top_p,
                "max_tokens": config.parameters.max_tokens or model_info.context_size,
                "stream": True
            }
            
            if model_info.parameters:
                data.update(model_info.parameters)
                
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{model_info.api_base}/v1/completions",
                    headers=headers,
                    json=data
                ) as response:
                    async for line in response.content:
                        if line:
                            try:
                                data = json.loads(line.decode('utf-8').strip('data: '))
                                if data.get("choices") and data["choices"][0].get("text"):
                                    yield data["choices"][0]["text"]
                            except Exception as e:
                                self.logger.error(f"Stream parsing failed: {str(e)}")
                                
        except Exception as e:
            self.logger.error(f"API streaming failed: {str(e)}")
            raise
            
    async def _stream_local(self, prompt: str, config: ModelConfig, model_info: LocalModelInfo) -> AsyncGenerator[str, None]:
        """Stream response using local model file"""
        try:
            if model_info.format == LocalModelFormat.LLAMA_CPP:
                from llama_cpp import Llama
                
                llm = Llama(
                    model_path=model_info.path,
                    n_ctx=model_info.context_size,
                    n_threads=4
                )
                
                for output in llm(
                    prompt,
                    max_tokens=config.parameters.max_tokens or model_info.context_size,
                    temperature=config.parameters.temperature,
                    top_p=config.parameters.top_p,
                    echo=False,
                    stream=True
                ):
                    yield output["choices"][0]["text"]
                    
            else:
                raise ValueError(f"Unsupported local format: {model_info.format}")
                
        except Exception as e:
            self.logger.error(f"Local streaming failed: {str(e)}")
            raise 