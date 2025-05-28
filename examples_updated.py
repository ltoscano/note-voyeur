#!/usr/bin/env python3
"""
Updated Examples for Note Voyeur - macOS Notes Extractor with Reverse Filtering
Shows various ways to use the note extraction tool with new reverse chronological filtering
"""

import subprocess
import sys

def run_example(command, description):
    """Run an example command and show its output"""
    print("\n" + "="*80)
    print(f"EXAMPLE: {description}")
    print("="*80)
    print(f"Command: {command}")
    print("-" * 40)
    
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Command timed out")
    except Exception as e:
        print(f"Error running command: {e}")
    
    print("-" * 40)

def main():
    """Run various examples of note extraction"""
    
    print("NOTE VOYEUR - UPDATED EXAMPLES WITH REVERSE FILTERING")
    print("=" * 80)
    print("This script demonstrates various ways to extract notes from macOS Notes app")
    print("including the new reverse chronological filtering functionality.")
    
    examples = [
        # Basic examples
        ("python3 note_reader.py", "Basic extraction (last 5 notes)"),
        ("python3 note_reader.py -n 10", "Extract last 10 notes"),
        ("python3 note_reader.py --count", "Show statistics and extract notes"),
        ("python3 note_reader.py --stats-only", "Show only statistics, no extraction"),
        
        # Forward filtering (existing functionality)
        ("python3 note_reader.py -d 2024-01-01", "Extract notes from specific date onwards"),
        ("python3 note_reader.py -d 7", "Extract notes from 7 days ago onwards"),
        ("python3 note_reader.py -d 2024-01-15 -n 20", "Extract 20 notes from specific date"),
        ("python3 note_reader.py -d 30 --count", "Extract notes from 30 days ago with statistics"),
        
        # NEW: Reverse filtering (backwards chronological)
        ("python3 note_reader.py -t 2024-01-01", "Extract notes before specific date (reverse filtering)"),
        ("python3 note_reader.py -t 7", "Extract notes before 7 days ago (reverse filtering)"),
        ("python3 note_reader.py -t 2024-12-01 -n 15", "Extract 15 notes before specific date"),
        ("python3 note_reader.py -t 30 --count", "Extract notes before 30 days ago with statistics"),
        
        # Date format variations
        ("python3 note_reader.py -d 01/12/2024", "Forward filtering with DD/MM/YYYY format"),
        ("python3 note_reader.py -t 15/11/2024", "Reverse filtering with DD/MM/YYYY format"),
        
        # Advanced combinations
        ("python3 note_reader.py -d 2024-01-01 -t 2024-12-31", "Extract notes between two dates"),
        ("python3 note_reader.py -t 2024-06-01 -n 50 --count", "Comprehensive reverse extraction with stats"),
    ]
    
    print(f"\nTotal examples to run: {len(examples)}")
    print("Each example will be executed automatically...")
    
    for i, (command, description) in enumerate(examples, 1):
        print(f"\n[{i}/{len(examples)}]")
        run_example(command, description)
        
        # Pause between examples for readability
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "="*80)
    print("ALL EXAMPLES COMPLETED!")
    print("="*80)
    print("\nKey Features Demonstrated:")
    print("✅ Basic note extraction")
    print("✅ Forward chronological filtering (--from-date)")
    print("✅ NEW: Reverse chronological filtering (--to-date)")
    print("✅ Multiple date formats (YYYY-MM-DD, DD/MM/YYYY, days ago)")
    print("✅ Statistics and counting")
    print("✅ Customizable extraction limits")
    print("✅ Automatic JSON export with descriptive filenames")
    
    print("\nNote: Each extraction creates a JSON file with extracted notes.")
    print("Files are automatically named based on filtering criteria used.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError running examples: {e}")
        sys.exit(1)
