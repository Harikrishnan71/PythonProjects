import tkinter as tk
import helper_functions as hf
def on_button_click():
    input1_value = entry1.get()
    input2_value = entry2.get()
    
    # Do something with the input values (you can customize this part)
    result_label.config(text=f"Input 1: {input1_value}, Input 2: {input2_value}")

# Create the main window
window = tk.Tk()
window.geometry(f"{500}x{600}")
window.title("Software Notifier")

# Create input fields
entry1_label = tk.Label(window, text="Email of the developer/sender : ")
entry1_label.pack()
entry1 = tk.Entry(window)
entry1.pack()

entry2_label = tk.Label(window, text="Name of the developer/sender : ")
entry2_label.pack()
entry2 = tk.Entry(window)
entry2.pack()

entry3 = tk.Text(window, width=180, height=40)
entry3.insert("end", "Enter the Work Item Details here :  ")
entry3.place(x = 500, y = 500, height = 50, width = 200)
#entry3 = tk.Entry(window)
#entry3.pack()
# Create action button
action_button = tk.Button(window, text="Click me", command=hf.CreateDraftEmail(entry1.get(),entry1.get(),entry1.get(),entry1.get()))
action_button.pack()

# Display the result
result_label = tk.Label(window, text="")
result_label.pack()

# Start the Tkinter event loop
window.mainloop()
