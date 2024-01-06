import random
import tkinter as tk
from tkinter import messagebox
from dbManagment import*
from datetime import datetime

date = datetime.now().strftime("%y/%b/%d/%H/%M/%S")
date = datetime.now().strftime("%d %b %Y : %Hh%M")


class Entity:
    def __init__(self,entity):
        self.entity = entity
        
    def cleanup_buttons(self):
        if hasattr(self, 'attack_button') and self.attack_button:
            self.attack_button.destroy()
        if hasattr(self, 'heal_button') and self.heal_button:
            self.heal_button.destroy()
        if hasattr(self, 'weapon_button') and self.weapon_button:
            self.weapon_button.destroy()

class Player(Entity) :
    def __init__(self, master):
        super().__init__("player")
        self.name = ""
        self.level = 1
        self.xp = 0    
        self.maxLife = 50
        self.life = self.maxLife
        self.speed = 1
        self.weapons = allWeapons()
        self.accessibleWeapons=[(0,"Poing",1,3)]
        self.currentWeapon = self.accessibleWeapons[0]
        self.equipments = allEquipments()
        self.equipmentDefense = 1
        self.equipmentSpeed = 1
        self.updateAttack()
        self.updateDefense()
        self.updateSpeed()
        
        self.master = master
        # Cadre principal
        self.frame_main = tk.Frame(self.master)
        self.frame_main.pack()

        # Étiquette pour les informations du joueur
        self.label_info = tk.Label(self.frame_main, text="")
        self.label_info.pack()

        # Cadre pour les boutons d'action
        self.frame_buttons = tk.Frame(self.frame_main)
        self.frame_buttons.pack()

    def heal(self) :
        life = random.randint(10,self.maxLife)*self.level
        if self.life + life > self.maxLife : 
            self.life = self.maxLife
        else :
            self.life += life
        self.update_display(f"Vous vous êtes soignés, vous avez maintenant {self.life} point de vie")

        
    def checkLevel(self,monster):
        if self.xp >= self.level*2 :
            self.level += 1
            self.maxLife += 2
            self.xp = 0
            self.updateAttack()
            self.updateDefense()
            self.updateSpeed()
            self.update_display(f"Bravo vous montez de niveau ! Vous êtes niveau {self.level}")
            if self.level%2 == 0 and len(self.weapons)!=0:
                self.update_display(f"Bravo, vous avez gagné l'arme : {self.weapons[0][1]}")
                self.accessibleWeapons.append(self.weapons[0])
                self.weapons.pop(0)
            if self.level%4 == 1 and len(self.equipments)!=0:
                if len(self.equipments) == 1 : 
                    newEquipment = self.equipments.pop(0)
                else : 
                    i = random.randint(0, len(self.equipments)-1)
                    newEquipment = self.equipments.pop(i)
                self.equipmentDefense += newEquipment[2]
                self.equipmentSpeed += newEquipment[3]
                self.updateDefense()
                self.updateSpeed()
                self.update_display(f"Bravo, vous avez gagné l'equipement : {newEquipment[1]}, votre défense est maintenant de {self.defenseLevel} points")
            if self.level%3 == 0 and len(monster.monsters) !=0 :
                monster.activeMonsters.append(monster.monsters[0])
                monster.monsters.pop(0)

                


    def updateAttack(self):
        self.attackLevel = self.level * self.currentWeapon[2]
        
    def updateDefense(self):
        self.defenseLevel = self.level * self.equipmentDefense

    def updateSpeed(self):
        self.speedLevel = 12*self.level * (self.currentWeapon[3]+self.equipmentSpeed)//2
        
    def update_display(self, message):
        self.label_info.config(text=message)    
        
class Monster(Entity) :
    def __init__(self):
        super().__init__("monster")
        self.attackLevel = 0
        self.monsters = allMonsters()
        self.activeMonsters = [self.monsters.pop(0)]

    def spawn(self,player): 
        self.currentMonster = self.activeMonsters[random.randint(0,len(self.activeMonsters)-1)]
        self.name = self.currentMonster[1]
        self.level = random.randint(player.level, player.level+2)
        self.attackLevel = self.level * self.currentMonster[2]
        self.defenseLevel = self.level * self.currentMonster[3]
        self.speedLevel = self.level + self.currentMonster[4]
        self.life = (self.attackLevel + self.defenseLevel) * 2
        player.update_display(f"Un monstre de type {self.currentMonster[1]} vient d'apparaitre : niveau = {self.level} / Points de vie : {self.life}")

    def player_action(self, player):
        self.attack_button = tk.Button(player.master, text="Attaquer", command=lambda: self.attack_player(player))
        self.heal_button = tk.Button(player.master, text="Te soigner", command=lambda: self.heal_player(player))
        self.weapon_button = tk.Button(player.master, text="Changer d'arme", command=lambda: self.change_weapon_player(player))
        self.attack_button.pack()
        self.heal_button.pack()
        self.weapon_button.pack()

    def monster_action(self, player):
        self.attack_monster(player)
        self.cleanup_buttons()
        
    def fight(self, player):
        self.spawn(player)
        while self.life > 0 :  
            self.player_action(player)
            self.monster_action(player)

    def attack_monster(self, player):
        if player.life > 0:
            damage = random.randint(1, 2) * self.attackLevel - player.defenseLevel
            player.life -= damage if damage > 0 else 1
            if player.life > 0:
                player.update_display(f"Le monstre vous a attaqué : il vous reste {player.life} points de vie")
            else:
                player.update_display("Vous êtes mort ! Vous avez perdu !")
                apiAddUser((player.name, player.level, player.attackLevel, player.defenseLevel, player.speedLevel, date))
                
    def attack_player(self, player):
        speed_rate = random.randint(1, (player.speedLevel - self.speedLevel) // 2 | 2 )
        if speed_rate == 1:
            player.update_display("Le monstre a évité votre attaque.")
        else:
            damage = random.randint(1, 2) * player.attackLevel - self.defenseLevel
            self.life -= damage if damage > 0 else 1
            if self.life > 0:
                player.update_display(f"Il reste {self.life} points de vie au monstre.")
            else:
                player.update_display("Le monstre est mort.")
        self.cleanup_buttons()

    def heal_player(self,player):
        player.heal()
        self.cleanup_buttons()

    def change_weapon_player(self,player):
        player.update_display("Choisissez une arme")

        def select_weapon(player):
            selected_weapon = weapon_var.get()
            player.currentWeapon = player.accessibleWeapons[selected_weapon]
            player.updateAttack()
            player.updateSpeed()
            player.update_display(f"Votre nouvelle arme est {player.currentWeapon[1]}.")

        weapon_var = tk.IntVar()
        for i, weapon in enumerate(player.accessibleWeapons):
            tk.Radiobutton(player.master, text=weapon[1], variable=weapon_var, value=i).pack()

        tk.Button(player.master, text="Arme choisie", command=select_weapon(player)).pack()
        self.cleanup_buttons()

