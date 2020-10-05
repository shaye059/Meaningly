import tkinter as tk
from tkinter import Tk, BOTH, X, LEFT, RIGHT, PhotoImage, filedialog, END, Message, RAISED
from tkinter.ttk import Frame, Label, Button
import meaningly as mn


# Splash screen


#Main app
class UserInterface(Frame):

    def __init__(self):
        super().__init__()
        self.fileName = None
        self.listOfEntries = []
        self.listOfPhrases = []
        self.threshold = None

        self.initUI()
        self.meaningly = mn.Meaningly()

    # Setting the filename
    def set_file(self, filename):
        self.fileName = filename

    # Function for clearing
    # the inputs
    def clear(self):
        for entry in self.listOfEntries:
            if isinstance(entry, tk.Entry):
                entry.delete(0, END)
            else:
                entry.delete('1.0', END)
            entry.config(highlightbackground='SystemButtonFace')
        #self.fileName = None

    # Function for opening the
    # file explorer window
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
        self.listOfPhrases = self.listOfEntries[2].get('1.0', END)
        self.threshold = self.listOfEntries[3].get()

        # If there's no entry for file, show error. Otherwise clear any previous errors.
        if len(self.fileName) == 0:
            self.listOfEntries[0].config(highlightbackground='red')
        else:
            self.listOfEntries[0].config(highlightbackground='SystemButtonFace')

        # If there's no entry for list of phrases, show error. Otherwise clear any previous errors.
        if len(self.listOfPhrases) == 1:
            self.listOfEntries[2].config(highlightbackground='red')
        else:
            self.listOfEntries[2].config(highlightbackground='SystemButtonFace')

        # TODO: Add an option to choose between positive correlation, negative correlation, or both.
        # If there's an entry for threshold, check to see if it's a number and if that number is between 0 and 1. If
        # there is no entry then set threshold to default value (0)
        if not(len(self.threshold) == 0):
            try:
                self.threshold = float(self.threshold)
                if not(0 <= self.threshold <= 1):
                    self.listOfEntries[3].config(highlightbackground='red')
                else:
                    self.listOfEntries[3].config(highlightbackground='SystemButtonFace')
            except ValueError:
                self.listOfEntries[3].config(highlightbackground='red')
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

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="File", width=9)
        lbl1.pack(side=LEFT, padx=5, pady=5)

        photo = PhotoImage(file=r"foldericon.png")
        photo2 = photo.subsample(25, 25)

        entry1 = tk.Entry(frame1, highlightthickness=1)

        button = Button(frame1, image=photo2, width=6, command=lambda: self.browseFiles(entry1))
        button.pack(side=RIGHT, padx=5, pady=5)
        button.image = photo2
        # button.grid(row=1, column=1)
        entry1.pack(fill=X, padx=5, pady=5, expand=True)
        self.listOfEntries.append(entry1)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Symbol", width=9)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        entry2 = tk.Entry(frame2)
        entry2.pack(fill=X, padx=5, expand=True)
        self.listOfEntries.append(entry2)

        frame3 = Frame(self)
        frame3.pack(fill=X, expand=True)

        lbl3 = Message(frame3, text="List of phrases", width=42)
        lbl3.pack(side=LEFT, padx=7, pady=7)

        entry3 = tk.Text(frame3, height=10, highlightthickness=1)
        entry3.pack(fill=BOTH, padx=5, pady=7)
        self.listOfEntries.append(entry3)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        lbl4 = Label(frame4, text="Threshold", width=9)
        lbl4.pack(side=LEFT, padx=5, pady=5)

        entry4 = tk.Entry(frame4, highlightthickness=1)
        entry4.pack(fill=X, padx=5, expand=True)
        self.listOfEntries.append(entry4)

        frame5 = Frame(self)
        frame5.pack(fill=X)

        button_run = tk.Button(frame5, text='Run', width=6, bg='green', command=lambda: self.run_encoding(button_run))
        button_run.pack(side=RIGHT, padx=5, pady=5)

        button_clear = Button(frame5, text='Clear', width=6, command=self.clear)
        button_clear.pack(side=RIGHT, padx=5, pady=5)


def main():
    root = Tk()
    root.iconbitmap("letterm.ico")
    root.geometry("500x350+100+100")
    app = UserInterface()
    root.mainloop()


if __name__ == '__main__':
    main()
