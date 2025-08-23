"""Analytics and analysis for Portia plan runs."""

import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from collections import defaultdict, Counter
from .client import PortiaClient, PlanRun, Plan

class PlanRunAnalyzer:
    """Analyze plan runs and compute metrics."""
    
    def __init__(self, client: PortiaClient):
        self.client = client
    
    def analyze_window(
        self,
        since: datetime,
        until: Optional[datetime] = None,
        with_tools: bool = False
    ) -> Dict[str, Any]:
        """Analyze plan runs in a time window."""
        if until is None:
            until = datetime.now(timezone.utc)
        
        # Fetch plan runs in window
        runs = self.client.list_plan_runs(
            state="COMPLETE",
            since=since,
            until=until,
            limit=1000
        )
        
        if not runs:
            return {
                "window": {"since": since.isoformat(), "until": until.isoformat()},
                "total_runs": 0,
                "message": "No completed plan runs found in the specified window."
            }
        
        # Get plan details
        plan_ids = list(set(run.plan_id for run in runs))
        plans = {plan.id: plan for plan in self._fetch_plans(plan_ids)}
        
        # Compute metrics
        durations = [run.duration_ms for run in runs if run.duration_ms is not None]
        
        analysis = {
            "window": {"since": since.isoformat(), "until": until.isoformat()},
            "total_runs": len(runs),
            "duration_stats": self._compute_duration_stats(durations),
            "per_plan_stats": self._compute_per_plan_stats(runs, plans),
            "fastest_runs": self._get_extreme_runs(runs, plans, fastest=True, limit=3),
            "slowest_runs": self._get_extreme_runs(runs, plans, fastest=False, limit=3),
            "hourly_distribution": self._compute_hourly_distribution(runs),
        }
        
        if with_tools:
            analysis["tool_usage"] = self._analyze_tool_usage(runs)
        
        return analysis
    
    def _fetch_plans(self, plan_ids: List[str]) -> List[Plan]:
        """Fetch plan details."""
        plans = []
        for plan_id in plan_ids:
            try:
                plans.append(self.client.get_plan(plan_id))
            except Exception:
                # Create a fallback plan if fetch fails
                plans.append(Plan(
                    id=plan_id,
                    name=f"Plan {plan_id[:8]}",
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc)
                ))
        return plans
    
    def _compute_duration_stats(self, durations: List[int]) -> Dict[str, Any]:
        """Compute duration statistics."""
        if not durations:
            return {"count": 0}
        
        durations_sec = [d / 1000 for d in durations]
        
        return {
            "count": len(durations),
            "mean_seconds": statistics.mean(durations_sec),
            "median_seconds": statistics.median(durations_sec),
            "p95_seconds": self._percentile(durations_sec, 95),
            "min_seconds": min(durations_sec),
            "max_seconds": max(durations_sec),
        }
    
    def _compute_per_plan_stats(self, runs: List[PlanRun], plans: Dict[str, Plan]) -> List[Dict[str, Any]]:
        """Compute per-plan statistics."""
        plan_runs = defaultdict(list)
        for run in runs:
            plan_runs[run.plan_id].append(run)
        
        stats = []
        for plan_id, plan_run_list in plan_runs.items():
            plan_name = plans.get(plan_id, Plan(
                id=plan_id, name=f"Plan {plan_id[:8]}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )).name
            
            durations = [r.duration_ms for r in plan_run_list if r.duration_ms is not None]
            durations_sec = [d / 1000 for d in durations] if durations else []
            
            stats.append({
                "plan_id": plan_id,
                "plan_name": plan_name,
                "run_count": len(plan_run_list),
                "mean_duration_seconds": statistics.mean(durations_sec) if durations_sec else None,
                "median_duration_seconds": statistics.median(durations_sec) if durations_sec else None,
            })
        
        return sorted(stats, key=lambda x: x["run_count"], reverse=True)
    
    def _get_extreme_runs(
        self, runs: List[PlanRun], plans: Dict[str, Plan], fastest: bool, limit: int
    ) -> List[Dict[str, Any]]:
        """Get fastest or slowest runs."""
        valid_runs = [r for r in runs if r.duration_ms is not None]
        if not valid_runs:
            return []
        
        sorted_runs = sorted(valid_runs, key=lambda r: r.duration_ms, reverse=not fastest)
        
        result = []
        for run in sorted_runs[:limit]:
            plan_name = plans.get(run.plan_id, Plan(
                id=run.plan_id, name=f"Plan {run.plan_id[:8]}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )).name
            
            result.append({
                "run_id": run.id,
                "plan_name": plan_name,
                "duration_seconds": run.duration_ms / 1000,
                "completed_at": run.completed_at.isoformat() if run.completed_at else None,
            })
        
        return result
    
    def _compute_hourly_distribution(self, runs: List[PlanRun]) -> Dict[int, int]:
        """Compute hourly distribution of run completions."""
        hourly_counts = Counter()
        for run in runs:
            if run.completed_at:
                hour = run.completed_at.hour
                hourly_counts[hour] += 1
        
        return dict(sorted(hourly_counts.items()))
    
    def _analyze_tool_usage(self, runs: List[PlanRun]) -> Dict[str, Any]:
        """Analyze tool usage from run metadata."""
        tool_counts = Counter()
        tool_durations = defaultdict(list)
        
        for run in runs:
            if "tools_used" in run.metadata:
                for tool in run.metadata["tools_used"]:
                    tool_name = tool.get("name", "unknown")
                    tool_counts[tool_name] += 1
                    if "duration_ms" in tool and run.duration_ms:
                        tool_durations[tool_name].append(tool["duration_ms"])
        
        tool_stats = []
        for tool_name, count in tool_counts.most_common(10):
            durations = tool_durations.get(tool_name, [])
            avg_duration = statistics.mean(durations) / 1000 if durations else None
            
            tool_stats.append({
                "tool_name": tool_name,
                "usage_count": count,
                "avg_duration_seconds": avg_duration,
            })
        
        return {
            "total_tool_invocations": sum(tool_counts.values()),
            "unique_tools_used": len(tool_counts),
            "top_tools": tool_stats,
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile of a dataset."""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = (percentile / 100.0) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower_index = int(index)
            upper_index = lower_index + 1
            weight = index - lower_index
            return sorted_data[lower_index] * (1 - weight) + sorted_data[upper_index] * weight