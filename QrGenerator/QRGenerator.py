import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode
from tkinter import filedialog
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        # Window setup
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme("dark-blue")
        super().__init__(fg_color='white')
        self.title_bar_color()
        self.title('')
        self.iconbitmap('empty.ico')
        self.geometry('700x700')

        # Entry
        self.entry_string = ctk.StringVar(value='put here a link or text')
        self.entry_string.trace('w', self.create_qr)
        EntryField(self, self.entry_string)
        self.bind('<Return>', self.save)

        # QR code image setup
        self.ri = None
        self.imagetk = None
        self.qr_image = QrImage(self)

        self.mainloop()

    def create_qr(self, *args):
        current_text = self.entry_string.get()
        if current_text:
            self.ri = qrcode.make(current_text)
            self.imagetk = ImageTk.PhotoImage(self.ri)
            self.qr_image.update_image(self.imagetk)
        else:
            self.qr_image.clear()
            self.ri = None
            self.imagetk = None

    def save(self, event=None):
        if self.ri:
            file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
            if file_path:
                self.ri.save(file_path)  # Save the QR code as a PNG file

    def title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                HWND,
                35,
                byref(c_int(0x00FFFFFF)),
                sizeof(c_int)
            )
        except:
            pass

class EntryField(ctk.CTkFrame):
    def __init__(self, parent, entry_string):
        super().__init__(master=parent, corner_radius=20, fg_color='dark blue')
        self.place(relx=0.5, rely=1, relwidth=0.9, relheight=0.3, anchor='center')

        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        # Widgets
        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.columnconfigure(0, weight=1, uniform='b')
        self.frame.columnconfigure(1, weight=4, uniform='b')
        self.frame.columnconfigure(2, weight=2, uniform='b')
        self.frame.columnconfigure(3, weight=1, uniform='b')
        self.frame.grid(row=0, column=0)

        # Entry widget
        self.entry = ctk.CTkEntry(self.frame, fg_color='#6587a6', border_color='#6587a6', textvariable=entry_string)
        self.entry.grid(row=0, column=1, padx=(10, 5), pady=10, sticky="ew")

        # Bind events to handle placeholder behavior
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)

        # Button widget
        button = ctk.CTkButton(self.frame, text='Save', fg_color='#6587a6', command=self.on_save_click)
        button.grid(row=0, column=2, padx=(5, 10), pady=10)

    def on_focus_in(self, event):
        if self.entry.get() == 'put here a link or text':
            self.entry.delete(0, tk.END)

    def on_focus_out(self, event):
        if not self.entry.get():
            self.entry.insert(0, 'put here a link or text')

    def on_save_click(self):
        # Simulate pressing Enter key to trigger the save function
        self.master.save()

class QrImage(tk.Canvas):
    def __init__(self, parent):
        super().__init__(master=parent, background='white', highlightthickness=0)
        self.place(relx=0.5, rely=0.35, width=500, height=500, anchor='center')

    def update_image(self, image_tk):
        # Clear the existing image first
        self.clear()
        # Center the image within the canvas
        self.image_id = self.create_image(self.winfo_width() // 2, self.winfo_height() // 2, image=image_tk, anchor='center')

    def clear(self):
        self.delete('all')

# Start the application
App()
