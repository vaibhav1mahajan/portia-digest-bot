"""Email formatting utilities for Portia digest emails."""

import json
from typing import Dict, Any, List
from datetime import datetime

class EmailFormatter:
    """Format comprehensive digest emails for developers."""
    
    @staticmethod
    def format_email_body_from_data(analysis: Dict[str, Any], summary: str, date: str) -> str:
        """Format a comprehensive email body from analysis data and summary."""
        
        # Extract clean summary
        clean_summary = EmailFormatter._extract_clean_summary(summary)
        
        # Build comprehensive email
        email_parts = []
        
        # Header
        email_parts.append(f"# 🚀 Portia Daily Digest - {date}")
        email_parts.append("")
        
        # Executive Summary
        email_parts.append("## 📊 Executive Summary")
        email_parts.append("")
        
        # Key Metrics
        total_runs = analysis.get("total_runs", 0)
        completed_runs = analysis.get("completed_runs", 0)
        failed_runs = analysis.get("failed_runs", 0)
        success_rate = analysis.get("success_rate", 0)
        plans_created = analysis.get("plans_created", 0)
        
        email_parts.append(f"**📈 Key Metrics:**")
        email_parts.append(f"- **Total Plan Runs:** {total_runs}")
        email_parts.append(f"- **Successful Runs:** {completed_runs}")
        email_parts.append(f"- **Failed Runs:** {failed_runs}")
        email_parts.append(f"- **Success Rate:** {success_rate:.1f}%")
        email_parts.append(f"- **New Plans Created:** {plans_created}")
        email_parts.append("")
        
        # Performance Overview
        duration_stats = analysis.get("duration_stats", {})
        if duration_stats.get("count", 0) > 0:
            email_parts.append("**⏱️ Performance Overview:**")
            email_parts.append(f"- **Average Run Time:** {duration_stats.get('mean_seconds', 0):.1f}s")
            email_parts.append(f"- **Median Run Time:** {duration_stats.get('median_seconds', 0):.1f}s")
            email_parts.append(f"- **P95 Run Time:** {duration_stats.get('p95_seconds', 0):.1f}s")
            email_parts.append(f"- **Fastest Run:** {duration_stats.get('min_seconds', 0):.1f}s")
            email_parts.append(f"- **Slowest Run:** {duration_stats.get('max_seconds', 0):.1f}s")
            email_parts.append("")
        
        # Plan Performance Analysis
        email_parts.append("## 📋 Plan Performance Analysis")
        email_parts.append("")
        
        # Fastest and Slowest Plans
        fastest_plans = analysis.get("fastest_plans", [])
        slowest_plans = analysis.get("slowest_plans", [])
        
        if fastest_plans:
            email_parts.append("**🏃‍♂️ Fastest Plans (by avg duration):**")
            for i, plan in enumerate(fastest_plans[:3], 1):
                email_parts.append(f"{i}. **{plan['plan_name']}** - {plan['avg_duration']:.1f}s avg ({plan['run_count']} runs)")
            email_parts.append("")
        
        if slowest_plans:
            email_parts.append("**🐌 Slowest Plans (by avg duration):**")
            for i, plan in enumerate(slowest_plans[:3], 1):
                email_parts.append(f"{i}. **{plan['plan_name']}** - {plan['avg_duration']:.1f}s avg ({plan['run_count']} runs)")
            email_parts.append("")
        
        # Plan Success Rates
        plan_success_rates = analysis.get("plan_success_rates", [])
        if plan_success_rates:
            email_parts.append("**🎯 Plan Success Rates:**")
            for plan in plan_success_rates[:5]:
                status_emoji = "✅" if plan['success_rate'] >= 90 else "⚠️" if plan['success_rate'] >= 70 else "❌"
                email_parts.append(f"- {status_emoji} **{plan['plan_name']}** - {plan['success_rate']:.1f}% ({plan['completed_runs']}/{plan['total_runs']})")
            email_parts.append("")
        
        # Run Performance Analysis
        email_parts.append("## 🏃‍♂️ Run Performance Analysis")
        email_parts.append("")
        
        # Fastest and Slowest Runs
        fastest_runs = analysis.get("fastest_runs", [])
        slowest_runs = analysis.get("slowest_runs", [])
        
        if fastest_runs:
            email_parts.append("**⚡ Fastest Runs:**")
            for i, run in enumerate(fastest_runs[:3], 1):
                email_parts.append(f"{i}. **{run['plan_name']}** - {run['duration_seconds']:.1f}s")
            email_parts.append("")
        
        if slowest_runs:
            email_parts.append("**🐌 Slowest Runs:**")
            for i, run in enumerate(slowest_runs[:3], 1):
                email_parts.append(f"{i}. **{run['plan_name']}** - {run['duration_seconds']:.1f}s")
            email_parts.append("")
        
        # Tool Usage Analysis
        tool_usage = analysis.get("tool_usage", {})
        if tool_usage and tool_usage.get("top_tools"):
            email_parts.append("## 🛠️ Tool Usage Analysis")
            email_parts.append("")
            
            email_parts.append(f"**📊 Tool Statistics:**")
            email_parts.append(f"- **Total Tool Invocations:** {tool_usage.get('total_tool_invocations', 0)}")
            email_parts.append(f"- **Unique Tools Used:** {tool_usage.get('unique_tools_used', 0)}")
            email_parts.append("")
            
            email_parts.append("**🔝 Top 5 Most Used Tools:**")
            for i, tool in enumerate(tool_usage.get("top_tools", [])[:5], 1):
                success_emoji = "✅" if tool.get('success_rate', 0) >= 90 else "⚠️" if tool.get('success_rate', 0) >= 70 else "❌"
                email_parts.append(f"{i}. **{tool['tool_name']}** - {tool['usage_count']} uses, {success_emoji} {tool.get('success_rate', 0):.1f}% success")
                if tool.get('avg_duration_seconds'):
                    email_parts.append(f"   ⏱️ Avg duration: {tool['avg_duration_seconds']:.1f}s")
            email_parts.append("")
        
        # Tool Performance Analysis
        tool_performance = analysis.get("tool_performance", {})
        if tool_performance and tool_performance.get("performance_details"):
            email_parts.append("**⚡ Tool Performance (by avg duration):**")
            for i, tool in enumerate(tool_performance.get("performance_details", [])[:5], 1):
                email_parts.append(f"{i}. **{tool['tool_name']}** - {tool['avg_duration']:.1f}s avg, {tool['success_rate']:.1f}% success")
            email_parts.append("")
        
        # Failure Analysis
        failure_analysis = analysis.get("failure_analysis", {})
        if failure_analysis and failure_analysis.get("count", 0) > 0:
            email_parts.append("## ❌ Failure Analysis")
            email_parts.append("")
            
            email_parts.append(f"**📉 Failed Runs:** {failure_analysis['count']}")
            email_parts.append("")
            
            if failure_analysis.get("details"):
                email_parts.append("**🔍 Recent Failures:**")
                for failure in failure_analysis["details"][:3]:
                    email_parts.append(f"- **{failure['plan_name']}** - {failure.get('error_message', 'Unknown error')}")
                email_parts.append("")
        
        # Resource Usage
        resource_usage = analysis.get("resource_usage", {})
        if resource_usage:
            email_parts.append("## 💾 Resource Usage")
            email_parts.append("")
            
            email_parts.append(f"**📊 Resource Statistics:**")
            email_parts.append(f"- **Total Execution Time:** {resource_usage.get('total_duration', 0):.1f}s")
            email_parts.append(f"- **Average Run Duration:** {resource_usage.get('avg_duration', 0):.1f}s")
            email_parts.append(f"- **Total Runs:** {resource_usage.get('total_runs', 0)}")
            email_parts.append("")
        
        # Temporal Analysis
        hourly_dist = analysis.get("hourly_distribution", {})
        daily_dist = analysis.get("daily_distribution", {})
        
        if hourly_dist or daily_dist:
            email_parts.append("## 📅 Temporal Analysis")
            email_parts.append("")
            
            if daily_dist:
                email_parts.append("**📈 Daily Distribution:**")
                for date, count in list(daily_dist.items())[-3:]:
                    email_parts.append(f"- **{date}:** {count} runs")
                email_parts.append("")
            
            if hourly_dist:
                peak_hour = max(hourly_dist.items(), key=lambda x: x[1]) if hourly_dist else None
                if peak_hour:
                    email_parts.append(f"**🕐 Peak Activity Hour:** {peak_hour[0]}:00 UTC ({peak_hour[1]} runs)")
                    email_parts.append("")
        
        # Execution Rate Analysis
        execution_rate = analysis.get("execution_rate", {})
        if execution_rate and execution_rate.get("total_plans", 0) > 0:
            email_parts.append("## 🎯 Plan Execution Analysis")
            email_parts.append("")
            
            email_parts.append(f"**📊 Plan Execution Rate:** {execution_rate.get('execution_rate', 0):.1f}%")
            email_parts.append(f"- **Plans Created:** {execution_rate.get('total_plans', 0)}")
            email_parts.append(f"- **Plans Executed:** {execution_rate.get('executed_plans', 0)}")
            email_parts.append("")
        
        # AI Summary
        if clean_summary:
            email_parts.append("## 🤖 AI Insights")
            email_parts.append("")
            email_parts.append(clean_summary)
            email_parts.append("")
        
        # Footer
        email_parts.append("---")
        email_parts.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*")
        email_parts.append("*Portia Digest Bot - Your AI-powered automation insights*")
        
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
