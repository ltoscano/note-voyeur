# Note Voyeur

A Python application that reads and analyzes notes from the macOS Notes app using AppleScript.

## Features

- Read the latest notes from macOS Notes app
- Display notes in structured format with metadata
- Export notes to JSON format
- Limit number of notes to read (default: 5)
- Timeout protection to prevent hanging

## Requirements

- macOS (required for Notes app integration)
- Python 3.6+
- Access to macOS Notes app

## Security Settings for macOS

**Important**: Before running this application, you need to configure macOS security settings to allow access to the Notes app.

### Step 1: Initial Permission Request
When you first run the script, macOS will prompt you to allow access to Notes. Click "Allow" when prompted.

### Step 2: Manual Security Configuration
If the script doesn't work or you need to manually configure permissions:

1. **Open System Settings (or System Preferences on older macOS)**
2. **Navigate to Privacy & Security**
3. **Click on "Automation"** (left sidebar)
4. **Find your Terminal or Python application** in the list
5. **Check the box next to "Notes"** to allow access

### Alternative Path for macOS Ventura and later:
1. **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Add Terminal or your Python executable if needed

### Step 3: Verify Permissions
If you're still having issues:

1. **System Settings** → **Privacy & Security** → **Files and Folders**
2. Look for Terminal or Python
3. Ensure it has access to necessary folders

### Troubleshooting Permission Issues

If you get permission errors:

```bash
# Check if Notes app is running
ps aux | grep Notes

# Kill Notes app if it's running and try again
killall Notes
```

**Note**: You may need to restart your terminal or Python environment after changing security settings.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ltoscano/note-voyeur.git
cd note-voyeur
```

2. No additional dependencies required (uses standard library)

## Usage

### Basic Usage

Run the script with default settings (last 5 notes):

```bash
python3 note_reader.py
```

### Advanced Usage with Parameters

The script now supports command-line arguments for flexible note extraction including **reverse chronological filtering**:

```bash
# Extract specific number of notes
python3 note_reader.py -n 10

# FORWARD FILTERING: Extract notes from a specific date onwards
python3 note_reader.py -d 2025-05-01 -n 20

# REVERSE FILTERING: Extract notes before a specific date (NEW!)
python3 note_reader.py -t 2025-04-30 -n 15

# Extract notes from 7 days ago onwards
python3 note_reader.py -d 7 -n 15

# Extract notes before 30 days ago (reverse filtering)
python3 note_reader.py -t 30 -n 10

# Extract notes between two dates
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 -n 25

# Show statistics only (don't extract notes)
python3 note_reader.py --stats-only

# Show statistics for reverse filtering
python3 note_reader.py -t 30 --stats-only

# Show statistics and extract notes
python3 note_reader.py -d 3 -n 5 -c
```

### Command Line Options

- `-n, --limit`: Number of notes to extract (default: 5)
- `-d, --from-date`: Extract notes from this date onwards (forward filtering)
  - Formats supported:
    - `YYYY-MM-DD` (e.g., `2025-05-01`)
    - `DD/MM/YYYY` (e.g., `01/05/2025`)
    - Days ago as number (e.g., `7` for 7 days ago)
- `-t, --to-date`: **NEW!** Extract notes before this date (reverse filtering)
  - Same formats as `--from-date`
  - Useful for reading older notes chronologically backwards
- `--filter-tag`: **NEW!** Filter notes containing this tag/string in title or body (case-insensitive)
  - Can be combined with date filtering for precise extraction
- `--mark`: **NEW!** Mark extracted notes by adding "NOTE-VOYEUR: TARGET ACQUIRED!" to their title
  - Modifies the note content to include the marked title as the first line
  - Automatically skips notes that are already marked
  - Can be combined with any filtering option
- `-c, --count`: Show count of total notes and filtered notes
- `--stats-only`: Show only statistics, don't extract notes

### Filtering Modes

**Forward Filtering** (`--from-date`): Extracts notes modified **from** a specific date **onwards** (towards present/future)
- Example: `--from-date 2025-04-01` gets notes from April 1st to today

**Reverse Filtering** (`--to-date`): Extracts notes modified **before** a specific date (going backwards into the past)  
- Example: `--to-date 2025-04-30` gets notes before April 30th

**Range Filtering**: Use both parameters to extract notes within a specific date range
- Example: `--from-date 2025-04-01 --to-date 2025-04-30` gets notes from April 2025 only

### Examples

```bash
# Get help
python3 note_reader.py -h

# Extract last 3 notes
python3 note_reader.py -n 3

# FORWARD FILTERING EXAMPLES
# Extract notes modified in the last 2 weeks
python3 note_reader.py -d 14 -n 50

# Extract notes from specific date with statistics
python3 note_reader.py -d 2025-05-15 -n 10 -c

# REVERSE FILTERING EXAMPLES (NEW!)
# Extract 5 notes from before 30 days ago
python3 note_reader.py -t 30 -n 5

# Extract notes before a specific date
python3 note_reader.py -t 2025-04-01 -n 20

# Get statistics for reverse filtering
python3 note_reader.py -t 30 --stats-only

# RANGE FILTERING EXAMPLES
# Extract notes from April 2025 only
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 -n 100

# Extract notes from last month with count
python3 note_reader.py -d 30 -t 0 -n 50 -c

# TAG FILTERING EXAMPLES (NEW!)
# Extract notes containing "AI" in title or body
python3 note_reader.py --filter-tag "AI" -n 10

# Extract recent notes containing "project" 
python3 note_reader.py --filter-tag "project" -d 7 -n 15

# Combine date range with tag filtering
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 --filter-tag "meeting" -n 20

# Case-insensitive tag search with statistics
python3 note_reader.py --filter-tag "Python" -n 5 -c

# MARKING EXAMPLES (NEW!)
# Mark the last 3 notes with VOYEUR tag
python3 note_reader.py -n 3 --mark

# Mark notes containing "meeting" from last week
python3 note_reader.py --filter-tag "meeting" -d 7 -n 5 --mark

# Mark notes from a specific date range with tag filtering
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 --filter-tag "project" -n 10 --mark

# Mark recent notes (already marked notes will be skipped)
python3 note_reader.py -d 3 -n 5 --mark

# Check how many notes you have total
python3 note_reader.py --stats-only
```

### Run Examples

To see various usage examples including the new reverse filtering:

```bash
# Run original examples
python3 examples.py

# Run updated examples with reverse filtering demonstrations
python3 examples_updated.py
```

## Output

The script generates:
- Console output with note titles, creation/modification dates, and content previews
- JSON export files with descriptive names based on filtering criteria:
  - `notes_export_last_X.json` (basic extraction)
  - `notes_export_from_YYYYMMDD_limit_X.json` (forward filtering)
  - `notes_export_before_YYYYMMDD_limit_X.json` (reverse filtering) 
  - `notes_export_YYYYMMDD_to_YYYYMMDD_limit_X.json` (range filtering)
  - `notes_export_*_tag_TAGNAME_*.json` (tag filtering - combined with other filters)
  - `notes_export_*_marked_*.json` (marked notes - includes "_marked" suffix)

## Privacy Note

- JSON export files are automatically excluded from git tracking
- Your note content remains on your local machine
- No data is sent to external services

## Error Handling

The script includes:
- 60-second timeout protection for complex filtering operations
- Permission error handling
- AppleScript execution error handling
- Graceful failure when Notes app is inaccessible
- Processing limits (500 notes max per operation) to prevent hanging with large note collections
- Italian macOS system compatibility for date parsing

## License

This project is open source. Use responsibly and respect privacy.
