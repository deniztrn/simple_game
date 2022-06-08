import question
import sqlite3
import datetime as dt


def add_score(name, score):
	"""Adds users score to a sqlite database"""
	try:
		# Connect to DB and create a cursor
		sqliteConnection = sqlite3.connect('leader_board.db')
		cursor_obj = sqliteConnection.cursor()
		# Write a query and execute it with cursor
		# Create table if it not exists
		table = ("""CREATE TABLE IF NOT EXISTS Leaderboard(
			id INTEGER PRIMARY KEY,
			Name TEXT NOT NULL,
			Score INTEGER,
			Date TEXT);
			""")
		cursor_obj.execute(table)
		# Insert Query
		insert_query = """INSERT INTO Leaderboard
		(Name, Score, Date) 
		VALUES (?, ?, ?);"""
		# Result of one game
		single_entry = (name, score, dt.datetime.now().strftime("%b %d %Y %H:%M"))
		# Entering the entry of a single user
		cursor_obj.execute(insert_query, single_entry)
		# print first 3 top players
		top_3 = cursor_obj.execute("SELECT * FROM 'Leaderboard' Order By Score DESC Limit 3")
		for row in top_3:
			print(row)
		# Commit your changes  in the database
		sqliteConnection.commit()
		cursor_obj.close()
	except sqlite3.Error as error:
		print("Failed to insert Python variable into sqlite table.", error)
	finally:
		if sqliteConnection:
			sqliteConnection.close()


# game
user_nm = input("Please enter your user name\n")
print(f"Hello {user_nm}!\n \t---Press Enter to start the game---\n")
input()

points = 0
questions = question.questions

for i in range(len(questions)):
	i += 1
	print(questions[i][0] + "\n")
	answer = input("").upper()
	if answer == questions[i][1]:
		points += int(questions[i][2])
		print(f"Correct! Your current score is: {points}\n")
	else:
		print(f"Incorrect answer should be {questions[i][1]}.\nPress 'Enter' to continue...")
		input()
		i += 1

print(f"Your final score is {points} \n")
print("------LEADERBOARD------")
add_score(user_nm, points)
