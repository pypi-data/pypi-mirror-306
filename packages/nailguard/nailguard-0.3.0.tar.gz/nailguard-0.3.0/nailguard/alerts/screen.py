import tkinter as tk
from screeninfo import get_monitors

from .base import Alert

class ScreenAlert(Alert):
    
    def on_start(self):
        roots = []
        for monitor in get_monitors():
            root = tk.Tk()
            root.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
            root.attributes('-fullscreen', True)
            root.configure(background='red')
            
            label = tk.Label(
                root,
                text="STOP BITING YOUR NAILS!",
                font=("Arial", 48),
                fg="white",
                bg="red"
            )
            label.place(relx=0.5, rely=0.5, anchor='center')
            
            root.after(2000, root.destroy)
            roots.append(root)
        
        for root in roots:
            root.update()
        tk.mainloop()
