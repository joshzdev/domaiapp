#!/usr/bin/env python3
"""
DōmAI Security Analysis Pipeline
Handles both real-time and historical security data analysis with terminal-like flexibility
"""

import logging
import threading
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import queue
import uuid

from ..security.data_store import (
    SecureDataStore, DataType, TimeRange, DataQuery,
    QueryFilter
)
from ..ai.analyzer import AIAnalyzer
from .types.security import SecurityEvent, SecurityLevel
from .stream_manager import StreamType, StreamOutput
from ..api.bridge import BridgeManager

class AnalysisScope(Enum):
    REAL_TIME = "real_time"
    HISTORICAL = "historical"
    SPECIFIED_RANGE = "specified_range"

@dataclass
class AnalysisContext:
    """Context for security analysis"""
    scope: AnalysisScope
    time_range: Optional[TimeRange]
    user_expertise: str
    system_state: Dict[str, Any]
    recent_events: List[Dict[str, Any]]
    related_findings: List[Dict[str, Any]]
    session_id: str

@dataclass
class AnalysisResult:
    """Result of security analysis"""
    findings: List[Dict[str, Any]]
    patterns: List[Dict[str, Any]]
    threats: List[Dict[str, Any]]
    recommendations: List[str]
    learning_points: List[str]
    timestamp: datetime
    session_id: str

