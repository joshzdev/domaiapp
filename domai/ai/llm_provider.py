"""
Enhanced LLM Provider for DōmAI
Integrates multiple AI providers with dual-stream architecture
"""

from enum import Enum
from typing import Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import logging
import aiohttp
import json
import google.generativeai as genai
from mistralai.client import MistralClient

from .model_config import ModelConfig, ModelProvider, ModelParameters

class LLMProvider:
    """Base class for LLM providers with dual-stream support"""
    
    async def generate_dual_stream(self, 
                                 prompt: str, 
                                 config: ModelConfig,
                                 stream: bool = False) -> tuple[str, str]:
        """Generate both crisis and knowledge responses"""
        try:
            # First generate crisis response
            crisis_prompt = self._format_crisis_prompt(prompt)
            crisis = await self.generate(crisis_prompt, config)
            
            # Then generate knowledge response with context from crisis
            knowledge_prompt = self._format_knowledge_prompt(prompt, crisis)
            knowledge = await self.generate(knowledge_prompt, config)
            
            return crisis, knowledge
            
        except Exception as e:
            self.logger.error(f"Dual-stream generation failed: {str(e)}")
            return (
                "I apologize, but I encountered an error. Please check your API key and connection.",
                "Make sure your API key is set correctly and you have a stable internet connection."
            )
            
    async def generate(self, prompt: str, config: ModelConfig) -> str:
        """Generate single response"""
        raise NotImplementedError
        
    async def stream(self, prompt: str, config: ModelConfig) -> AsyncGenerator[str, None]:
        """Stream response"""
        raise NotImplementedError
        
    async def _collect_stream(self, generator: AsyncGenerator[str, None]) -> str:
        """Collect streamed response into single string"""
        chunks = []
        async for chunk in generator:
            chunks.append(chunk)
        return ''.join(chunks)
        
    def _format_crisis_prompt(self, prompt: str) -> str:
        """Format prompt for crisis stream"""
        return f"""You are a MacOS security assistant. Focus on providing immediate, actionable security guidance.
        User Query: {prompt}
        
        Provide a clear, concise response that:
        1. Addresses any immediate security concerns
        2. Gives specific, actionable steps if needed
        3. Maintains a calm, professional tone
        
        Response:"""
        
    def _format_knowledge_prompt(self, prompt: str, crisis_response: str) -> str:
        """Format prompt for knowledge stream with context from crisis response"""
        return f"""You are a MacOS security educator. Based on the user's query and the immediate response provided,
        offer deeper educational context and understanding.
        
        User Query: {prompt}
        
        Immediate Response Given: {crisis_response}
        
        Provide educational content that:
        1. Explains relevant security concepts
        2. Provides background information
        3. Helps the user understand the 'why' behind the actions
        4. Suggests best practices and preventive measures
        
        Educational Response:"""

