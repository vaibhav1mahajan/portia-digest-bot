"""Email formatting utilities for Portia digest emails."""

import json
from typing import Dict, Any, List
from datetime import datetime

class EmailFormatter:
    """Format comprehensive digest emails for developers."""
    
    @staticmethod
    def format_email_body_from_data(analysis: Dict[str, Any], summary: str, date: str) -> str:
        """Format a concise email body from analysis data and summary."""
        
        # Extract clean summary
        clean_summary = EmailFormatter._extract_clean_summary(summary)
        
        # Build concise email
        email_parts = []
        
        # Header
        email_parts.append(f"🚀 Portia Daily Digest - {date}")
        email_parts.append("")
        
        # Key Metrics
        total_runs = analysis.get("total_runs", 0)
        completed_runs = analysis.get("completed_runs", 0)
        failed_runs = analysis.get("failed_runs", 0)
        success_rate = analysis.get("success_rate", 0)
        
        email_parts.append("📊 Executive Summary:")
        email_parts.append(f"• Total Plan Runs: {total_runs}")
        email_parts.append(f"• Successful Runs: {completed_runs}")
        email_parts.append(f"• Failed Runs: {failed_runs}")
        email_parts.append(f"• Success Rate: {success_rate:.1f}%")
        email_parts.append("")
        
        # Performance Overview
        duration_stats = analysis.get("duration_stats", {})
        if duration_stats.get("count", 0) > 0:
            email_parts.append("⏱️ Performance:")
            email_parts.append(f"• Average Run Time: {duration_stats.get('mean_seconds', 0):.1f}s")
            email_parts.append(f"• P95 Run Time: {duration_stats.get('p95_seconds', 0):.1f}s")
            email_parts.append(f"• Fastest Run: {duration_stats.get('min_seconds', 0):.1f}s")
            email_parts.append(f"• Slowest Run: {duration_stats.get('max_seconds', 0):.1f}s")
            email_parts.append("")
        
        # Top Plans
        fastest_plans = analysis.get("fastest_plans", [])
        if fastest_plans:
            email_parts.append("🏃‍♂️ Top Performing Plans:")
            for i, plan in enumerate(fastest_plans[:3], 1):
                email_parts.append(f"{i}. {plan['plan_name']} - {plan['avg_duration']:.1f}s avg")
            email_parts.append("")
        
        # Tool Usage (if available)
        tool_usage = analysis.get("tool_usage", {})
        if tool_usage.get("total_tool_invocations", 0) > 0:
            email_parts.append("🛠️ Tool Usage:")
            email_parts.append(f"• Total Tool Invocations: {tool_usage.get('total_tool_invocations', 0)}")
            email_parts.append(f"• Unique Tools Used: {tool_usage.get('unique_tools_used', 0)}")
            
            top_tools = tool_usage.get("top_tools", [])
            if top_tools:
                email_parts.append("• Top Tools:")
                for tool in top_tools[:3]:
                    email_parts.append(f"  - {tool['tool_name']}: {tool['usage_count']} uses")
            email_parts.append("")
        
        # AI Insights
        email_parts.append("🤖 AI Insights:")
        email_parts.append(clean_summary)
        email_parts.append("")
        
        # Footer
        email_parts.append("---")
        email_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC")
        email_parts.append("Portia Digest Bot - Your AI-powered automation insights")
        
        return "\n".join(email_parts)
    
    @staticmethod
    def format_email_body(analysis_file: str, summary_file: str, date: str) -> str:
        """Format a clean, concise email body from files."""
        
        # Read analysis data
        with open(analysis_file, 'r') as f:
            analysis = json.load(f)
        
        # Read summary (extract only the clean summary part)
        with open(summary_file, 'r') as f:
            summary_content = f.read()
        
        # Extract the clean summary (remove logs and extra content)
        clean_summary = EmailFormatter._extract_clean_summary(summary_content)
        
        return EmailFormatter.format_email_body_from_data(analysis, clean_summary, date)
    
    @staticmethod
    def _extract_clean_summary(summary_content: str) -> str:
        """Extract clean summary content from raw summary."""
        if not summary_content:
            return ""
        
        # Remove common log artifacts and verbose content
        lines = summary_content.split('\n')
        clean_lines = []
        
        # Skip lines that are likely logs or verbose content
        skip_patterns = [
            'DEBUG:', 'INFO:', 'WARNING:', 'ERROR:',
            'Traceback:', 'File "', 'line ',
            'Generated:', 'Summary:', 'Period:',
            'Total Runs:', 'Mean Duration:', 'P95 Duration:',
            'Generated: 2025-08-24'
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines with skip patterns
            if any(pattern in line for pattern in skip_patterns):
                continue
            
            # Skip lines that are just numbers or very short
            if len(line) < 10 and line.replace('.', '').replace('s', '').isdigit():
                continue
            
            clean_lines.append(line)
        
        # Join and clean up whitespace
        clean_summary = ' '.join(clean_lines)
        clean_summary = ' '.join(clean_summary.split())  # Remove extra whitespace
        
        return clean_summary
