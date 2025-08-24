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
        
        # Fetch all plan runs in window (including failed ones)
        all_runs = self.client.list_plan_runs(
            since=since,
            until=until,
            limit=1000
        )
        
        # Fetch completed runs separately for detailed analysis
        completed_runs = self.client.list_plan_runs(
            state="COMPLETE",
            since=since,
            until=until,
            limit=1000
        )
        
        # Fetch failed runs
        failed_runs = self.client.list_plan_runs(
            state="FAILED",
            since=since,
            until=until,
            limit=1000
        )
        
        # Fetch plans created in window
        plans_created = self._fetch_plans_created_in_window(since, until)
        
        if not all_runs:
            return {
                "window": {"since": since.isoformat(), "until": until.isoformat()},
                "total_runs": 0,
                "message": "No plan runs found in the specified window."
            }
        
        # Get plan details for all runs
        plan_ids = list(set(run.plan_id for run in all_runs))
        plans = {plan.id: plan for plan in self._fetch_plans(plan_ids)}
        
        # Compute comprehensive metrics
        analysis = {
            "window": {"since": since.isoformat(), "until": until.isoformat()},
            
            # Plan Creation Metrics
            "plans_created": len(plans_created),
            "plans_created_details": self._analyze_plans_created(plans_created),
            
            # Execution Metrics
            "total_runs": len(all_runs),
            "completed_runs": len(completed_runs),
            "failed_runs": len(failed_runs),
            "success_rate": (len(completed_runs) / len(all_runs) * 100) if all_runs else 0,
            "execution_rate": self._compute_execution_rate(plans_created, all_runs),
            
            # Duration Statistics
            "duration_stats": self._compute_duration_stats([run.duration_ms for run in completed_runs if run.duration_ms]),
            "plan_duration_stats": self._compute_plan_duration_stats(completed_runs, plans),
            
            # Performance Analysis
            "fastest_runs": self._get_extreme_runs(completed_runs, plans, fastest=True, limit=5),
            "slowest_runs": self._get_extreme_runs(completed_runs, plans, fastest=False, limit=5),
            "fastest_plans": self._get_extreme_plans(completed_runs, plans, fastest=True, limit=5),
            "slowest_plans": self._get_extreme_plans(completed_runs, plans, fastest=False, limit=5),
            
            # Plan Performance
            "per_plan_stats": self._compute_per_plan_stats(completed_runs, plans),
            "plan_success_rates": self._compute_plan_success_rates(all_runs, plans),
            
            # Temporal Analysis
            "hourly_distribution": self._compute_hourly_distribution(completed_runs),
            "daily_distribution": self._compute_daily_distribution(completed_runs),
            
            # Failure Analysis
            "failure_analysis": self._analyze_failures(failed_runs, plans),
            
            # Resource Usage
            "resource_usage": self._analyze_resource_usage(completed_runs),
        }
        
        if with_tools:
            analysis["tool_usage"] = self._analyze_tool_usage(completed_runs)
            analysis["tool_performance"] = self._analyze_tool_performance(completed_runs)
        
        return analysis
    
    def _fetch_plans_created_in_window(self, since: datetime, until: datetime) -> List[Plan]:
        """Fetch plans created in the time window."""
        try:
            all_plans = self.client.list_plans(limit=1000)
            return [plan for plan in all_plans if since <= plan.created_at <= until]
        except Exception:
            return []
    
    def _analyze_plans_created(self, plans: List[Plan]) -> Dict[str, Any]:
        """Analyze plans created in the window."""
        if not plans:
            return {"count": 0, "details": []}
        
        plan_details = []
        for plan in plans:
            plan_details.append({
                "plan_id": plan.id,
                "plan_name": plan.name,
                "created_at": plan.created_at.isoformat(),
                "updated_at": plan.updated_at.isoformat(),
            })
        
        return {
            "count": len(plans),
            "details": sorted(plan_details, key=lambda x: x["created_at"], reverse=True)
        }
    
    def _compute_execution_rate(self, plans_created: List[Plan], all_runs: List[PlanRun]) -> Dict[str, Any]:
        """Compute execution rate of created plans."""
        if not plans_created:
            return {"execution_rate": 0, "executed_plans": 0, "total_plans": 0}
        
        created_plan_ids = {plan.id for plan in plans_created}
        executed_plan_ids = {run.plan_id for run in all_runs}
        executed_created_plans = created_plan_ids.intersection(executed_plan_ids)
        
        return {
            "execution_rate": (len(executed_created_plans) / len(created_plan_ids) * 100) if created_plan_ids else 0,
            "executed_plans": len(executed_created_plans),
            "total_plans": len(created_plan_ids),
            "executed_plan_ids": list(executed_created_plans)
        }
    
    def _compute_plan_duration_stats(self, runs: List[PlanRun], plans: Dict[str, Plan]) -> Dict[str, Any]:
        """Compute duration statistics per plan."""
        plan_durations = defaultdict(list)
        for run in runs:
            if run.duration_ms:
                plan_durations[run.plan_id].append(run.duration_ms / 1000)
        
        plan_stats = []
        for plan_id, durations in plan_durations.items():
            plan_name = plans.get(plan_id, Plan(
                id=plan_id, name=f"Plan {plan_id[:8]}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )).name
            
            plan_stats.append({
                "plan_id": plan_id,
                "plan_name": plan_name,
                "avg_duration": statistics.mean(durations),
                "median_duration": statistics.median(durations),
                "min_duration": min(durations),
                "max_duration": max(durations),
                "run_count": len(durations)
            })
        
        return {
            "plan_count": len(plan_stats),
            "overall_avg_plan_duration": statistics.mean([p["avg_duration"] for p in plan_stats]) if plan_stats else 0,
            "plan_details": sorted(plan_stats, key=lambda x: x["avg_duration"], reverse=True)
        }
    
    def _get_extreme_plans(self, runs: List[PlanRun], plans: Dict[str, Plan], fastest: bool, limit: int) -> List[Dict[str, Any]]:
        """Get fastest or slowest plans based on average duration."""
        plan_durations = defaultdict(list)
        for run in runs:
            if run.duration_ms:
                plan_durations[run.plan_id].append(run.duration_ms / 1000)
        
        plan_avg_durations = []
        for plan_id, durations in plan_durations.items():
            plan_name = plans.get(plan_id, Plan(
                id=plan_id, name=f"Plan {plan_id[:8]}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )).name
            
            plan_avg_durations.append({
                "plan_id": plan_id,
                "plan_name": plan_name,
                "avg_duration": statistics.mean(durations),
                "run_count": len(durations)
            })
        
        sorted_plans = sorted(plan_avg_durations, key=lambda x: x["avg_duration"], reverse=not fastest)
        return sorted_plans[:limit]
    
    def _compute_plan_success_rates(self, all_runs: List[PlanRun], plans: Dict[str, Plan]) -> List[Dict[str, Any]]:
        """Compute success rates for each plan."""
        plan_runs = defaultdict(lambda: {"completed": 0, "failed": 0, "total": 0})
        
        for run in all_runs:
            plan_runs[run.plan_id]["total"] += 1
            if run.state == "COMPLETE":
                plan_runs[run.plan_id]["completed"] += 1
            elif run.state == "FAILED":
                plan_runs[run.plan_id]["failed"] += 1
        
        success_rates = []
        for plan_id, stats in plan_runs.items():
            plan_name = plans.get(plan_id, Plan(
                id=plan_id, name=f"Plan {plan_id[:8]}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )).name
            
            success_rate = (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            
            success_rates.append({
                "plan_id": plan_id,
                "plan_name": plan_name,
                "success_rate": success_rate,
                "completed_runs": stats["completed"],
                "failed_runs": stats["failed"],
                "total_runs": stats["total"]
            })
        
        return sorted(success_rates, key=lambda x: x["success_rate"], reverse=True)
    
    def _compute_daily_distribution(self, runs: List[PlanRun]) -> Dict[str, int]:
        """Compute daily distribution of run completions."""
        daily_counts = Counter()
        for run in runs:
            if run.completed_at:
                date_str = run.completed_at.strftime('%Y-%m-%d')
                daily_counts[date_str] += 1
        
        return dict(sorted(daily_counts.items()))
    
    def _analyze_failures(self, failed_runs: List[PlanRun], plans: Dict[str, Plan]) -> Dict[str, Any]:
        """Analyze failed runs."""
        if not failed_runs:
            return {"count": 0, "details": []}
        
        failure_details = []
        for run in failed_runs:
            plan_name = plans.get(run.plan_id, Plan(
                id=run.plan_id, name=f"Plan {run.plan_id[:8]}",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )).name
            
            failure_details.append({
                "run_id": run.id,
                "plan_id": run.plan_id,
                "plan_name": plan_name,
                "failed_at": run.completed_at.isoformat() if run.completed_at else None,
                "error_message": run.metadata.get("error", "Unknown error") if run.metadata else "Unknown error"
            })
        
        return {
            "count": len(failed_runs),
            "details": failure_details
        }
    
    def _analyze_resource_usage(self, runs: List[PlanRun]) -> Dict[str, Any]:
        """Analyze resource usage patterns."""
        if not runs:
            return {"total_duration": 0, "avg_duration": 0}
        
        total_duration = sum(run.duration_ms for run in runs if run.duration_ms) / 1000
        avg_duration = total_duration / len(runs) if runs else 0
        
        return {
            "total_duration": total_duration,
            "avg_duration": avg_duration,
            "total_runs": len(runs)
        }

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
        tool_success_rates = defaultdict(lambda: {"success": 0, "total": 0})
        
        for run in runs:
            if "tools_used" in run.metadata:
                for tool in run.metadata["tools_used"]:
                    tool_name = tool.get("name", "unknown")
                    tool_counts[tool_name] += 1
                    tool_success_rates[tool_name]["total"] += 1
                    
                    if tool.get("success", True):
                        tool_success_rates[tool_name]["success"] += 1
                    
                    if "duration_ms" in tool and run.duration_ms:
                        tool_durations[tool_name].append(tool["duration_ms"])
        
        tool_stats = []
        for tool_name, count in tool_counts.most_common(10):
            durations = tool_durations.get(tool_name, [])
            avg_duration = statistics.mean(durations) / 1000 if durations else None
            
            success_rate = (tool_success_rates[tool_name]["success"] / tool_success_rates[tool_name]["total"] * 100) if tool_success_rates[tool_name]["total"] > 0 else 0
            
            tool_stats.append({
                "tool_name": tool_name,
                "usage_count": count,
                "avg_duration_seconds": avg_duration,
                "success_rate": success_rate,
                "success_count": tool_success_rates[tool_name]["success"],
                "total_invocations": tool_success_rates[tool_name]["total"]
            })
        
        return {
            "total_tool_invocations": sum(tool_counts.values()),
            "unique_tools_used": len(tool_counts),
            "top_tools": tool_stats,
            "tool_distribution": dict(tool_counts.most_common(10))
        }
    
    def _analyze_tool_performance(self, runs: List[PlanRun]) -> Dict[str, Any]:
        """Analyze tool performance metrics."""
        tool_performance = defaultdict(lambda: {"durations": [], "success_count": 0, "total_count": 0})
        
        for run in runs:
            if "tools_used" in run.metadata:
                for tool in run.metadata["tools_used"]:
                    tool_name = tool.get("name", "unknown")
                    tool_performance[tool_name]["total_count"] += 1
                    
                    if tool.get("success", True):
                        tool_performance[tool_name]["success_count"] += 1
                    
                    if "duration_ms" in tool:
                        tool_performance[tool_name]["durations"].append(tool["duration_ms"])
        
        performance_stats = []
        for tool_name, stats in tool_performance.items():
            if stats["durations"]:
                durations_sec = [d / 1000 for d in stats["durations"]]
                success_rate = (stats["success_count"] / stats["total_count"] * 100) if stats["total_count"] > 0 else 0
                
                performance_stats.append({
                    "tool_name": tool_name,
                    "avg_duration": statistics.mean(durations_sec),
                    "median_duration": statistics.median(durations_sec),
                    "min_duration": min(durations_sec),
                    "max_duration": max(durations_sec),
                    "success_rate": success_rate,
                    "total_invocations": stats["total_count"]
                })
        
        return {
            "tool_count": len(performance_stats),
            "performance_details": sorted(performance_stats, key=lambda x: x["avg_duration"], reverse=True)
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