
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


from storage import get_item, get_items, create_item, delete_item, update_item, update_status

@get('/')
def get_show_list():
    result = get_items()
    return template("show_list", rows=result)


@get("/new_item")
def get_new_item():
    return template("new_item")


@post("/new_item")
def post_new_item():
    new_item = request.forms.get("new_item").strip()
    create_item(new_item, 1)
    redirect("/")


@get("/delete_item/<id:int>")
def get_delete_item(id):
    delete_item(id)
    redirect("/")


@get("/set_status/<id:int>/<value:int>")
def get_set_status(id, value):
    update_status(id, value)
    redirect("/")


@get("/update_item/<id:int>")
def get_update_item(id):
    result = get_item(id)
    return template("update_item", row=result)


@post("/update_item")
def post_update_item():
    update = request.forms.get("update_item").strip()
    id = request.forms.get("id").strip()
    update_item(update, id)
    redirect("/")


if PYTHONANYWHERE:
    application = default_app()
else:
    run(host='localhost', port=8080)

