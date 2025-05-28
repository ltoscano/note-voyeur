#!/usr/bin/env python3
"""
Note Reader for macOS Notes App
Reads and displays all notes from the default Notes account
"""

import subprocess
import json
from datetime import datetime


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


def read_notes_structured(limit=10):
    """
    Reads notes in a more structured way, returning individual note data
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
    Main function to demonstrate note reading functionality
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
