#!/usr/bin/env python3
"""
Note Reader for macOS Notes App
Reads and displays all notes from the default Notes account
"""

import subprocess
import json
from datetime import datetime, timedelta
import argparse


def read_all_notes(limit=10):
    """
    Reads the latest notes from macOS Notes app using AppleScript
    Returns a string with note information
    """
    script = f'''
    tell application "Notes"
        set noteList to ""
        set noteCount to 0
        repeat with n in notes of default account
            set noteCount to noteCount + 1
            if noteCount > {limit} then exit repeat
            set noteList to noteList & the name of n & " -> " & the body of n & "\n"
        end repeat
        return noteList
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        else:
            print(f"Error executing AppleScript: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print("AppleScript execution timed out after 30 seconds")
        return None
    except Exception as e:
        print(f"Error running subprocess: {e}")
        return None


def read_notes_with_filters(limit=5, from_date=None, to_date=None, filter_tag=None):
    """
    Reads notes from macOS Notes app with date and limit filters
    Returns individual note data filtered by date and limited by count
    
    Args:
        limit: Maximum number of notes to return
        from_date: Only return notes modified on or after this date (forward filtering)
        to_date: Only return notes modified before this date (reverse filtering)
        filter_tag: Only return notes containing this string in title or body (case-insensitive)
    """
    # If no dates specified, use current date minus 30 days as reasonable default
    if from_date is None and to_date is None:
        from_date = datetime.now() - timedelta(days=30)
    
    # AppleScript with dynamic filtering
    if from_date is not None and to_date is not None:
        # Range filtering script
        script = f'''
        tell application "Notes"
            set noteData to {{}}
            set noteCount to 0
            set processedCount to 0
            
            repeat with n in notes of default account
                set processedCount to processedCount + 1
                
                try
                    set fromFilterDate to current date
                    set day of fromFilterDate to {from_date.day}
                    set month of fromFilterDate to {from_date.month}
                    set year of fromFilterDate to {from_date.year}
                    set hours of fromFilterDate to 0
                    set minutes of fromFilterDate to 0
                    set seconds of fromFilterDate to 0
                    
                    set toFilterDate to current date
                    set day of toFilterDate to {to_date.day}
                    set month of toFilterDate to {to_date.month}
                    set year of toFilterDate to {to_date.year}
                    set hours of toFilterDate to 23
                    set minutes of toFilterDate to 59
                    set seconds of toFilterDate to 59
                    
                    set noteModDate to modification date of n
                    if noteModDate ≥ fromFilterDate and noteModDate ≤ toFilterDate then
                        set noteCount to noteCount + 1
                        if noteCount > {limit} then exit repeat
                        set noteInfo to (name of n) & "|" & (body of n) & "|" & (creation date of n) & "|" & (modification date of n)
                        set end of noteData to noteInfo
                    end if
                on error
                    -- Skip notes that can't be read
                end try
                
                -- Limit processing to avoid timeout (check only first 500 notes)
                if processedCount > 500 then exit repeat
            end repeat
            
            set AppleScript's text item delimiters to "~~~"
            set noteDataString to noteData as string
            set AppleScript's text item delimiters to ""
            return noteDataString
        end tell
        '''
    elif from_date is not None:
        # Forward filtering script
        script = f'''
        tell application "Notes"
            set noteData to {{}}
            set noteCount to 0
            set processedCount to 0
            
            repeat with n in notes of default account
                set processedCount to processedCount + 1
                
                try
                    set filterDate to current date
                    set day of filterDate to {from_date.day}
                    set month of filterDate to {from_date.month}
                    set year of filterDate to {from_date.year}
                    set hours of filterDate to 0
                    set minutes of filterDate to 0
                    set seconds of filterDate to 0
                    
                    set noteModDate to modification date of n
                    if noteModDate ≥ filterDate then
                        set noteCount to noteCount + 1
                        if noteCount > {limit} then exit repeat
                        set noteInfo to (name of n) & "|" & (body of n) & "|" & (creation date of n) & "|" & (modification date of n)
                        set end of noteData to noteInfo
                    end if
                on error
                    -- Skip notes that can't be read
                end try
                
                -- Limit processing to avoid timeout (check only first 500 notes)
                if processedCount > 500 then exit repeat
            end repeat
            
            set AppleScript's text item delimiters to "~~~"
            set noteDataString to noteData as string
            set AppleScript's text item delimiters to ""
            return noteDataString
        end tell
        '''
    elif to_date is not None:
        # Reverse filtering script
        script = f'''
        tell application "Notes"
            set noteData to {{}}
            set noteCount to 0
            set processedCount to 0
            
            repeat with n in notes of default account
                set processedCount to processedCount + 1
                
                try
                    set filterDate to current date
                    set day of filterDate to {to_date.day}
                    set month of filterDate to {to_date.month}
                    set year of filterDate to {to_date.year}
                    set hours of filterDate to 23
                    set minutes of filterDate to 59
                    set seconds of filterDate to 59
                    
                    set noteModDate to modification date of n
                    if noteModDate < filterDate then
                        set noteCount to noteCount + 1
                        if noteCount > {limit} then exit repeat
                        set noteInfo to (name of n) & "|" & (body of n) & "|" & (creation date of n) & "|" & (modification date of n)
                        set end of noteData to noteInfo
                    end if
                on error
                    -- Skip notes that can't be read
                end try
                
                -- Limit processing to avoid timeout (check only first 500 notes)
                if processedCount > 500 then exit repeat
            end repeat
            
            set AppleScript's text item delimiters to "~~~"
            set noteDataString to noteData as string
            set AppleScript's text item delimiters to ""
            return noteDataString
        end tell
        '''
    else:
        # No date filtering script
        script = f'''
        tell application "Notes"
            set noteData to {{}}
            set noteCount to 0
            set processedCount to 0
            
            repeat with n in notes of default account
                set processedCount to processedCount + 1
                
                try
                    set noteCount to noteCount + 1
                    if noteCount > {limit} then exit repeat
                    set noteInfo to (name of n) & "|" & (body of n) & "|" & (creation date of n) & "|" & (modification date of n)
                    set end of noteData to noteInfo
                on error
                    -- Skip notes that can't be read
                end try
                
                -- Limit processing to avoid timeout (check only first 500 notes)
                if processedCount > 500 then exit repeat
            end repeat
            
            set AppleScript's text item delimiters to "~~~"
            set noteDataString to noteData as string
            set AppleScript's text item delimiters to ""
            return noteDataString
        end tell
        '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            notes = []
            note_strings = result.stdout.strip().split("~~~")
            
            for note_string in note_strings:
                if note_string.strip():
                    parts = note_string.split("|", 3)
                    if len(parts) >= 4:
                        note = {
                            "title": parts[0].strip(),
                            "body": parts[1].strip(),
                            "created": parts[2].strip(),
                            "modified": parts[3].strip()
                        }
                        notes.append(note)
            
            # Apply tag filter if specified
            if filter_tag:
                filtered_notes = []
                filter_tag_lower = filter_tag.lower()
                for note in notes:
                    # Check if filter_tag is in title or body (case-insensitive)
                    title_lower = note["title"].lower()
                    body_lower = note["body"].lower()
                    if filter_tag_lower in title_lower or filter_tag_lower in body_lower:
                        filtered_notes.append(note)
                notes = filtered_notes
            
            return notes
        else:
            print(f"Error executing AppleScript: {result.stderr}")
            return []
    except subprocess.TimeoutExpired:
        print("AppleScript execution timed out after 60 seconds")
        return []
    except Exception as e:
        print(f"Error running subprocess: {e}")
        return []


