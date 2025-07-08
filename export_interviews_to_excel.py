#!/usr/bin/env python3
"""
Export Interview Questions to Excel

This script parses the interview markdown files and exports them to Excel format
with separate sheets for different developer levels (Junior, Intermediate, Senior).
"""

import os
import re
import pandas as pd
from pathlib import Path
import argparse
from openpyxl.styles import Font, Alignment

class InterviewExporter:
    def __init__(self, interviews_dir="interviews"):
        self.interviews_dir = Path(interviews_dir)
        self.data = {}
    
    def parse_markdown_file(self, file_path):
        """Parse a markdown interview file and extract structured data"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract basic info
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else file_path.stem
        
        # Extract duration and format info
        duration_match = re.search(r'\*\*Duration\*\*:\s*(.+)', content)
        duration = duration_match.group(1) if duration_match else "N/A"
        
        format_match = re.search(r'\*\*Format\*\*:\s*(.+)', content)
        format_info = format_match.group(1) if format_match else "N/A"
        
        target_match = re.search(r'\*\*Target Level\*\*:\s*(.+)', content)
        target_level = target_match.group(1) if target_match else "N/A"
        
        # Extract questions and sections
        questions = self.extract_questions(content)
        alternatives = self.extract_alternatives(content)
        
        return {
            'title': title,
            'duration': duration,
            'format': format_info,
            'target_level': target_level,
            'questions': questions,
            'alternatives': alternatives
        }
    
    def extract_questions(self, content):
        """Extract main questions from markdown content"""
        questions = []
        
        # Split content by main sections (Parts)
        parts = re.split(r'^## (Part \d+.*?)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                part_title = parts[i]
                part_content = parts[i + 1]
                
                # Extract individual questions within this part
                part_questions = self.extract_questions_from_part(part_title, part_content)
                questions.extend(part_questions)
        
        return questions
    
    def extract_questions_from_part(self, part_title, part_content):
        """Extract questions from a specific part/section"""
        questions = []
        
        # Find question subsections (Question, Challenge, SQL Query, Database Schema Design, Scenario)
        question_sections = re.split(r'^### ((?:Question|Challenge|SQL Query|Database Schema Design|Scenario).*?)$', part_content, flags=re.MULTILINE)
        
        for i in range(1, len(question_sections), 2):
            if i + 1 < len(question_sections):
                question_title = question_sections[i]
                question_content = question_sections[i + 1]
                
                # Extract question text (usually in quotes)
                question_match = re.search(r'\*\*"(.+?)"\*\*', question_content, re.DOTALL)
                question_text = question_match.group(1) if question_match else "N/A"
                
                # Extract expected answer points (try multiple patterns for different question types)
                expected_match = re.search(r'\*\*Expected.*?Answer.*?Points?\*\*:\s*(.+?)(?=\*\*|---|$)', 
                                         question_content, re.DOTALL)
                if not expected_match:
                    # Try for coding challenges - look for "Problem Statement" or "Expected Solution"
                    expected_match = re.search(r'\*\*(?:Problem Statement|Expected Solution.*?)\*\*\s*(.+?)(?=\*\*|---|$)', 
                                             question_content, re.DOTALL)
                if not expected_match:
                    # Try for "Expected Solution Structure" with code blocks
                    expected_match = re.search(r'### (?:Problem Statement|Expected Solution.*?)\s*(.+?)(?=###|---|$)', 
                                             question_content, re.DOTALL)
                expected_answer = expected_match.group(1).strip() if expected_match else "N/A"
                
                # Extract follow-up questions
                followup_match = re.search(r'\*\*Follow-up.*?\*\*:\s*(.+?)(?=\*\*|---|$)', 
                                         question_content, re.DOTALL)
                followup = followup_match.group(1).strip() if followup_match else "N/A"
                
                # Extract reference information and fetch content
                reference_match = re.search(r'\*\*Reference\*\*:\s*(.+?)(?=\*\*|---|$)', 
                                          question_content, re.DOTALL)
                reference_text = reference_match.group(1).strip() if reference_match else "N/A"
                reference_content = self.fetch_reference_content(reference_text)
                
                # Extract code answer for coding questions
                code_answer = self.extract_code_answer(question_content)
                
                # Extract time allocation
                time_match = re.search(r'\((\d+.*?minutes?)\)', question_title)
                time_allocation = time_match.group(1) if time_match else "N/A"
                
                questions.append({
                    'part': part_title,
                    'question_title': question_title,
                    'question_text': question_text,
                    'expected_answer': expected_answer,
                    'followup': followup,
                    'reference_link': reference_text,
                    'reference_content': reference_content,
                    'code_answer': code_answer
                })
        
        return questions
    
    def extract_alternatives(self, content):
        """Extract alternative questions from markdown content"""
        alternatives = []
        
        # Find alternative questions sections
        alt_sections = re.findall(r'### Alternative.*?Questions.*?\n(.*?)(?=^##|^---|\Z)', 
                                content, re.MULTILINE | re.DOTALL)
        
        for section in alt_sections:
            # Extract individual alternative questions
            alt_questions = re.findall(r'#### Alternative.*?\n(.*?)(?=####|###|^##|\Z)', 
                                     section, re.MULTILINE | re.DOTALL)
            
            for alt_content in alt_questions:
                # Extract question text
                question_match = re.search(r'\*\*"(.+?)"\*\*', alt_content, re.DOTALL)
                question_text = question_match.group(1) if question_match else "N/A"
                
                # Extract expected answer points
                expected_match = re.search(r'\*\*Expected.*?Answer.*?Points?\*\*:\s*(.+?)(?=\*\*|---|$)', 
                                         alt_content, re.DOTALL)
                expected_answer = expected_match.group(1).strip() if expected_match else "N/A"
                
                alternatives.append({
                    'question_text': question_text,
                    'expected_answer': expected_answer
                })
        
        return alternatives
    
    def fetch_reference_content(self, reference_text):
        """Fetch content from referenced files based on reference links"""
        if reference_text == "N/A" or not reference_text:
            return "N/A"
        
        try:
            # Parse reference links like "See [golang/junior.md - Question 1](../golang/junior.md#1-what-is-go-and-what-are-its-main-features)"
            # or "Similar to queries in [sql/query.md](../sql/query.md)"
            
            # Extract file path from markdown link
            file_match = re.search(r'\[.*?\]\(([^)]+)\)', reference_text)
            if not file_match:
                return reference_text
            
            file_path = file_match.group(1)
            
            # Handle relative paths (remove ../ and handle fragments)
            if file_path.startswith('../'):
                file_path = file_path[3:]  # Remove ../
            
            # Remove anchor fragments for now (after #)
            if '#' in file_path:
                file_path = file_path.split('#')[0]
            
            # Construct full path
            full_path = Path(file_path)
            if not full_path.exists():
                return f"Referenced file not found: {file_path}"
            
            # Read the referenced file
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to extract specific section if anchor is provided
            original_ref = file_match.group(1)
            if '#' in original_ref:
                anchor = original_ref.split('#')[1]
                section_content = self.extract_section_by_anchor(content, anchor)
                if section_content:
                    return section_content
            
            # If no specific section found, return a summary of the file
            return self.create_file_summary(content, file_path)
            
        except Exception as e:
            return f"Error fetching reference: {str(e)}"
    
    def extract_section_by_anchor(self, content, anchor):
        """Extract specific section content based on anchor"""
        try:
            # Convert anchor to heading pattern (replace hyphens with spaces, etc.)
            # Anchors like "1-what-is-go-and-what-are-its-main-features" 
            heading_pattern = anchor.replace('-', '[ -]').replace('_', '[ _]')
            
            # Look for numbered sections first
            if re.match(r'^\d+', anchor):
                # Try to find numbered question/section
                pattern = rf'^#+\s*{re.escape(anchor.split("-")[0])}[\.:]?\s*(.+?)$'
                match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
                if match:
                    # Extract content until next heading of same or higher level
                    start_pos = match.start()
                    lines = content[start_pos:].split('\n')
                    section_lines = [lines[0]]  # Include the heading
                    
                    for line in lines[1:]:
                        if re.match(r'^#+\s*\d+', line):  # Next numbered section
                            break
                        if re.match(r'^##[^#]', line):  # Higher level heading
                            break
                        section_lines.append(line)
                    
                    return '\n'.join(section_lines).strip()
            
            return None
            
        except Exception:
            return None
    
    def create_file_summary(self, content, file_path):
        """Create a summary of the file content"""
        lines = content.split('\n')
        summary_lines = []
        
        # Get title
        for line in lines[:10]:
            if line.startswith('# '):
                summary_lines.append(line)
                break
        
        # Get first few headings/questions
        heading_count = 0
        for line in lines:
            if re.match(r'^#+\s+', line) and heading_count < 5:
                summary_lines.append(line)
                heading_count += 1
        
        if summary_lines:
            return f"Content from {file_path}:\n\n" + '\n'.join(summary_lines)
        else:
            return f"Content available in {file_path} (no specific section extracted)"
    
    def extract_code_answer(self, question_content):
        """Extract code blocks and solutions from coding questions"""
        if not question_content:
            return ""
        
        # Look for patterns that indicate this is a coding question
        coding_indicators = [
            'Challenge:', 'Coding', 'Implementation', 'Algorithm', 
            'Write a', 'Implement', 'Create a Go', 'Design and implement'
        ]
        
        is_coding_question = any(indicator.lower() in question_content.lower() 
                               for indicator in coding_indicators)
        
        if not is_coding_question:
            return ""  # Return empty string instead of "N/A" to avoid pandas NaN issues
        
        # Extract all code blocks (```go or ``` blocks)
        code_blocks = []
        
        # Find Go code blocks
        go_blocks = re.findall(r'```go\s*\n(.*?)\n```', question_content, re.DOTALL)
        code_blocks.extend(go_blocks)
        
        # Find generic code blocks that might be Go code
        generic_blocks = re.findall(r'```\s*\n(.*?)\n```', question_content, re.DOTALL)
        for block in generic_blocks:
            # Check if it looks like Go code (contains Go keywords)
            go_keywords = ['package', 'import', 'func', 'type', 'var', 'const', 'go ', 'chan', 'select']
            if any(keyword in block for keyword in go_keywords):
                code_blocks.append(block)
        
        # Look for "Expected Answer", "Expected Solution", "Solution" sections
        solution_patterns = [
            r'\*\*Expected.*?Answer.*?\*\*:?\s*```.*?\n(.*?)\n```',
            r'\*\*Expected.*?Solution.*?\*\*:?\s*```.*?\n(.*?)\n```',
            r'\*\*Solution.*?\*\*:?\s*```.*?\n(.*?)\n```',
            r'### Expected Solution Structure\s*```.*?\n(.*?)\n```'
        ]
        
        for pattern in solution_patterns:
            matches = re.findall(pattern, question_content, re.DOTALL | re.IGNORECASE)
            code_blocks.extend(matches)
        
        if code_blocks:
            # Join all code blocks with separators
            cleaned_blocks = []
            for block in code_blocks:
                # Clean up the block
                cleaned_block = block.strip()
                if cleaned_block and len(cleaned_block) > 20:  # Filter out very short blocks
                    cleaned_blocks.append(cleaned_block)
            
            if cleaned_blocks:
                return '\n\n--- CODE BLOCK ---\n\n'.join(cleaned_blocks)
        
        # If no code blocks found, look for inline code or structured solutions
        # Look for "Expected Code Example" or similar patterns
        code_example_match = re.search(r'\*\*Expected.*?Code.*?Example.*?\*\*:?\s*(.+?)(?=\*\*|---|$)', 
                                     question_content, re.DOTALL | re.IGNORECASE)
        if code_example_match:
            return code_example_match.group(1).strip()
        
        return ""
    
    def format_worksheet(self, worksheet):
        """Apply formatting to worksheet: font size 14, text wrapping, and auto-adjust columns"""
        # Define styles
        default_font = Font(size=14)
        wrap_alignment = Alignment(wrap_text=True, vertical='top')
        
        # Apply styles to all cells
        for row in worksheet.iter_rows():
            for cell in row:
                cell.font = default_font
                cell.alignment = wrap_alignment
        
        # Auto-adjust column widths with text wrapping considerations
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if cell.value:
                        # For wrapped text, we want reasonable width limits
                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                except:
                    pass
            
            # Set width with reasonable limits for text wrapping
            if max_length > 0:
                # For very long content, limit width to encourage wrapping
                if max_length > 300:
                    adjusted_width = 80  # Wide column for long content
                elif max_length > 100:
                    adjusted_width = 60  # Medium-wide column
                else:
                    adjusted_width = min(max_length + 5, 40)  # Normal sizing with minimum padding
                
                worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def export_to_excel(self, output_file="interview_questions.xlsx"):
        """Export parsed data to Excel with separate sheets for each level"""
        
        # Parse all interview files
        interview_files = {
            'Junior': 'junior-go-developer.md',
            'Intermediate': 'intermediate-go-developer.md',
            'Senior': 'senior-go-developer.md'
        }
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            
            for level, filename in interview_files.items():
                file_path = self.interviews_dir / filename
                
                if not file_path.exists():
                    print(f"Warning: {filename} not found, skipping {level} level")
                    continue
                
                print(f"Processing {level} level: {filename}")
                interview_data = self.parse_markdown_file(file_path)
                
                # Create main questions DataFrame
                questions_data = []
                for q in interview_data['questions']:
                    questions_data.append({
                        'Part': q['part'],
                        'Question Title': q['question_title'],
                        'Question Text': q['question_text'],
                        'Expected Answer Points': q['expected_answer'],
                        'Code Answer': q['code_answer'],
                        'Follow-up Questions': q['followup'],
                        'Reference Link': q['reference_link'],
                        'Reference Content': q['reference_content']
                    })
                
                if questions_data:
                    df_questions = pd.DataFrame(questions_data)
                    df_questions.to_excel(writer, sheet_name=f'{level}_Questions', index=False)
                    
                    # Apply formatting (font 14, text wrap, auto-adjust columns)
                    worksheet = writer.sheets[f'{level}_Questions']
                    self.format_worksheet(worksheet)
                
                # Create alternatives DataFrame if alternatives exist
                if interview_data['alternatives']:
                    alternatives_data = []
                    for alt in interview_data['alternatives']:
                        alternatives_data.append({
                            'Alternative Question Text': alt['question_text'],
                            'Expected Answer Points': alt['expected_answer']
                        })
                    
                    df_alternatives = pd.DataFrame(alternatives_data)
                    df_alternatives.to_excel(writer, sheet_name=f'{level}_Alternatives', index=False)
                    
                    # Apply formatting to alternatives sheet
                    if f'{level}_Alternatives' in writer.sheets:
                        worksheet_alt = writer.sheets[f'{level}_Alternatives']
                        self.format_worksheet(worksheet_alt)
                
                # Create summary sheet with interview metadata
                summary_data = [{
                    'Level': level,
                    'Title': interview_data['title'],
                    'Duration': interview_data['duration'],
                    'Format': interview_data['format'],
                    'Target Level': interview_data['target_level'],
                    'Number of Questions': len(interview_data['questions']),
                    'Number of Alternatives': len(interview_data['alternatives'])
                }]
                
                if level == 'Junior':  # Create summary sheet only once
                    df_summary = pd.DataFrame([])
                
                # Append to summary data
                if 'df_summary' not in locals():
                    df_summary = pd.DataFrame(summary_data)
                else:
                    df_summary = pd.concat([df_summary, pd.DataFrame(summary_data)], ignore_index=True)
            
            # Write summary sheet
            if 'df_summary' in locals():
                df_summary.to_excel(writer, sheet_name='Summary', index=False)
                
                # Apply formatting to summary sheet
                worksheet_summary = writer.sheets['Summary']
                self.format_worksheet(worksheet_summary)
        
        print(f"Excel file exported successfully: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Export interview questions to Excel')
    parser.add_argument('--interviews-dir', default='interviews', 
                       help='Directory containing interview markdown files')
    parser.add_argument('--output', default='interview_questions.xlsx',
                       help='Output Excel file name')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.interviews_dir):
        print(f"Error: Directory '{args.interviews_dir}' not found")
        return 1
    
    exporter = InterviewExporter(args.interviews_dir)
    exporter.export_to_excel(args.output)
    
    return 0

if __name__ == '__main__':
    exit(main()) 