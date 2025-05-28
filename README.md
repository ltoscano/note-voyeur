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

The script now supports command-line arguments for flexible note extraction:

```bash
# Extract specific number of notes
python3 note_reader.py -n 10

# Extract notes from a specific date (YYYY-MM-DD format)
python3 note_reader.py -d 2025-05-01 -n 20

# Extract notes from 7 days ago
python3 note_reader.py -d 7 -n 15

# Show statistics only (don't extract notes)
python3 note_reader.py --stats-only

# Show statistics and extract notes
python3 note_reader.py -d 3 -n 5 -c
```

### Command Line Options

- `-n, --limit`: Number of notes to extract (default: 5)
- `-d, --from-date`: Extract notes from this date onwards
  - Formats supported:
    - `YYYY-MM-DD` (e.g., `2025-05-01`)
    - `DD/MM/YYYY` (e.g., `01/05/2025`)
    - Days ago as number (e.g., `7` for 7 days ago)
- `-c, --count`: Show count of total notes and filtered notes
- `--stats-only`: Show only statistics, don't extract notes

### Examples

```bash
# Get help
python3 note_reader.py -h

# Extract last 3 notes
python3 note_reader.py -n 3

# Extract notes modified in the last 2 weeks
python3 note_reader.py -d 14 -n 50

# Extract notes from specific date with statistics
python3 note_reader.py -d 2025-05-15 -n 10 -c

# Check how many notes you have
python3 note_reader.py --stats-only
```

### Run Examples

To see various usage examples:

```bash
python3 examples.py
```

## Output

The script generates:
- Console output with note titles, creation/modification dates, and content previews
- JSON export file (`notes_export_last_X.json`) with full note data

## Privacy Note

- JSON export files are automatically excluded from git tracking
- Your note content remains on your local machine
- No data is sent to external services

## Error Handling

The script includes:
- 30-second timeout protection
- Permission error handling
- AppleScript execution error handling
- Graceful failure when Notes app is inaccessible

## License

This project is open source. Use responsibly and respect privacy.