class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.openai")
        
    async def generate(self, prompt: str, config: ModelConfig) -> str:
        """Generate response using OpenAI"""
        try:
            import openai
            openai.api_key = config.api_key
            if config.api_base:
                openai.api_base = config.api_base
                
            response = await openai.chat.completions.create(
                model=config.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.parameters.temperature,
                max_tokens=config.parameters.max_tokens,
                top_p=config.parameters.top_p,
                presence_penalty=config.parameters.presence_penalty,
                frequency_penalty=config.parameters.frequency_penalty,
                stop=config.parameters.stop_sequences
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI generation failed: {str(e)}")
            raise

    async def stream(self, prompt: str, config: ModelConfig) -> AsyncGenerator[str, None]:
        """Stream response using OpenAI"""
        try:
            import openai
            openai.api_key = config.api_key
            if config.api_base:
                openai.api_base = config.api_base
                
            stream = await openai.chat.completions.create(
                model=config.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.parameters.temperature,
                max_tokens=config.parameters.max_tokens,
                top_p=config.parameters.top_p,
                presence_penalty=config.parameters.presence_penalty,
                frequency_penalty=config.parameters.frequency_penalty,
                stop=config.parameters.stop_sequences,
                stream=True
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            self.logger.error(f"OpenAI streaming failed: {str(e)}")
            raise

class GoogleProvider(LLMProvider):
    """Google (Gemini) provider implementation"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.google")
        
    async def generate(self, prompt: str, config: ModelConfig) -> str:
        """Generate response using Google"""
        try:
            genai.configure(api_key=config.api_key)
            model = genai.GenerativeModel(
                model_name=config.model_id,
                generation_config={
                    "temperature": config.parameters.temperature,
                    "top_p": config.parameters.top_p,
                    "max_output_tokens": config.parameters.max_tokens
                }
            )
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Google generation failed: {str(e)}")
            raise

    async def stream(self, prompt: str, config: ModelConfig) -> AsyncGenerator[str, None]:
        """Stream response using Google"""
        try:
            genai.configure(api_key=config.api_key)
            model = genai.GenerativeModel(
                model_name=config.model_id,
                generation_config={
                    "temperature": config.parameters.temperature,
                    "top_p": config.parameters.top_p,
                    "max_output_tokens": config.parameters.max_tokens
                }
            )
            
            response = model.generate_content(prompt, stream=True)
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            self.logger.error(f"Google streaming failed: {str(e)}")
            raise

class MistralProvider(LLMProvider):
    """Mistral AI provider implementation"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.mistral")
        
    async def generate(self, prompt: str, config: ModelConfig) -> str:
        """Generate response using Mistral"""
        try:
            client = MistralClient(api_key=config.api_key)
            
            response = client.chat(
                model=config.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.parameters.temperature,
                max_tokens=config.parameters.max_tokens,
                top_p=config.parameters.top_p
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Mistral generation failed: {str(e)}")
            raise

    async def stream(self, prompt: str, config: ModelConfig) -> AsyncGenerator[str, None]:
        """Stream response using Mistral"""
        try:
            client = MistralClient(api_key=config.api_key)
            
            stream = client.chat_stream(
                model=config.model_id,
                messages=[{"role": "user", "content": prompt}],
                temperature=config.parameters.temperature,
                max_tokens=config.parameters.max_tokens,
                top_p=config.parameters.top_p
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            self.logger.error(f"Mistral streaming failed: {str(e)}")
            raise

class LLMManager:
    """Manages multiple LLM providers with dual-stream support"""
    
    def __init__(self):
        self.providers = {
            ModelProvider.OPENAI: OpenAIProvider(),
            ModelProvider.GOOGLE: GoogleProvider(),
            ModelProvider.MISTRAL: MistralProvider()
        }
        self.logger = logging.getLogger("domai.llm")
        
    async def generate_dual_stream(self, 
                                 prompt: str, 
                                 config: ModelConfig,
                                 stream: bool = False) -> tuple[str, str]:
        """Generate dual-stream response using specified provider"""
        try:
            provider = self.providers.get(config.provider)
            if not provider:
                raise ValueError(f"Unsupported provider: {config.provider}")
                
            return await provider.generate_dual_stream(prompt, config, stream)
            
        except Exception as e:
            self.logger.error(f"Dual-stream generation failed: {str(e)}")
            raise

    async def generate(self, prompt: str, config: ModelConfig) -> str:
        """Generate single response using specified provider"""
        try:
            provider = self.providers.get(config.provider)
            if not provider:
                raise ValueError(f"Unsupported provider: {config.provider}")
                
            return await provider.generate(prompt, config)
            
        except Exception as e:
            self.logger.error(f"Generation failed: {str(e)}")
            raise

    async def stream(self, prompt: str, config: ModelConfig) -> AsyncGenerator[str, None]:
        """Stream response using specified provider"""
        try:
            provider = self.providers.get(config.provider)
            if not provider:
                raise ValueError(f"Unsupported provider: {config.provider}")
                
            async for chunk in provider.stream(prompt, config):
                yield chunk
                
        except Exception as e:
            self.logger.error(f"Streaming failed: {str(e)}")
            raise