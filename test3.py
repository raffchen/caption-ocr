# loop
# -------------------------------
# tk update
# PIL grab image
# tesseract OCR
# google translate
# display results on main window
import tkinter as tk

import numpy as np
import pytesseract
from PIL import Image, ImageChops, ImageGrab, ImageTk


class Application:
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("600x600")
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

        self.image_display.grid(
            column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )
        self.orig_text_display.grid(
            column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )
        self.trans_text_display.grid(
            column=0, row=2, sticky=(tk.N, tk.S, tk.E, tk.W), pady=5, padx=5
        )

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        self.scanner = tk.Toplevel(self.root)
        self.scanner.title("Scanner")
        self.scanner.geometry("800x200")
        self.scanner.attributes("-transparent", "maroon3")
        self.scanner.attributes("-topmost", True)

        frame = tk.Frame(self.scanner, background="maroon3")
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        canvas = tk.Canvas(frame, background="maroon3")
        canvas.pack(fill=tk.BOTH, expand=tk.YES)

        self.current_image = Image.fromarray(np.zeros((800, 200, 3)), mode="RGB")

    def mainloop(self):
        while True:
            self.root.update()
            self.grab_image()

    def grab_image(self):
        x, y, w, h = (
            self.scanner.winfo_x(),
            self.scanner.winfo_y(),
            self.scanner.winfo_width(),
            self.scanner.winfo_height(),
        )
        image = ImageGrab.grab(bbox=(x+10, y+30, x+w, y+h+30))

        diff = ImageChops.difference(self.current_image, image)

        if diff.getbbox():
            self.current_image = image

            ratio = self.image_display.winfo_width() / image.width

            tkimage = ImageTk.PhotoImage(image.resize((int(image.width * ratio), int(image.height * ratio))))
            self.image_display.configure(image=tkimage)
            self.image_display.image = tkimage

            text = pytesseract.image_to_string(image, lang="chi_tra")
            self.orig_text_display.delete("1.0", tk.END)
            self.orig_text_display.insert(tk.END, text)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
