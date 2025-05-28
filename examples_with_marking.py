#!/usr/bin/env python3
"""
Examples demonstrating the NOTE-VOYEUR marking functionality.
The --mark option adds "NOTE-VOYEUR: TARGET ACQUIRED!" to note titles.
"""

import subprocess
import time

def run_example(description, command):
    """Run an example command with description"""
    print(f"\n{'='*80}")
    print(f"EXAMPLE: {description}")
    print(f"COMMAND: {command}")
    print(f"{'='*80}")
    
    try:
        result = subprocess.run(command.split(), capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.stderr:
            print(f"Warnings/Errors: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Command timed out after 60 seconds")
    except Exception as e:
        print(f"Error running command: {e}")
    
    # Small delay between examples
    time.sleep(1)

def main():
    print("NOTE-VOYEUR MARKING FUNCTIONALITY EXAMPLES")
    print("==========================================")
    print()
    print("This script demonstrates the --mark option that adds")
    print("'NOTE-VOYEUR: TARGET ACQUIRED!' to note titles.")
    print()
    print("⚠️  WARNING: This will MODIFY your actual Notes!")
    print("Make sure you have backups of important notes.")
    print()
    
    response = input("Do you want to proceed with marking examples? (y/N): ")
    if response.lower() != 'y':
        print("Examples cancelled. No notes will be modified.")
        return
    
    # Example 1: Basic marking of recent notes
    run_example(
        "Mark the last 2 notes with VOYEUR tag",
        "python3 note_reader.py -n 2 --mark"
    )
    
    # Example 2: Mark with statistics
    run_example(
        "Mark recent notes with statistics",
        "python3 note_reader.py -n 3 --mark -c"
    )
    
    # Example 3: Mark with tag filtering
    run_example(
        "Mark notes containing 'AI' in title or body",
        "python3 note_reader.py --filter-tag AI -n 3 --mark"
    )
    
    # Example 4: Mark with date filtering
    run_example(
        "Mark notes from the last 7 days",
        "python3 note_reader.py -d 7 -n 5 --mark"
    )
    
    # Example 5: Mark with range and tag filtering
    run_example(
        "Mark notes from April 2025 containing 'WPE'",
        "python3 note_reader.py -d 2025-04-01 -t 2025-04-30 --filter-tag WPE -n 5 --mark"
    )
    
    # Example 6: Attempt to mark already marked notes (should skip)
    run_example(
        "Try to mark already marked notes (should skip them)",
        "python3 note_reader.py -n 2 --mark"
    )
    
    # Example 7: Statistics only with marking info
    run_example(
        "Show statistics for recent notes (no marking performed)",
        "python3 note_reader.py -d 3 --stats-only"
    )
    
    print(f"\n{'='*80}")
    print("MARKING EXAMPLES COMPLETED")
    print("='*80")
    print()
    print("Key features demonstrated:")
    print("✅ Basic note marking with VOYEUR tag")
    print("✅ Marking with statistics display")
    print("✅ Combining marking with tag filtering")
    print("✅ Combining marking with date filtering")
    print("✅ Complex filtering with range + tag + marking")
    print("✅ Automatic skip of already marked notes")
    print("✅ Filename generation includes '_marked' suffix")
    print()
    print("All marked notes are saved to JSON files with descriptive names.")
    print("Check your Notes app to see the marked notes with 'NOTE-VOYEUR: TARGET ACQUIRED!' prefix.")

if __name__ == "__main__":
    main()
