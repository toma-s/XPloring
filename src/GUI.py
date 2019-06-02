import tkinter

class GUI:
    def __init__(self,game,width=850, height=600):
        self.game = game
        self.window_width = width
        self.window_height = height
        self.window = tkinter.Tk()
        self.window.config(bg='lightgrey')
        self.window.geometry(str(width) + 'x' + str(height))
        self.window.title("X-Ploring game")
        self.window.bind('<Return>',self.enterPressed)

        self.text_output = tkinter.Text(self.window)
        self.text_output.insert(tkinter.END,"This is yes!")
        self.text_output.configure(state='disabled')
        self.text_output.grid(column=0, row=0)

        self.text_input = tkinter.Text(self.window,height=1, width=80)
        self.text_input.insert(tkinter.END, "Input here!")
        self.text_input.grid(column=0, row=1)

    def getInput(self):
        input_text = self.text_input.get("1.0", "end-1c")
        self.text_input.delete('1.0', tkinter.END)
        return input_text

    def setOutput(self, text):
        self.text_output.configure(state='normal')
        self.text_output.delete('1.0', tkinter.END)
        self.text_output.insert(tkinter.INSERT, text)
        self.text_output.configure(state='disabled')

    def enterPressed(self,e):
        self.game.react_to_input(self.getInput())