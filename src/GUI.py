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
        self.window.bind('<Return>', self.enter_pressed)

        self.main_frame = tkinter.Frame(self.window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.text_output = tkinter.Text(self.main_frame)
        self.text_output.configure(state='disabled')
        self.text_output.grid(column=0, row=0)

        self.text_input = tkinter.Text(self.main_frame, height=1, width=80)
        self.text_input.insert(tkinter.END, "Input here!")
        self.text_input.grid(column=0, row=1)

    def set_output(self, text):
        self.text_output.configure(state='normal')
        self.text_output.insert(tkinter.INSERT, text)
        self.text_output.configure(state='disabled')
        self.text_output.see("end")

    def enter_pressed(self, e):
        self.game.react_to_input(self._get_input())

    def _get_input(self):
        input_text = self.text_input.get("1.0", "end-1c")
        self.text_input.delete('1.0', tkinter.END)
        return input_text


class GamePickerGUI:
    def __init__(self, choices_arr, width=850, height=600):
        self.return_val = None
        self.window_width = width
        self.window_height = height
        self.window = tkinter.Tk()
        self.window.config(bg='lightgrey')
        self.window.geometry(str(width) + 'x' + str(height))
        self.window.title("X-Ploring game")
        self.window.bind('<Return>', self.enter_pressed)

        self.main_frame = tkinter.Frame(self.window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.label = tkinter.Label(self.main_frame, text="Select map and press enter to commit.")
        self.label.grid(column=0, row=0)

        # Create a Tkinter variable
        self.tk_var = tkinter.StringVar(self.main_frame)

        # Dictionary with options
        self.choices = set(choices_arr)
        self.tk_var.set(choices_arr[0])  # set the default option

        popup_menu = tkinter.OptionMenu(self.main_frame, self.tk_var, *self.choices)
        popup_menu.grid(column=1, row=0)

    def enter_pressed(self, e):
        try:
            GameState(join(parent_path, self.tk_var.get()))
            self.return_val = self.tk_var.get()
            self.window.destroy()
        except Exception as e:
            self.label.config(text='' + str(e))
