from text_auto_complete import TextAutoComplete
from tkinter import *

# TODO : key release debounce
# TODO : Handle delete key


class AutoCompleterUI:
    def __init__(self, words, tk_root, text):
        self.words = words
        self.auto_complete = TextAutoComplete(words)
        self.prefix = []
        self.text_pane = text
        self.listbox = Listbox(tk_root)
        self.list_visible = False

        self.listbox.bind('<KeyRelease>', self.__on_key_released)
        self.text_pane.bind('<KeyRelease>', self.__on_key_released)

    def __show(self):
        location = self.__get_last_character_coordinate()
        self.listbox.place(x=location[0], y=location[1], width=165, height=100)
        self.listbox.select_set(0)
        self.listbox.focus_set()
        self.list_visible = True

    def __hide_and_append_text(self, string=None):
        if string is not None:
            self.text_pane.insert('insert', string)

        self.listbox.place(x=0, y=0, width=0, height=0)
        self.text_pane.focus_set()
        self.list_visible = False

    def __on_listbox(self, event):
        if event.keysym == 'Return' and self.list_visible:
            value = self.listbox.get(self.listbox.curselection()[0])
            self.__hide_and_append_text(value[len(self.prefix):])
        elif str.isalnum(event.char):
            # Allow typing to continue, ignoring the auto complete suggestions
            self.__hide_and_append_text(event.char)

    def __on_key_released(self, event):
        if event.keysym == 'Down' and self.list_visible:
            return

        if event.keysym == 'Escape':
            self.__hide_and_append_text()
            return

        if self.list_visible:
            if event.char == ' ':
                self.__hide_and_append_text(event.char)
            else:
                self.__on_listbox(event)

        if not str.isalnum(event.char):
            self.prefix = []
            return

        self.prefix.append(event.char)

        words = self.auto_complete.autocomplete(''.join(self.prefix))
        if words is None and self.list_visible:
            # hide
            self.__hide_and_append_text()
        index = 0
        self.listbox.delete(0, END)
        if words is not None:
            for w in words:
                if w == ' ':
                    continue

                word = ''.join(self.prefix) + w
                self.listbox.insert(index, word)
                index += 1

            self.__show()


    def __get_last_character_coordinate(self):
        x_pos, y_pos, _, height = text_pane.bbox('insert')
        return x_pos, y_pos + height + 20


def read_autocomplete_words(filename):
    words = []

    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())

    return words


if __name__ == '__main__':
    # creating root window
    root = Tk()
    root.title("Auto Completed Demo")
    root.geometry('800x600')

    frame = Frame(root)
    frame.pack(pady=5)

    text_scroll = Scrollbar(frame)
    text_scroll.pack(side=RIGHT, fill=Y)
    text_pane = Text(frame, width=97, height=25, font=("Helvetica", 16), undo=True, yscrollcommand=text_scroll.set, highlightthickness=0)
    text_pane.pack()

    text_scroll.config(command=text_pane.yview)

    auto_complete = AutoCompleterUI(read_autocomplete_words('keywords.txt'), root, text_pane)
    root.mainloop()

