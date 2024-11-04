import tkinter as tk

class Virus:
    def __init__(self):
        self.window = None

    def question(self, question_text):
        """Savolni o'rnatadi"""
        self.question_text = question_text

    def disable_event(self):
        """X tugmasini bosganda oynani yopmaslik"""
        pass

    def block_task_switching(self):
        """Boshqa ilovalarga o'tishni cheklash"""
        self.window.attributes("-fullscreen", True)
        self.window.attributes("-topmost", True)
        self.window.overrideredirect(True)

    def run(self):
        """Oynani ochish"""
        self.window = tk.Tk()
        self.window.title("Warning!")
        self.window.geometry("600x400")
        self.window.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.window.resizable(False, False)

        self.label = tk.Label(self.window, text=self.question_text, font=("Arial", 20))
        self.label.pack(pady=50)

        self.yes_button = tk.Button(self.window, text='Yes', font=("Arial", 16), command=self.close_window)
        self.yes_button.pack(side="left", padx=50)

        self.no_button = tk.Button(self.window, text='No', font=("Arial", 16), command=self.reopen_window)
        self.no_button.pack(side="right", padx=50)

        self.block_task_switching()

        self.window.mainloop()

    def close_window(self):
        """Yes tugmasi bosilganda dasturni to'xtatish"""
        self.window.overrideredirect(False)
        self.window.attributes("-fullscreen", False)
        self.window.quit()

    def reopen_window(self):
        """No tugmasi bosilganda oyna qayta ochiladi"""
        self.window.destroy()
        self.run()


if __name__ == '__main__':
    virus = Virus()
    virus.question('Are you gay?')
    virus.run()