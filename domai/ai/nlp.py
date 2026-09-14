"""
Natural Language Processing for DōmAI
Processes user input for MacOS security analysis
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
import re

from .model_config import ModelConfig, ModelProvider, ModelParameters

@dataclass
class ProcessedQuery:
    """Processed user query about MacOS security"""
    raw_text: str
    normalized_text: str
    key_terms: set[str]
    command_indicators: bool  # Whether query implies command execution
    security_category: Optional[str] = None  # e.g., 'permissions', 'firewall', etc.

class NLProcessor:
    """Natural language processor for MacOS security queries"""
    
    def __init__(self):
        self.logger = logging.getLogger("domai.nlp")
        
        # MacOS security-specific term normalization
        self.term_mapping = {
            'permissions': ['permission', 'chmod', 'chown', 'access'],
            'firewall': ['pf', 'packet filter', 'network protection'],
            'disk_encryption': ['filevault', 'encryption', 'decrypt'],
            'app_security': ['gatekeeper', 'quarantine', 'sandbox'],
            'authentication': ['sudo', 'password', 'keychain'],
            'system_integrity': ['sip', 'rootless', 'csrutil']
        }
        
    async def process_query(self, query: str) -> ProcessedQuery:
        """Process user query about MacOS security"""
        try:
            # Normalize text
            normalized = self._normalize_text(query)
            
            # Extract key terms
            key_terms = self._extract_key_terms(normalized)
            
            # Detect command intent
            command_indicators = self._detect_command_indicators(normalized)
            
            # Identify security category
            category = self._identify_security_category(key_terms)
            
            return ProcessedQuery(
                raw_text=query,
                normalized_text=normalized,
                key_terms=key_terms,
                command_indicators=command_indicators,
                security_category=category
            )
            
        except Exception as e:
            self.logger.error(f"Query processing failed: {str(e)}")
            return ProcessedQuery(
                raw_text=query,
                normalized_text=query,
                key_terms=set(),
                command_indicators=False
            )
            
    def get_response_config(self) -> ModelConfig:
        """Get model configuration for response generation"""
        return ModelConfig(
            provider=ModelProvider.OPENAI,
            model_id="gpt-4",
            api_key="",  # Set via environment variable
            parameters=ModelParameters(
                temperature=0.7,
                max_tokens=1000,
                presence_penalty=0.0,
                frequency_penalty=0.0
            )
        )
        
    def get_education_config(self) -> ModelConfig:
        """Get model configuration for educational content"""
        return ModelConfig(
            provider=ModelProvider.OPENAI,
            model_id="gpt-4",
            api_key="",  # Set via environment variable
            parameters=ModelParameters(
                temperature=0.5,  # More focused
                max_tokens=2000,  # Longer for educational content
                presence_penalty=0.0,
                frequency_penalty=0.3  # Reduce repetition
            )
        )
            
    def _normalize_text(self, text: str) -> str:
        """Normalize query text"""
        # Convert to lowercase
        text = text.lower()
        
        # Standardize MacOS-specific terms
        text = text.replace('mac os', 'macos')
        text = text.replace('os x', 'macos')
        
        # Standardize security terms
        text = text.replace('file vault', 'filevault')
        text = text.replace('gate keeper', 'gatekeeper')
        
        # Remove unnecessary punctuation
        text = re.sub(r'[^\w\s-]', ' ', text)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text
        
    def _extract_key_terms(self, text: str) -> set[str]:
        """Extract MacOS security-related key terms"""
        terms = set()
        
        # Check each term category
        for category, related_terms in self.term_mapping.items():
            for term in related_terms:
                if term in text:
                    terms.add(term)
                    terms.add(category)  # Add category as a term
                    
        return terms
        
    def _detect_command_indicators(self, text: str) -> bool:
        """Detect if query implies command execution"""
        command_indicators = {
            'how to',
            'how do i',
            'can you',
            'please',
            'help me',
            'i want to',
            'enable',
            'disable',
            'change',
            'modify',
            'set',
            'configure'
        }
        
        return any(indicator in text for indicator in command_indicators)
        
    def _identify_security_category(self, terms: set[str]) -> Optional[str]:
        """Identify primary MacOS security category"""
        category_scores = {}
        
        # Score each category based on term matches
        for category, related_terms in self.term_mapping.items():
            score = sum(1 for term in related_terms if term in terms)
            if score > 0:
                category_scores[category] = score
                
        # Return highest scoring category
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        return None 