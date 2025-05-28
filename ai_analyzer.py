#!/usr/bin/env python3
"""
AI Analyzer for Note Voyeur
Analyzes notes using OpenAI GPT-4 to extract concepts and links,
then uses MarkItDown to fetch and summarize linked content.
"""

import json
import argparse
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    from openai import OpenAI
except ImportError:
    print("⚠️  OpenAI library not found. Installing...")
    import subprocess
    subprocess.run(["pip3", "install", "openai"], check=True)
    from openai import OpenAI

try:
    from markitdown import MarkItDown
except ImportError:
    print("⚠️  MarkItDown library not found. Installing...")
    import subprocess
    subprocess.run(["pip3", "install", "markitdown[all]"], check=True)
    from markitdown import MarkItDown


def load_env_file(file_path: str = '.env') -> Dict[str, str]:
    """
    Load environment variables from a .env file.
    
    Args:
        file_path: Path to the .env file (default: '.env' in current directory)
        
    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"⚠️  Warning: Could not read .env file: {e}")
    return env_vars


class AIAnalyzer:
    """
    Analyzes notes using AI to extract concepts and links
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI analyzer with OpenAI client and MarkItDown
        
        Args:
            api_key: OpenAI API key (if None, will try to get from environment)
        """
        # Initialize OpenAI client
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            # Try to get from environment variable first
            api_key = os.getenv('OPENAI_API_KEY')
            
            # If not found in environment, try to load from .env file
            if not api_key:
                env_vars = load_env_file()
                api_key = env_vars.get('OPENAI_API_KEY')
            
            if not api_key:
                raise ValueError(
                    "OpenAI API key is required. Set OPENAI_API_KEY environment variable, "
                    "add it to a .env file, or pass it as argument"
                )
            self.client = OpenAI(api_key=api_key)
        
        # Initialize MarkItDown for content extraction
        self.markitdown = MarkItDown()
    
    def extract_concepts_and_links(self, note_title: str, note_body: str) -> List[Dict[str, str]]:
        """
        Extract concepts and links from a note using GPT-4
        
        Args:
            note_title: Title of the note
            note_body: Body content of the note
            
        Returns:
            List of dictionaries with 'concept' and 'link' keys
        """
        # Prepare the prompt for GPT-4
        prompt = f"""
Analizza la seguente nota e estrai tutti i concetti principali discussi insieme ai link menzionati.

Titolo: {note_title}

Contenuto:
{note_body}

Per ogni concetto identificato, estrai:
1. Una descrizione chiara e concisa del concetto (in italiano)
2. Il link associato se presente nel testo

Rispondi SOLO con un array JSON nel formato:
[
    {{"concept": "descrizione del concetto", "link": "http://esempio.com"}},
    {{"concept": "altro concetto", "link": ""}},
    ...
]