def read_notes_structured(limit=10):
    """
    Reads notes in a more structured way, returning individual note data
    Original function for backward compatibility
    """
    script = f'''
    tell application "Notes"
        set noteData to {{}}
        set noteCount to 0
        repeat with n in notes of default account
            set noteCount to noteCount + 1
            if noteCount > {limit} then exit repeat
            set noteInfo to (name of n) & "|" & (body of n) & "|" & (creation date of n) & "|" & (modification date of n)
            set end of noteData to noteInfo
        end repeat
        set AppleScript's text item delimiters to "~~~"
        set noteDataString to noteData as string
        set AppleScript's text item delimiters to ""
        return noteDataString
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            notes = []
            note_strings = result.stdout.strip().split("~~~")
            
            for note_string in note_strings:
                if note_string.strip():
                    parts = note_string.split("|", 3)
                    if len(parts) >= 4:
                        note = {
                            "title": parts[0].strip(),
                            "body": parts[1].strip(),
                            "created": parts[2].strip(),
                            "modified": parts[3].strip()
                        }
                        notes.append(note)
            
            return notes
        else:
            print(f"Error executing AppleScript: {result.stderr}")
            return []
    except subprocess.TimeoutExpired:
        print("AppleScript execution timed out after 30 seconds")
        return []
    except Exception as e:
        print(f"Error running subprocess: {e}")
        return []


def count_total_notes():
    """
    Count total number of notes in the Notes app
    """
    script = '''
    tell application "Notes"
        return count of notes of default account
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            print(f"Error counting notes: {result.stderr}")
            return 0
    except Exception as e:
        print(f"Error counting notes: {e}")
        return 0


