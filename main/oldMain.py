from threading import Thread
from time import sleep
from tkinter import Button, Label, Tk


class App(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.label = Label(self, text="Stopped.")
        self.label.pack()
        self.play_button = Button(self, text="Play", command=self.play)
        self.play_button.pack(side="left", padx=2, pady=2)
        self.stop_button = Button(self, text="Stop", command=self.stop)
        self.stop_button.pack(side="left", padx=2, pady=2)
        self._thread, self._pause, self._stop = None, False, True

    def action(self):
        for i in range(1000):
            if self._stop:
                break
            while self._pause:
                self.label["text"] = "Pause... (count: {})".format(i)
                sleep(0.1)
            self.label["text"] = "Playing... (count: {})".format(i)
            sleep(0.1)
        self.label["text"] = "Stopped."

    def play(self):
        if self._thread is None:
            self._stop = False
            self._thread = Thread(target=self.action)
            self._thread.start()
        self._pause = False
        self.play_button.configure(text="Pause", command=self.pause)

    def pause(self):
        self._pause = True
        self.play_button.configure(text="Play", command=self.play)

    def stop(self):
        if self._thread is not None:
            self._thread, self._pause, self._stop = None, False, True
        self.play_button.configure(text="Play", command=self.play)


if __name__ == "__main__":
    app = App()
    app.title("Rammus Scanning")
    app.mainloop()
