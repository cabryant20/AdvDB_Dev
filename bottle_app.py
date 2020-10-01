
import sqlite3
import os
from bottle import get, post, template, request, redirect


#are we executing on PythonAnywhere?
PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ

#assert PYTHONANYWHERE == False
if PYTHONANYWHERE:
    from bottle import default_app, route
else:
    from bottle import run, debug


@get('/')
def get_show_list():
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("select * from todo")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return template("show_list", rows=result)


@get("/new_item")
def get_new_item():
    return template("new_item")


@post("/new_item")
def post_new_item():
    new_item = request.forms.get("new_item").strip()
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("insert into todo (task, status) values (?,?)", (new_item, 1))
    #cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    redirect("/")


@get("/delete_item/<id:int>")
def get_delete_item(id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("delete from todo where id=?", (id,)) #fake being a tuple
    connection.commit()
    cursor.close()
    connection.close()
    redirect("/")


@get("/set_status/<id:int>/<value:int>")
def get_set_status(id, value):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("update todo set status=? where id=?", (value, id))
    connection.commit()
    cursor.close()
    connection.close()
    redirect("/")


@get("/update_item/<id:int>")
def get_update_item(id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("select * from todo where id=?", (id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    #can add error checking to verify the row is found
    return template("update_item", row=result[0])


@post("/update_item/<id:int>")
def post_update_item(id):
    update_item = request.forms.get("update_item").strip()
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("update todo set task=? where id=?", (update_item, id))
    #cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    redirect("/")


if PYTHONANYWHERE:
    application = default_app()
else:
    run(host='localhost', port=8080)