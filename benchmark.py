#!/usr/bin/env python3
"""
Performance benchmark comparing TypeScript vs Python implementations.
Runs identical Gondor civilization examples and measures execution times.
"""

import subprocess
import time
import json
import statistics
from pathlib import Path
from datetime import datetime

def run_benchmark(command: str, label: str, iterations: int = 10) -> dict:
    """Run a command multiple times and record execution times."""
    print(f"\n{'='*60}")
    print(f"Benchmarking: {label}")
    print(f"Command: {command}")
    print(f"Iterations: {iterations}")
    print(f"{'='*60}")
    
    times = []
    errors = []
    
    for i in range(1, iterations + 1):
        try:
            start = time.time()
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            elapsed = time.time() - start
            
            if result.returncode == 0:
                times.append(elapsed)
                print(f"  Iteration {i:2d}: {elapsed:.4f}s ✓")
            else:
                error_msg = result.stderr[:100] if result.stderr else "Unknown error"
                errors.append(f"Iteration {i}: {error_msg}")
                print(f"  Iteration {i:2d}: FAILED - {error_msg}")
        except subprocess.TimeoutExpired:
            errors.append(f"Iteration {i}: Timeout (30s)")
            print(f"  Iteration {i:2d}: TIMEOUT")
        except Exception as e:
            errors.append(f"Iteration {i}: {str(e)}")
            print(f"  Iteration {i:2d}: ERROR - {str(e)}")
    
    # Calculate statistics
    if times:
        stats = {
            "label": label,
            "iterations_total": iterations,
            "iterations_successful": len(times),
            "iterations_failed": len(errors),
            "min": min(times),
            "max": max(times),
            "mean": statistics.mean(times),
            "median": statistics.median(times),
            "stdev": statistics.stdev(times) if len(times) > 1 else 0,
            "times": times,
            "errors": errors
        }
    else:
        stats = {
            "label": label,
            "iterations_total": iterations,
            "iterations_successful": 0,
            "iterations_failed": len(errors),
            "min": None,
            "max": None,
            "mean": None,
            "median": None,
            "stdev": None,
            "times": [],
            "errors": errors
        }
    
    return stats

def print_stats(stats: dict) -> None:
    """Print formatted benchmark statistics."""
    print(f"\n{stats['label']} Results:")
    print(f"  Successful: {stats['iterations_successful']}/{stats['iterations_total']}")
    
    if stats['mean'] is not None:
        print(f"  Min:        {stats['min']:.4f}s")
        print(f"  Max:        {stats['max']:.4f}s")
        print(f"  Mean:       {stats['mean']:.4f}s")
        print(f"  Median:     {stats['median']:.4f}s")
        print(f"  Stdev:      {stats['stdev']:.4f}s")
    else:
        print(f"  ERROR: All iterations failed!")
        for error in stats['errors'][:3]:
            print(f"    - {error}")

def main():
    print("\n" + "="*60)
    print("CIV7 MODDING TOOLS - PERFORMANCE BENCHMARK")
    print("="*60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    workspace_root = Path(__file__).parent
    
    # Benchmark TypeScript
    ts_stats = run_benchmark(
        "npm run build",
        "TypeScript Gondor Build",
        iterations=10
    )
    print_stats(ts_stats)
    
    # Benchmark Python
    py_stats = run_benchmark(
        "uv run python examples/gondor_civilization.py",
        "Python Gondor Build",
        iterations=10
    )
    print_stats(py_stats)
    
    # Comparison
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    if ts_stats['mean'] and py_stats['mean']:
        ratio = py_stats['mean'] / ts_stats['mean']
        faster = "TypeScript" if ts_stats['mean'] < py_stats['mean'] else "Python"
        print(f"\n  TypeScript Mean:  {ts_stats['mean']:.4f}s")
        print(f"  Python Mean:      {py_stats['mean']:.4f}s")
        print(f"  Ratio:            Python is {ratio:.2f}x {'slower' if ratio > 1 else 'faster'}")
        print(f"  Faster:           {faster}")
        print(f"  Time Difference:  {abs(ts_stats['mean'] - py_stats['mean']):.4f}s")
    else:
        print("\n  ERROR: Unable to calculate comparison (failed iterations)")
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "typescript": ts_stats,
        "python": py_stats,
        "comparison": {
            "ts_mean": ts_stats['mean'],
            "py_mean": py_stats['mean'],
            "ratio": py_stats['mean'] / ts_stats['mean'] if ts_stats['mean'] else None
        }
    }
    
    results_file = workspace_root / "benchmark_results.json"
    with open(results_file, 'w') as f:
        # Convert time lists to mean for JSON serialization
        clean_results = {
            "timestamp": results["timestamp"],
            "typescript": {
                **ts_stats,
                "times": None  # Exclude raw times list
            },
            "python": {
                **py_stats,
                "times": None  # Exclude raw times list
            },
            "comparison": results["comparison"]
        }
        json.dump(clean_results, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")
    print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
