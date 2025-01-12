import tkinter as tk
from tkinter import ttk

class DarkBlueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Blue Theme")
        
        # Configure dark blue theme colors
        self.dark_blue = "#1a237e"  # Dark blue background
        self.light_blue = "#534bae"  # Light blue for hover states
        self.text_color = "white"
        
        # Configure window
        self.root.geometry("400x300")
        self.root.configure(bg=self.dark_blue)
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('default')
        
        # Configure button style
        style.configure(
            'Dark.TButton',
            background=self.dark_blue,
            foreground=self.text_color,
            padding=10
        )
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create widgets
        self.label = tk.Label(
            self.main_frame,
            text="Dark Blue Theme Test",
            font=("Arial", 16),
            bg=self.dark_blue,
            fg=self.text_color
        )
        self.label.grid(row=0, column=0, pady=20)
        
        self.entry = tk.Entry(
            self.main_frame,
            bg=self.light_blue,
            fg=self.text_color,
            insertbackground=self.text_color
        )
        self.entry.grid(row=1, column=0, pady=10)
        
        self.button = ttk.Button(
            self.main_frame,
            text="Click Me",
            style='Dark.TButton',
            command=self.button_click
        )
        self.button.grid(row=2, column=0, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
    
    def button_click(self):
        text = self.entry.get()
        if text:
            self.label.config(text=f"You entered: {text}")
        else:
            self.label.config(text="Please enter some text")

if __name__ == "__main__":
    root = tk.Tk()
    app = DarkBlueApp(root)
    root.mainloop()