"""
VirtualMachine Class - Represents a VM resource in the cloud system
"""

class VirtualMachine:
    """
    Represents a Virtual Machine that executes tasks.
    
    Attributes:
        vm_id (str): Unique identifier for the VM
        available_time (int): Time when VM becomes available for next task
        task_history (list): List of tasks executed on this VM
        total_busy_time (int): Total time VM was executing tasks
    """
    
    def __init__(self, vm_id):
        """
        Initialize a new Virtual Machine.
        
        Args:
            vm_id (str): Unique identifier for the VM
        """
        self.vm_id = vm_id
        self.available_time = 0
        self.task_history = []
        self.total_busy_time = 0
        
    def assign_task(self, task):
        """
        Assign a task to this VM and update scheduling information.
        
        Args:
            task (Task): The task to assign
            
        Returns:
            tuple: (start_time, completion_time)
        """
        # Task starts when both VM is available AND task has arrived
        start_time = max(self.available_time, task.arrival_time)
        completion_time = start_time + task.burst_time
        
        # Update task information
        task.start_time = start_time
        task.completion_time = completion_time
        task.vm_id = self.vm_id
        
        # Update VM state
        self.available_time = completion_time
        self.total_busy_time += task.burst_time
        self.task_history.append(task)
        
        return start_time, completion_time
    
    def get_utilization(self, makespan):
        """
        Calculate utilization percentage of this VM.
        
        Args:
            makespan (int): Total time to complete all tasks
            
        Returns:
            float: Utilization percentage
        """
        if makespan == 0:
            return 0.0
        return (self.total_busy_time / makespan) * 100
    
    def __repr__(self):
        """String representation of the VM."""
        return f"VM({self.vm_id}, Available={self.available_time}, Tasks={len(self.task_history)})"
