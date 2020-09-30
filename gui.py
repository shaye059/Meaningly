import tkinter as tk
from tkinter import Tk, BOTH, X, LEFT, RIGHT, PhotoImage, filedialog, END, Message
from tkinter.ttk import Frame, Label, Button
import meaningly as mn


# Function for opening the
# file explorer window


class Example(Frame):

    def __init__(self):
        super().__init__()
        self.fileName = None
        self.listOfEntries = []
        self.listOfPhrases = []

        self.initUI()

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
        self.fileName = None

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

        # If File and List of Phrases have a value, try processing the file
        if not ((len(self.fileName) == 0) or (len(self.listOfPhrases) == 1)):
            self.listOfPhrases = self.listOfPhrases.splitlines()
            try:
                mn.process_file(self.fileName, self.listOfPhrases, start_symbol=':')
                print('Done')
            except mn.FileError:
                self.listOfEntries[0].config(highlightbackground='red')
            except FileNotFoundError:
                self.listOfEntries[0].config(highlightbackground='red')

    def initUI(self):
        self.master.title("meaning.ly")
        self.pack(fill=BOTH, expand=True)

        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="File", width=7)
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

        lbl2 = Label(frame2, text="Symbol", width=7)
        lbl2.pack(side=LEFT, padx=5, pady=5)

        entry2 = tk.Entry(frame2)
        entry2.pack(fill=X, padx=5, expand=True)
        self.listOfEntries.append(entry2)

        frame3 = Frame(self)
        frame3.pack(fill=X, expand=True)

        lbl3 = Message(frame3, text="List of phrases", width=40)
        lbl3.pack(side=LEFT, padx=1, pady=7)

        entry3 = tk.Text(frame3, height=10, highlightthickness=1)
        entry3.pack(fill=BOTH, padx=5, pady=7)
        self.listOfEntries.append(entry3)

        frame4 = Frame(self)
        frame4.pack(fill=X)

        button_run = tk.Button(frame4, text='Run', width=6, bg='green', command=lambda: self.run_encoding(button_run))
        button_run.pack(side=RIGHT, padx=5, pady=5)

        button_clear = Button(frame4, text='Clear', width=6, command=self.clear)
        button_clear.pack(side=RIGHT, padx=5, pady=5)


def main():
    root = Tk()
    root.iconbitmap("letterm.ico")
    root.geometry("500x300+100+100")
    app = Example()
    root.mainloop()
    #mn.initialize_model()


if __name__ == '__main__':
    main()
