"""
Student Task Tracker Application
Main entry point for the application
"""

from task_manager import TaskManager
import sys

def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 40)
    print("      STUDENT TASK TRACKER")
    print("=" * 40)
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Search Tasks")
    print("6. Exit")
    print("=" * 40)

def main():
    """Main function to run the application"""
    # Create task manager instance
    task_manager = TaskManager()
    
    # Load existing tasks from file
    task_manager.load_from_file()
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                # Add new task
                print("\n--- Add New Task ---")
                title = input("Task Title: ").strip()
                description = input("Description: ").strip()
                
                if title:
                    task_manager.add_task(title, description)
                    print("✓ Task added successfully!")
                else:
                    print("✗ Task title cannot be empty!")
                    
            elif choice == '2':
                # View all tasks
                print("\n--- All Tasks ---")
                task_manager.view_tasks()
                
            elif choice == '3':
                # Update task
                print("\n--- Update Task ---")
                task_manager.view_tasks()
                
                if task_manager.tasks:
                    try:
                        task_id = int(input("\nEnter Task ID to update: "))
                        title = input("New Title (press Enter to keep current): ").strip()
                        description = input("New Description (press Enter to keep current): ").strip()
                        
                        if task_manager.update_task(task_id, title, description):
                            print("✓ Task updated successfully!")
                        else:
                            print("✗ Task not found!")
                    except ValueError:
                        print("✗ Please enter a valid Task ID!")
                        
            elif choice == '4':
                # Delete task
                print("\n--- Delete Task ---")
                task_manager.view_tasks()
                
                if task_manager.tasks:
                    try:
                        task_id = int(input("\nEnter Task ID to delete: "))
                        
                        if task_manager.delete_task(task_id):
                            print("✓ Task deleted successfully!")
                        else:
                            print("✗ Task not found!")
                    except ValueError:
                        print("✗ Please enter a valid Task ID!")
                        
            elif choice == '5':
                # Search tasks
                print("\n--- Search Tasks ---")
                keyword = input("Enter search keyword: ").strip()
                if keyword:
                    task_manager.search_tasks(keyword)
                else:
                    print("✗ Please enter a search keyword!")
                    
            elif choice == '6':
                # Exit and save
                print("\nSaving tasks to file...")
                task_manager.save_to_file()
                print("✓ Tasks saved successfully!")
                print("\nThank you for using Student Task Tracker!")
                sys.exit(0)
                
            else:
                print("✗ Invalid choice! Please enter a number between 1-6.")
                
        except KeyboardInterrupt:
            print("\n\nSaving tasks before exit...")
            task_manager.save_to_file()
            print("✓ Tasks saved successfully!")
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()