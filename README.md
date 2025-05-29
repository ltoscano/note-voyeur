# Note Voyeur

A Python application that reads and analyzes notes from the macOS Notes app using AppleScript, with AI-powered content analysis capabilities.

## Features

### Core Features
- Read the latest notes from macOS Notes app
- Display notes in structured format with metadata
- Export notes to JSON format with custom filenames
- Advanced filtering by date ranges and content tags
- Smart marker system to avoid re-processing notes
- Mark notes with special tags for tracking (only when explicitly requested)
- Limit number of notes to read (default: 5)
- Timeout protection to prevent hanging

### AI Analysis Features ✨ NEW!
- **AI-powered concept extraction** using OpenAI GPT-4
- **Automatic link detection** and content analysis
- **Content summarization** from web links using MarkItDown
- **Structured analysis output** with concepts, links, and explanations
- **Category classification** with 7 predefined categories for better organization
- **Clean JSON output** with markers and filter-tags removed from analysis

## Requirements

- macOS (required for Notes app integration)
- Python 3.10+ (required for MarkItDown library)
- Access to macOS Notes app
- OpenAI API key (for AI analysis features)

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

3. Install required dependencies:

```bash
# For basic note reading functionality
pip install -r requirements.txt

# For AI analysis (automatically installs MarkItDown)
pip install openai markitdown[all]
```

4. Set your OpenAI API key (for AI analysis features):

