import sqlite3
import random

DbName = 'discord.db'
connection = sqlite3.connect(DbName)
cursor = connection.cursor()
users = []

for user_id in cursor.execute("SELECT user_id FROM pidors"):
    users.append(int(''.join(map(str, user_id))))
print(users)
winner_id = random.choice(users)

scores = []
for user_id in cursor.execute("SELECT score FROM pidors"):
    scores.append(int(''.join(map(str, user_id))))
print(scores)


top = []
for row in cursor.execute("SELECT user_name, score FROM pidors order by score DESC"):
    top.append(' - '.join(map(str, row)), '\n')
    top.append('\n')
    print(row)
print(top)





# top = cursor.execute("SELECT user_name, score FROM pidors order by score DESC")
# print(top)
# names, scores = top.fetchmany(len(users))
# print(names, scores)