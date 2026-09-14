"""
DōmAI - Main Entry Point
Launches either CLI or UI mode
"""

import sys
import argparse

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DōmAI - MacOS Security Assistant")
    parser.add_argument(
        "--cli",
        action="store_true",
        help="Run in CLI mode (default: UI mode)"
    )
    
    args = parser.parse_args()
    
    if args.cli:
        from .main import main as cli_main
        cli_main()
    else:
        from .ui.main_window import launch_ui
        launch_ui()

if __name__ == "__main__":
    main() 