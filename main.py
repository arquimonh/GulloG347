import tkinter as tk
from pynput import keyboard
import ttkbootstrap as ttk
from pathlib import Path
from tkinter import colorchooser
import configparser
import os


class Counter:
    def __init__(self, master):
        self.master = master
        self.value = tk.IntVar()
        self.value.set(0)
        self.frame_1 = tk.Frame(master)
        self.label = tk.Label(self.frame_1, text="Mortes: ", font='TkHeadingFont')
        self.label.pack(side=tk.LEFT)
        self.label_count = ttk.Label(self.frame_1, textvariable=self.value, font='TkHeadingFont', bootstyle=ttk.DANGER)
        self.label_count.pack(side=tk.LEFT)
        self.font = None
        self.ico = Path(__file__).parent / "assets" / Path('ico.ico')

        # Configura o listener do teclado
        self.listener = keyboard.Listener(on_press=self.key_pressed)
        self.listener.start()

        # Configura a entrada de texto
        vcmd = (master.register(self.validate), '%P')
        self.entry = ttk.Entry(master, width=40, validate='key', validatecommand=vcmd)
        self.entry.pack(padx=10, pady=10)
        self.entry.bind('<Return>', self.update_value)

        self.frame_1.pack(padx=10, pady=10)

        # Configura o menu de configurações
        self.config_menu = tk.Menu(master, tearoff=0)
        self.theme_menu = ttk.Menu(master, tearoff=0)
        self.config_menu.add_command(label="Mudar fonte", command=self.change_font)
        self.config_menu.add_command(label="mudar cor da fonte", command=self.change_color)
        
        self.config_menu.add_cascade(label="mudar thema", menu=self.theme_menu)
        for t in self.master.style.theme_names():
            self.theme_menu.add_command(label=t, command=lambda theme=t: self.change_theme(theme))

        self.config_button = ttk.Label(master, text="⚙️", cursor='hand2')
        self.config_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.config_button.bind("<Button-1>", self.open_config)
    
    def open_config(self, event):
        self.config_menu.post(self.config_button.winfo_rootx() + 20,  self.config_button.winfo_rooty())
    
    
    def change_font(self):
        # Cria uma instância da caixa de diálogo FontDialog
        font_dialog = ttk.dialogs.FontDialog()
        font_dialog.show()
        self.label.configure(font=font_dialog._result)
        self.label_count.configure(font=font_dialog._result)
        self.save_config()

    def change_color(self):
        # Abre a caixa de diálogo para escolher a cor
        color_code = colorchooser.askcolor(title ="Choose color")
        self.label.configure(fg=color_code[1])
        self.save_config()
    
    def change_theme(self, theme):
        self.master.style.theme_use(theme)
        self.save_config()

    def key_pressed(self, key):
        try:
            if key.char == '+':
                self.value.set(self.value.get() + 1)
            elif key.char == '-':
                self.value.set(self.value.get() - 1) if (self.value.get() - 1 ) >= 0 else 0
        except AttributeError:
            pass

    def update_value(self, event):
        try:
            self.value.set(int(self.entry.get()))
            self.entry.delete(0, 'end')
        except ValueError:
            pass

    def validate(self, new_text):
        if not new_text:  # the field is being cleared
            return True
        try:
            int(new_text)
            return True
        except ValueError:
            return False
    
    def check_config_file(self):
        if not os.path.exists('config.ini'):
            # Cria um arquivo de configuração com valores padrão se ele não existir
            config = configparser.ConfigParser()
            config['DEFAULT'] = {'Theme': 'litera',
                                'Font': 'TkHeadingFont',
                                'Color': 'black'}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

    def save_config(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'Theme': self.master.style.theme_use(),
                             'Font': str(self.label.cget("font")),
                             'Color': self.label.cget("fg")}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def load_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.master.style.theme_use(config['DEFAULT']['theme'])
        self.label.configure(font=config['DEFAULT']['Font'])
        self.label.configure(fg=config['DEFAULT']['Color'])

if __name__ == '__main__':
    root = ttk.Window()
    counter = Counter(root)
    counter.check_config_file()
    counter.load_config()
    root.title('GulloG347')
    root.iconbitmap(counter.ico)
    root.place_window_center()
    root.mainloop()
