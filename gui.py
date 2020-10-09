import tkinter as tk
from tkinter import Tk, BOTH, X, LEFT, RIGHT, PhotoImage, filedialog, END, Message
from tkinter.ttk import Frame, Label, Button
import meaningly as mn
from PIL import ImageTk, Image


# Splash screen
class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.iconbitmap("assets/letterm.ico")
        self.title("Loading")
        loadphoto = ImageTk.PhotoImage(Image.open('assets/3147390.jpg').resize((400, 400)))
        image_label = tk.Label(self, image=loadphoto)
        image_label.image = loadphoto
        image_label.pack()

        self.update()  # required to make window show before the program gets to the mainloop


def popup_bonus():
    win = tk.Toplevel()
    win.geometry("300x300+120+120")
    win.iconbitmap("assets/letterm.ico")
    win.wm_title("Help")
    win.resizable(False, False)
    frame_popup = Frame(win)
    frame_popup.pack(fill=BOTH)

    help_text = "File: The path to the transcript file. The file must be a Word doc." \
                "\n\nList of phrases: List of sentences to search the text for. Include " \
                "all punctuation and start each new sentence one a new line. \n\nThreshold: When given a threshold, " \
                "the program will only display sentences that are correlated to the input phrases above the given " \
                "value. Default is 0. Must be a decimal value between 0 and 1.\n\nSymbol: Not implemented yet."

    lbl_phrases = Message(frame_popup, text=help_text, width=280)
    lbl_phrases.pack(side=LEFT, padx=(5, 9), pady=7)

    frame_okay = Frame(win)
    frame_okay.pack(side='bottom', fill=BOTH)
    b = Button(frame_okay, text="Okay", command=win.destroy)
    b.pack(pady=(5, 35))


