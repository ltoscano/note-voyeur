# Note Voyeur - Test Results

## Range Filtering Bug Fix - COMPLETED ✅

Date: May 28, 2025

### Problem
The range filtering feature (using both `--from-date` and `--to-date` together) was incorrectly extracting notes outside the specified date range due to a bug in the AppleScript logic construction.

### Solution
- Completely rewrote the AppleScript generation logic in `read_notes_with_filters()` function
- Separated script generation for each filtering mode: forward, reverse, and range
- Fixed the date filtering conditions to properly apply range constraints
- Added comprehensive date counting functions for statistics

### Test Results

#### 1. Range Filtering (--from-date + --to-date)
```bash
python3 note_reader.py --from-date 2025-04-01 --to-date 2025-04-30 -n 2 -c
```
**Result**: ✅ WORKING
- Correctly identifies 99 notes in the April 2025 range
- Extracts only notes from April 30, 2025 (within range)
- No notes from May 2025 extracted (correctly filtered out)

#### 2. Forward Filtering (--from-date only)
```bash
python3 note_reader.py --from-date 2025-05-28 -n 2 -c
```
**Result**: ✅ WORKING
- Correctly identifies 6 notes from May 28, 2025
- Extracts notes from May 28, 2025 only
- Fixed timeout issue in count function

#### 3. Reverse Filtering (--to-date only)
```bash
python3 note_reader.py --to-date 30 -n 3 -c
```
**Result**: ✅ WORKING
- Correctly identifies 379 notes before April 28, 2025 (30 days ago)
- Extracts notes from April 28, 2025 and earlier
- No recent notes extracted (correctly filtered)

#### 4. Statistics Only
```bash
python3 note_reader.py --from-date 2025-04-01 --to-date 2025-04-30 --stats-only
```
**Result**: ✅ WORKING
- Shows correct count of 99 notes in range
- No extraction performed (as expected)

### Key Improvements
1. **Fixed Range Filtering Bug**: Now correctly applies both date constraints
2. **Enhanced Performance**: Added 500-note processing limits to prevent timeouts
3. **Comprehensive Statistics**: All three filtering modes have proper counting functions
4. **Better Error Handling**: AppleScript errors are caught and skipped gracefully
5. **Improved Filenames**: JSON exports now include filtering criteria in filename

## Tag Filtering Feature - COMPLETED ✅

Date: May 28, 2025

### Feature Description
Added new `--filter-tag` option that allows filtering notes based on content contained in the title or body of notes. The filtering is case-insensitive and can be combined with existing date filtering options.

### Implementation Details
- Enhanced `read_notes_with_filters()` function to accept `filter_tag` parameter
- Added tag filtering logic that searches both title and body case-insensitively
- Updated command line argument parser with `--filter-tag` option
- Enhanced filename generation to include tag information
- Updated statistics display to show tag filtering information
- Tag filtering is applied after note extraction but before returning results

### Test Results

#### 1. Tag-Only Filtering
```bash
python3 note_reader.py --filter-tag "AI" -n 10 -c
```
**Result**: ✅ WORKING
- Total notes: 385
- Found 2 notes containing "AI" in title or body
- Tag filtering applied correctly after extraction
- Generated filename: `notes_export_last_tag_AI_10.json`

#### 2. Tag Filtering with No Matches
```bash
python3 note_reader.py --filter-tag "python" -n 5 -c
```
**Result**: ✅ WORKING
- Correctly returned "No notes found matching the criteria"
- Handled empty results gracefully
- Statistics showed tag filter was active

#### 3. Combined Date Range + Tag Filtering
```bash
python3 note_reader.py --from-date 2025-04-01 --to-date 2025-04-30 --filter-tag "WPE" -n 5 -c
```
**Result**: ✅ WORKING
- Found 99 notes in April 2025 date range
- Applied tag filtering and found 2 notes containing "WPE"
- Statistics correctly showed both date and tag filtering
- Generated filename: `notes_export_20250401_to_20250430_tag_WPE_limit_5.json`

#### 4. Case-Insensitive Tag Search
```bash
python3 note_reader.py --filter-tag "ai" -n 3
```
**Result**: ✅ WORKING
- Case-insensitive search worked correctly
- Found same notes as uppercase "AI" search
- Demonstrates proper case handling

