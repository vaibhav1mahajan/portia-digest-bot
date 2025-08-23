"""LLM summarizer using Portia SDK."""

import json
from typing import Dict, Any, Optional
from portia import Portia, Config, StorageClass

class DigestSummarizer:
    """Summarize analytics using Portia LLM."""
    
    def __init__(self):
        config = Config.from_default(storage_class=StorageClass.MEMORY)
        self.portia = Portia(config=config)
    
    def summarize_analysis(
        self, 
        analysis: Dict[str, Any], 
        format_type: str = "text"
    ) -> str:
        """Summarize analysis data using LLM."""
        
        prompt = self._build_summarization_prompt(analysis)
        
        try:
            # Use Portia's run method with a prompt that asks for summarization
            task = f"""
{self._get_system_prompt(format_type)}

{prompt}
"""
            plan_run = self.portia.run(task)
            
            # Handle different output formats from the new API
            if hasattr(plan_run, 'outputs') and hasattr(plan_run.outputs, 'final_output'):
                output = plan_run.outputs.final_output
            elif hasattr(plan_run, 'final_output'):
                output = plan_run.final_output
            elif hasattr(plan_run, 'output'):
                output = plan_run.output
            else:
                # Fallback: try to get the output from the last step
                if hasattr(plan_run, 'steps') and plan_run.steps:
                    last_step = plan_run.steps[-1]
                    if hasattr(last_step, 'output'):
                        output = last_step.output
                    else:
                        # If all else fails, return a basic message
                        return f"Summary generated successfully. Raw analysis:\n{json.dumps(analysis, indent=2)}"
                else:
                    return f"Summary generated successfully. Raw analysis:\n{json.dumps(analysis, indent=2)}"
            
            # Convert output to string and extract the actual content
            output_str = str(output)
            
            # If the output contains a 'summary' field, extract it
            if 'summary=' in output_str:
                # Extract the summary part after 'summary='
                summary_start = output_str.find('summary=') + 8
                summary_end = output_str.find('\n', summary_start)
                if summary_end == -1:
                    summary_end = len(output_str)
                output_str = output_str[summary_start:summary_end].strip()
            
            # Clean up the output
            output_str = output_str.strip()
            if output_str.startswith("'") and output_str.endswith("'"):
                output_str = output_str[1:-1]
            
            return output_str
            
        except Exception as e:
            return f"❌ Failed to generate summary: {e}\n\nRaw analysis:\n{json.dumps(analysis, indent=2)}"
    
    def _get_system_prompt(self, format_type: str) -> str:
        """Get system prompt based on format type."""
        if format_type == "email":
            return """You are a helpful assistant that creates concise daily digest summaries for software developers.

Create a professional but friendly email-style summary of Portia plan run analytics. Focus on:

- Key metrics and trends
- Notable performance insights  
- Any concerning patterns
- Brief actionable insights

Keep it concise (2-3 paragraphs max), developer-friendly, and highlight the most important findings."""
        else:  # text format
            return """You are a helpful assistant that creates daily digest summaries for software developers.

Analyze the Portia plan run data and create a clear, structured summary. Focus on:

- Overview of activity
- Performance metrics (duration stats, p95, etc.)
- Top performing plans
- Any notable patterns or outliers
- Brief insights for developers

Use clear sections and bullet points where helpful. Keep it informative but concise."""
    
    def _build_summarization_prompt(self, analysis: Dict[str, Any]) -> str:
        """Build the summarization prompt."""
        
        # Extract key information
        window = analysis.get("window", {})
        total_runs = analysis.get("total_runs", 0)
        duration_stats = analysis.get("duration_stats", {})
        per_plan_stats = analysis.get("per_plan_stats", [])
        fastest_runs = analysis.get("fastest_runs", [])
        slowest_runs = analysis.get("slowest_runs", [])
        tool_usage = analysis.get("tool_usage", {})
        
        prompt_parts = [
            f"Analyze this Portia plan run data from {window.get('since', 'unknown')} to {window.get('until', 'now')}:",
            f"\n📊 Overview:",
            f"- Total completed runs: {total_runs}",
        ]
        
        if duration_stats.get("count", 0) > 0:
            prompt_parts.extend([
                f"\n⏱️ Performance:",
                f"- Mean duration: {duration_stats.get('mean_seconds', 0):.1f}s",
                f"- Median duration: {duration_stats.get('median_seconds', 0):.1f}s", 
                f"- P95 duration: {duration_stats.get('p95_seconds', 0):.1f}s",
                f"- Range: {duration_stats.get('min_seconds', 0):.1f}s - {duration_stats.get('max_seconds', 0):.1f}s"
            ])
        
        if per_plan_stats:
            prompt_parts.append(f"\n📋 Top Plans by Activity:")
            for i, plan in enumerate(per_plan_stats[:5]):
                mean_dur = plan.get('mean_duration_seconds')
                dur_str = f", avg {mean_dur:.1f}s" if mean_dur else ""
                prompt_parts.append(f"- {plan.get('plan_name', 'Unknown')}: {plan.get('run_count', 0)} runs{dur_str}")
        
        if fastest_runs:
            prompt_parts.append(f"\n🚀 Fastest Runs:")
            for run in fastest_runs:
                prompt_parts.append(f"- {run.get('plan_name', 'Unknown')}: {run.get('duration_seconds', 0):.1f}s")
        
        if slowest_runs:
            prompt_parts.append(f"\n🐌 Slowest Runs:")
            for run in slowest_runs:
                prompt_parts.append(f"- {run.get('plan_name', 'Unknown')}: {run.get('duration_seconds', 0):.1f}s")
        
        if tool_usage and tool_usage.get('total_tool_invocations', 0) > 0:
            prompt_parts.extend([
                f"\n🔧 Tool Usage:",
                f"- Total tool invocations: {tool_usage.get('total_tool_invocations', 0)}",
                f"- Unique tools used: {tool_usage.get('unique_tools_used', 0)}"
            ])
            
            top_tools = tool_usage.get('top_tools', [])[:3]
            if top_tools:
                prompt_parts.append("- Top tools:")
                for tool in top_tools:
                    avg_dur = tool.get('avg_duration_seconds')
                    dur_str = f", avg {avg_dur:.1f}s" if avg_dur else ""
                    prompt_parts.append(f"  - {tool.get('tool_name', 'Unknown')}: {tool.get('usage_count', 0)} uses{dur_str}")
        
        prompt_parts.append("\nProvide a concise, developer-focused summary highlighting key insights and any notable patterns.")
        
        return "\n".join(prompt_parts)