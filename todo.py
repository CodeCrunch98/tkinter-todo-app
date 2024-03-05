import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def add_task():
    # Function to add a task
    task = task_entry.get()
    if task and task != "Enter your task here...":  # Check if the task is not empty and not the placeholder
        task_listbox.insert(tk.END, f"{len(task_listbox.get(0, tk.END)) + 1}. {task}")  # Insert the task into the listbox
        task_entry.delete(0, tk.END)  # Clear the task entry
        update_counters()  # Update the task counters
    else:
        messagebox.showwarning("Warning", "Please enter a task.")  # Show a warning message if the task is empty or placeholder

def delete_task():
    # Function to delete a task
    try:
        selected_task_index = task_listbox.curselection()[0]  # Get the index of the selected task
        task_listbox.delete(selected_task_index)  # Delete the selected task from the listbox
        update_counters()  # Update the task counters
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to delete.")  # Show a warning message if no task is selected

def toggle_complete():
    # Function to toggle the completion status of a task
    try:
        selected_task_index = task_listbox.curselection()[0]  # Get the index of the selected task
        bg_color = task_listbox.itemcget(selected_task_index, 'bg')  # Get the background color of the selected task
        task_text = task_listbox.get(selected_task_index)  # Get the text of the selected task
        if bg_color == 'light green':
            # If the task is already completed, remove the checkmark symbol
            if '✓' in task_text:
                task_listbox.itemconfig(selected_task_index, {'bg': 'white'})  # Set background color to white
                task_listbox.delete(selected_task_index)  # Delete the selected task from the listbox
                task_listbox.insert(selected_task_index, task_text.replace(' ✓', ''))  # Insert the task text without the checkmark symbol
            else:
                task_listbox.itemconfig(selected_task_index, {'bg': 'white'})  # Set background color to white
        else:
            # If the task is not completed, add the checkmark symbol
            if '✓' not in task_text:
                task_text += ' ✓'  # Add checkmark symbol to the task text
                task_listbox.delete(selected_task_index)  # Delete the selected task from the listbox
                task_listbox.insert(selected_task_index, task_text)  # Insert the task text with the checkmark symbol
            task_listbox.itemconfig(selected_task_index, {'bg': 'light green'})  # Set background color to light green
        update_counters()  # Update the task counters
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task.")  # Show a warning message if no task is selected

def edit_task(event):
    # Function to edit a task
    try:
        selected_task_index = task_listbox.curselection()[0]  # Get the index of the selected task
        task_text = task_listbox.get(selected_task_index)  # Get the text of the selected task
        
        # Remove the checkmark symbol ('✓') from the task text if present
        task_text = task_text.replace(' ✓', '')

        task_entry.delete(0, tk.END)  # Clear the task entry
        task_entry.insert(tk.END, task_text.split('. ', 1)[1])  # Insert the task text into the task entry
        delete_task()  # Delete the selected task
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to edit.")  # Show a warning message if no task is selected

def show_info():
    # Function to show information about the application
    info_message = "This is a To-Do List Application.\n\nYou can use it to add, delete, toggle complete, and edit tasks.\n\nTo add a task, type in the text box and click 'Add Task'.\n\nTo delete a task, select it from the list and click 'Delete Task'.\n\nTo mark a task as completed or incomplete, select it from the list and click 'Toggle Complete'.\n\nTo edit a task, double-click on it in the list and make changes in the text box."
    messagebox.showinfo("About", info_message)  # Show an information message with application details

def update_counters():
    # Function to update the task counters
    total_tasks = len(task_listbox.get(0, tk.END))  # Get the total number of tasks
    completed_tasks = sum(1 for i in range(total_tasks) if 'light green' in task_listbox.itemcget(i, 'bg'))  # Get the number of completed tasks
    pending_tasks = total_tasks - completed_tasks  # Calculate the number of pending tasks
    counter_label.config(text=f"Total Tasks: {total_tasks} | Completed: {completed_tasks} | Pending: {pending_tasks}")  # Update the counter label text