Se non ci sono link per un concetto, usa una stringa vuota per "link".
Se non ci sono concetti identificabili, ritorna un array vuoto [].
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",  # Note: using gpt-4 as gpt-4.1 might not be available
                messages=[
                    {"role": "system", "content": "Sei un assistente esperto nell'analisi di contenuti e nell'estrazione di concetti chiave. Rispondi sempre con JSON valido."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            # Extract JSON from response
            content = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                concepts = json.loads(content)
                if isinstance(concepts, list):
                    # Validate each concept entry
                    validated_concepts = []
                    for concept in concepts:
                        if isinstance(concept, dict) and 'concept' in concept:
                            validated_concept = {
                                'concept': str(concept.get('concept', '')),
                                'link': str(concept.get('link', ''))
                            }
                            validated_concepts.append(validated_concept)
                    return validated_concepts
                else:
                    print(f"⚠️  GPT response is not a list: {content}")
                    return []
            except json.JSONDecodeError as e:
                print(f"⚠️  Failed to parse GPT response as JSON: {content}")
                print(f"Error: {e}")
                return []
                
        except Exception as e:
            print(f"❌ Error calling OpenAI API: {e}")
            return []
    
    def extract_content_from_url(self, url: str) -> str:
        """
        Extract content from URL using MarkItDown
        
        Args:
            url: URL to extract content from
            
        Returns:
            Extracted content as markdown string
        """
        if not url or not url.startswith(('http://', 'https://')):
            return ""
        
        try:
            result = self.markitdown.convert(url)
            return result.text_content
        except Exception as e:
            print(f"⚠️  Failed to extract content from {url}: {e}")
            return ""
    
    def explain_content(self, concept: str, link: str, content: str) -> str:
        """
        Generate explanation of content using GPT-4
        
        Args:
            concept: The concept being explained
            link: The source link
            content: The extracted content
            
        Returns:
            Brief explanation of the content
        """
        if not content.strip():
            return ""
        
        # Limit content length to avoid token limits
        max_content_length = 4000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        prompt = f"""
Analizza il seguente contenuto web e fornisci un riassunto breve ma chiaro in italiano.

Concetto di riferimento: {concept}
Link: {link}

Contenuto:
{content}

Fornisci un riassunto di massimo 2-3 frasi che spiega:
1. Di cosa tratta il contenuto
2. Come si relaziona al concetto di riferimento
3. Le informazioni più importanti

Rispondi SOLO con il testo del riassunto, senza formattazione aggiuntiva.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "Sei un assistente esperto nel creare riassunti chiari e concisi di contenuti web."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ Error generating explanation: {e}")
            return ""
    
    def analyze_note(self, note: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single note to extract concepts, links, and explanations
        
        Args:
            note: Note dictionary with 'title' and 'body' keys
            
        Returns:
            Note dictionary with added 'ai_analysis' field
        """
        print(f"🔍 Analyzing note: '{note.get('title', 'Untitled')[:50]}...'")
        
        # Extract concepts and links
        concepts_and_links = self.extract_concepts_and_links(
            note.get('title', ''), 
            note.get('body', '')
        )
        
        if not concepts_and_links:
            print("   No concepts found")
            note['ai_analysis'] = []
            return note
        
        print(f"   Found {len(concepts_and_links)} concept(s)")
        
        # Process each concept to add explanations for links
        ai_analysis = []
        for item in concepts_and_links:
            concept = item.get('concept', '')
            link = item.get('link', '')
            
            analysis_item = {
                'concept': concept,
                'link': link,
                'explain': ''
            }
            
            # If there's a link, try to extract and explain content
            if link and link.startswith(('http://', 'https://')):
                print(f"   📝 Extracting content from: {link[:50]}...")
                content = self.extract_content_from_url(link)
                
                if content:
                    print(f"   🤖 Generating explanation...")
                    explanation = self.explain_content(concept, link, content)
                    analysis_item['explain'] = explanation
                else:
                    print(f"   ⚠️  No content extracted from link")
            
            ai_analysis.append(analysis_item)
        
        note['ai_analysis'] = ai_analysis
        print(f"   ✅ Analysis complete")
        return note
    
    def analyze_notes_file(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        Analyze all notes in a JSON file
        
        Args:
            input_file: Path to input JSON file
            output_file: Path to output JSON file (if None, will auto-generate)
            
        Returns:
            Path to output file
        """
        # Load notes from file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                notes = json.load(f)
        except Exception as e:
            raise ValueError(f"Failed to load notes from {input_file}: {e}")
        
        if not isinstance(notes, list):
            raise ValueError("Input file must contain a list of notes")
        
        print(f"📚 Loaded {len(notes)} notes from {input_file}")
        print("🚀 Starting AI analysis...")
        print("=" * 60)
        
        # Analyze each note
        analyzed_notes = []
        for i, note in enumerate(notes, 1):
            print(f"\n[{i}/{len(notes)}] ", end="")
            try:
                analyzed_note = self.analyze_note(note)
                analyzed_notes.append(analyzed_note)
            except Exception as e:
                print(f"❌ Error analyzing note {i}: {e}")
                # Add the note without analysis
                note['ai_analysis'] = []
                analyzed_notes.append(note)
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_ai_analyzed.json"
        
        # Save analyzed notes
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(analyzed_notes, f, indent=2, ensure_ascii=False)
            
            print("\n" + "=" * 60)
            print(f"✅ AI analysis completed!")
            print(f"📁 Results saved to: {output_file}")
            
            # Print summary statistics
            total_concepts = sum(len(note.get('ai_analysis', [])) for note in analyzed_notes)
            total_links = sum(1 for note in analyzed_notes 
                            for analysis in note.get('ai_analysis', []) 
                            if analysis.get('link'))
            total_explanations = sum(1 for note in analyzed_notes 
                                   for analysis in note.get('ai_analysis', []) 
                                   if analysis.get('explain'))
            
            print(f"\n📊 SUMMARY:")
            print(f"   Notes processed: {len(analyzed_notes)}")
            print(f"   Concepts extracted: {total_concepts}")
            print(f"   Links found: {total_links}")
            print(f"   Content explanations: {total_explanations}")
            
            return output_file
            
        except Exception as e:
            raise ValueError(f"Failed to save results to {output_file}: {e}")


def main():
    """
    Main function with command line interface
    """
    parser = argparse.ArgumentParser(
        description='AI Analyzer for Note Voyeur - Extract concepts and analyze links using OpenAI GPT-4',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 ai_analyzer.py notes_export_last_5.json
  python3 ai_analyzer.py notes_export_last_5.json -o analyzed_notes.json
  python3 ai_analyzer.py notes_export_last_5.json --api-key sk-your-key-here

Environment Variables:
  OPENAI_API_KEY    OpenAI API key (can be set via environment variable, .env file, or --api-key parameter)
  
.env File Support:
  You can create a .env file in the same directory as this script with:
  OPENAI_API_KEY=your-api-key-here
        """
    )
    
    parser.add_argument('input_file', 
                       help='Input JSON file generated by note_reader.py')
    parser.add_argument('-o', '--output', 
                       help='Output JSON file (default: input_file_ai_analyzed.json)')
    parser.add_argument('--api-key', 
                       help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
    parser.add_argument('--test', action='store_true',
                       help='Test API connection without processing notes')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input_file):
        print(f"❌ Input file not found: {args.input_file}")
        return 1
    
    print("🤖 AI Analyzer for Note Voyeur")
    print("=" * 40)
    
    try:
        # Initialize analyzer
        analyzer = AIAnalyzer(api_key=args.api_key)
        
        # Test API connection if requested
        if args.test:
            print("🔗 Testing OpenAI API connection...")
            try:
                response = analyzer.client.chat.completions.create(
                    model="gpt-4.1",
                    messages=[{"role": "user", "content": "Hello, this is a test."}],
                    max_tokens=10
                )
                print("✅ OpenAI API connection successful!")
                return 0
            except Exception as e:
                print(f"❌ OpenAI API connection failed: {e}")
                return 1
        
        # Process notes
        output_file = analyzer.analyze_notes_file(args.input_file, args.output)
        print(f"\n🎉 Processing completed successfully!")
        print(f"📁 Output file: {output_file}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
