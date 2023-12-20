from player import *
from dbManagment import *


class Game : 
    
    def __init__(self):
        loadTables()
        self.player = Player()
        self.monster = Monster()
        self.nbMonstres = 0

        
    def run(self) :
        #Boucle du jeu
        run = True
        console.print("Bienvenue dans l'Épopée des Ombres", style="bold")
        self.player.name = input("Comment vous appelez vous ?\n")
        while run : 
            print("------------------------------------------------------------DUEL------------------------------------------------------------")
            self.monster.fight(self.player)
            self.player.checkLevel(self.monster)
            self.nbMonstres += 1
            print("---------------------------------------------------------FIN DU DUEL---------------------------------------------------------")
            console.print(f"Félicitations vous aves battu {self.nbMonstres} monstres", style="cyan")
            if self.player.level >= 100 :
                run = False
        deletTables()