def count_notes_from_date(from_date):
    """
    Count notes modified from a specific date
    """
    if from_date is None:
        from_date = datetime.now() - timedelta(days=30)
    
    script = f'''
    tell application "Notes"
        set noteCount to 0
        set processedCount to 0
        
        set filterDate to current date
        set day of filterDate to {from_date.day}
        set month of filterDate to {from_date.month}
        set year of filterDate to {from_date.year}
        set hours of filterDate to 0
        set minutes of filterDate to 0
        set seconds of filterDate to 0
        
        repeat with n in notes of default account
            set processedCount to processedCount + 1
            try
                set noteModDate to modification date of n
                if noteModDate ≥ filterDate then
                    set noteCount to noteCount + 1
                end if
            on error
                -- Skip notes that can't be read
            end try
            
            -- Limit processing to avoid timeout (check only first 500 notes)
            if processedCount > 500 then exit repeat
        end repeat
        
        return noteCount
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            print(f"Error counting notes from date: {result.stderr}")
            return 0
    except Exception as e:
        print(f"Error counting notes from date: {e}")
        return 0


def count_notes_to_date(to_date):
    """
    Count notes modified before a specific date (reverse filtering)
    """
    if to_date is None:
        return 0
    
    script = f'''
    tell application "Notes"
        set noteCount to 0
        set processedCount to 0
        
        set filterDate to current date
        set day of filterDate to {to_date.day}
        set month of filterDate to {to_date.month}
        set year of filterDate to {to_date.year}
        set hours of filterDate to 23
        set minutes of filterDate to 59
        set seconds of filterDate to 59
        
        repeat with n in notes of default account
            set processedCount to processedCount + 1
            try
                set noteModDate to modification date of n
                if noteModDate < filterDate then
                    set noteCount to noteCount + 1
                end if
            on error
                -- Skip notes that can't be read
            end try
            
            -- Limit processing to avoid timeout (check only first 500 notes)
            if processedCount > 500 then exit repeat
        end repeat
        
        return noteCount
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            print(f"Error counting notes to date: {result.stderr}")
            return 0
    except Exception as e:
        print(f"Error counting notes to date: {e}")
        return 0


def count_notes_in_range(from_date, to_date):
    """
    Count notes modified within a date range
    """
    if from_date is None or to_date is None:
        return 0
    
    script = f'''
    tell application "Notes"
        set noteCount to 0
        set processedCount to 0
        
        set fromFilterDate to current date
        set day of fromFilterDate to {from_date.day}
        set month of fromFilterDate to {from_date.month}
        set year of fromFilterDate to {from_date.year}
        set hours of fromFilterDate to 0
        set minutes of fromFilterDate to 0
        set seconds of fromFilterDate to 0
        
        set toFilterDate to current date
        set day of toFilterDate to {to_date.day}
        set month of toFilterDate to {to_date.month}
        set year of toFilterDate to {to_date.year}
        set hours of toFilterDate to 23
        set minutes of toFilterDate to 59
        set seconds of toFilterDate to 59
        
        repeat with n in notes of default account
            set processedCount to processedCount + 1
            try
                set noteModDate to modification date of n
                if noteModDate ≥ fromFilterDate and noteModDate ≤ toFilterDate then
                    set noteCount to noteCount + 1
                end if
            on error
                -- Skip notes that can't be read
            end try
            
            -- Limit processing to avoid timeout (check only first 500 notes)
            if processedCount > 500 then exit repeat
        end repeat
        
        return noteCount
    end tell
    '''
    
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return int(result.stdout.strip())
        else:
            print(f"Error counting notes in range: {result.stderr}")
            return 0
    except Exception as e:
        print(f"Error counting notes in range: {e}")
        return 0


