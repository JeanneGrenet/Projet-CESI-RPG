from player import *
from dbManagment import *
import tkinter as tk


class RPGGameGUI():
    def __init__(self, master):
        self.master = master
        self.master.title("L'épopée des ombres")

        self.player = Player(master)
        self.monster = Monster()
        self.nbMonsters = 0

        self.label_info = tk.Label(master, text="Bienvenue dans l'épopée des ombres", font=("Helvetica", 12, "bold"))
        self.label_info.pack()

        self.label_name = tk.Label(master, text="Quel est ton nom")
        self.label_name.pack()

        self.entry_name = tk.Entry(master)
        self.entry_name.pack()

        self.button_start = tk.Button(master, text="Start Game", command=self.start_game)
        self.button_start.pack()

        self.button_fight = tk.Button(master, text="Fight", command=self.run_game_iteration, state=tk.DISABLED)
        self.button_fight.pack()

    def start_game(self):
        self.player.name = self.entry_name.get()
        self.label_info.config(text=f"Bonjour, {self.player.name}! Puisse le sort vous être favorable.")
        self.button_start.destroy()
        self.button_fight.config(state=tk.NORMAL)

    def run_game_iteration(self):
        self.button_fight.config(state=tk.DISABLED) 

        if self.player.level < 100:
            self.monster.fight(self.player)
            self.player.checkLevel(self.monster)
            self.nbMonsters += 1
            self.label_info.config(text=f"Duel... Congratulations! You have defeated {self.nbMonsters} monsters")

            # Attendez un certain temps avant de lancer la prochaine itération
            self.master.after(2000, self.setup_fight_button)
        else:
            self.label_info.config(text=f"Congratulations! You have reached level 100. Game Over.")

    def setup_fight_button(self):
        # Recréez le bouton Fight après l'attente
        self.button_fight.config(state=tk.NORMAL)
