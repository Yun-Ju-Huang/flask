
import flask_bcrypt

p_hash = flask_bcrypt.generate_password_hash("1234").decode("utf-8")
print(p_hash)

check = flask_bcrypt.check_password_hash("$2b$05$omfOnTlGYnByY9vhhyMceuJa0RIzmGoMTkbfT2tRHJ8qbgBnUTPFG", "1234")
print(check)