"""
Task Class - Represents a video rendering job in the cloud system
"""

class Task:
    """
    Represents a single video rendering task with arrival time and burst time.
    
    Attributes:
        task_id (str): Unique identifier for the task
        arrival_time (int): Time when task arrives in the system
        burst_time (int): CPU time required to complete the task
        start_time (int): Time when task starts execution (set during scheduling)
        completion_time (int): Time when task completes (set during scheduling)
        vm_id (str): ID of VM assigned to this task (set during scheduling)
    """
    
    def __init__(self, task_id, arrival_time, burst_time):
        """
        Initialize a new task.
        
        Args:
            task_id (str): Unique identifier for the task
            arrival_time (int): Time when task arrives
            burst_time (int): CPU time required
        """
        self.task_id = task_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.start_time = None
        self.completion_time = None
        self.vm_id = None
        
    def __repr__(self):
        """String representation of the task."""
        return f"Task({self.task_id}, Arrival={self.arrival_time}, Burst={self.burst_time})"
    
    def get_waiting_time(self):
        """
        Calculate waiting time for this task.
        
        Returns:
            int: Waiting time (start_time - arrival_time)
        """
        if self.start_time is not None:
            return self.start_time - self.arrival_time
        return 0
    
    def get_turnaround_time(self):
        """
        Calculate turnaround time for this task.
        
        Returns:
            int: Turnaround time (completion_time - arrival_time)
        """
        if self.completion_time is not None:
            return self.completion_time - self.arrival_time
        return 0
