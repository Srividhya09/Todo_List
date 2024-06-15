import tkinter as tk
from tkinter import messagebox
import datetime

# Define a task class to store task details
class Task:
    def __init__(self, description, priority, due_date, completed=False):
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

# Function to load tasks from a text file
def load_tasks():
    tasks = []
    try:
        with open("tasks.txt", "r") as file:
            for line in file:
                description, priority, due_date, completed = line.strip().split(",")
                tasks.append(Task(description, priority, due_date, completed.lower() == "true"))
    except FileNotFoundError:
        with open("tasks.txt", "w") as file:
            pass
    return tasks

# Function to save tasks to a text file
def save_tasks(tasks):
    with open("tasks.txt", "w") as file:
        for task in tasks:
            completed_str = "True" if task.completed else "False"
            file.write(f"{task.description},{task.priority},{task.due_date},{completed_str}\n")

# GUI Application
class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List")
        self.tasks = load_tasks()
        
        self.task_listbox = tk.Listbox(master, width=50, height=15)
        self.task_listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        
        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=1, column=0, padx=10, pady=5)

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=1, column=1, padx=10, pady=5)

        self.complete_button = tk.Button(master, text="Mark Complete", command=self.mark_complete)
        self.complete_button.grid(row=1, column=2, padx=10, pady=5)

        self.update_button = tk.Button(master, text="Update Task", command=self.update_task)
        self.update_button.grid(row=1, column=3, padx=10, pady=5)

        self.pending_button = tk.Button(master, text="Filter Pending", command=lambda: self.filter_tasks(False))
        self.pending_button.grid(row=2, column=0, padx=10, pady=5)

        self.completed_button = tk.Button(master, text="Filter Completed", command=lambda: self.filter_tasks(True))
        self.completed_button.grid(row=2, column=1, padx=10, pady=5)

        self.show_all_button = tk.Button(master, text="Show All Tasks", command=self.show_all_tasks)
        self.show_all_button.grid(row=2, column=2, padx=10, pady=5)

        self.load_task_list()

    def load_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task.completed else "Pending"
            task_str = f"{status} - {task.priority.capitalize()} - {task.description} ({task.due_date})"
            self.task_listbox.insert(tk.END, task_str)

    def add_task(self):
        new_task_window = tk.Toplevel(self.master)
        new_task_window.title("Add New Task")

        tk.Label(new_task_window, text="Description:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(new_task_window, text="Priority (low, medium, high):").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(new_task_window, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)

        description_entry = tk.Entry(new_task_window, width=30)
        description_entry.grid(row=0, column=1, padx=10, pady=5)
        priority_entry = tk.Entry(new_task_window, width=30)
        priority_entry.grid(row=1, column=1, padx=10, pady=5)
        due_date_entry = tk.Entry(new_task_window, width=30)
        due_date_entry.grid(row=2, column=1, padx=10, pady=5)

        def save_new_task():
            description = description_entry.get()
            priority = priority_entry.get()
            due_date = due_date_entry.get()
            if not description or not priority or not due_date:
                messagebox.showwarning("Input Error", "All fields are required")
                return
            try:
                datetime.datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Date Error", "Invalid date format")
                return
            self.tasks.append(Task(description, priority, due_date))
            save_tasks(self.tasks)
            self.load_task_list()
            new_task_window.destroy()

        save_button = tk.Button(new_task_window, text="Save", command=save_new_task)
        save_button.grid(row=3, column=1, padx=10, pady=5)

    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Selection Error", "No task selected")
            return
        task_index = selected_task_index[0]
        del self.tasks[task_index]
        save_tasks(self.tasks)
        self.load_task_list()

    def mark_complete(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Selection Error", "No task selected")
            return
        task_index = selected_task_index[0]
        self.tasks[task_index].completed = True
        save_tasks(self.tasks)
        self.load_task_list()

    def filter_tasks(self, completed):
        filtered_tasks = [task for task in self.tasks if task.completed == completed]
        self.task_listbox.delete(0, tk.END)
        for task in filtered_tasks:
            status = "Completed" if task.completed else "Pending"
            task_str = f"{status} - {task.priority.capitalize()} - {task.description} ({task.due_date})"
            self.task_listbox.insert(tk.END, task_str)

    def show_all_tasks(self):
        self.load_task_list()

    def update_task(self):
        selected_task_index = self.task_listbox.curselection()
        if not selected_task_index:
            messagebox.showwarning("Selection Error", "No task selected")
            return
        task_index = selected_task_index[0]
        task = self.tasks[task_index]

        update_task_window = tk.Toplevel(self.master)
        update_task_window.title("Update Task")

        tk.Label(update_task_window, text="Description:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(update_task_window, text="Priority (low, medium, high):").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(update_task_window, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)

        description_entry = tk.Entry(update_task_window, width=30)
        description_entry.grid(row=0, column=1, padx=10, pady=5)
        description_entry.insert(0, task.description)

        priority_entry = tk.Entry(update_task_window, width=30)
        priority_entry.grid(row=1, column=1, padx=10, pady=5)
        priority_entry.insert(0, task.priority)

        due_date_entry = tk.Entry(update_task_window, width=30)
        due_date_entry.grid(row=2, column=1, padx=10, pady=5)
        due_date_entry.insert(0, task.due_date)

        def save_updated_task():
            description = description_entry.get()
            priority = priority_entry.get()
            due_date = due_date_entry.get()
            if not description or not priority or not due_date:
                messagebox.showwarning("Input Error", "All fields are required")
                return
            try:
                datetime.datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Date Error", "Invalid date format")
                return
            task.description = description
            task.priority = priority
            task.due_date = due_date
            save_tasks(self.tasks)
            self.load_task_list()
            update_task_window.destroy()

        save_button = tk.Button(update_task_window, text="Save", command=save_updated_task)
        save_button.grid(row=3, column=1, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
