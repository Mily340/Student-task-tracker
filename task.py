"""
Task class definition
Represents a single task in the task tracker
"""

from datetime import datetime

class Task:
    """Class representing a single task"""
    
    def __init__(self, task_id, title, description, created_at=None):
        """
        Initialize a new task
        
        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task
            description (str): Description of the task
            created_at (str, optional): Creation timestamp. Defaults to current time.
        """
        self.id = task_id
        self.title = title
        self.description = description
        
        if created_at:
            self.created_at = created_at
        else:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """
        Convert task object to dictionary for JSON serialization
        
        Returns:
            dict: Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Task object from dictionary data
        
        Args:
            data (dict): Dictionary containing task data
        
        Returns:
            Task: Task object created from dictionary
        """
        return cls(
            task_id=data['id'],
            title=data['title'],
            description=data['description'],
            created_at=data['created_at']
        )
    
    def __str__(self):
        """String representation of the task"""
        return f"ID: {self.id} | Title: {self.title} | Created: {self.created_at}"
    
    def display_details(self):
        """Display task details in a formatted way"""
        print("\n" + "-" * 40)
        print(f"Task ID: {self.id}")
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Created At: {self.created_at}")
        print("-" * 40)