"""
DōmAI Command Line Interface
Dual-stream interface with flexible output control
"""

import click
import json
import subprocess
import shlex
import sys
import threading
import queue
from pathlib import Path
from typing import Dict, Any, Optional, List, TextIO
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from .core.app import DomaiApp
from .core.analysis_pipeline import AnalysisScope
from .security.data_store import TimeRange

# Global application instance
app = DomaiApp()

class StreamConfig:
    """Configuration for output streams"""
    def __init__(self):
        self.crisis_stream = sys.stdout
        self.education_stream = sys.stdout
        self.education_file = None
        self.show_education = True
        
    def set_education_file(self, filepath: str):
        """Set file for educational content"""
        self.education_file = open(filepath, 'a')
        self.education_stream = self.education_file
        
    def close(self):
        """Clean up file handles"""
        if self.education_file:
            self.education_file.close()

# Global stream configuration
stream_config = StreamConfig()

@click.group()
def cli():
    """DōmAI - Just tell me what you need"""
    pass

@cli.command()
@click.argument('request', nargs=-1)
@click.option('--quiet', '-q', is_flag=True, help='Hide educational content from terminal')
@click.option('--education-file', '-f', help='Save educational content to file')
def help(request: tuple, quiet: bool, education_file: Optional[str]):
    """Just tell me what you need help with
    
    Examples:
    \b
    # Immediate help
    domai help my network activity is high
    
    # Hide educational content from terminal
    domai help -q my cpu is maxed out
    
    # Save educational content to file
    domai help -f learning.txt suspicious process running
    
    # Both quiet and save to file
    domai help -q -f learning.txt what is accessing my camera
    """
    # Configure streams
    if quiet:
        stream_config.show_education = False
    if education_file:
        stream_config.set_education_file(education_file)
    
    try:
        query = ' '.join(request)
        
        # Handle streams using threads
        _handle_streams(query)
    finally:
        # Cleanup
        stream_config.close()

def _handle_streams(query: str):
    """Handle both crisis and educational streams"""
    # Set up streaming response
    crisis_queue = queue.Queue()
    education_queue = queue.Queue()
    
    # Start the crisis and education streams
    producer_thread = threading.Thread(
        target=app.stream_response,
        args=(query, crisis_queue, education_queue),
        daemon=True
    )
    
    crisis_thread = threading.Thread(
        target=_handle_crisis_stream,
        args=(crisis_queue,),
        daemon=True
    )
    
    education_thread = threading.Thread(
        target=_handle_education_stream,
        args=(education_queue,),
        daemon=True
    )
    
    # Start all threads
    producer_thread.start()
    crisis_thread.start()
    education_thread.start()
    
    # Wait for all threads to complete
    producer_thread.join()
    crisis_thread.join()
    education_thread.join()

def _handle_crisis_stream(queue_obj: queue.Queue):
    """Handle crisis stream output"""
    while True:
        try:
            msg = queue_obj.get(timeout=1)  # 1 second timeout
            if msg is None:  # End of stream
                break
                
            if isinstance(msg, dict):
                if msg.get('type') == 'command':
                    # Execute command
                    cmd = msg['command']
                    click.echo(f"\n$ {cmd}", file=stream_config.crisis_stream)
                    try:
                        output = subprocess.check_output(
                            shlex.split(cmd),
                            stderr=subprocess.STDOUT,
                            text=True
                        )
                        click.echo(output, file=stream_config.crisis_stream)
                    except subprocess.CalledProcessError as e:
                        click.echo(f"Error: {e.output}", file=stream_config.crisis_stream)
                        
                elif msg.get('type') == 'analysis':
                    click.echo(f"\nAnalysis:", file=stream_config.crisis_stream)
                    click.echo(msg['content'], file=stream_config.crisis_stream)
                    
                elif msg.get('type') == 'action':
                    click.echo(f"\nRecommended Action:", file=stream_config.crisis_stream)
                    click.echo(f"- {msg['content']}", file=stream_config.crisis_stream)
            else:
                click.echo(msg, file=stream_config.crisis_stream)
                
            queue_obj.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            click.echo(f"Error in crisis stream: {str(e)}", file=sys.stderr)
            break

def _handle_education_stream(queue_obj: queue.Queue):
    """Handle educational stream output"""
    while True:
        try:
            msg = queue_obj.get(timeout=1)  # 1 second timeout
            if msg is None:  # End of stream
                break
                
            # Write to education stream if enabled
            if stream_config.show_education or stream_config.education_file:
                if isinstance(msg, dict):
                    if msg.get('type') == 'concept':
                        click.echo(f"\nConcept:", file=stream_config.education_stream)
                        click.echo(msg['content'], file=stream_config.education_stream)
                        
                    elif msg.get('type') == 'explanation':
                        click.echo(f"\nExplanation:", file=stream_config.education_stream)
                        click.echo(msg['content'], file=stream_config.education_stream)
                        
                    elif msg.get('type') == 'resource':
                        click.echo(f"\nResource:", file=stream_config.education_stream)
                        click.echo(f"- {msg['content']}", file=stream_config.education_stream)
                else:
                    click.echo(msg, file=stream_config.education_stream)
                    
            queue_obj.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            click.echo(f"Error in education stream: {str(e)}", file=sys.stderr)
            break

@cli.command()
@click.argument('command', nargs=-1)
@click.option('--quiet', '-q', is_flag=True, help='Hide educational content')
@click.option('--education-file', '-f', help='Save educational content to file')
def run(command: tuple, quiet: bool, education_file: Optional[str]):
    """Run commands with real-time dual stream output
    
    Examples:
    \b
    # Run with both streams
    domai run tcpdump -i any
    
    # Hide educational content
    domai run -q netstat -an
    
    # Save education to file
    domai run -f learning.txt ps aux
    """
    # Configure streams
    if quiet:
        stream_config.show_education = False
    if education_file:
        stream_config.set_education_file(education_file)
    
    try:
        cmd = ' '.join(command)
        _handle_command_streams(cmd)
    finally:
        stream_config.close()

def _handle_command_streams(cmd: str):
    """Handle streaming for command execution"""
    crisis_queue = queue.Queue()
    education_queue = queue.Queue()
    
    # Start command execution with streaming
    producer_thread = threading.Thread(
        target=app.stream_command_execution,
        args=(cmd, crisis_queue, education_queue),
        daemon=True
    )
    
    crisis_thread = threading.Thread(
        target=_handle_crisis_stream,
        args=(crisis_queue,),
        daemon=True
    )
    
    education_thread = threading.Thread(
        target=_handle_education_stream,
        args=(education_queue,),
        daemon=True
    )
    
    # Start all threads
    producer_thread.start()
    crisis_thread.start()
    education_thread.start()
    
    # Wait for all threads to complete
    producer_thread.join()
    crisis_thread.join()
    education_thread.join()

def main():
    """Main entry point"""
    try:
        cli()
    finally:
        # Ensure cleanup
        stream_config.close()

if __name__ == "__main__":
    main() 