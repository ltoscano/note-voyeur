#!/usr/bin/env python3
"""
Note Voyeur - Enhanced Examples with Tag Filtering
Demonstrates all filtering capabilities including the new tag filtering feature
"""

import subprocess
import time
from datetime import datetime


def run_command(description, command):
    """Run a command and display results"""
    print(f"\n{'='*60}")
    print(f"EXAMPLE: {description}")
    print(f"COMMAND: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("Command timed out after 60 seconds")
    except Exception as e:
        print(f"Error running command: {e}")
    
    # Wait a bit between commands
    time.sleep(2)


def main():
    """
    Run comprehensive examples of the note-voyeur functionality
    """
    print("🚀 NOTE VOYEUR - COMPREHENSIVE EXAMPLES WITH TAG FILTERING")
    print("=" * 70)
    print("This script demonstrates all filtering capabilities:")
    print("✅ Basic extraction")
    print("✅ Forward filtering (--from-date)")
    print("✅ Reverse filtering (--to-date)")
    print("✅ Range filtering (--from-date + --to-date)")
    print("✅ NEW: Tag filtering (--filter-tag)")
    print("✅ NEW: Combined filtering (date + tag)")
    print("✅ Statistics and counting")
    print("=" * 70)
    
    # Basic Examples
    run_command(
        "Basic extraction - Last 3 notes",
        "python3 note_reader.py -n 3"
    )
    
    run_command(
        "Statistics only - Show total notes count",
        "python3 note_reader.py --stats-only"
    )
    
    # Forward Filtering Examples
    run_command(
        "Forward filtering - Notes from 7 days ago with statistics",
        "python3 note_reader.py -d 7 -n 5 -c"
    )
    
    run_command(
        "Forward filtering - Notes from specific date",
        "python3 note_reader.py -d 2025-05-01 -n 3"
    )
    
    # Reverse Filtering Examples
    run_command(
        "Reverse filtering - Notes before 30 days ago",
        "python3 note_reader.py -t 30 -n 3 -c"
    )
    
    run_command(
        "Reverse filtering - Statistics for notes before specific date",
        "python3 note_reader.py -t 2025-04-30 --stats-only"
    )
    
    # Range Filtering Examples
    run_command(
        "Range filtering - Notes from April 2025 only",
        "python3 note_reader.py -d 2025-04-01 -t 2025-04-30 -n 5 -c"
    )
    
    # TAG FILTERING EXAMPLES (NEW!)
    run_command(
        "Tag filtering - Notes containing 'AI' anywhere in title or body",
        "python3 note_reader.py --filter-tag 'AI' -n 5 -c"
    )
    
    run_command(
        "Tag filtering - Case-insensitive search for 'python'",
        "python3 note_reader.py --filter-tag 'python' -n 10"
    )
    
    run_command(
        "Tag filtering - Search for 'https' (finding notes with links)",
        "python3 note_reader.py --filter-tag 'https' -n 3"
    )
    
    # COMBINED FILTERING EXAMPLES (NEW!)
    run_command(
        "Combined filtering - Recent notes containing 'script'",
        "python3 note_reader.py --filter-tag 'script' -d 7 -n 5 -c"
    )
    
    run_command(
        "Combined filtering - April 2025 notes containing 'WPE'",
        "python3 note_reader.py -d 2025-04-01 -t 2025-04-30 --filter-tag 'WPE' -n 3 -c"
    )
    
    run_command(
        "Combined filtering - Old notes containing 'Agent' before 30 days ago",
        "python3 note_reader.py -t 30 --filter-tag 'Agent' -n 5"
    )
    
    # Advanced Examples
    run_command(
        "Advanced - Find all notes with specific tag in a date range",
        "python3 note_reader.py -d 2025-04-01 -t 2025-05-31 --filter-tag 'h1' -n 10 -c"
    )
    
    print(f"\n{'='*70}")
    print("🎉 ALL EXAMPLES COMPLETED!")
    print("=" * 70)
    print("Key Features Demonstrated:")
    print("• Basic note extraction with limits")
    print("• Date-based filtering (forward, reverse, range)")
    print("• NEW: Tag/content filtering (case-insensitive)")
    print("• NEW: Combined date + tag filtering")
    print("• Statistics and counting capabilities")
    print("• Automatic JSON export with descriptive filenames")
    print("• Performance optimization for large note collections")
    print(f"\nScript completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