def create_rounded_widget(widget):
    # Function to create rounded widget
    widget.config(
        borderwidth=2,
        highlightthickness=2,
        relief="flat",
        bg="white"
    )
    widget.bind("<FocusIn>", lambda event: widget.config(bg="lightgray"))
    widget.bind("<FocusOut>", lambda event: widget.config(bg="white"))

def on_entry_click(event):
    # Function to handle click event on task entry
    if task_entry.get() == "Enter your task here...":  # Check if the placeholder text is present
        task_entry.delete(0, tk.END)  # Clear the task entry
        task_entry.config(fg='black')  # Change text color to black

def on_focus_out(event):
    # Function to handle focus out event on task entry
    if task_entry.get() == "":  # Check if the task entry is empty
        task_entry.insert(0, "Enter your task here...")  # Insert the placeholder text
        task_entry.config(fg='grey')  # Change text color to grey

def on_enter(event):
    # Function to handle mouse enter event on info button
    tooltip_label.place(x=center_x + 289, y=center_y - 240)  # Show the tooltip label

def on_leave(event):
    # Function to handle mouse leave event on info button
    tooltip_label.place_forget()  # Hide the tooltip label

# Create the main window
root = tk.Tk()
root.title("To-Do List App")
root.config(bg="gray20")  # Set background color

window_width = 650
window_height = 540
root.geometry(f"{window_width}x{window_height}")  # Set window size
root.resizable(False, False)  # Disable window resizing
center_x = window_width // 2
center_y = window_height // 2

# Create and position widgets
header_label = tk.Label(root, text="MY TO-DO", font=("Helvetica", 18, "bold"), bg="gray20", fg="white")
header_label.place(x=center_x, y=center_y - 240, anchor="center")

# Create and position widgets
task_entry = tk.Entry(root, width=45, font=("Cascadia Mono", 10))
create_rounded_widget(task_entry)
task_entry.insert(0, "Enter your task here...")  # Set placeholder text
task_entry.bind('<FocusIn>', on_entry_click)  # Bind click event to task entry
task_entry.bind('<FocusOut>', on_focus_out)  # Bind focus out event to task entry
task_entry.pack(pady=10)
task_entry.place(x=center_x, y=center_y - 165, anchor="center")

add_button = tk.Button(root, text="Add Task", command=add_task)
create_rounded_widget(add_button)
add_button.place(x=center_x + 205, y=center_y - 178)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
create_rounded_widget(delete_button)
delete_button.place(x=center_x + 244, y=center_y - 97)

toggle_button = tk.Button(root, text="Toggle Complete", command=toggle_complete)
create_rounded_widget(toggle_button)
toggle_button.place(x=center_x + 138, y=center_y - 97)

task_listbox = tk.Listbox(root, height=14, width=70, font=("Cascadia Mono", 12), bg='gray49', selectbackground="gray73", selectforeground="black", activestyle="none")
task_listbox.place(x=center_x - 317, y=center_y - 75)
task_listbox.bind("<Double-Button-1>", edit_task)

info_img = Image.open("info.png")  # Load info icon image
info_img = info_img.resize((20, 20))  # Resize icon image
info_icon = ImageTk.PhotoImage(info_img)
info_button = tk.Button(root, image=info_icon, command=show_info, bg="gray20", bd=0, highlightthickness=0)
info_button.image = info_icon
info_button.place(x=center_x + 300, y=center_y - 265)

# Create tooltip label for info button
tooltip_label = tk.Label(root, text="Help", bg="gray20", fg='white')
tooltip_label.config(font=("Helvetica", 8))

info_button.bind("<Enter>", on_enter)
info_button.bind("<Leave>", on_leave)

counter_label = tk.Label(root, text="", bg="gray20", fg='white')
counter_label.place(x=center_x - 100, y=center_y + 240)

# Run the main event loop
root.mainloop()
