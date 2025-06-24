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
        self.title("CS2 AIGL")
        self.geometry("900x600")
        self.configure(bg="black")
        self.current_typing_job = None

        self.steamid = None

        self.create_splash_screen()


    def create_splash_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.ascii_label = tk.Label(self, text=ASCII_ART,
                                    fg="#66CCFF",
                                    bg="black",
                                    font=("Courier New", 18, "bold"))
        self.ascii_label.pack(pady=(30, 10))

        self.prompt_label = tk.Label(self, text="Enter your SteamID:", fg="white", bg="black",
                                     # font=("Courier New", 14))
                                     font=("JetBrains Mono", 14))
        self.prompt_label.pack(pady=(10, 5))

        self.steamid_var = tk.StringVar()
        self.steamid_entry = tk.Entry(self, textvariable=self.steamid_var,
                                      # font=("Courier New", 14),
                                      font=("JetBrains Mono", 14),
                                      bg="black", fg="white", insertbackground="white", width=30)
        self.steamid_entry.pack(pady=(0, 15))
        self.steamid_entry.focus_set()

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("SleekGray.TButton",
                        foreground="#222222",
                        background="#BBBBBB",
                        font=("Segoe UI", 14, "bold"),
                        padding=6,
                        borderwidth=1,
                        relief="flat")

        style.map("SleekGray.TButton",
                  background=[('pressed', '#666666'), ('active', '#888888')],
                  foreground=[('pressed', '#000000'), ('active', '#111111')])

        self.submit_btn = ttk.Button(self, text="▶ Start",
                                     style="SleekGray.TButton",
                                     command=self.on_submit)
        self.submit_btn.pack()

        self.bind('<Return>', lambda event: self.on_submit())


    def on_submit(self):
        steamid = self.steamid_var.get().strip()
        if steamid:
            self.steamid = steamid
            self.create_dashboard_screen()
        else:
            self.steamid_entry.configure(bg="#330000")
            self.after(200, lambda: self.steamid_entry.configure(bg="black"))


    def create_dashboard_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.log_lines = []  # store log lines here

        self.dashboard_label = tk.Label(
            self,
            text=f"Welcome! SteamID: {self.steamid}\n\nWaiting for updates...",
            bg="black",
            fg="white",
            # font=("Courier New", 16),
            font=("JetBrains Mono", 14),
            justify=tk.LEFT,
            anchor="nw",
            padx=20,
            pady=20,
            wraplength=1040
        )
        self.dashboard_label.pack(expand=True, fill=tk.BOTH)

        self.after(100, self.poll_log_queue)


    def type_out_text(self, full_text, color, delay=10):
        # Cancel any ongoing typing
        if self.current_typing_job is not None:
            self.after_cancel(self.current_typing_job)
            self.current_typing_job = None

        self.current_text = ""
        self.dashboard_label.config(text="", fg=color)

        def type_char(index=0):
            if index < len(full_text):
                self.current_text += full_text[index]
                self.dashboard_label.config(text=self.current_text)
                self.current_typing_job = self.after(delay, lambda: type_char(index + 1))
            else:
                self.flash_label_bg()
                self.current_typing_job = None  # typing done

        type_char()


    def poll_log_queue(self):
        latest_line = None

        try:
            while True:
                line = log_queue.get_nowait()
                latest_line = line
        except queue.Empty:
            pass

        if latest_line:
            timestamp = datetime.datetime.now().strftime("[%H:%M:%S] ")
            color = self.get_color_for_line(latest_line)
            self.type_out_text(timestamp + latest_line, color)

        self.after(100, self.poll_log_queue)


    def flash_label_bg(self, flash_color="#111111", duration=120):
        self.dashboard_label.config(bg=flash_color)
        self.after(duration, lambda: self.dashboard_label.config(bg="black"))


    def get_color_for_line(self, line):
        upper = line.upper()
        if "[ACTION]" in upper:
            return "#FF5E5E"  # soft urgent red
        elif "[STRATEGY]" in upper:
            return "#00BFFF"  # bright blue
        elif "[INFO]" in upper:
            return "#A9F871"  # gentle neon green
        else:
            return "#AAAAAA"  # subtle gray


def start_terminal():
    app = LogTerminal()
    app.mainloop()
