"""
Visualizer - Creates Gantt charts and utilization graphs
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np


class Visualizer:
    """
    Creates visualizations for the scheduling results.
    """
    
    def __init__(self, scheduler):
        """
        Initialize the visualizer.
        
        Args:
            scheduler (FCFSScheduler): The scheduler with executed tasks
        """
        self.scheduler = scheduler
        
    def generate_gantt_chart(self, filename='gantt_chart.png'):
        """
        Generate a Gantt chart showing task execution timeline across VMs.
        
        Args:
            filename (str): Output filename for the chart
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Color palette for different tasks
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.scheduler.tasks)))
        task_colors = {task.task_id: colors[i] for i, task in enumerate(self.scheduler.tasks)}
        
        # Plot each task as a horizontal bar on its assigned VM
        vm_positions = {vm.vm_id: i for i, vm in enumerate(self.scheduler.vms)}
        
        for task in self.scheduler.tasks:
            vm_pos = vm_positions[task.vm_id]
            ax.barh(vm_pos, task.burst_time, left=task.start_time, 
                   height=0.6, color=task_colors[task.task_id],
                   edgecolor='black', linewidth=1.5)
            
            # Add task label in the middle of the bar
            ax.text(task.start_time + task.burst_time / 2, vm_pos,
                   task.task_id, ha='center', va='center',
                   fontsize=10, fontweight='bold')
        
        # Configure axes
        ax.set_yticks(range(len(self.scheduler.vms)))
        ax.set_yticklabels([vm.vm_id for vm in self.scheduler.vms])
        ax.set_xlabel('Time Units', fontsize=12, fontweight='bold')
        ax.set_ylabel('Virtual Machines', fontsize=12, fontweight='bold')
        ax.set_title('FCFS Scheduling - Gantt Chart\nCloud Video Rendering System', 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Add grid for better readability
        ax.grid(True, axis='x', alpha=0.3, linestyle='--')
        ax.set_xlim(0, self.scheduler.makespan + 1)
        
        # Add makespan indicator
        ax.axvline(x=self.scheduler.makespan, color='red', linestyle='--', 
                  linewidth=2, label=f'Makespan: {self.scheduler.makespan}')
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n✓ Gantt chart saved as '{filename}'")
        plt.close()
        
    def generate_utilization_chart(self, filename='vm_utilization.png'):
        """
        Generate a bar chart showing VM utilization percentages.
        
        Args:
            filename (str): Output filename for the chart
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        vm_ids = [vm.vm_id for vm in self.scheduler.vms]
        utilizations = [vm.get_utilization(self.scheduler.makespan) 
                       for vm in self.scheduler.vms]
        
        # Create bars with gradient colors based on utilization
        colors = ['#2ecc71' if u >= 70 else '#f39c12' if u >= 40 else '#e74c3c' 
                 for u in utilizations]
        
        bars = ax.bar(vm_ids, utilizations, color=colors, edgecolor='black', 
                     linewidth=2, alpha=0.8)
        
        # Add percentage labels on top of bars
        for i, (bar, util) in enumerate(zip(bars, utilizations)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{util:.2f}%', ha='center', va='bottom',
                   fontsize=12, fontweight='bold')
            
            # Add busy time info below
            busy_time = self.scheduler.vms[i].total_busy_time
            ax.text(bar.get_x() + bar.get_width()/2., -5,
                   f'{busy_time}/{self.scheduler.makespan} units',
                   ha='center', va='top', fontsize=10)
        
        # Configure axes
        ax.set_ylabel('Utilization (%)', fontsize=12, fontweight='bold')
        ax.set_xlabel('Virtual Machines', fontsize=12, fontweight='bold')
        ax.set_title('Virtual Machine Utilization\nFCFS Scheduling Performance', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, 110)
        ax.grid(True, axis='y', alpha=0.3, linestyle='--')
        
        # Add average line
        avg_util = sum(utilizations) / len(utilizations)
        ax.axhline(y=avg_util, color='blue', linestyle='--', linewidth=2,
                  label=f'Average: {avg_util:.2f}%')
        ax.legend(loc='upper right')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"✓ VM utilization chart saved as '{filename}'")
        plt.close()
        
    def print_execution_table(self):
        """
        Print a formatted table showing task execution details.
        """
        data = self.scheduler.get_scheduling_data()
        df = pd.DataFrame(data)
        
        print("\n" + "=" * 70)
        print("TASK EXECUTION DETAILS")
        print("=" * 70)
        print(df.to_string(index=False))
        print("=" * 70)
        
    def generate_all_visualizations(self):
        """
        Generate all visualizations and display execution table.
        """
        self.print_execution_table()
        self.generate_gantt_chart()
        self.generate_utilization_chart()
