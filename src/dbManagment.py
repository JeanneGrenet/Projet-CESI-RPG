import sqlite3




def addMonster(monster): 
    connection = sqlite3.connect('src/rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO monsters(type, attackPoints, defensePoints, speedPoints) VALUES(?,?,?,?)
    """, monster)
    connection.commit()
    connection.close()
    
def addWeapon(weapon): 
    connection = sqlite3.connect('src/rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO weapons(name, attackMultiplier, speedMultiplier) VALUES(?,?,?)
    """, weapon)
    connection.commit()
    connection.close()
    
def addEquipment(equipment): 
    connection = sqlite3.connect('src/rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO equipments(name, defenseMultiplier, speedMultiplier) VALUES(?,?,?)
    """, equipment)
    connection.commit()
    connection.close()
        
def deletTables():
    connection = sqlite3.connect('src/rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
        DROP TABLE monsters
    """)
    cursor.execute("""
        DROP TABLE weapons
    """)
    cursor.execute("""
        DROP TABLE equipments
    """)
    connection.commit()
    connection.close()
        
def allWeapons():
    connection = sqlite3.connect('rpg.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM weapons""")
    weapons = cursor.fetchall()
    connection.close()
    return weapons

def allEquipments():
    connection = sqlite3.connect('rpg.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM equipments""")
    equipments = cursor.fetchall()
    connection.close()
    return equipments

def allMonsters():
    connection = sqlite3.connect('rpg.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM monsters ORDER BY attackPoints""")
    monsters = cursor.fetchall()
    connection.close()
    return monsters

def addUser(user):
    connection = sqlite3.connect('rpg.db')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO User(name, level, attackPoints, defensePoints, speedPoints, date) VALUES(?,?,?,?,?,?)
    """, user)
    connection.commit()
    connection.close()

#Create the table to save users

# connection = sqlite3.connect('src/rpg.db')
# cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS User(
#         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#         name TEXT,
#         level INTERGER,
#         attackPoints INTEGER,
#         defensePoints INTERGER,
#         speedPoints INTEGER
#     )
#     """)
# connection.commit()
# connection.close()


# connection = sqlite3.connect('src/rpg.db')
# cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS monsters(
#         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#         type TEXT,
#         attackPoints INTERGER,
#         defensePoints INTERGER,
#         speedPoints INTEGER
#     )
#     """)
# connection.commit()
# connection.close()

# connection = sqlite3.connect('src/rpg.db')
# cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS weapons(
#         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#         name TEXT,
#         attackMultiplier INTERGER,
#         speedMultiplier INTEGER
#     )
#     """)
# connection.commit()
# connection.close()

# connection = sqlite3.connect('src/rpg.db')
# cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS equipments(
#         id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
#         name TEXT,
#         defenseMultiplier INTERGER,
#         speedMultiplier INTEGER
#     )
#     """)
# connection.commit()
# connection.close()

# monsterList = ["Serpent","Squelette", "Loup-Garou", "Gobelin", "Orc", "Troll", "Ogre", "Dragon", "Chimère", "Vampire", "Hydre"]
# weaponList = [ "Batton", "Hâche", "Marteau", "Poignard", "Épée", "Lame du Héro" ]
# equipmentList= [ ["Casque", 3, 3], ["Plastron", 5, 2], ["Bouclier", 4, 1], ["Gant", 1, 5], ["Bottes",2, 4], ["Armure du Héro", 10, 10] ]

# for i in range(len(monsterList)):
#     addMonster((monsterList[i], i+2, i+1, 15-i))
    
# for i in range(len(weaponList)):
#     addWeapon((weaponList[i], i+2, i+4))
    
# for i in range(len(equipmentList)):
#     addEquipment((equipmentList[i][0], equipmentList[i][1], equipmentList[i][2]))




