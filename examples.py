#!/usr/bin/env python3
"""
Note Voyeur Examples - Usage examples for the note extraction tool
"""

import subprocess
import sys
from datetime import datetime, timedelta

def run_example(description, command):
    """Run an example command and display results"""
    print(f"\n{'='*60}")
    print(f"EXAMPLE: {description}")
    print(f"COMMAND: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
    except Exception as e:
        print(f"Error running example: {e}")

def main():
    """Run various usage examples"""
    print("NOTE VOYEUR - Usage Examples")
    print("Run these examples to see different ways to extract notes")
    
    # Example 1: Basic usage
    run_example(
        "Extract last 5 notes (default)",
        "python3 note_reader.py"
    )
    
    # Example 2: Extract more notes
    run_example(
        "Extract last 10 notes",
        "python3 note_reader.py -n 10"
    )
    
    # Example 3: Extract notes from specific date
    run_example(
        "Extract notes from 7 days ago",
        "python3 note_reader.py -d 7 -n 20"
    )
    
    # Example 4: Extract notes from specific date (format YYYY-MM-DD)
    last_week = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    run_example(
        f"Extract notes from {last_week}",
        f"python3 note_reader.py -d {last_week} -n 15"
    )
    
    # Example 5: Just show statistics
    run_example(
        "Show statistics only",
        "python3 note_reader.py --stats-only"
    )
    
    # Example 6: Show count and extract
    run_example(
        "Show count and extract notes from 3 days ago",
        "python3 note_reader.py -d 3 -n 5 -c"
    )

if __name__ == "__main__":
    main()