# Main app
class UserInterface(Frame):

    def __init__(self):
        super().__init__()
        self.master.withdraw()
        splash = Splash(self)
        self.fileName = None
        self.listOfEntries = []
        self.listOfPhrases = []
        self.threshold = None

        self.initUI()
        self.meaningly = mn.Meaningly()
        splash.destroy()
        self.master.deiconify()

    # Setting the filename
    def set_file(self, filename):
        self.fileName = filename

    # Function for clearing the inputs
    def clear(self):
        for entry in self.listOfEntries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, END)
            else:
                entry.delete('1.0', END)
            entry.config(highlightbackground='SystemButtonFace')
        # self.fileName = None

    # Function for opening the file explorer window
    def browseFiles(self, e):
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Word files", "*.docx"), ("all files", "*.*")))

        # Change label contents
        e.delete(0, END)
        e.insert(0, filename)

    def run_encoding(self, run_button):
        # Set focus on run button so that any error outlines are visible
        run_button.focus()

        # Assign the entries to their respective variables
        self.fileName = self.listOfEntries[0].get()
        self.listOfPhrases = self.listOfEntries[1].get('1.0', END)
        self.threshold = self.listOfEntries[2].get()

        # If there's no entry for file, show error. Otherwise clear any previous errors.
        if len(self.fileName) == 0:
            self.listOfEntries[0].config(highlightbackground='red')
        else:
            self.listOfEntries[0].config(highlightbackground='SystemButtonFace')

        # If there's no entry for list of phrases, show error. Otherwise clear any previous errors.
        if len(self.listOfPhrases) == 1:
            self.listOfEntries[1].config(highlightbackground='red')
        else:
            self.listOfEntries[1].config(highlightbackground='SystemButtonFace')

        # TODO: (Feature) Add an option to choose between positive correlation, negative correlation, or both.
        # If there's an entry for threshold, check to see if it's a number and if that number is between 0 and 1. If
        # there is no entry then set threshold to default value (0)
        if not (len(self.threshold) == 0):
            try:
                self.threshold = float(self.threshold)
                if not (0 <= self.threshold <= 1):
                    self.listOfEntries[2].config(highlightbackground='red')
                else:
                    self.listOfEntries[2].config(highlightbackground='SystemButtonFace')
            except ValueError:
                self.listOfEntries[2].config(highlightbackground='red')
                return
        else:
            self.threshold = 0

        # If File and List of Phrases have a value, try processing the file
        if not ((len(self.fileName) == 0) or (len(self.listOfPhrases) == 1)):
            self.listOfPhrases = self.listOfPhrases.splitlines()

            try:
                self.meaningly.process_run_plot(self.fileName, self.listOfPhrases, self.threshold, start_symbol=':')
            except mn.FileError:
                self.listOfEntries[0].config(highlightbackground='red')
            except FileNotFoundError:
                self.listOfEntries[0].config(highlightbackground='red')

    def initUI(self):
        self.master.title("meaning.ly")
        self.pack(fill=BOTH, expand=True)

        # File input
        frame_file = Frame(self)
        frame_file.pack(fill=X)

        lbl_file = Label(frame_file, text="File", width=9)
        lbl_file.pack(side=LEFT, padx=5, pady=5)

        photo = PhotoImage(file=r"assets/foldericon.png")
        photo2 = photo.subsample(25, 25)

        entry_file = tk.Entry(frame_file, highlightthickness=1)

        button_file = Button(frame_file, image=photo2, width=6, command=lambda: self.browseFiles(entry_file))
        button_file.pack(side=RIGHT, padx=5, pady=5)
        button_file.image = photo2
        entry_file.pack(fill=X, padx=5, pady=5, expand=True)
        self.listOfEntries.append(entry_file)

        # List of phrases input
        frame_phrases = Frame(self)
        frame_phrases.pack(fill=X, expand=True)

        lbl_phrases = Message(frame_phrases, text="List of phrases", width=42)
        lbl_phrases.pack(side=LEFT, padx=(5, 9), pady=7)

        entry_phrases = tk.Text(frame_phrases, height=10, highlightthickness=1)
        entry_phrases.pack(fill=BOTH, padx=5, pady=7)
        self.listOfEntries.append(entry_phrases)

        # Options label
        frame_opt = Frame(self)
        frame_opt.pack(fill=X)

        lbl_opt = Label(frame_opt, text="Optional:", width=9)
        lbl_opt.pack(side=LEFT, padx=5, pady=5)

        # Threshold input
        frame_thresh = Frame(self)
        frame_thresh.pack(fill=X)

        lbl_thresh = Label(frame_thresh, text="Threshold", width=9)
        lbl_thresh.pack(side=LEFT, padx=(5, 5), pady=5)

        entry_thresh = tk.Entry(frame_thresh, highlightthickness=1)
        entry_thresh.pack(fill=X, padx=5, expand=True)
        self.listOfEntries.append(entry_thresh)

        # Symbol input
        frame_symbol = Frame(self)
        frame_symbol.pack(fill=X)

        lbl_symbol = Label(frame_symbol, text="Symbol", width=9)
        lbl_symbol.pack(side=LEFT, padx=(5, 5), pady=5)

        entry_symbol = tk.Entry(frame_symbol)
        entry_symbol.pack(fill=X, padx=5, expand=True)
        self.listOfEntries.append(entry_symbol)

        # Run & clear buttons
        frame_buttons = Frame(self)
        frame_buttons.pack(fill=X)

        button_help = Button(frame_buttons, text='Help', width=6, command=popup_bonus)
        button_help.pack(side=LEFT, padx=5, pady=5)

        button_run = tk.Button(frame_buttons, text='Run', width=6, bg='green', command=lambda: self.run_encoding(button_run))
        button_run.pack(side=RIGHT, padx=5, pady=5)

        button_clear = Button(frame_buttons, text='Clear', width=6, command=self.clear)
        button_clear.pack(side=RIGHT, padx=5, pady=5)


def main():
    root = Tk()
    root.iconbitmap("assets/letterm.ico")
    root.geometry("500x350+100+100")
    root.withdraw()
    app = UserInterface()
    root.mainloop()


if __name__ == '__main__':
    main()
