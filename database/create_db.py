import mysql.connector
import models, database

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="5503",
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE ecommerce")

models.Base.metadata.create_all(bind=database.engine)