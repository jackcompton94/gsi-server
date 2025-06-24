import tkinter as tk
import queue
import datetime
import core.session as session
from tkinter import ttk
from core.globals import validator
from utils.logger_hooks import push_log, log_queue


ASCII_ART = """
 ██████╗███████╗     █████╗ ██╗ ██████╗ ██╗     
██╔════╝██╔════╝    ██╔══██╗██║██╔════╝ ██║     
██║     ███████╗    ███████║██║██║  ███╗██║     
██║     ╚════██║    ██╔══██║██║██║   ██║██║     
╚██████╗███████║    ██║  ██║██║╚██████╔╝███████╗
 ╚═════╝╚══════╝    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚══════╝ 
"""

class LogTerminal(tk.Tk):
    def __init__(self, skip_splash=False):
        super().__init__()
        self.title("CS2 AIGL")
        self.geometry("900x600")
        self.configure(bg="black")
        self.current_typing_job = None
        self.steamid = None

        if skip_splash:
            self.steamid = "TestUser"
            self.create_dashboard_screen()
        else:
            self.create_splash_screen()


    def create_splash_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Background color consistent with dashboard
        self.configure(bg="#121212")

        # ASCII art label (same colors, font tweak)
        self.ascii_label = tk.Label(self, text=ASCII_ART,
                                    # fg="#5C5C5C", # dark grey
                                    fg="#BBBBBB", # grey - almost white
                                    # fg="#999999", # light grey
                                    bg="#121212",
                                    font=("Courier New", 18, "bold"),
                                    justify=tk.CENTER)
        self.ascii_label.pack(pady=(40, 20))

        # Blue underline glow right below ASCII art (like header underline)
        self.ascii_underline = tk.Frame(self, bg="#00BFFF", height=3)
        self.ascii_underline.pack(fill=tk.X, padx=120, pady=(0, 25))

        # SteamID prompt label (matching dashboard colors)
        self.prompt_label = tk.Label(self, text="Enter your SteamID:", fg="#BBBBBB", bg="#121212",
                                     font=("JetBrains Mono", 14))
        self.prompt_label.pack(pady=(0, 8))

        # SteamID entry box
        self.steamid_var = tk.StringVar()
        self.steamid_entry = tk.Entry(self, textvariable=self.steamid_var,
                                      font=("JetBrains Mono", 14),
                                      bg="#121212", fg="white", insertbackground="white",
                                      width=30, relief="flat", highlightthickness=2, highlightbackground="#00BFFF", highlightcolor="#00BFFF")
        self.steamid_entry.pack(pady=(0, 20))
        self.steamid_entry.focus_set()

        # Submit button styled similarly to dashboard
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("SleekGreen.TButton",
                        foreground="#121212",
                        background="#4CAF50",  # Medium Green, modern & calm
                        font=("JetBrains Mono", 14, "bold"),
                        padding=8,
                        borderwidth=0,
                        relief="flat")

        style.map("SleekGreen.TButton",
                  background=[('pressed', '#388E3C'),  # Darker green for pressed
                              ('active', '#66BB6A')], # Lighter green for hover
                  foreground=[('pressed', '#EEEEEE'),
                              ('active', '#FFFFFF')])

        self.submit_btn = ttk.Button(self, text="▶ Start", style="SleekGreen.TButton", command=self.on_submit)
        self.submit_btn.pack(pady=(0, 40))



        self.bind('<Return>', lambda event: self.on_submit())


    def on_submit(self):
        steamid = self.steamid_var.get().strip()
        if steamid:
            self.steamid = steamid
            session.steamid = steamid

            validator.update_steamid(steamid)  # ✅ This is correct now

            self.create_dashboard_screen()
        else:
            self.steamid_entry.configure(bg="#330000")
            self.after(200, lambda: self.steamid_entry.configure(bg="black"))




    def create_dashboard_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

        # Header area
        self.header_label = tk.Label(
            self,
            text=f"CS2 AIGL Terminal  |  SteamID: {self.steamid}",
            bg="#121212",
            fg="#BBBBBB",
            font=("JetBrains Mono", 12, "bold"),
            anchor="w",
            padx=20,
            pady=10
        )
        self.header_label.pack(fill=tk.X)

        # Blue underline glow right below header
        self.header_underline = tk.Frame(self, bg="#00BFFF", height=3)
        self.header_underline.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Main live log label
        self.dashboard_label = tk.Label(
            self,
            text="Waiting for updates...",
            bg="#121212",
            fg="#AAAAAA",
            font=("JetBrains Mono", 18),
            justify=tk.LEFT,
            anchor="w",
            padx=20,
            pady=20,
            wraplength=880
        )
        self.dashboard_label.pack(expand=True, fill=tk.BOTH)

        # Blue underline glow at bottom of log label
        self.dashboard_underline = tk.Frame(self, bg="#00BFFF", height=3)
        self.dashboard_underline.pack(fill=tk.X, padx=20, pady=(10, 10))

        self.after(100, self.poll_log_queue)



    def flash_label_bg(self, flash_color="#222222", duration=250):
        # Smooth fade effect (example)
        self.dashboard_label.config(bg=flash_color)
        self.after(duration, lambda: self.dashboard_label.config(bg="#121212"))


    def type_out_text(self, full_text, color, delay=10):
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
                self.current_typing_job = None

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


def start_terminal(skip_splash=False):
    app = LogTerminal(skip_splash=skip_splash)
    app.mainloop()
