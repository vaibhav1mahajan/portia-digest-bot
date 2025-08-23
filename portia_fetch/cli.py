"""Command-line interface for Portia Digest Bot."""

import os
import json
import sys
from datetime import datetime, timezone, timedelta
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .client import PortiaClient
from .analyzer import PlanRunAnalyzer
from .summarizer import DigestSummarizer
from .mail_preview import MailPreview
import logging

app = typer.Typer(help="Portia Digest Bot - Fetch, analyze, and summarize plan runs")
console = Console()

# Subcommands
plans_app = typer.Typer(help="Manage plans")
runs_app = typer.Typer(help="Manage plan runs")
app.add_typer(plans_app, name="plans")
app.add_typer(runs_app, name="plan-runs")


def get_client() -> PortiaClient:
    """Get configured Portia client."""
    try:
        return PortiaClient()
    except ValueError as e:
        rprint(f"[red]❌ Configuration error: {e}[/red]")
        rprint("[yellow]💡 Please set PORTIA_API_KEY and PORTIA_ORG_ID environment variables[/yellow]")
        raise typer.Exit(1)


@plans_app.command("list")
def list_plans(
    limit: int = typer.Option(10, help="Maximum number of plans to return"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON")
):
    """List plans for the organization."""
    with get_client() as client:
        plans = client.list_plans(limit)
        
        if json_output:
            print(json.dumps([plan.dict() for plan in plans], indent=2, default=str))
        else:
            if not plans:
                rprint("[yellow]No plans found[/yellow]")
                return
                
            table = Table(title="Plans")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Description", style="white")
            table.add_column("Created", style="blue")
            
            for plan in plans:
                table.add_row(
                    plan.id[:12] + "...",
                    plan.name,
                    (plan.description or "")[:50] + ("..." if plan.description and len(plan.description) > 50 else ""),
                    plan.created_at.strftime("%Y-%m-%d %H:%M")
                )
            
            console.print(table)


@plans_app.command("get")
def get_plan(plan_id: str = typer.Argument(help="Plan ID to retrieve")):
    """Get details for a specific plan."""
    with get_client() as client:
        try:
            plan = client.get_plan(plan_id)
            print(json.dumps(plan.dict(), indent=2, default=str))
        except Exception as e:
            rprint(f"[red]❌ Failed to get plan: {e}[/red]")
            raise typer.Exit(1)


@runs_app.command("list")
def list_plan_runs(
    plan_id: Optional[str] = typer.Option(None, help="Filter by plan ID"),
    state: Optional[str] = typer.Option(None, help="Filter by state (COMPLETE, RUNNING, etc.)"),
    limit: int = typer.Option(10, help="Maximum number of runs to return"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
    since: Optional[str] = typer.Option(None, help="Start time (ISO format)")
):
    """List plan runs with optional filters."""
    with get_client() as client:
        since_dt = None
        if since:
            try:
                since_dt = datetime.fromisoformat(since.replace('Z', '+00:00'))
            except ValueError:
                rprint(f"[red]❌ Invalid date format: {since}[/red]")
                raise typer.Exit(1)
        
        runs = client.list_plan_runs(
            plan_id=plan_id,
            state=state,
            limit=limit,
            since=since_dt
        )
        
        if json_output:
            print(json.dumps([run.dict() for run in runs], indent=2, default=str))
        else:
            if not runs:
                rprint("[yellow]No plan runs found[/yellow]")
                return
                
            table = Table(title="Plan Runs")
            table.add_column("Run ID", style="cyan")
            table.add_column("Plan ID", style="green")
            table.add_column("State", style="yellow")
            table.add_column("Duration", style="blue")
            table.add_column("Completed", style="white")
            
            for run in runs:
                duration = f"{run.duration_ms/1000:.1f}s" if run.duration_ms else "N/A"
                completed = run.completed_at.strftime("%Y-%m-%d %H:%M") if run.completed_at else "N/A"
                
                table.add_row(
                    run.id[:12] + "...",
                    run.plan_id[:12] + "...",
                    run.state,
                    duration,
                    completed
                )
            
            console.print(table)


@runs_app.command("get")
def get_plan_run(run_id: str = typer.Argument(help="Plan run ID to retrieve")):
    """Get details for a specific plan run."""
    with get_client() as client:
        try:
            run = client.get_plan_run(run_id)
            print(json.dumps(run.dict(), indent=2, default=str))
        except Exception as e:
            rprint(f"[red]❌ Failed to get plan run: {e}[/red]")
            raise typer.Exit(1)


@app.command("analyze")
def analyze(
    today: bool = typer.Option(False, help="Analyze today's window"),
    yesterday: bool = typer.Option(False, help="Analyze yesterday's window"),
    since: Optional[str] = typer.Option(None, help="Start time (ISO format)"),
    until: Optional[str] = typer.Option(None, help="End time (ISO format)"),
    with_tools: bool = typer.Option(False, help="Include tool usage analysis"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON")
):
    """Analyze plan runs in a time window."""
    
    since_dt = None
    until_dt = None
    
    if today:
        now = datetime.now(timezone.utc)
        since_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = now
    elif yesterday:
        yesterday_dt = datetime.now(timezone.utc) - timedelta(days=1)
        since_dt = yesterday_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = since_dt + timedelta(days=1)
    elif since:
        try:
            since_dt = datetime.fromisoformat(since.replace('Z', '+00:00'))
            if until:
                until_dt = datetime.fromisoformat(until.replace('Z', '+00:00'))
        except ValueError as e:
            rprint(f"[red]❌ Invalid date format: {e}[/red]")
            raise typer.Exit(1)
    else:
        # Default to last 24 hours
        until_dt = datetime.now(timezone.utc)
        since_dt = until_dt - timedelta(days=1)
    
    with get_client() as client:
        try:
            analyzer = PlanRunAnalyzer(client)
            analysis = analyzer.analyze_window(since_dt, until_dt, with_tools)
            
            if json_output:
                print(json.dumps(analysis, indent=2, default=str))
            else:
                rprint(f"[green]📊 Analysis for {since_dt.strftime('%Y-%m-%d %H:%M')} to {until_dt.strftime('%Y-%m-%d %H:%M')} UTC[/green]")
                rprint(f"Total runs: {analysis.get('total_runs', 0)}")
                
                duration_stats = analysis.get('duration_stats', {})
                if duration_stats.get('count', 0) > 0:
                    rprint(f"Mean duration: {duration_stats.get('mean_seconds', 0):.1f}s")
                    rprint(f"Median duration: {duration_stats.get('median_seconds', 0):.1f}s")
                    rprint(f"P95 duration: {duration_stats.get('p95_seconds', 0):.1f}s")
                
                per_plan = analysis.get('per_plan_stats', [])
                if per_plan:
                    rprint("\n[blue]Top plans by activity:[/blue]")
                    for plan in per_plan[:5]:
                        mean_dur = plan.get('mean_duration_seconds')
                        dur_str = f", avg {mean_dur:.1f}s" if mean_dur else ""
                        rprint(f"  • {plan.get('plan_name', 'Unknown')}: {plan.get('run_count', 0)} runs{dur_str}")
                
        except Exception as e:
            rprint(f"[red]❌ Analysis failed: {e}[/red]")
            raise typer.Exit(1)


@app.command("summarize")
def summarize(
    today: bool = typer.Option(False, help="Summarize today's window"),
    yesterday: bool = typer.Option(False, help="Summarize yesterday's window"),
    since: Optional[str] = typer.Option(None, help="Start time (ISO format)"),
    until: Optional[str] = typer.Option(None, help="End time (ISO format)"),
    with_tools: bool = typer.Option(False, help="Include tool usage analysis"),
    json_only: bool = typer.Option(False, help="Output raw analysis JSON only")
):
    """Generate LLM summary of plan runs in a time window."""
    
    since_dt = None
    until_dt = None
    
    if today:
        now = datetime.now(timezone.utc)
        since_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = now
    elif yesterday:
        yesterday_dt = datetime.now(timezone.utc) - timedelta(days=1)
        since_dt = yesterday_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = since_dt + timedelta(days=1)
    elif since:
        try:
            since_dt = datetime.fromisoformat(since.replace('Z', '+00:00'))
            if until:
                until_dt = datetime.fromisoformat(until.replace('Z', '+00:00'))
        except ValueError as e:
            rprint(f"[red]❌ Invalid date format: {e}[/red]")
            raise typer.Exit(1)
    else:
        # Default to last 24 hours
        until_dt = datetime.now(timezone.utc)
        since_dt = until_dt - timedelta(days=1)
    
    with get_client() as client:
        try:
            analyzer = PlanRunAnalyzer(client)
            analysis = analyzer.analyze_window(since_dt, until_dt, with_tools)
            
            if json_only:
                print(json.dumps(analysis, indent=2, default=str))
                return
            
            summarizer = DigestSummarizer()
            summary = summarizer.summarize_analysis(analysis)
            
            rprint(f"[green]🤖 Summary for {since_dt.strftime('%Y-%m-%d %H:%M')} to {until_dt.strftime('%Y-%m-%d %H:%M')} UTC[/green]")
            rprint()
            print(summary)
            
        except Exception as e:
            rprint(f"[red]❌ Summarization failed: {e}[/red]")
            raise typer.Exit(1)


@app.command("preview-mail")
def preview_mail(
    today: bool = typer.Option(False, help="Preview today's email"),
    yesterday: bool = typer.Option(False, help="Preview yesterday's email"),
    since: Optional[str] = typer.Option(None, help="Start time (ISO format)"),
    until: Optional[str] = typer.Option(None, help="End time (ISO format)"),
    with_tools: bool = typer.Option(False, help="Include tool usage analysis")
):
    """Preview email content for digest summary."""
    
    since_dt = None
    until_dt = None
    
    if today:
        now = datetime.now(timezone.utc)
        since_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = now
    elif yesterday:
        yesterday_dt = datetime.now(timezone.utc) - timedelta(days=1)
        since_dt = yesterday_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = since_dt + timedelta(days=1)
    elif since:
        try:
            since_dt = datetime.fromisoformat(since.replace('Z', '+00:00'))
            if until:
                until_dt = datetime.fromisoformat(until.replace('Z', '+00:00'))
        except ValueError as e:
            rprint(f"[red]❌ Invalid date format: {e}[/red]")
            raise typer.Exit(1)
    else:
        # Default to yesterday
        yesterday_dt = datetime.now(timezone.utc) - timedelta(days=1)
        since_dt = yesterday_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        until_dt = since_dt + timedelta(days=1)
    
    preview = MailPreview()
    preview.print_preview(since_dt, until_dt, with_tools)


if __name__ == "__main__":
    app()
