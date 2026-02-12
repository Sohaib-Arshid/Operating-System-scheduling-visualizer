"""
Main Application - FCFS Cloud Video Rendering Task Scheduling System

This program simulates a cloud-based operating system scheduler using the
First Come First Served (FCFS) algorithm to manage video rendering tasks
across multiple Virtual Machines.

Operating System Concepts Demonstrated:
- CPU Scheduling (FCFS Algorithm)
- Multi-processor Scheduling
- Resource Allocation
- Performance Metrics (Makespan, Utilization)
"""

from task import Task
from virtual_machine import VirtualMachine
from scheduler import FCFSScheduler
from visualizer import Visualizer


def create_sample_tasks():
    """
    Create sample video rendering tasks.
    
    Returns:
        list: List of Task objects representing video rendering jobs
    """
    tasks = [
        Task('T1', arrival_time=0, burst_time=5),   # Short video render
        Task('T2', arrival_time=1, burst_time=8),   # Medium video render
        Task('T3', arrival_time=2, burst_time=3),   # Quick video render
        Task('T4', arrival_time=3, burst_time=7),   # Medium video render
        Task('T5', arrival_time=4, burst_time=4),   # Short video render
        Task('T6', arrival_time=5, burst_time=6),   # Medium video render
    ]
    return tasks


def create_virtual_machines(num_vms=3):
    """
    Create Virtual Machines for task execution.
    
    Args:
        num_vms (int): Number of VMs to create
        
    Returns:
        list: List of VirtualMachine objects
    """
    vms = [VirtualMachine(f'VM{i+1}') for i in range(num_vms)]
    return vms


def main():
    """
    Main function to run the FCFS scheduling simulation.
    """
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  FCFS CLOUD VIDEO RENDERING TASK SCHEDULING SYSTEM  ".center(68) + "║")
    print("║" + "  Operating System Project - CPU Scheduling Simulation  ".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝\n")
    
    # Step 1: Create tasks and VMs
    print("📋 Initializing System Components...")
    tasks = create_sample_tasks()
    vms = create_virtual_machines(num_vms=3)
    
    print(f"✓ Created {len(tasks)} video rendering tasks")
    print(f"✓ Initialized {len(vms)} Virtual Machines")
    
    # Step 2: Create and run scheduler
    print("\n🚀 Starting FCFS Scheduler...")
    scheduler = FCFSScheduler(tasks, vms)
    scheduler.simulate_execution()
    
    # Step 3: Calculate metrics
    metrics = scheduler.calculate_metrics()
    
    # Step 4: Generate visualizations
    print("\n📊 Generating Visualizations...")
    visualizer = Visualizer(scheduler)
    visualizer.generate_all_visualizations()
    
    # Step 5: Summary
    print("\n" + "=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    print(f"\n✅ All {len(tasks)} tasks have been successfully scheduled and executed")
    print(f"✅ System makespan: {metrics['makespan']} time units")
    print(f"✅ Average VM utilization: {metrics['avg_utilization']:.2f}%")
    print(f"\n📁 Output files generated:")
    print("   • gantt_chart.png - Task execution timeline")
    print("   • vm_utilization.png - VM performance metrics")
    print("\n" + "=" * 70)
    print("\n🎓 Operating System Concepts Demonstrated:")
    print("   ✓ FCFS (First Come First Served) Scheduling Algorithm")
    print("   ✓ Multi-processor Task Assignment")
    print("   ✓ Resource Utilization Analysis")
    print("   ✓ Performance Metric Calculation (Makespan, Waiting Time)")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