**Option 1: Environment variable**
```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

**Option 2: .env file (recommended)**
Create a `.env` file in the project directory:
```
OPENAI_API_KEY=your-openai-api-key-here
```

**Option 3: Command line parameter**
```bash
python ai_analyzer.py notes.json --api-key your-openai-api-key-here
```

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

# Filter notes by content tag
python3 note_reader.py --filter-tag "AI" -n 10

# Custom output filename
python3 note_reader.py -n 5 -o my_notes.json

# Mark extracted notes (adds marker to prevent re-processing)
python3 note_reader.py -n 3 --mark

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
  - Notes with this tag are preserved in original files for future filtering
- `--mark`: **NEW!** Mark extracted notes by adding "NOTE-VOYEUR: TARGET ACQUIRED!" to their title
  - **Only marks when explicitly specified** - no automatic marking
  - Automatically skips notes that are already marked to avoid re-processing
  - Marking happens AFTER extraction and saving, preserving filter-tags
  - Can be combined with any filtering option
- `-o, --output`: **NEW!** Force a specific JSON output filename (auto-adds .json extension)
  - Example: `-o my_notes` creates `my_notes.json`
  - If not specified, auto-generates descriptive filename based on filters
- `-c, --count`: Show count of total notes and filtered notes
- `--stats-only`: Show only statistics, don't extract notes

### Filtering Modes & Smart Marker System

**Forward Filtering** (`--from-date`): Extracts notes modified **from** a specific date **onwards** (towards present/future)
- Example: `--from-date 2025-04-01` gets notes from April 1st to today

**Reverse Filtering** (`--to-date`): Extracts notes modified **before** a specific date (going backwards into the past)  
- Example: `--to-date 2025-04-30` gets notes before April 30th

**Range Filtering**: Use both parameters to extract notes within a specific date range
- Example: `--from-date 2025-04-01 --to-date 2025-04-30` gets notes from April 2025 only

**Tag Filtering** (`--filter-tag`): Filter notes containing specific text in title or body
- Case-insensitive search using "in" operator
- Can be combined with date filters for precise extraction

**Smart Marker System**: 
- Notes with "NOTE-VOYEUR: TARGET ACQUIRED!" marker are automatically excluded from extraction
- Prevents re-processing previously analyzed notes
- Markers and filter-tags are removed from JSON output for clean analysis
- Original notes preserve filter-tags for future use

### Operation Sequence

The Note Voyeur system follows this precise sequence:

1. **Extract** → Filter and extract notes (excluding already marked notes)
2. **Clean** → Remove markers and filter-tags from extracted data for JSON output
3. **Display** → Show extracted notes in console
4. **Save** → Save clean JSON file 
5. **Mark** → **ONLY IF `--mark` is specified**, add markers to original notes

This sequence ensures that:
- JSON files are clean and suitable for AI analysis
- Original notes preserve filter-tags for future filtering
- Previously marked notes are never re-processed
- Marking only happens when explicitly requested

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

# CUSTOM OUTPUT EXAMPLES (NEW!)
# Force specific output filename
python3 note_reader.py -n 10 -o weekly_notes

# Custom filename with tag filtering
python3 note_reader.py --filter-tag "meeting" -d 7 -o meetings

# Custom filename with date range
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 -o april_notes

# MARKING EXAMPLES (NEW!)
# Mark the last 3 notes with VOYEUR tag (ONLY when --mark is specified)
python3 note_reader.py -n 3 --mark

# Mark notes containing "meeting" from last week
python3 note_reader.py --filter-tag "meeting" -d 7 -n 5 --mark

# Mark notes from a specific date range with tag filtering and custom output
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 --filter-tag "project" -n 10 --mark -o project_april

# Mark recent notes (already marked notes will be automatically skipped)
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
  - Custom filenames when using `-o/--output` parameter (e.g., `my_notes.json`)

**Important**: JSON output is automatically cleaned of markers and filter-tags for clean analysis, while original notes preserve filter-tags for future filtering operations.

### AI Analysis Output

The AI analysis script (`ai_analyzer.py`) generates:
- Console output with analysis results
- JSON files with AI analysis details appended to original note exports:
  - `notes_export_*_ai_analyzed.json` (AI analysis results)

## Project Files

### Core Scripts
- **`note_reader.py`** - Main script for extracting notes from macOS Notes app
- **`ai_analyzer.py`** ✨ NEW! - AI-powered analysis of extracted notes using OpenAI GPT-4
- **`examples_ai_analyzer.py`** - Example usage and demonstrations for AI analyzer

### Example Scripts
- **`examples.py`** - Basic usage examples for note_reader.py
- **`examples_with_tags.py`** - Examples using tag filtering functionality
- **`examples_with_marking.py`** - Examples using note marking functionality
- **`examples_updated.py`** - Updated examples with latest features

### Documentation
- **`README.md`** - This documentation file
- **`test_results.md`** - Comprehensive test results and validation

## AI Analysis Features

The project includes an `ai_analyzer.py` script that uses **OpenAI GPT-4** and **MarkItDown** to automatically analyze extracted notes and:

1. **Extract key concepts** from each note using artificial intelligence
2. **Identify and analyze links** present in the notes
3. **Generate explanations** of link content using MarkItDown for extraction and GPT-4 for summarization
4. **Categorize concepts** into predefined categories:
   - **Foundations & Theory** - Basic concepts, research foundations, theoretical frameworks
   - **Models & Architectures** - AI models, neural networks, system architectures
   - **Tools & Frameworks** - Development tools, libraries, platforms, software
   - **Experiments & Applications** - Practical implementations, use cases, projects
   - **Evaluation & Alignment** - Testing methods, performance metrics, safety measures
   - **Society & Ethics** - Social impact, ethical considerations, policy discussions
   - **News & Announcements** - Industry updates, product launches, announcements

The AI analysis adds an `ai_analysis` field to each note containing an array of objects with:
- `concept`: Description of the identified concept
- `link`: Associated URL (if any)
- `explain`: AI-generated explanation of linked content
- `category`: Assigned category classification

**Important**: The AI analyzer processes clean JSON files (with markers and filter-tags removed) to ensure accurate analysis without interference from Note Voyeur system tags.

## Installation and Setup

### Prerequisites
- macOS (required for Notes app integration)
- Python 3.10+ (required for MarkItDown library)
- Access to macOS Notes app
- OpenAI API key (for AI analysis features)

### Basic Installation
1. Clone this repository:
```bash
git clone https://github.com/ltoscano/note-voyeur.git
cd note-voyeur
```

2. Install basic dependencies:
```bash
pip install -r requirements.txt
```

### AI Analysis Setup
For AI analysis capabilities, install additional dependencies:

```bash
# Install AI analysis dependencies
pip install openai 'markitdown[all]'
```

### OpenAI API Configuration

**Option 1: .env file (recommended)**
Create a `.env` file in the project directory:
```
OPENAI_API_KEY=your-openai-api-key-here
```

**Option 2: Environment variable**
```bash
export OPENAI_API_KEY='your-openai-api-key-here'
```

**Option 3: Command line parameter**
```bash
python ai_analyzer.py notes.json --api-key your-openai-api-key-here
```

### Setup Script
Use the provided setup script for quick environment preparation:

```bash
source setup_env.sh
```

This script:
- Activates the correct virtual environment
- Verifies installed dependencies
- Checks for OpenAI API key presence
- Changes to project directory

## AI Analyzer Usage

### Basic Examples
```bash
# Analyze a notes file
python ai_analyzer.py notes_export_last_10.json

# Specify custom output filename
python ai_analyzer.py notes_export_last_10.json -o analyzed_notes.json

# Test API connection
python ai_analyzer.py notes_export_last_10.json --test

# Pass API key directly
python ai_analyzer.py notes_export_last_10.json --api-key sk-your-key-here

# Analyze with verbose output
python ai_analyzer.py notes_export_last_10.json --verbose
```

### Integration Workflow
```bash
# Complete workflow: Extract → Analyze
python note_reader.py -n 10 --filter-tag "AI" -o ai_notes
python ai_analyzer.py ai_notes.json

