import flask
import sqlite3

app = flask.Flask(__name__, template_folder='views')

@app.route('/')
def home():
   connection = sqlite3.connect('Projet-CESI-RPG/rpg.db')
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

      }) 

   return flask.render_template('index.html', uses=list_users)

