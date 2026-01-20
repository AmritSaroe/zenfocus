import customtkinter as ctk
import winsound  # Native Windows sound library

# Configuration
WORK_MIN = 25
FONT_FAMILY = "Roboto"

class ZenFocusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Zen Mode Setup ---
        self.title("ZenFocus")
        self.geometry("400x300")
        
        # Removes the Windows Title Bar (Frameless)
        self.overrideredirect(True) 
        
        # Center the window on launch
        self.eval('tk::PlaceWindow . center')
        
        ctk.set_appearance_mode("Dark")
        self.configure(fg_color="#1a1a1a") # Deep dark gray

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # 1. Timer Display
        self.label_timer = ctk.CTkLabel(
            self, 
            text=f"{WORK_MIN}:00", 
            font=(FONT_FAMILY, 90, "bold"),
            text_color="#ffffff"
        )
        self.label_timer.grid(row=0, column=0, pady=(50, 0))

        # 2. Minimalist Progress Bar
        self.progress = ctk.CTkProgressBar(self, width=300, height=4, progress_color="#3498db")
        self.progress.set(1.0)
        self.progress.grid(row=1, column=0, pady=10)

        # 3. Helper Text (Subtle)
        self.label_help = ctk.CTkLabel(
            self, 
            text="[SPACE] Start   [R] Reset   [F] Fullscreen   [ESC] Quit", 
            font=(FONT_FAMILY, 12),
            text_color="#555555"
        )
        self.label_help.grid(row=2, column=0, pady=(0, 30))

        # --- Logic Variables ---
        self.time_left = WORK_MIN * 60
        self.running = False
        self.fullscreen = False
        
        # --- Keyboard Bindings (The Magic) ---
        self.bind("<space>", self.toggle_timer)
        self.bind("r", self.reset_timer)
        self.bind("f", self.toggle_fullscreen)
        self.bind("<Escape>", self.quit_app)
        
        # Allow dragging the frameless window
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

    # --- Window Dragging Logic ---
    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

    # --- Timer Logic ---
    def toggle_timer(self, event=None):
        if self.running:
            self.running = False
        else:
            self.running = True
            self.count_down()

    def count_down(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            self.label_timer.configure(text=f"{mins:02d}:{secs:02d}", text_color="white")
            self.progress.set(self.time_left / (WORK_MIN * 60))
            self.after(1000, self.count_down)
        elif self.time_left == 0:
            self.running = False
            self.label_timer.configure(text="ZEN", text_color="#2ecc71")
            winsound.Beep(1000, 500) # Frequency 1000Hz, Duration 500ms
            self.attributes('-topmost', True) # Bring to front

    def reset_timer(self, event=None):
        self.running = False
        self.time_left = WORK_MIN * 60
        self.label_timer.configure(text=f"{WORK_MIN}:00", text_color="white")
        self.progress.set(1.0)

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        # Hide help text in fullscreen for pure focus
        if self.fullscreen:
            self.label_help.grid_remove()
            self.configure(fg_color="black")
        else:
            self.label_help.grid()
            self.configure(fg_color="#1a1a1a")

    def quit_app(self, event=None):
        self.destroy()

if __name__ == "__main__":
    app = ZenFocusApp()
    app.mainloop()
