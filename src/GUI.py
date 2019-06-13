import tkinter
from src.GameState import GameState
from os.path import join

parent_path = '..\\game_states'


class GUI:
    def __init__(self, game, width=850, height=600):
        self.game = game
        self.window_width = width
        self.window_height = height
        self.window = tkinter.Tk()
        self.window.config(bg='lightgrey')
        self.window.geometry(str(width) + 'x' + str(height))
        self.window.title("XPloring game")
        self.window.bind('<Return>', self.enterPressed)

        self.main_frame = tkinter.Frame(self.window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.text_output = tkinter.Text(self.main_frame)
        self.text_output.configure(state='disabled')
        self.text_output.grid(column=0, row=0)

        self.text_input = tkinter.Text(self.main_frame, height=1, width=80, fg='grey')
        self.text_input.insert(tkinter.END, "Input here!")
        self.text_input.grid(column=0, row=1)
        self.text_input.bind("<FocusIn>", self.handle_focus_in)

    def handle_focus_in(self,e):
        self.text_input.delete('1.0', tkinter.END)
        self.text_input.config(fg='black')

    def getInput(self):
        input_text = self.text_input.get("1.0", "end-1c")
        self.text_input.delete('1.0', tkinter.END)
        return input_text

    def setOutput(self, text):
        self.text_output.configure(state='normal')
        self.text_output.insert(tkinter.INSERT, text)
        self.text_output.configure(state='disabled')
        self.text_output.see("end")


    def enterPressed(self, e):
        self.game.react_to_input(self.getInput())

class GamePickerGUI:
    def __init__(self,choices_arr,width=850, height=600):
        self.retun_val = None
        self.window_width = width
        self.window_height = height
        self.window = tkinter.Tk()
        self.window.config(bg='lightgrey')
        self.window.geometry(str(width) + 'x' + str(height))
        self.window.title("X-Ploring game")
        self.window.bind('<Return>', self.enterPressed)

        self.main_frame = tkinter.Frame(self.window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label = tkinter.Label(self.main_frame, text = "Select map and press enter to commit.")
        self.label.grid(column=0, row=0)

        # Create a Tkinter variable
        self.tkvar = tkinter.StringVar(self.main_frame)

        # Dictionary with options
        self.choices = set(choices_arr)
        self.tkvar.set(choices_arr[0])  # set the default option

        popupMenu = tkinter.OptionMenu(self.main_frame, self.tkvar, *self.choices)
        popupMenu.grid(column=1, row=0)

    def enterPressed(self, e):
        try:
            GameState(join(parent_path,self.tkvar.get()))
            self.retun_val = self.tkvar.get()
            self.window.destroy()
        except Exception as e:
            self.label.config(text=''+str(e))

