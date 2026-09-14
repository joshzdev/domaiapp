#!/usr/bin/env python3
"""
DōmAI Port Scanner Module
Provides intelligent port scanning with real-time analysis and explanation
"""

import json
import socket
import nmap # type: ignore
import logging
import threading
from queue import Queue
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ScanType(Enum):
    QUICK = "quick"       # Quick TCP scan of common ports
    FULL = "full"         # Full TCP port scan
    STEALTH = "stealth"   # SYN scan (requires root)
    SERVICE = "service"   # Service version detection
    VULN = "vuln"        # Vulnerability scan

@dataclass
class PortInfo:
    """Port scan result with context"""
    port: int
    state: str
    service: Optional[str] = None
    version: Optional[str] = None
    cpe: Optional[str] = None  # Common Platform Enumeration
    vulns: List[Dict] = None
    context: Dict = None       # Additional context about the port/service

@dataclass
class ScanResult:
    """Complete scan result for a target"""
    target: str
    scan_type: ScanType
    timestamp: datetime
    ports: List[PortInfo]
    metadata: Dict
    raw_output: str

class PortScanner:
    """Intelligent port scanner with natural language analysis"""
    
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.scan_queue = Queue()
        self.scan_thread = None
        self.should_scan = False
        self.common_ports = {
            80: "Web server (HTTP)",
            443: "Secure web server (HTTPS)",
            22: "SSH remote access",
            21: "FTP file transfer",
            25: "Email server (SMTP)",
            53: "DNS server",
            3389: "Remote Desktop",
            445: "Microsoft-DS (File sharing)",
            139: "NetBIOS",
            23: "Telnet",
        }
        
        # Port categories for context
        self.port_categories = {
            "web": [80, 443, 8080, 8443],
            "email": [25, 110, 143, 587, 993],
            "database": [1433, 3306, 5432, 27017],
            "remote_access": [22, 23, 3389, 5900],
            "file_sharing": [21, 445, 139, 2049],
        }
        
    def scan_target(
        self, 
        target: str, 
        scan_type: ScanType = ScanType.QUICK,
        ports: Optional[str] = None,
        callback: Optional[callable] = None
    ) -> ScanResult:
        """Perform port scan with real-time analysis"""
        try:
            # Build nmap arguments
            args = self._build_nmap_args(scan_type, ports)
            
            # Run scan
            raw_output = self._run_scan(target, args)
            
            # Parse results
            ports_info = self._parse_scan_results(target)
            
            # Add context to results
            self._enrich_port_info(ports_info)
            
            result = ScanResult(
                target=target,
                scan_type=scan_type,
                timestamp=datetime.now(),
                ports=ports_info,
                metadata={"args": args},
                raw_output=raw_output
            )
            
            # Call callback if provided
            if callback:
                callback(result)
                
            return result
            
        except Exception as e:
            logging.error(f"Scan failed: {str(e)}")
            raise
            
    def analyze_scan(self, result: ScanResult, user_level: str) -> Tuple[str, str]:
        """Generate dual-stream analysis of scan results"""
        try:
            # Crisis stream - immediate security concerns
            crisis = self._generate_crisis_analysis(result)
            
            # Knowledge stream - educational context
            knowledge = self._generate_knowledge_analysis(result, user_level)
            
            return crisis, knowledge
            
        except Exception as e:
            logging.error(f"Analysis failed: {str(e)}")
            return self._get_fallback_analysis()
            
    def start_continuous_scan(
        self,
        target: str,
        scan_type: ScanType = ScanType.QUICK,
        interval: int = 300,  # 5 minutes
        callback: Optional[callable] = None
    ) -> None:
        """Start continuous scanning thread"""
        if self.scan_thread and self.scan_thread.is_alive():
            raise RuntimeError("Continuous scan already running")
            
        self.should_scan = True
        self.scan_thread = threading.Thread(
            target=self._continuous_scan_loop,
            args=(target, scan_type, interval, callback),
            daemon=True
        )
        self.scan_thread.start()
        
    def stop_continuous_scan(self) -> None:
        """Stop continuous scanning"""
        self.should_scan = False
        if self.scan_thread:
            self.scan_thread.join(timeout=5)
            self.scan_thread = None
            
    def _continuous_scan_loop(
        self,
        target: str,
        scan_type: ScanType,
        interval: int,
        callback: Optional[callable]
    ) -> None:
        """Background scanning loop"""
        while self.should_scan:
            try:
                result = self.scan_target(target, scan_type)
                if callback:
                    callback(result)
            except Exception as e:
                logging.error(f"Continuous scan error: {str(e)}")
            finally:
                # Sleep for interval
                for _ in range(interval):
                    if not self.should_scan:
                        break
                    threading.Event().wait(1)
            
    def _build_nmap_args(self, scan_type: ScanType, ports: Optional[str]) -> str:
        """Build appropriate nmap arguments"""
        args = []
        
        if scan_type == ScanType.QUICK:
            args.extend(["-F", "-T4"])  # Fast scan of common ports
        elif scan_type == ScanType.FULL:
            args.extend(["-p-", "-T4"])  # All ports
        elif scan_type == ScanType.STEALTH:
            args.extend(["-sS", "-T4"])  # SYN scan
        elif scan_type == ScanType.SERVICE:
            args.extend(["-sV", "-T4"])  # Version detection
        elif scan_type == ScanType.VULN:
            args.extend(["-sV", "--script vuln", "-T4"])  # Vuln scan
            
        if ports:
            args.extend(["-p", ports])
            
        return " ".join(args)
        
    def _run_scan(self, target: str, args: str) -> str:
        """Run nmap scan"""
        try:
            self.nm.scan(hosts=target, arguments=args)
            return self.nm.get_nmap_last_output()
        except Exception as e:
            logging.error(f"Scan execution failed: {str(e)}")
            raise
            
    def _parse_scan_results(self, target: str) -> List[PortInfo]:
        """Parse nmap results into structured data"""
        ports_info = []
        
        try:
            # Get scan data for target
            if target not in self.nm.all_hosts():
                return ports_info
                
            host = self.nm[target]
            
            # Parse each protocol
            for proto in host.all_protocols():
                ports = host[proto].keys()
                
                for port in ports:
                    port_data = host[proto][port]
                    
                    port_info = PortInfo(
                        port=port,
                        state=port_data["state"],
                        service=port_data.get("name"),
                        version=port_data.get("version"),
                        cpe=port_data.get("cpe", []),
                        vulns=[],
                        context={},
                    )
                    
                    ports_info.append(port_info)
                    
            return ports_info
            
        except Exception as e:
            logging.error(f"Results parsing failed: {str(e)}")
            return ports_info
            
    def _enrich_port_info(self, ports_info: List[PortInfo]):
        """Add context and categorization to port information"""
        for port_info in ports_info:
            # Add common port description
            if port_info.port in self.common_ports:
                port_info.context["description"] = self.common_ports[port_info.port]
                
            # Add category
            for category, ports in self.port_categories.items():
                if port_info.port in ports:
                    port_info.context["category"] = category
                    break
                    
            # Add security notes
            self._add_security_context(port_info)
            
    def _add_security_context(self, port_info: PortInfo):
        """Add security-relevant context to port"""
        context = port_info.context
        
        # Check for sensitive services
        if port_info.port in [22, 23, 3389]:
            context["security_note"] = "Remote access service - ensure strong authentication"
        elif port_info.port in [80, 443]:
            context["security_note"] = "Web service - check for security headers and HTTPS"
        elif port_info.port in [139, 445]:
            context["security_note"] = "File sharing service - verify access controls"
            
    def _generate_crisis_analysis(self, result: ScanResult) -> str:
        """Generate crisis stream analysis focusing on security issues"""
        issues = []
        
        # Check for high-risk open ports
        high_risk_ports = [23, 139, 445]  # telnet, NetBIOS, SMB
        for port_info in result.ports:
            if port_info.state == "open":
                if port_info.port in high_risk_ports:
                    issues.append(f"High-risk port {port_info.port} ({port_info.service}) is open")
                    
        # Check for version information
        unidentified = [p for p in result.ports 
                       if p.state == "open" and not p.version]
        if unidentified:
            issues.append(f"Unable to identify versions for {len(unidentified)} services")
            
        # Format crisis output
        if issues:
            return "Security Concerns Found:\n" + "\n".join(f"- {issue}" for issue in issues)
        return "No immediate security concerns found in port scan"
        
    def _generate_knowledge_analysis(self, result: ScanResult, user_level: str) -> str:
        """Generate educational knowledge stream based on user level"""
        knowledge = []
        
        # Basic port information
        open_ports = [p for p in result.ports if p.state == "open"]
        if user_level == "beginner":
            knowledge.append(f"Found {len(open_ports)} open ports")
            for port in open_ports:
                if port.port in self.common_ports:
                    knowledge.append(f"Port {port.port}: {self.common_ports[port.port]}")
                    
        # More detailed for intermediate users
        elif user_level == "intermediate":
            categories = {}
            for port in open_ports:
                category = next((c for c, ports in self.port_categories.items() 
                               if port.port in ports), "other")
                if category not in categories:
                    categories[category] = []
                categories[category].append(port)
                
            for category, ports in categories.items():
                knowledge.append(f"\n{category.title()} Services:")
                for port in ports:
                    service_info = f"Port {port.port}"
                    if port.service:
                        service_info += f" ({port.service})"
                    if port.version:
                        service_info += f" version {port.version}"
                    knowledge.append(f"- {service_info}")
                    
        # Advanced includes security context
        else:
            knowledge.extend(self._generate_advanced_analysis(open_ports))
            
        return "\n".join(knowledge)
        
    def _generate_advanced_analysis(self, open_ports: List[PortInfo]) -> List[str]:
        """Generate advanced analysis with security context"""
        analysis = []
        
        # Group by security risk
        high_risk = []
        medium_risk = []
        low_risk = []
        
        for port in open_ports:
            if port.port in [23, 139, 445]:  # High risk
                high_risk.append(port)
            elif port.port in [21, 80, 3389]:  # Medium risk
                medium_risk.append(port)
            else:
                low_risk.append(port)
                
        # Format analysis
        if high_risk:
            analysis.append("\nHigh Risk Services:")
            for port in high_risk:
                analysis.append(f"- Port {port.port}: {port.context.get('security_note', '')}")
                
        if medium_risk:
            analysis.append("\nMedium Risk Services:")
            for port in medium_risk:
                analysis.append(f"- Port {port.port}: {port.context.get('security_note', '')}")
                
        if low_risk:
            analysis.append("\nLow Risk Services:")
            for port in low_risk:
                analysis.append(f"- Port {port.port}: {port.service or 'Unknown service'}")
                
        return analysis
        
    def _get_fallback_analysis(self) -> Tuple[str, str]:
        """Generate fallback analysis when normal analysis fails"""
        return (
            "Unable to generate security analysis",
            "Port scan completed but analysis failed"
        )