# Extract and mark, then analyze
python note_reader.py -n 5 --mark -o research_notes
python ai_analyzer.py research_notes.json -o research_analyzed
```

### Expected Output

The AI analyzer adds an `ai_analysis` field to each note with the following structure:

```json
{
  "title": "Note title",
  "body": "Note content...",
  "created": "creation date",
  "modified": "modification date",
  "ai_analysis": [
    {
      "concept": "Description of identified concept",
      "link": "https://example.com/link-in-content",
      "explain": "AI-generated explanation of link content",
      "category": "Tools & Frameworks"
    },
    {
      "concept": "Another concept without link",
      "link": "",
      "explain": "",
      "category": "Foundations & Theory"
    }
  ]
}
```

## Utility Scripts

### Deployment Script
The `to-synthetic.sh` script automates deployment of extracted resources:

```bash
# Deploy resources.json to external repository
./to-synthetic.sh
```

This script:
- Copies `resources.json` to `../ltoscano.github.io/data/resources/`
- Creates destination directory if needed
- Provides deployment confirmation

### Example Scripts
- **`examples.py`** - Basic usage demonstrations
- **`examples_updated.py`** - Latest features with reverse filtering
- **`examples_with_tags.py`** - Tag filtering examples
- **`examples_with_marking.py`** - Note marking demonstrations
- **`examples_ai_analyzer.py`** - AI analysis examples
- **`final_integration_test.py`** - Comprehensive integration testing

## Privacy & Security

- **Local Processing**: All note extraction happens locally on your macOS system
- **Selective AI Analysis**: Only explicitly extracted notes are sent to OpenAI for analysis
- **JSON Export Protection**: Export files are automatically excluded from git tracking
- **No Automatic Uploads**: Your note content remains on your local machine unless you choose AI analysis
- **Marker System**: Prevents accidental re-processing of previously analyzed notes
- **Clean Outputs**: Markers and system tags are removed from JSON exports for clean analysis

## Error Handling & Reliability

The system includes comprehensive error handling:
- **60-second timeout protection** for complex filtering operations
- **Permission error handling** with clear guidance for macOS security settings
- **AppleScript execution error handling** with fallback mechanisms
- **Graceful failure** when Notes app is inaccessible
- **Processing limits** (500 notes max per operation) to prevent hanging with large collections
- **Italian macOS compatibility** for date parsing and system integration
- **API failure recovery** for OpenAI connectivity issues
- **File validation** to ensure proper JSON structure and content integrity

## Troubleshooting

### Common Issues

**Permission Denied Errors:**
```bash
# Kill Notes app and restart
killall Notes
# Check running processes
ps aux | grep Notes
# Re-run the script
python note_reader.py -n 5
```

**OpenAI API Issues:**
```bash
# Test API connection
python ai_analyzer.py notes.json --test
# Verify API key
echo $OPENAI_API_KEY
```

**Large Note Collections:**
```bash
# Use stats-only to check collection size
python note_reader.py --stats-only
# Process in smaller batches
python note_reader.py -n 50 --mark
```

**Date Filtering Issues:**
```bash
# Check date format compatibility
python note_reader.py -d 2025-05-01 --stats-only
# Use alternative date format
python note_reader.py -d 01/05/2025 --stats-only
```

## Performance Tips

### Optimizing Note Extraction
```bash
# Use stats-only first to understand your collection
python note_reader.py --stats-only

# Process in manageable batches with marking
python note_reader.py -n 50 --mark -o batch1
python note_reader.py -n 50 --mark -o batch2

# Use date filtering for targeted extraction
python note_reader.py -d 7 --filter-tag "work" -n 25

# Combine filters for precision
python note_reader.py -d 2025-05-01 -t 2025-05-29 --filter-tag "AI" -n 20
```

### AI Analysis Best Practices
```bash
# Start with smaller batches for testing
python ai_analyzer.py small_batch.json --test

# Use descriptive output names
python ai_analyzer.py notes.json -o "may_2025_ai_research_analyzed"

# Process marked batches sequentially
python ai_analyzer.py batch1.json -o batch1_analyzed
python ai_analyzer.py batch2.json -o batch2_analyzed
```

## Project Status & Future Development

### Current Version Features
- ✅ Complete note extraction with smart filtering
- ✅ Advanced date range and tag filtering
- ✅ Smart marker system to prevent re-processing
- ✅ Custom output filenames
- ✅ AI-powered concept extraction and categorization
- ✅ Link analysis with content summarization
- ✅ Clean JSON outputs for analysis
- ✅ Comprehensive error handling and reliability

### Roadmap
- 🔄 Multi-language support for international Notes apps
- 🔄 Batch processing optimization for large collections
- 🔄 Alternative AI provider support (Anthropic Claude, local models)
- 🔄 Advanced export formats (CSV, Markdown, HTML)
- 🔄 Web interface for easier interaction

## Contributing

This project welcomes contributions! Areas of interest:
- macOS compatibility testing across versions
- Additional AI provider integrations
- Performance optimizations for large note collections
- UI/UX improvements
- Documentation and examples

## License

This project is open source. Use responsibly and respect privacy.

**Note**: This tool is designed for personal productivity and research. Always respect the privacy and confidentiality of your notes when using AI analysis features.
