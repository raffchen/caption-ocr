# loop
# -------------------------------
# tk update
# PIL grab image
# tesseract OCR
# google translate
# display results on main window
import asyncio
import tkinter as tk
from dataclasses import dataclass

import easyocr
import httpx
import numpy as np
from googletrans import Translator
from PIL import Image, ImageChops, ImageGrab, ImageTk

class Application:
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("600x700+500+500")
        self.root.title("Main")
        self.root.attributes("-topmost", True)

        self.image_display = tk.Label(
            self.root, highlightbackground="black", highlightthickness=2
        )
        self.orig_text_display = tk.Text(
            self.root, highlightbackground="black", highlightthickness=2, height=2
        )
        self.trans_text_display = tk.Text(
            self.root, highlightbackground="black", highlightthickness=2, height=2
        )
        self.notes = tk.Text(
            self.root, highlightbackground="black", highlightthickness=2, height=2
        )

        self.image_display.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )
        self.orig_text_display.grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )
        self.trans_text_display.grid(
            column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )
        self.notes.grid(
            column=0, row=3, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )

        self.text_changed = False

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)

        self.scanner = tk.Toplevel(self.root)
        self.scanner.title("Scanner")
        self.scanner.geometry("800x200")
        self.scanner.attributes("-transparent", "maroon3")
        self.scanner.attributes("-topmost", True)
        self.scanner.attributes("-alpha", 0.2)

        frame = tk.Frame(self.scanner, background="red")
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        canvas = tk.Canvas(frame, background="red")
        canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.reader = easyocr.Reader(["ch_tra", "en"])

        self.current_image = Image.fromarray(np.zeros((800, 200, 3)), mode="RGB")

    def mainloop(self):
        while True:
            self.root.update()
            self.grab_image()
            self.translate()

    def grab_image(self):
        x, y, w, h = (
            self.scanner.winfo_x(),
            self.scanner.winfo_y(),
            self.scanner.winfo_width(),
            self.scanner.winfo_height(),
        )
        image = ImageGrab.grab(
            bbox=(x + 10, y + 30, x + w, y + h + 30), all_screens=True
        )

        diff = ImageChops.difference(self.current_image, image)

        if diff.getbbox():
            self.current_image = image
            self.text_changed = True

            ratio = self.image_display.winfo_width() / image.width

            tkimage = ImageTk.PhotoImage(
                image.resize((int(image.width * ratio), int(image.height * ratio)))
            )
            self.image_display.configure(image=tkimage)
            self.image_display.image = tkimage

            result = self.reader.readtext(np.array(image), detail=0)
            self.orig_text_display.delete("1.0", tk.END)
            self.orig_text_display.insert(tk.END, "\n".join(result))

    def translate(self):
        async def get_translation():
            async with Translator() as translator:
                try:
                    translation = await translator.translate(self.orig_text_display.get("1.0", tk.END), dest='en')
                    self.trans_text_display.delete("1.0", tk.END)
                    self.trans_text_display.insert(tk.END, translation.text)
                except httpx.ConnectTimeout:
                    pass
            
        if self.text_changed:
            asyncio.run(get_translation())
            self.text_changed = False


if __name__ == "__main__":
    app = Application()
    app.mainloop()
