"""
Response Generator for DōmAI
Generates responses and educational content for MacOS security queries
"""

import logging
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GeneratedResponse:
    """Generated response with educational content"""
    response: str
    education: Optional[str] = None
    metadata: Dict[str, Any] = None
    timestamp: datetime = datetime.now()

class ResponseGenerator:
    """Generates responses for MacOS security queries"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.logger = logging.getLogger("domai.generator")
        
        # Response templates for common security topics
        self.templates = {
            'permissions': {
                'response': "Here's how to {action} the permissions for {target}: {command}",
                'education': """
                MacOS uses Unix-style permissions with three levels:
                - Read (4): View file contents
                - Write (2): Modify file contents
                - Execute (1): Run files or access directories
                
                Common permission patterns:
                - 755: rwxr-xr-x (standard for executables)
                - 644: rw-r--r-- (standard for regular files)
                - 700: rwx------ (private files)
                """
            },
            'firewall': {
                'response': "The firewall is currently {status}. {action_text}",
                'education': """
                MacOS includes multiple firewall layers:
                - Application Firewall: Controls per-app network access
                - Packet Filter (pf): Low-level network filtering
                - Socket Filter: Kernel-level network control
                """
            },
            'disk_encryption': {
                'response': "FileVault encryption is {status}. {details}",
                'education': """
                FileVault provides full-disk encryption:
                - Uses XTS-AES-128 encryption
                - Protects data at rest
                - Minimal performance impact
                - Recovery key stored with Apple (optional)
                """
            },
            'app_security': {
                'response': "App security settings: {settings}. {recommendations}",
                'education': """
                MacOS app security features:
                - Gatekeeper: Verifies app sources
                - App Sandbox: Limits app capabilities
                - Notarization: Apple security check
                - Quarantine: Flags downloaded files
                """
            },
            'system_integrity': {
                'response': "System Integrity Protection (SIP) is {status}. {details}",
                'education': """
                System Integrity Protection (SIP):
                - Protects system files and processes
                - Prevents root-level changes
                - Maintains system integrity
                - Can be configured in Recovery Mode
                """
            }
        }
        
    async def generate_response(self, 
                              query: str,
                              context: Dict[str, Any],
                              security_category: Optional[str] = None) -> GeneratedResponse:
        """Generate response for security query"""
        try:
            # Get appropriate model config
            model_config = self.model_manager.get_config(context.get('model_provider'))
            
            # Generate base response
            response = await self._generate_base_response(
                query,
                context,
                model_config,
                security_category
            )
            
            # Add educational content
            education = await self._generate_education(
                query,
                context,
                security_category
            )
            
            # Add metadata
            metadata = {
                'query': query,
                'category': security_category,
                'context': context,
                'model': model_config.model_id
            }
            
            return GeneratedResponse(
                response=response,
                education=education,
                metadata=metadata
            )
            
        except Exception as e:
            self.logger.error(f"Response generation failed: {str(e)}")
            return self._get_fallback_response(query)
            
    async def _generate_base_response(self,
                                    query: str,
                                    context: Dict[str, Any],
                                    model_config: Any,
                                    security_category: Optional[str]) -> str:
        """Generate base response using AI model"""
        # Use template if available
        if security_category and security_category in self.templates:
            template = self.templates[security_category]['response']
            return self._fill_template(template, context)
            
        # Fall back to model generation
        prompt = self._create_response_prompt(query, context)
        response = await self.model_manager.generate(
            prompt,
            model_config
        )
        
        return response
        
    async def _generate_education(self,
                                query: str,
                                context: Dict[str, Any],
                                security_category: Optional[str]) -> Optional[str]:
        """Generate educational content"""
        # Use template if available
        if security_category and security_category in self.templates:
            return self.templates[security_category]['education']
            
        # Generate custom education based on technical level
        technical_level = context.get('technical_level', 'beginner')
        prompt = self._create_education_prompt(query, technical_level)
        
        model_config = self.model_manager.get_config(context.get('model_provider'))
        education = await self.model_manager.generate(
            prompt,
            model_config
        )
        
        return education
        
    def _create_response_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Create prompt for response generation"""
        return f"""
        Generate a clear and helpful response for this MacOS security question:
        Question: {query}
        Technical Level: {context.get('technical_level', 'beginner')}
        Focus on practical, accurate security advice.
        """
        
    def _create_education_prompt(self, query: str, technical_level: str) -> str:
        """Create prompt for educational content"""
        return f"""
        Generate educational content about the MacOS security concepts in this query:
        Query: {query}
        Technical Level: {technical_level}
        Include key concepts, best practices, and security implications.
        """
        
    def _fill_template(self, template: str, context: Dict[str, Any]) -> str:
        """Fill response template with context"""
        try:
            return template.format(**context)
        except KeyError:
            return template
            
    def _get_fallback_response(self, query: str) -> GeneratedResponse:
        """Generate fallback response when generation fails"""
        return GeneratedResponse(
            response="I'm analyzing your MacOS security question. Please try again.",
            education="MacOS provides multiple layers of security protection."
        ) 