def parse_date_string(date_str):
    """
    Parse date string in various formats
    Supported formats: YYYY-MM-DD, DD/MM/YYYY, relative days (e.g., '7' for 7 days ago)
    """
    if not date_str:
        return None
    
    # Try relative days (e.g., "7" means 7 days ago)
    try:
        days_ago = int(date_str)
        return datetime.now() - timedelta(days=days_ago)
    except ValueError:
        pass
    
    # Try YYYY-MM-DD format
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass
    
    # Try DD/MM/YYYY format
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        pass
    
    # Try MM/DD/YYYY format
    try:
        return datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        pass
    
    print(f"Could not parse date '{date_str}'. Use formats: YYYY-MM-DD, DD/MM/YYYY, or number of days ago (e.g., '7')")
    return None


def display_notes(notes):
    """
    Display notes in a readable format
    """
    if not notes:
        print("No notes found or error occurred.")
        return
    
    print(f"\n{'='*60}")
    print(f"FOUND {len(notes)} NOTES")
    print(f"{'='*60}\n")
    
    for i, note in enumerate(notes, 1):
        print(f"NOTE #{i}")
        print(f"Title: {note['title']}")
        print(f"Created: {note['created']}")
        print(f"Modified: {note['modified']}")
        print(f"Content Preview: {note['body'][:100]}{'...' if len(note['body']) > 100 else ''}")
        print("-" * 60)


