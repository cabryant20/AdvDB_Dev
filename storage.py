import sqlite3
from bottle import template

def get_items():
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("select * from todo")
    result = cursor.fetchall()
    cursor.close()
    return result


def update_status(id, value):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("update todo set status=? where id=?", (value, id))
    connection.commit()
    cursor.close()
    connection.close()


def create_item(task, status):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("insert into todo (task, status) values (?,?)", (task, status))
    id = cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()
    return id


def get_item(id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("select * from todo where id=?", (id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    #can add error checking to verify the row is found
    return result[0]


def delete_item(id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("delete from todo where id=?", (id,)) #fake being a tuple
    connection.commit()
    cursor.close()
    connection.close()


def update_item(update, id):
    connection = sqlite3.connect("todo.db")
    cursor = connection.cursor()
    cursor.execute("update todo set task=? where id=?", (update, id))
    #cursor.lastrowid
    connection.commit()
    cursor.close()
    connection.close()


#tests
def test_get_items():
    print("Test get_items")
    results = get_items()
    assert type(results) is list
    assert len(results) > 0
    print(results)


def test_get_item():
    print("Testing get_item(id)")
    results = get_items()
    assert len(results) > 0
    id,_,_ = results[0]
    result = get_item(id)
    print(result)
    assert type(result) is tuple



#call tests if file is run by itself only
if __name__ == "__main__":
    test_get_items()
    test_get_item()

