"""
TaskManager class definition
Handles all application operations and file management
"""

import json
import random
from datetime import datetime
from task import Task
from pathlib import Path

class TaskManager:
    """Class to manage tasks and handle file operations"""
    
    def __init__(self, filename="tasks.json"):
        """
        Initialize TaskManager
        
        Args:
            filename (str): Name of the JSON file to store tasks
        """
        self.filename = filename
        self.tasks = []
    
    def generate_task_id(self):
        """
        Generate a unique task ID using random module
        
        Returns:
            int: Unique task ID
        """
        existing_ids = {task.id for task in self.tasks}
        
        while True:
            # Generate ID between 1000 and 9999
            new_id = random.randint(1000, 9999)
            if new_id not in existing_ids:
                return new_id
    
    def add_task(self, title, description):
        """
        Add a new task
        
        Args:
            title (str): Task title
            description (str): Task description
        
        Returns:
            Task: The created task object
        """
        try:
            task_id = self.generate_task_id()
            new_task = Task(task_id, title, description)
            self.tasks.append(new_task)
            return new_task
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def view_tasks(self, tasks_list=None):
        """
        View all tasks or a specific list of tasks
        
        Args:
            tasks_list (list, optional): Specific list of tasks to display. 
                                       Defaults to all tasks.
        """
        tasks_to_display = tasks_list if tasks_list else self.tasks
        
        if not tasks_to_display:
            print("No tasks found!")
            return
        
        print(f"\nTotal Tasks: {len(tasks_to_display)}")
        print("-" * 60)
        
        for task in tasks_to_display:
            # Truncate description if too long
            desc_preview = task.description
            if len(desc_preview) > 40:
                desc_preview = desc_preview[:37] + "..."
            
            print(f"ID: {task.id:4d} | {task.title:20s} | {desc_preview:40s} | {task.created_at}")
        
        print("-" * 60)
    
    def get_task_by_id(self, task_id):
        """
        Get a task by its ID
        
        Args:
            task_id (int): Task ID to search for
        
        Returns:
            Task or None: Found task or None if not found
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id, new_title=None, new_description=None):
        """
        Update an existing task
        
        Args:
            task_id (int): ID of task to update
            new_title (str, optional): New title. Defaults to None.
            new_description (str, optional): New description. Defaults to None.
        
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            task = self.get_task_by_id(task_id)
            
            if not task:
                return False
            
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            
            return True
            
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def delete_task(self, task_id):
        """
        Delete a task by ID
        
        Args:
            task_id (int): ID of task to delete
        
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            initial_count = len(self.tasks)
            self.tasks = [task for task in self.tasks if task.id != task_id]
            return len(self.tasks) < initial_count
            
        except Exception as e:
            print(f"Error deleting task: {e}")
            return False
    
    def search_tasks(self, keyword):
        """
        Search tasks by keyword in title or description
        
        Args:
            keyword (str): Search keyword
        
        Returns:
            list: List of matching tasks
        """
        keyword_lower = keyword.lower()
        matching_tasks = []
        
        for task in self.tasks:
            if (keyword_lower in task.title.lower() or 
                keyword_lower in task.description.lower()):
                matching_tasks.append(task)
        
        if matching_tasks:
            print(f"\nFound {len(matching_tasks)} task(s) matching '{keyword}':")
            self.view_tasks(matching_tasks)
        else:
            print(f"\nNo tasks found matching '{keyword}'")
        
        return matching_tasks
    
    def save_to_file(self):
        """Save tasks to JSON file with error handling"""
        try:
            # Convert tasks to dictionaries
            tasks_data = [task.to_dict() for task in self.tasks]
            
            # Write to JSON file
            with open(self.filename, 'w') as file:
                json.dump(tasks_data, file, indent=2)
            
            return True
            
        except FileNotFoundError:
            print(f"Error: Directory not found for file '{self.filename}'")
            return False
        except PermissionError:
            print(f"Error: Permission denied when writing to '{self.filename}'")
            return False
        except json.JSONEncodeError as e:
            print(f"Error encoding JSON: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error saving file: {e}")
            return False
    
    def load_from_file(self):
        """Load tasks from JSON file with error handling"""
        try:
            # Check if file exists
            file_path = Path(self.filename)
            
            if not file_path.exists():
                print(f"Info: File '{self.filename}' not found. Starting with empty task list.")
                return True
            
            # Read from JSON file
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
            
            # Convert dictionaries to Task objects
            self.tasks = [Task.from_dict(data) for data in tasks_data]
            
            print(f"✓ Loaded {len(self.tasks)} task(s) from '{self.filename}'")
            return True
            
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in '{self.filename}': {e}")
            return False
        except KeyError as e:
            print(f"Error: Missing required field in JSON data: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error loading file: {e}")
            return False
    
    def get_statistics(self):
        """
        Get statistics about tasks
        
        Returns:
            dict: Dictionary containing task statistics
        """
        if not self.tasks:
            return {"total_tasks": 0, "recent_tasks": 0}
        
        # Count tasks created today
        today = datetime.now().strftime("%Y-%m-%d")
        recent_tasks = sum(1 for task in self.tasks 
                          if task.created_at.startswith(today))
        
        return {
            "total_tasks": len(self.tasks),
            "recent_tasks": recent_tasks
        }