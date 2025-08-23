"""Email preview generator for digest summaries."""

import os
import json
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any
from .client import PortiaClient
from .analyzer import PlanRunAnalyzer
from .summarizer import DigestSummarizer

class MailPreview:
    """Generate email preview for digest summaries."""
    
    def __init__(self):
        self.client = PortiaClient()
        self.analyzer = PlanRunAnalyzer(self.client)
        self.summarizer = DigestSummarizer()
    
    def generate_preview(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        with_tools: bool = False
    ) -> Dict[str, str]:
        """Generate email subject and body preview."""
        
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=1)
        if until is None:
            until = datetime.now(timezone.utc)
        
        # Get analysis
        analysis = self.analyzer.analyze_window(since, until, with_tools)
        
        # Generate summary
        summary = self.summarizer.summarize_analysis(analysis, format_type="email")
        
        # Create subject
        total_runs = analysis.get("total_runs", 0)
        date_str = since.strftime("%Y-%m-%d")
        subject_prefix = os.getenv("DIGEST_SUBJECT_PREFIX", "Portia Daily Digest")
        subject = f"{subject_prefix} - {total_runs} runs on {date_str}"
        
        # Create body
        body = self._format_email_body(summary, analysis, since, until)
        
        return {
            "subject": subject,
            "body": body
        }
    
    def _format_email_body(
        self, 
        summary: str, 
        analysis: Dict[str, Any], 
        since: datetime, 
        until: datetime
    ) -> str:
        """Format email body."""
        
        lines = [
            f"Portia Plan Runs Summary",
            f"Period: {since.strftime('%Y-%m-%d %H:%M UTC')} to {until.strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            summary,
            "",
            "---",
            f"Generated at: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"Total runs analyzed: {analysis.get('total_runs', 0)}",
        ]
        
        duration_stats = analysis.get('duration_stats', {})
        if duration_stats.get('count', 0) > 0:
            lines.extend([
                f"Mean duration: {duration_stats.get('mean_seconds', 0):.1f}s",
                f"P95 duration: {duration_stats.get('p95_seconds', 0):.1f}s"
            ])
        
        return "\n".join(lines)
    
    def print_preview(
        self,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
        with_tools: bool = False
    ):
        """Print email preview to stdout."""
        
        try:
            preview = self.generate_preview(since, until, with_tools)
            
            print("=" * 60)
            print("EMAIL PREVIEW")
            print("=" * 60)
            print()
            print(f"Subject: {preview['subject']}")
            print()
            print("Body:")
            print("-" * 40)
            print(preview['body'])
            print("-" * 40)
            print()
            
        except Exception as e:
            print(f"❌ Failed to generate preview: {e}")
        
        finally:
            self.client.close()

def main():
    """CLI entry point for mail preview."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate email preview")
    parser.add_argument("--today", action="store_true", help="Use today's window")
    parser.add_argument("--yesterday", action="store_true", help="Use yesterday's window")
    parser.add_argument("--with-tools", action="store_true", help="Include tool usage analysis")
    parser.add_argument("--since", help="Start time (ISO format)")
    parser.add_argument("--until", help="End time (ISO format)")
    
    args = parser.parse_args()
    
    since = None
    until = None
    
    if args.today:
        now = datetime.now(timezone.utc)
        since = now.replace(hour=0, minute=0, second=0, microsecond=0)
        until = now
    elif args.yesterday:
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        since = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        until = since + timedelta(days=1)
    elif args.since:
        since = datetime.fromisoformat(args.since.replace('Z', '+00:00'))
        if args.until:
            until = datetime.fromisoformat(args.until.replace('Z', '+00:00'))
    
    preview = MailPreview()
    preview.print_preview(since, until, args.with_tools)

if __name__ == "__main__":
    main()