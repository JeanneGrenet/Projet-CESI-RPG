import flask
import sqlite3



app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
   connection = sqlite3.connect('src/rpg.db')
   cursor = connection.cursor()
   cursor.execute('SELECT * FROM User')
   users = cursor.fetchall()
   connection.close()
   
   list_users = []

   for user in users:
      list_users.append({
         "id": user[0],
         "name": user[1],
         "level": user[2],
         "attackPoints": user[3],
         "defensePoints": user[4],
         "speedPoints": user[5],
         "date": user[6],

      }) 

   return flask.render_template('index.html', users=list_users)

@app.route('/monsters')
def monsters():
   connection = sqlite3.connect('src/rpg.db')
   cursor = connection.cursor()
   cursor.execute('SELECT * FROM monsters ORDER BY attackPoints')
   monsters = cursor.fetchall()
   connection.close()
   
   list_monsters = []

   for monster in monsters:
      list_monsters.append({
         "id": monster[0],
         "type": monster[1],
         "attackPoints": monster[2],
         "defensePoints": monster[3],
         "speedPoints": monster[4],

      }) 

   return flask.render_template('monsters.html', monsters=list_monsters)

@app.route('/add', methods=['GET', 'POST'])
def add():

    #on vérifie le protocole HTML de la requête
    if flask.request.method == 'POST':

        #Si c'est POST, on récupère les valeurs du formulaire
        typeMonster = flask.request.values.get('type')
        attackPoints = flask.request.values.get('attackPoints')
        defensePoints = flask.request.values.get('defensePoints')
        speedPoints = flask.request.values.get('speedPoints')

        #On se connecte à la base de données et on INSERT notre nouveau chien !
        connection = sqlite3.connect('src/rpg.db')

        cursor = connection.cursor()
        cursor.execute('INSERT INTO monsters (type, attackPoints, defensePoints, speedPoints) VALUES ("' + typeMonster + '", "' + attackPoints + '", "' + defensePoints + '", "' + speedPoints + '")')
        connection.commit()
        connection.close()

        #Quand c'est bon, on redirige vers la page d'accueil
        return flask.redirect('/monsters')
    else:

        #Si ce n'est pas une requête POST, on affiche le formulaire
        return flask.render_template('add.html')

@app.route('/deleteMonster/<id>')
#On prend en paramètre l'id de la donnée qu'on veut suppriemr
def deleteMonster(id):
    #On se connecte à la base de données
    connection = sqlite3.connect('src/rpg.db')

    cursor = connection.cursor()

    #On supprime la donnée si l'ID est égal au paramètre
    cursor.execute('DELETE FROM monsters WHERE id = ' + id)
    connection.commit()
    connection.close()

    #On redirige l'utilisateur sur la page d'accueil
    return flask.redirect('/monsters')

@app.route('/deleteUser/<id>')
#On prend en paramètre l'id de la donnée qu'on veut suppriemr
def deleteUser(id):
    #On se connecte à la base de données
    connection = sqlite3.connect('src/rpg.db')

    cursor = connection.cursor()

    #On supprime la donnée si l'ID est égal au paramètre
    cursor.execute('DELETE FROM User WHERE id = ' + id)
    connection.commit()
    connection.close()

    #On redirige l'utilisateur sur la page d'accueil
    return flask.redirect('/')