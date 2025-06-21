import tkinter as tk
import queue
import datetime
from tkinter import ttk

log_queue = queue.Queue()

def push_log(line):
    log_queue.put(line)

ASCII_ART = """
 ░▒▓██████▓▒░ ░▒▓███████▓▒░       ░▒▓██████▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░        
░▒▓█▓▒░       ░▒▓██████▓▒░       ░▒▓████████▓▒░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░        
░▒▓█▓▒░             ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓███████▓▒░       ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░ 
"""

class LogTerminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CS2 AI Coach")
        self.geometry("1080x800")
        self.configure(bg="black")

        self.steamid = None

        self.create_splash_screen()

    def create_splash_screen(self):
        # Clear window in case
        for widget in self.winfo_children():
            widget.destroy()

        # ASCII art label (using a monospace font)
        self.ascii_label = tk.Label(self, text=ASCII_ART, fg="#00FF00", bg="black",
                                    font=("Courier New", 18, "bold"))
        self.ascii_label.pack(pady=(30, 10))

        # SteamID entry prompt
        self.prompt_label = tk.Label(self, text="Enter your SteamID:", fg="white", bg="black",
                                     font=("Courier New", 14))
        self.prompt_label.pack(pady=(10, 5))

        self.steamid_var = tk.StringVar()
        self.steamid_entry = tk.Entry(self, textvariable=self.steamid_var, font=("Courier New", 14),
                                      bg="black", fg="white", insertbackground="white", width=30)
        self.steamid_entry.pack(pady=(0, 15))
        self.steamid_entry.focus_set()

        # Submit button
        style = ttk.Style()
        style.theme_use('clam')  # Use a theme that lets us customize everything

        # Custom hacker-style button
        style.configure("Neon.TButton",
                        foreground="black",
                        background="#00FF00",
                        font=("Courier New", 14, "bold"),
                        padding=6,
                        borderwidth=0)
        style.map("Neon.TButton",
                  background=[('active', '#00CC00')],
                  foreground=[('active', 'black')])

        self.submit_btn = ttk.Button(self, text="▶ Start",
                                     style="Neon.TButton",
                                     command=self.on_submit)
        self.submit_btn.pack()
        self.submit_btn.pack()

        # Bind Enter key to submit
        self.bind('<Return>', lambda event: self.on_submit())

    def on_submit(self):
        steamid = self.steamid_var.get().strip()
        if steamid:
            self.steamid = steamid
            self.create_terminal_screen()
        else:
            # Optional: flash the entry or show an error message
            self.steamid_entry.configure(bg="#330000")
            self.after(200, lambda: self.steamid_entry.configure(bg="black"))

    def create_terminal_screen(self):
        # Clear splash widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Now create the log terminal UI
        self.text_widget = tk.Text(
            self,
            bg="black",
            fg="white",
            insertbackground="white",
            font=("Courier New", 12),
            state=tk.DISABLED,
            wrap=tk.WORD,
            padx=10,
            pady=10,
            spacing3=2
        )
        self.text_widget.pack(expand=True, fill=tk.BOTH)

        # Show a welcome message with SteamID
        self.append_line(f"Welcome! SteamID: {self.steamid}", tag="INFO")

        # Setup tags for coloring
        self.text_widget.tag_config("INFO", foreground="#00FF00")       # Bright Green
        self.text_widget.tag_config("ACTION", foreground="#FF6F61")     # Soft Red-Orange
        self.text_widget.tag_config("STRATEGY", foreground="#66CCFF")   # Light Blue

        self.after(100, self.poll_log_queue)

    def poll_log_queue(self):
        while True:
            try:
                line = log_queue.get_nowait()
            except queue.Empty:
                break
            else:
                self.append_line(line, self.get_tag_for_line(line))
        self.after(100, self.poll_log_queue)

    def append_line(self, line, tag="INFO"):
        self.text_widget.config(state=tk.NORMAL)
        timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
        self.text_widget.insert(tk.END, timestamp, "INFO")  # timestamp always green
        self.text_widget.insert(tk.END, line + "\n", tag)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def get_tag_for_line(self, line):
        upper_line = line.upper()
        if "[ACTION]" in upper_line:
            return "ACTION"
        elif "[STRATEGY]" in upper_line:
            return "STRATEGY"
        else:
            return "INFO"

def start_terminal():
    app = LogTerminal()
    app.mainloop()
