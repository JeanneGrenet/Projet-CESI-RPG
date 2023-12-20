import random
from rich.console import*
from dbManagment import*
console = Console()


class Entity:
    def __init__(self,entity):
        self.level = 1
        self.entity = entity
        self.maxLife = 10
        
    def attack(self, defender) :
        damage = random.randint(1,2)*self.attackLevel - defender.defenseLevel 
        defender.life -= damage if damage > 0 else 1

class Player(Entity) :
    def __init__(self):
        super().__init__("player")
        self.name = ""
        self.xp = 0    
        self.maxLife = 50
        self.life = self.maxLife
        self.speed = 1
        self.weapons = allWeapons()
        self.accessibleWeapons=[(0,"Poing",1,3)]
        self.currentWeapon = self.accessibleWeapons[0]
        self.equipments = allEquipments()
        self.equipmentDefense = 0
        self.defenseLevel = self.level
        self.attackLevel = self.level * self.currentWeapon[2]
        self.speedLevel = 10*self.level * self.currentWeapon[3] 
    
    def heal(self) :
        life = random.randint(10,self.maxLife)*self.level
        if self.life + life > self.maxLife : 
            self.life = self.maxLife
        else :
            self.life += life
        console.print(f"Vous vous êtes soignés, vous avez maintenant {self.life} point de vie", style="green" )

        
    def checkLevel(self,monster):
        if self.xp >= self.level*2 :
            self.level += 1
            self.maxLife += 2
            self.xp = 0
            self.attackLevel = self.level + self.currentWeapon[2]
            self.speedLevel = 10*self.level * self.currentWeapon[3] 
            console.print(f"Bravo vous montez de niveau ! Vous êtes niveau {self.level}", style = "bold green")
            if self.level%2 == 0 and len(self.weapons)!=0:
                console.print(f"Bravo, vous avez gagné l'arme : {self.weapons[0][1]}", style="bold green")
                self.accessibleWeapons.append(self.weapons[0])
                self.weapons.pop(0)
            if self.level%4 == 1 and len(self.equipments)!=0:
                if len(self.equipments) == 1 : 
                    newEquipment = self.equipments.pop(0)
                    self.equipmentDefense += newEquipment[2]
                    self.defenseLevel = self.level * self.equipmentDefense
                else : 
                    i = random.randint(0, len(self.equipments)-1)
                    newEquipment = self.equipments.pop(i)
                    self.equipmentDefense += newEquipment[2]
                    self.defenseLevel = self.level * self.equipmentDefense
                console.print(f"Bravo, vous avez gagné l'equipement : {newEquipment[1]}, votre défense est maintenant de {self.defenseLevel} points", style="bold green")
            if self.level%3 == 0 :
                monster.activeMonsters.append(monster.monsters[0])
                monster.monsters.pop(0)

                
    def fightPlayer(self,monster):
        action = 0
        while True :
            action = input("Que voulez vous faire ? 1 : Attaquer, 2 : Te soigner, 3 : Changer d'arme\n")
            try : 
                action = int(action)
            except : 
                print("Veuillez entrer un nombre entre 1 et 3")
            if action == 1 :
                speedRate = random.randint(1,(self.speedLevel - monster.speedLevel)//2)
                if speedRate == 1 :
                    console.print("Le monstre a évité votre attaque", style="bold red")
                    break
                else : 
                    self.attack(monster)
                    if monster.life > 0 :
                        console.print(f"Il reste {monster.life} points de vie au monstre", style="red")
                    else :
                        console.print("Le monste est mort", style="red")
                    break
            if action == 2 :
                self.heal()
                break
            if action == 3 :
                weapons = ""
                for i in range(len(self.accessibleWeapons)) : 
                    weapons += f"{i+1} : {self.accessibleWeapons[i][1]} "
                selectedWeapon = int(input("Quelle arme voulez vous choisir ? " + weapons+"\n"))
                try:
                    self.currentWeapon = self.accessibleWeapons[selectedWeapon-1]
                except : 
                    console.print("Cette arme n'est pas attribuée, vous ne réussissez pas à changer d'arme", style="bold cyan")
                break
                

class Monster(Entity) :
    def __init__(self):
        super().__init__("monster")
        self.attackLevel = 0
        self.monsters = allMonsters()
        self.activeMonsters = [[0,"Serpent",1,1,15]]

    def spawn(self,player): 
        self.currentMonster = self.activeMonsters[random.randint(0,len(self.activeMonsters)-1)]
        self.name = self.currentMonster[1]
        self.level = random.randint(player.level, player.level+2)
        self.attackLevel = self.level * self.currentMonster[2]
        self.defenseLevel = self.level * self.currentMonster[3]
        self.speedLevel = self.level + self.currentMonster[4]
        self.life = (self.attackLevel + self.defenseLevel) * 2
        console.print(f"Un monstre de type {self.currentMonster[1]} vient d'apparaitre : niveau = {self.level} / Points de vie : {self.life}", style="bold red")

    def fight(self,player) :
        self.spawn(player)
        while self.life > 0 :
            console.print(f"Votre arme actuelle est {player.currentWeapon[1]}", style="cyan")
            player.fightPlayer(self)
            self.attack(player)
            if self.life > 0 and player.life>0:
                console.print(f"Le monstre vous a attaqué : il vous reste {player.life} points de vie", style="green")
            if player.life <= 0 :
                console.print("Vous êtes mort ! Vous avez perdu !", style="bold red")
                deletTables()
                addUser((player.name, player.level, player.attackLevel, player.defenseLevel, player.speedLevel))
                exit()
        player.xp += self.level//2 | 1
        player.life = player.maxLife
        