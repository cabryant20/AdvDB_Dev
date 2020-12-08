
#Convert to use mongodb

#import sqlite3
import os
from bottle import get, post, template, request, redirect
import pymongo


client = pymongo.MongoClient("mongodb+srv://tester_1:testing1234@cluster0.qxejs.mongodb.net/todo?retryWrites=true&w=majority",
                                connectTimeoutMS=30000,
                                socketTimeoutMS=None,
                                #socketKeepAlive=True,
                                connect=False,
                                maxPoolsize=1)
db = client.todo


#are we executing on PythonAnywhere?
PYTHONANYWHERE = "PYTHONANYWHERE_DOMAIN" in os.environ


#assert PYTHONANYWHERE == False
if PYTHONANYWHERE:
    from bottle import default_app, route
else:
    from bottle import run, debug


#from storage import get_item, get_items, create_item, delete_item, update_item, update_status
from postgres_storage import get_item, get_items, create_item, delete_item, update_item, update_status
#from mongo_storage import get_item, get_items, create_item, delete_item, update_item, update_status


@get('/')
def get_show_list():
    result = db.task.find()
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
    db.task.delete_one({"id":id})
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
    db.todo.update_one({"id":id}, {"$set" : {"task":new_task})
    redirect("/")


if PYTHONANYWHERE:
    application = default_app()
else:
    run(host='localhost', port=8080)






def update_status(id):
    item = db.todo.find_one({"id":id})
    result = [item['id'], item['task'], item['status']]
    db.todo.update_one({"id":id}, {"$set" : {"status":((result[2]+1)%2)})


def create_item(task, status):
    id = next_id()
    db.todo.insert_one({"id":id, "task":task, "status":status})
    return id


def get_item(id):
    item = db.todo.find_one({"id":id})
    if len(item) == 0:
        return None
    result = [(item['id'], item['task'], item['status'])]
    return result



def update_item(new_task, id):
    db.todo.update_one({"id":id}, {"$set" : {"task":new_task})



#call tests if file is run by itself only
if __name__ == "__main__":

    print("Done")

