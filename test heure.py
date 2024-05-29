import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

def get_selected_datetime():
    selected_date = cal.get_date()
    selected_hour = hour_var.get()
    selected_minute = minute_var.get()
    selected_time = f"{selected_hour}:{selected_minute}"
    datetime_str = f"{selected_date} {selected_time}"
    datetime_obj = datetime.strptime(datetime_str, "%m/%d/%y %H:%M")
    print("Selected Date and Time:", datetime_obj)

root = tk.Tk()
root.title("Date and Time Picker")

# Create Calendar widget
cal = Calendar(root, selectmode='day', date_pattern='mm/dd/yy')
cal.pack(pady=20)

# Create time selection
time_frame = ttk.Frame(root)
time_frame.pack(pady=10)

ttk.Label(time_frame, text="Hour:").pack(side=tk.LEFT)
hour_var = tk.StringVar(value='00')
hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, textvariable=hour_var, width=3, format="%02.0f")
hour_spinbox.pack(side=tk.LEFT, padx=5)

ttk.Label(time_frame, text="Minute:").pack(side=tk.LEFT)
minute_var = tk.StringVar(value='00')
minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=3, format="%02.0f")
minute_spinbox.pack(side=tk.LEFT, padx=5)

# Button to get the selected date and time
select_button = ttk.Button(root, text="Get Selected Date and Time", command=get_selected_datetime)
select_button.pack(pady=20)

root.mainloop()
