"""Clean email formatter for digest summaries."""

import json
from datetime import datetime, timezone
from typing import Dict, Any


class EmailFormatter:
    """Format clean, concise email content."""
    
    @staticmethod
    def format_email_body(analysis_file: str, summary_file: str, date: str) -> str:
        """Format a clean, concise email body."""
        
        # Read analysis data
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        # Read summary (extract only the clean summary part)
        with open(summary_file, 'r') as f:
            summary_content = f.read()
        
        # Extract the clean summary (remove logs and extra content)
        clean_summary = EmailFormatter._extract_clean_summary(summary_content)
        
        # Get key metrics
        total_runs = analysis.get('total_runs', 0)
        duration_stats = analysis.get('duration_stats', {})
        
        # Create a simple, clean email body
        lines = [
            f"Portia Daily Digest - {date}",
            "",
            "Summary:",
            clean_summary,
            "",
            f"Total Runs: {total_runs}",
        ]
        
        # Add duration stats if available
        if duration_stats.get('count', 0) > 0:
            mean_duration = duration_stats.get('mean_seconds', 0)
            p95_duration = duration_stats.get('p95_seconds', 0)
            lines.extend([
                f"Mean Duration: {mean_duration:.1f}s",
                f"P95 Duration: {p95_duration:.1f}s"
            ])
        
        # Add top plans if available
        top_plans = analysis.get('top_plans', [])
        if top_plans:
            lines.append("")
            lines.append("Top Plans:")
            for plan in top_plans[:3]:  # Show top 3
                plan_id = plan.get('plan_id', 'Unknown')
                runs = plan.get('runs', 0)
                avg_duration = plan.get('avg_duration_seconds', 0)
                if avg_duration > 0:
                    lines.append(f"- {plan_id}: {runs} runs, {avg_duration:.1f}s avg")
                else:
                    lines.append(f"- {plan_id}: {runs} runs")
        
        lines.extend([
            "",
            f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
        ])
        
        return "\n".join(lines)
    
    @staticmethod
    def _extract_clean_summary(summary_content: str) -> str:
        """Extract clean summary from verbose content."""
        
        # Look for the actual summary content (after the logs)
        lines = summary_content.split('\n')
        clean_lines = []
        in_summary = False
        
        for line in lines:
            # Skip log lines
            if '| INFO |' in line or '| ERROR |' in line or '| WARNING |' in line:
                continue
            
            # Skip empty lines at the beginning
            if not in_summary and not line.strip():
                continue
            
            # Skip lines that look like logs
            if line.strip().startswith('2025-') and '|' in line:
                continue
            
            # Skip lines with just timestamps
            if line.strip().startswith('2025-') and len(line.strip()) < 30:
                continue
            
            # Skip verbose prompt content
            if 'You are a helpful assistant' in line:
                continue
            if 'Analyze the Portia plan run data' in line:
                continue
            if 'Use clear sections and bullet points' in line:
                continue
            if 'Analyze this Portia plan run data from' in line:
                continue
            if 'Provide a concise, developer-focused summary' in line:
                continue
            
            # Start collecting summary content
            if not in_summary and line.strip():
                in_summary = True
            
            if in_summary:
                clean_lines.append(line)
        
        # Join and clean up
        clean_summary = '\n'.join(clean_lines).strip()
        
        # Remove any remaining log artifacts and verbose content
        clean_summary = '\n'.join([
            line for line in clean_summary.split('\n')
            if not any(skip in line for skip in [
                '| INFO |', '| ERROR |', '| WARNING |',
                'Starting Portia', 'Using Portia cloud API',
                'Running planning_agent', 'Plan created with',
                'Step output', 'Final output', 'Generated:',
                'You are a helpful assistant',
                'Analyze the Portia plan run data',
                'Use clear sections and bullet points',
                'Analyze this Portia plan run data from',
                'Provide a concise, developer-focused summary',
                'Top Plans by Activity:',
                'Fastest Runs:',
                'Slowest Runs:'
            ])
        ])
        
        # Clean up extra whitespace and formatting
        clean_summary = '\n'.join([
            line.strip() for line in clean_summary.split('\n')
            if line.strip()
        ])
        
        return clean_summary.strip()
