import tkinter


class GUI:
    def __init__(self, game, width=850, height=600):
        self.game = game
        self.window_width = width
        self.window_height = height
        self.window = tkinter.Tk()
        self.window.config(bg='lightgrey')
        self.window.geometry(str(width) + 'x' + str(height))
        self.window.title("XPloring game")
        self.window.bind('<Return>', self._enter_pressed)

        self.main_frame = tkinter.Frame(self.window)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.text_output = tkinter.Text(self.main_frame)
        self.text_output.insert(tkinter.END, "This is yes!")
        self.text_output.configure(state='disabled')
        self.text_output.grid(column=0, row=0)

        self.text_input = tkinter.Text(self.main_frame, height=1, width=80)
        self.text_input.insert(tkinter.END, "Input here!")
        self.text_input.grid(column=0, row=1)

    def _enter_pressed(self):
        self.game.react_to_input(self._get_input())

    def _get_input(self):
        input_text = self.text_input.get("1.0", "end-1c")
        self.text_input.delete('1.0', tkinter.END)
        return input_text

    def set_output(self, text):
        self.text_output.configure(state='normal')
        self.text_output.insert(tkinter.INSERT, text)
        self.text_output.configure(state='disabled')
        self.text_output.see("end")
