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

Run the script:

```bash
python3 note_reader.py
```

The script will:
1. Read the last 5 notes from your Notes app
2. Display them in two formats:
   - Simple text output
   - Structured data with metadata
3. Save the structured data to a JSON file (automatically ignored by git)

## Configuration

You can modify the number of notes to read by editing the `limit` variable in the `main()` function:

```python
limit = 5  # Change this number to read more or fewer notes
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
