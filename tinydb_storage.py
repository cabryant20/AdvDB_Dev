
from tinydb import TinyDB, Query
from bottle import template


db = TinyDB('todo.json')


def get_items():
    global db
    return db.all()


#def update_status(id, value):
#    connection = sqlite3.connect("todo.db")
#    cursor = connection.cursor()
#    cursor.execute("update todo set status=? where id=?", (value, id))
#    connection.commit()
#    cursor.close()
#    connection.close()


#def create_item(task, status):
#    connection = sqlite3.connect("todo.db")
#    cursor = connection.cursor()
#    cursor.execute("insert into todo (task, status) values (?,?)", (task, status))
#    id = cursor.lastrowid
#    connection.commit()
#    cursor.close()
#    connection.close()
#    return id


#def get_item(id):
#    connection = sqlite3.connect("todo.db")
#    cursor = connection.cursor()
#    cursor.execute("select * from todo where id=?", (id,))
#    result = cursor.fetchall()
#    cursor.close()
#    connection.close()
#    #can add error checking to verify the row is found
#    if len(result) == 0:
#        return None
#    return result[0]


#def delete_item(id):
#    connection = sqlite3.connect("todo.db")
#    cursor = connection.cursor()
#    cursor.execute("delete from todo where id=?", (id,)) #fake being a tuple
#    connection.commit()
#    cursor.close()
#    connection.close()


#def update_item(update, id):
#    connection = sqlite3.connect("todo.db")
#    cursor = connection.cursor()
#    cursor.execute("update todo set task=? where id=?", (update, id))
#    #cursor.lastrowid
#    connection.commit()
#    cursor.close()
#    connection.close()


def print_results(results):
    for result in results:
        print(result.doc_id, result)


#tests
import random
random.seed()
def _random_text():
    rand_txt = str(random.randint(10000, 20000))
    return rand_txt

def test_get_items():
    global db
    #db.insert({'task':'task1','status':0})
    #db.insert({'task':'task2','status':1})
    #db.insert({'task':'task3','status':0})
    print("Testing get_items()")
    results = get_items()
    assert type(results) is list
    assert len(results) > 0
    for result in results:
        print(result.doc_id, result['task'], result['status'])


#def test_get_item():
#    print("Testing get_item(id)")
#    results = get_items()
#    assert len(results) > 0
#    id,_,_ = results[0]
#    result = get_item(id)
#    #print(result)
#    assert type(result) is tuple


#def test_update_item():
#    print("Testing update_item(update, id)")
#    ex_task = "This is an example item: " + _random_text()
#    id = create_item(ex_task, 0)
#    _, _, status = get_item(id)
#    updated_task = ex_task + " UPDATED"
#    update_item(updated_task, id)
#    _, task, status = get_item(id)
#    assert task == updated_task


#def test_create_item():
#    print("Testing create_item()")
#    ex_task = "This is an example item: " + _random_text()
#    create_item(ex_task, 0)
#    items = get_items()
#    found = False
#    for item in items:
#        if item[1] == ex_task:
#            found = True
#    assert found


#def test_delete_item():
#    print("Testing delete_item(id)")
#    ex_task = "This is an example item: " + _random_text()
#    id = create_item(ex_task, 0)
#    delete_item(id)
#    check = get_item(id)
#    assert check == None


#def test_update_status():
#    print("Testing update_status(id, value)")
#    ex_task = "This is an example item: " + _random_text()
#    create_item(ex_task, 0)
#    items = get_items()
#    for item in items:
#        if item[1] == ex_task:
#            ex_id = item[0]
#            assert item[2] == 0
#    update_status(ex_id, 1)
#    tmp = get_item(ex_id)
#    print(tmp)
#    assert tmp[2] == 1


#call tests if file is run by itself only
if __name__ == "__main__":
    test_get_items()
 #   test_get_item()
 #   test_update_item()
 #   test_create_item()
 #   test_delete_item()
 #   test_update_status()
    print("Done")