class SecurityAnalysisPipeline:
    """Comprehensive security analysis pipeline with terminal-like flexibility"""
    
    def __init__(self, bridge_manager: BridgeManager):
        self._lock = threading.Lock()
        self.data_store = SecureDataStore()
        self.ai_analyzer = AIAnalyzer()
        self.bridge = bridge_manager
        self.logger = logging.getLogger(__name__)
        
        # Analysis queues
        self.analysis_queues: Dict[str, queue.Queue] = {}
        self.analysis_threads: Dict[str, threading.Thread] = {}
        self.active_analyses: Dict[str, bool] = {}
        
        # Register bridge handlers
        self._register_bridge_handlers()
        
    def analyze_security_data(
        self,
        source: str,
        scope: AnalysisScope,
        user_expertise: str,
        session_id: str,
        time_spec: Optional[str] = None,
        filters: Optional[List[Dict[str, Any]]] = None,
        pattern: Optional[str] = None,
        context_lines: int = 0,
        sort_by: Optional[str] = None,
        sort_desc: bool = False,
        limit: Optional[int] = None,
        aggregation: Optional[str] = None,
        group_by: Optional[str] = None
    ) -> StreamOutput:
        """Analyze security data with terminal-like flexibility"""
        try:
            # Validate inputs
            if not self._validate_inputs(source, scope, user_expertise):
                raise ValueError("Invalid analysis parameters")
            
            # Parse time specification
            time_range = self._parse_time_spec(time_spec, scope)
            
            # Build analysis context
            analysis_context = self._build_context(
                source,
                scope,
                user_expertise,
                time_range,
                session_id
            )
            
            # Convert filters to QueryFilters
            query_filters = self._build_query_filters(filters)
            
            # Build data query
            query = self._build_query(
                source,
                time_range,
                query_filters,
                sort_by,
                sort_desc,
                limit,
                aggregation,
                group_by
            )
            
            # Get data with pattern matching if specified
            data = self._get_data(query, pattern, context_lines)
            
            # Queue analysis
            analysis_id = self._queue_analysis(
                data,
                source,
                analysis_context
            )
            
            # Return initial response
            return StreamOutput(
                crisis=self._get_initial_crisis_response(analysis_id),
                knowledge=self._get_initial_knowledge_response(analysis_id),
                timestamp=datetime.now(),
                metadata={
                    'analysis_id': analysis_id,
                    'scope': scope.value,
                    'source': source,
                    'time_range': time_range._asdict() if time_range else None,
                    'pattern': pattern,
                    'filters': filters,
                    'status': 'queued'
                }
            )
            
        except Exception as e:
            self.logger.error(f"Analysis pipeline error: {str(e)}")
            return self._get_fallback_output(session_id)
            
    def _validate_inputs(self, source: str, scope: AnalysisScope,
                        user_expertise: str) -> bool:
        """Validate analysis input parameters"""
        try:
            # Validate source
            if not source or not isinstance(source, str):
                return False
                
            # Validate scope
            if not isinstance(scope, AnalysisScope):
                return False
                
            # Validate user expertise
            if not user_expertise or not isinstance(user_expertise, str):
                return False
                
            return True
            
        except Exception:
            return False
            
    def _parse_time_spec(self, time_spec: Optional[str],
                        scope: AnalysisScope) -> Optional[TimeRange]:
        """Parse time specification"""
        try:
            if time_spec:
                return TimeRange.from_string(time_spec)
            elif scope == AnalysisScope.REAL_TIME:
                return TimeRange(
                    datetime.now() - timedelta(minutes=5),
                    datetime.now()
                )
            else:
                return TimeRange(
                    datetime.now() - timedelta(days=1),
                    datetime.now()
                )
        except Exception as e:
            self.logger.error(f"Time spec parsing error: {str(e)}")
            raise
            
    def _build_query_filters(self,
                           filters: Optional[List[Dict[str, Any]]]) -> Optional[List[QueryFilter]]:
        """Convert filters to QueryFilters"""
        if not filters:
            return None
            
        try:
            return [
                QueryFilter(
                    field=f['field'],
                    operator=f['operator'],
                    value=f['value']
                )
                for f in filters
            ]
        except Exception as e:
            self.logger.error(f"Filter conversion error: {str(e)}")
            raise
            
    def _build_query(self, source: str, time_range: Optional[TimeRange],
                    filters: Optional[List[QueryFilter]], sort_by: Optional[str],
                    sort_desc: bool, limit: Optional[int],
                    aggregation: Optional[str],
                    group_by: Optional[str]) -> DataQuery:
        """Build data query"""
        try:
            return DataQuery(
                data_type=self.data_store._map_source_to_data_type(source),
                time_range=time_range,
                filters=filters,
                sort_by=sort_by,
                sort_desc=sort_desc,
                limit=limit,
                aggregation=aggregation,
                group_by=group_by
            )
        except Exception as e:
            self.logger.error(f"Query building error: {str(e)}")
            raise
            
    def _get_data(self, query: DataQuery, pattern: Optional[str],
                 context_lines: int) -> List[Dict[str, Any]]:
        """Get data from data store"""
        try:
            if pattern:
                return self.data_store.grep_data(
                    query.data_type,
                    pattern,
                    query.time_range,
                    context_lines=context_lines
                )
            else:
                return self.data_store.query_data(query)
        except Exception as e:
            self.logger.error(f"Data retrieval error: {str(e)}")
            raise
            
    def _queue_analysis(self, data: List[Dict[str, Any]], source: str,
                       context: AnalysisContext) -> str:
        """Queue analysis for processing"""
        analysis_id = str(uuid.uuid4())
        
        with self._lock:
            # Create analysis queue
            self.analysis_queues[analysis_id] = queue.Queue()
            self.active_analyses[analysis_id] = True
            
            # Start analysis thread
            thread = threading.Thread(
                target=self._analysis_worker,
                args=(analysis_id, data, source, context),
                daemon=True
            )
            self.analysis_threads[analysis_id] = thread
            thread.start()
            
        return analysis_id
            
    def _analysis_worker(self, analysis_id: str, data: List[Dict[str, Any]],
                        source: str, context: AnalysisContext) -> None:
        """Worker thread for analysis processing"""
        try:
            # Perform analysis
            analysis = self._analyze_data(data, source, context)
            
            # Generate stream outputs
            crisis_stream = self._generate_crisis_response(
                analysis,
                context
            )
            
            knowledge_stream = self._generate_knowledge_content(
                analysis,
                context
            )
            
            # Send results through bridge
            self.bridge.send_analysis_result(
                analysis_id,
                crisis_stream,
                knowledge_stream,
                context.session_id
            )
            
        except Exception as e:
            self.logger.error(f"Analysis worker error: {str(e)}")
            self.bridge.send_analysis_error(
                analysis_id,
                str(e),
                context.session_id
            )
        finally:
            with self._lock:
                # Cleanup
                self.active_analyses[analysis_id] = False
                self.analysis_queues.pop(analysis_id, None)
                self.analysis_threads.pop(analysis_id, None)
                
    def _analyze_data(self, data: List[Dict[str, Any]], source: str,
                     context: AnalysisContext) -> AnalysisResult:
        """Analyze collected security data"""
        try:
            # Identify patterns
            patterns = self._identify_patterns(data, context)
            
            # Assess threats
            threats = self._assess_threats(data, patterns, context)
            
            # Generate findings
            findings = self._generate_findings(
                data,
                patterns,
                threats,
                context
            )
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                findings,
                threats,
                context
            )
            
            # Generate learning points
            learning_points = self._generate_learning_points(
                findings,
                threats,
                context
            )
            
            return AnalysisResult(
                findings=findings,
                patterns=patterns,
                threats=threats,
                recommendations=recommendations,
                learning_points=learning_points,
                timestamp=datetime.now(),
                session_id=context.session_id
            )
            
        except Exception as e:
            self.logger.error(f"Data analysis error: {str(e)}")
            raise
            
    def _identify_patterns(self, data: List[Dict[str, Any]],
                         context: AnalysisContext) -> List[Dict[str, Any]]:
        """Identify patterns in security data"""
        # TODO: Implement pattern identification with AI analyzer
        return []
        
    def _assess_threats(self, data: List[Dict[str, Any]],
                       patterns: List[Dict[str, Any]],
                       context: AnalysisContext) -> List[Dict[str, Any]]:
        """Assess threats from patterns"""
        # TODO: Implement threat assessment with AI analyzer
        return []
        
    def _generate_findings(self, data: List[Dict[str, Any]],
                         patterns: List[Dict[str, Any]],
                         threats: List[Dict[str, Any]],
                         context: AnalysisContext) -> List[Dict[str, Any]]:
        """Generate security findings"""
        # TODO: Implement finding generation with AI analyzer
        return []
        
    def _generate_recommendations(self, findings: List[Dict[str, Any]],
                                threats: List[Dict[str, Any]],
                                context: AnalysisContext) -> List[str]:
        """Generate security recommendations"""
        # TODO: Implement recommendation generation with AI analyzer
        return []
        
    def _generate_learning_points(self, findings: List[Dict[str, Any]],
                                threats: List[Dict[str, Any]],
                                context: AnalysisContext) -> List[str]:
        """Generate learning points"""
        # TODO: Implement learning point generation with AI analyzer
        return []
        
    def _get_initial_crisis_response(self, analysis_id: str) -> str:
        """Get initial crisis stream response"""
        return f"Starting security analysis {analysis_id}..."
        
    def _get_initial_knowledge_response(self, analysis_id: str) -> str:
        """Get initial knowledge stream response"""
        return f"Preparing analysis context {analysis_id}..."
        
    def _get_fallback_output(self, session_id: str) -> StreamOutput:
        """Generate fallback output for error cases"""
        return StreamOutput(
            crisis="Continuing security monitoring...",
            knowledge="System is analyzing security data...",
            timestamp=datetime.now(),
            metadata={
                'fallback': True,
                'session_id': session_id
            }
        )
        
    def _register_bridge_handlers(self) -> None:
        """Register handlers for bridge messages"""
        self.bridge.register_handler(
            "cancel_analysis",
            self._handle_cancel_analysis
        )
        
    def _handle_cancel_analysis(self, message: Dict[str, Any]) -> None:
        """Handle analysis cancellation request"""
        analysis_id = message.get("analysis_id")
        if not analysis_id:
            return
            
        with self._lock:
            if analysis_id in self.active_analyses:
                self.active_analyses[analysis_id] = False
</rewritten_file> 