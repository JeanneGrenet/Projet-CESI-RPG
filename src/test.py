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
                    self.updateAttack()
                    self.updateSpeed()
                except : 
                    console.print("Cette arme n'est pas attribuée, vous ne réussissez pas à changer d'arme", style="bold cyan")
                break