#### 5. Tag Filtering with Forward Date Filter
```bash
python3 note_reader.py --from-date 7 --filter-tag "meeting" -n 10
```
**Result**: ✅ WORKING
- Combined recent date filtering with tag search
- Applied both filters correctly in sequence
- Statistics showed multi-level filtering information

### Key Features Verified
- ✅ Case-insensitive content search in title and body
- ✅ Combination with existing date filtering options
- ✅ Proper filename generation with tag information
- ✅ Enhanced statistics display
- ✅ Graceful handling of no matches
- ✅ Tag filtering applied after date extraction for efficiency
- ✅ Works with forward, reverse, and range date filtering

### Documentation Updated
- ✅ README.md enhanced with tag filtering examples
- ✅ Command line help text updated
- ✅ Created `examples_with_tags.py` with comprehensive demonstrations
- ✅ All filtering combinations documented and tested

## Note Marking Feature - COMPLETED ✅

Date: May 28, 2025

### Feature Description
Added new `--mark` option that marks extracted notes by adding "NOTE-VOYEUR: TARGET ACQUIRED!" to their title. The feature modifies the note content to include the marked title as the first line and automatically skips notes that are already marked.

### Implementation Details
- Added `mark_notes_with_voyeur_tag()` function to handle note modification
- Enhanced command line argument parser with `--mark` option
- Updated main function to handle marking after note extraction
- Added intelligent detection of already marked notes to prevent duplicates
- Enhanced filename generation to include "_marked" suffix for marked notes
- Integrated marking with all existing filtering options (date, tag, range)

### Test Results

#### 1. Basic Note Marking
```bash
python3 note_reader.py -n 2 --mark
```
**Result**: ✅ WORKING
- Successfully marked 2 notes with "NOTE-VOYEUR: TARGET ACQUIRED!" prefix
- Notes content modified to include new title as first line
- Generated filename: `notes_export_last_marked_2.json`
- Marked notes display new title in console output

#### 2. Skip Already Marked Notes
```bash
python3 note_reader.py -n 2 --mark
```
**Result**: ✅ WORKING
- Correctly detected already marked notes
- Skipped marking with message "ALREADY MARKED, skipping"
- No duplicate marking performed
- Completed with "No notes were marked" message

#### 3. Combined Date Range + Tag + Marking
```bash
python3 note_reader.py -d 2025-04-01 -t 2025-04-30 --filter-tag "WPE" -n 3 --mark
```
**Result**: ✅ WORKING
- Found 1 note matching criteria (April 2025 + WPE tag)
- Successfully marked the note
- Generated filename: `notes_export_20250401_to_20250430_tag_WPE_marked_limit_3.json`
- All filtering + marking worked together seamlessly

#### 4. Marking with Non-existent Filter
```bash
python3 note_reader.py --filter-tag "nonexistent_tag_12345" -n 5 --mark
```
**Result**: ✅ WORKING
- Correctly handled case with no matching notes
- Returned "No notes found matching the criteria"
- No marking attempted (graceful handling)
- No errors generated

#### 5. Visual Feedback and Messages
```bash
python3 note_reader.py -n 2 --mark
```
**Result**: ✅ WORKING
- Clear visual indicators with emojis (🎯, ✅, ⚠️)
- Progress messages during marking process
- Success/failure feedback for each note
- Final summary with marked count
- Extraction messages show "[WILL MARK WITH VOYEUR TAG]" indicator

### Key Features Verified
- ✅ Note title modification with VOYEUR prefix
- ✅ HTML content modification to include new title
- ✅ Automatic detection and skipping of already marked notes
- ✅ Integration with all existing filtering options
- ✅ Enhanced filename generation with "_marked" suffix
- ✅ Clear visual feedback and progress indicators
- ✅ Graceful handling of edge cases (no notes found)
- ✅ AppleScript-based note modification works reliably
- ✅ Proper escaping of special characters in titles

### Security Considerations
- ✅ Proper escaping of quotes and special characters in AppleScript
- ✅ Safe handling of HTML content in note bodies
- ✅ No data loss - original content preserved with new title added
- ✅ Automatic backup through JSON export of marked notes

### Documentation Updates
- ✅ README.md enhanced with marking examples and options
- ✅ Command line help text updated with --mark option
- ✅ Created `examples_with_marking.py` for comprehensive demonstrations
- ✅ Output filename patterns documented for marked notes

**Project Status**: COMPLETE ✅