def save_notes_to_file(notes, filename="notes_export.json"):
    """
    Save notes to a JSON file
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        print(f"\nNotes saved to {filename}")
    except Exception as e:
        print(f"Error saving notes: {e}")


def main():
    """
    Main function with command line argument support
    """
    parser = argparse.ArgumentParser(description='Extract notes from macOS Notes app with filters')
    parser.add_argument('-n', '--limit', type=int, default=5, 
                       help='Number of notes to extract (default: 5)')
    parser.add_argument('-d', '--from-date', type=str, default=None,
                       help='Extract notes from this date onwards. Formats: YYYY-MM-DD, DD/MM/YYYY, or days ago (e.g., 7)')
    parser.add_argument('-t', '--to-date', type=str, default=None,
                       help='Extract notes up to this date (reverse filtering). Formats: YYYY-MM-DD, DD/MM/YYYY, or days ago (e.g., 7)')
    parser.add_argument('--filter-tag', type=str, default=None,
                       help='Filter notes containing this tag/string in title or body (case-insensitive)')
    parser.add_argument('-c', '--count', action='store_true',
                       help='Count total notes and notes matching criteria')
    parser.add_argument('--stats-only', action='store_true',
                       help='Show only statistics, do not extract notes')
    
    args = parser.parse_args()
    
    # Parse the dates
    from_date = parse_date_string(args.from_date) if args.from_date else None
    to_date = parse_date_string(args.to_date) if args.to_date else None
    filter_tag = args.filter_tag
    
    print("=" * 60)
    print("NOTE VOYEUR - macOS Notes Extractor")
    print("=" * 60)
    
    # Show statistics
    if args.count or args.stats_only:
        total_notes = count_total_notes()
        print(f"\nSTATISTICS:")
        print(f"Total notes in Notes app: {total_notes}")
        
        if filter_tag:
            print(f"Tag filter: '{filter_tag}' (applied after extraction)")
        
        if from_date and to_date:
            # Range filtering statistics
            filtered_count = count_notes_in_range(from_date, to_date)
            print(f"Notes modified between {from_date.strftime('%Y-%m-%d')} and {to_date.strftime('%Y-%m-%d')}: {filtered_count}")
            base_extract = min(args.limit, filtered_count)
            print(f"Will extract: {base_extract} notes{' (before tag filtering)' if filter_tag else ''}")
        elif from_date:
            # Forward filtering statistics
            filtered_count = count_notes_from_date(from_date)
            print(f"Notes modified from {from_date.strftime('%Y-%m-%d')}: {filtered_count}")
            base_extract = min(args.limit, filtered_count)
            print(f"Will extract: {base_extract} notes{' (before tag filtering)' if filter_tag else ''}")
        elif to_date:
            # Reverse filtering statistics
            filtered_count = count_notes_to_date(to_date)
            print(f"Notes modified before {to_date.strftime('%Y-%m-%d')}: {filtered_count}")
            base_extract = min(args.limit, filtered_count)
            print(f"Will extract: {base_extract} notes{' (before tag filtering)' if filter_tag else ''}")
        else:
            base_extract = min(args.limit, total_notes)
            print(f"Will extract: {base_extract} most recent notes{' (before tag filtering)' if filter_tag else ''}")
    
    # Exit if only stats requested
    if args.stats_only:
        return
    
    # Extract notes with appropriate filtering
    filter_msg = f" (filtering by tag: '{filter_tag}')" if filter_tag else ""
    
    if from_date and to_date:
        print(f"\nExtracting up to {args.limit} notes between {from_date.strftime('%Y-%m-%d')} and {to_date.strftime('%Y-%m-%d')}{filter_msg}...")
        notes = read_notes_with_filters(args.limit, from_date, to_date, filter_tag)
    elif from_date:
        print(f"\nExtracting up to {args.limit} notes modified from {from_date.strftime('%Y-%m-%d')}{filter_msg}...")
        notes = read_notes_with_filters(args.limit, from_date, None, filter_tag)
    elif to_date:
        print(f"\nExtracting up to {args.limit} notes modified before {to_date.strftime('%Y-%m-%d')}{filter_msg}...")
        notes = read_notes_with_filters(args.limit, None, to_date, filter_tag)
    else:
        if filter_tag:
            print(f"\nExtracting up to {args.limit} notes{filter_msg}...")
            notes = read_notes_with_filters(args.limit, None, None, filter_tag)
        else:
            print(f"\nExtracting last {args.limit} notes...")
            notes = read_notes_structured(args.limit)
    
    # Display results
    if notes:
        display_notes(notes)
        
        # Save to file with descriptive name
        tag_suffix = f"_tag_{filter_tag.replace(' ', '_')}" if filter_tag else ""
        
        if from_date and to_date:
            filename = f"notes_export_{from_date.strftime('%Y%m%d')}_to_{to_date.strftime('%Y%m%d')}{tag_suffix}_limit_{args.limit}.json"
        elif from_date:
            filename = f"notes_export_from_{from_date.strftime('%Y%m%d')}{tag_suffix}_limit_{args.limit}.json"
        elif to_date:
            filename = f"notes_export_before_{to_date.strftime('%Y%m%d')}{tag_suffix}_limit_{args.limit}.json"
        else:
            filename = f"notes_export_last{tag_suffix}_{args.limit}.json"
        
        save_notes_to_file(notes, filename)
    else:
        print("No notes found matching the criteria.")
    
    print(f"\nScript completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def interactive_main():
    """
    Interactive version of main function for backward compatibility
    """
    limit = 5  # Set a reasonable default
    print(f"Reading last {limit} notes from macOS Notes app...")
    
    # Method 1: Simple output (original approach)
    print("\n" + "="*60)
    print(f"METHOD 1: Simple AppleScript Output (last {limit} notes)")
    print("="*60)
    simple_output = read_all_notes(limit)
    if simple_output:
        print(simple_output)
    
    # Method 2: Structured output
    print("\n" + "="*60)
    print(f"METHOD 2: Structured Note Data (last {limit} notes)")
    print("="*60)
    notes = read_notes_structured(limit)
    display_notes(notes)
    
    # Save to file
    if notes:
        save_notes_to_file(notes, f"notes_export_last_{limit}.json")
    
    print(f"\nScript completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
