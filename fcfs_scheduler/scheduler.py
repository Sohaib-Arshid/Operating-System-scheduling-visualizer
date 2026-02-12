"""
FCFS Scheduler - Implements First Come First Served scheduling algorithm
"""

class FCFSScheduler:
    """
    Implements FCFS (First Come First Served) scheduling algorithm.
    
    This scheduler assigns tasks to VMs based on arrival order and VM availability.
    """
    
    def __init__(self, tasks, vms):
        """
        Initialize the scheduler.
        
        Args:
            tasks (list): List of Task objects
            vms (list): List of VirtualMachine objects
        """
        self.tasks = tasks
        self.vms = vms
        self.makespan = 0
        
    def sort_tasks_by_arrival(self):
        """
        Sort tasks by arrival time (FCFS principle).
        Tasks with the same arrival time maintain their original order.
        """
        self.tasks.sort(key=lambda task: (task.arrival_time, task.task_id))
        
    def find_earliest_available_vm(self):
        """
        Find the VM that will be available first.
        
        Returns:
            VirtualMachine: The VM with the earliest available time
        """
        return min(self.vms, key=lambda vm: vm.available_time)
    
    def simulate_execution(self):
        """
        Simulate the execution of all tasks using FCFS algorithm.
        
        Process:
        1. Sort tasks by arrival time
        2. For each task, assign to earliest available VM
        3. Update VM and task scheduling information
        """
        # Step 1: Sort tasks by arrival time (FCFS)
        self.sort_tasks_by_arrival()
        
        print("=" * 70)
        print("FCFS SCHEDULING SIMULATION - Cloud Video Rendering System")
        print("=" * 70)
        print(f"\nTotal Tasks: {len(self.tasks)}")
        print(f"Total VMs: {len(self.vms)}")
        print("\nTask Execution Order (FCFS):")
        print("-" * 70)
        
        # Step 2: Assign each task to the earliest available VM
        for task in self.tasks:
            vm = self.find_earliest_available_vm()
            start_time, completion_time = vm.assign_task(task)
            
            print(f"Task {task.task_id}: "
                  f"Arrival={task.arrival_time}, "
                  f"Burst={task.burst_time}, "
                  f"Start={start_time}, "
                  f"End={completion_time}, "
                  f"VM={vm.vm_id}")
        
        # Step 3: Calculate makespan (time when last task completes)
        self.makespan = max(vm.available_time for vm in self.vms)
        
        print("-" * 70)
        
    def calculate_metrics(self):
        """
        Calculate and display performance metrics.
        
        Metrics:
        - Makespan: Total time to complete all tasks
        - VM Utilization: Percentage of time each VM was busy
        - Average Waiting Time: Average time tasks waited before execution
        - Average Turnaround Time: Average total time from arrival to completion
        """
        print("\n" + "=" * 70)
        print("PERFORMANCE METRICS")
        print("=" * 70)
        
        # Makespan
        print(f"\n1. Makespan (Total Completion Time): {self.makespan} time units")
        
        # VM Utilization
        print(f"\n2. Virtual Machine Utilization:")
        for vm in self.vms:
            utilization = vm.get_utilization(self.makespan)
            print(f"   {vm.vm_id}: {utilization:.2f}% "
                  f"(Busy: {vm.total_busy_time}/{self.makespan} time units)")
        
        # Average utilization
        avg_utilization = sum(vm.get_utilization(self.makespan) for vm in self.vms) / len(self.vms)
        print(f"   Average VM Utilization: {avg_utilization:.2f}%")
        
        # Waiting and Turnaround times
        total_waiting_time = sum(task.get_waiting_time() for task in self.tasks)
        total_turnaround_time = sum(task.get_turnaround_time() for task in self.tasks)
        
        avg_waiting_time = total_waiting_time / len(self.tasks)
        avg_turnaround_time = total_turnaround_time / len(self.tasks)
        
        print(f"\n3. Average Waiting Time: {avg_waiting_time:.2f} time units")
        print(f"4. Average Turnaround Time: {avg_turnaround_time:.2f} time units")
        
        print("\n" + "=" * 70)
        
        return {
            'makespan': self.makespan,
            'avg_utilization': avg_utilization,
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        }
    
    def get_scheduling_data(self):
        """
        Get scheduling data for visualization.
        
        Returns:
            list: List of dictionaries containing task scheduling information
        """
        data = []
        for task in self.tasks:
            data.append({
                'Task ID': task.task_id,
                'Arrival Time': task.arrival_time,
                'Burst Time': task.burst_time,
                'Start Time': task.start_time,
                'Completion Time': task.completion_time,
                'VM': task.vm_id,
                'Waiting Time': task.get_waiting_time(),
                'Turnaround Time': task.get_turnaround_time()
            })
        return data
