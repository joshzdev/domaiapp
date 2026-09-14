#!/usr/bin/env python3
"""
DōmAI - MacOS Security Assistant
Main application entry point
"""

import asyncio
import os
import json
from pathlib import Path
import logging
from typing import Optional

from .ai.analyzer import AIAnalyzer, SecurityContext
from .ai.model_config import ModelConfigManager, ModelProvider
from .core.dual_stream_core import DualStreamAnalyzer

class DomAI:
    """Main application class"""
    
    def __init__(self):
        # Initialize components
        self.analyzer = AIAnalyzer()
        self.config_manager = ModelConfigManager()
        self.dual_stream = DualStreamAnalyzer()
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("domai")
        
        # Load configuration
        self._load_config()
        
    def _load_config(self):
        """Load API keys and configuration"""
        # Check environment variables first
        self._load_env_config()
        
        # Then check config file
        config_path = Path.home() / ".domai" / "config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    config = json.load(f)
                self._apply_config(config)
            except Exception as e:
                self.logger.error(f"Failed to load config file: {e}")
                
    def _load_env_config(self):
        """Load configuration from environment variables"""
        # OpenAI
        if api_key := os.getenv("OPENAI_API_KEY"):
            self.config_manager.update_config(
                ModelProvider.OPENAI,
                api_key=api_key
            )
            
        # Google
        if api_key := os.getenv("GOOGLE_API_KEY"):
            self.config_manager.update_config(
                ModelProvider.GOOGLE,
                api_key=api_key
            )
            
        # Mistral
        if api_key := os.getenv("MISTRAL_API_KEY"):
            self.config_manager.update_config(
                ModelProvider.MISTRAL,
                api_key=api_key
            )
            
    def _apply_config(self, config: dict):
        """Apply configuration from config file"""
        if api_keys := config.get("api_keys"):
            for provider, key in api_keys.items():
                try:
                    self.config_manager.update_config(
                        ModelProvider(provider),
                        api_key=key
                    )
                except ValueError:
                    self.logger.warning(f"Unknown provider: {provider}")
                    
    async def process_query(self, query: str, user_level: str = "beginner") -> tuple[str, str]:
        """Process user query and return dual-stream response"""
        try:
            # Create security context
            context = SecurityContext(
                event_history=[],
                user_proficiency=user_level,
                system_state={},
                threat_context={}
            )
            
            # Get command and initial response
            command, output = await self.analyzer.process_user_query(query, user_level)
            
            # If command is generated, analyze it
            if command:
                event = {
                    "type": "command",
                    "command": command,
                    "query": query
                }
                command_output = await self.analyzer.analyze_security_event(event, context)
                
                # Combine outputs
                crisis = f"{output.crisis}\n\nCommand: {command}\n{command_output.crisis}"
                knowledge = f"{output.knowledge}\n\n{command_output.knowledge}"
            else:
                crisis = output.crisis
                knowledge = output.knowledge
                
            return crisis, knowledge
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {e}")
            return (
                "I apologize, but I encountered an error processing your request.",
                "I'll make sure to handle this better next time."
            )
            
    async def interactive_session(self):
        """Start interactive session"""
        print("DōmAI - MacOS Security Assistant")
        print("Type 'exit' to quit\n")
        
        while True:
            try:
                # Get user input
                query = input("\nHow can I help? > ").strip()
                if query.lower() in ['exit', 'quit']:
                    break
                    
                # Process query
                crisis, knowledge = await self.process_query(query)
                
                # Display responses
                print("\n🔒 Security Response:")
                print(crisis)
                print("\n📚 Learn More:")
                print(knowledge)
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                self.logger.error(f"Session error: {e}")
                print("\nI encountered an error, but I'm still here to help.")
                
def main():
    """Main entry point"""
    app = DomAI()
    asyncio.run(app.interactive_session())
    
if __name__ == "__main__":
    main() 