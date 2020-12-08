#Convert to use nosql

import pickle
import os

items = []
filename = None

def everything(v):
    return v

def always(v):
    return True

def never(v):
    return False

def next_id():
    global items
    id = 1
    for item in items:
        if item['id'] > id:
            id = item['id']
    return id

def open_database(name):
    global filename
    global items
    filename = name
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            items = pickle.load(f)
    else:
        items = []

def commit():
    global filename
    global items
    with open(filename, "wb") as f:
        pickle.dump(items, f)

def insert(data):
    items.append(data)
    commit()

def query(select=everything, where=always):                     #default select *
    return [select(item) for item in items if where(item)]

def update(where=never, content=lambda v:{}):                          #default update nothing
    global items
    for item in items:
        if where(item):
            new_values = content(item)
            for key in new_values.keys():
                item[key] = new_values[key]
    commit()
    return

def delete(where=never):                                        #delete nothing by default
    global items
    #should lock items to this transaction
    kept_items = [item for item in items if not where(item)]    #make a copy of all items except those to be deleted
    items = kept_items
    commit()
    #unlock
    return

def get_items():
    items = query(select=everything, where=always)
    results = [(item['id'], item['task'], item['status']) for item in items]
    return results


def update_status(id):
    update(where=lambda v:v['id']==id, content=lambda v:{'status':(v['status']+1)%2})


def create_item(task, status):
    id = next_id()
    insert({"id":id, "task":task, "status":status})
    return id


def get_item(id):
    items = query(select=everything, where=lambda v:v['id']==id)
    if len(items) == 0:
        return None
    results = [(item['id'], item['task'], item['status']) for item in items]
    return results[0]


def delete_item(id):
    delete(lambda v:v['id']==id)


def update_item(new_task, id):
    update(where=lambda v:v['id']==id, content=lambda v:{'task':new_task})


#tests
import random
random.seed()
def _random_text():
    rand_txt = str(random.randint(10000, 20000))
    return rand_txt


def test_get_items():
    print("Testing get_items()")
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
    #print(result)
    assert type(result) is tuple


def test_update_item():
    print("Testing update_item(update, id)")
    ex_task = "This is an example item: " + _random_text()
    id = create_item(ex_task, 0)
    _, _, status = get_item(id)
    updated_task = ex_task + " UPDATED"
    update_item(updated_task, id)
    _, task, status = get_item(id)
    assert task == updated_task


def test_create_item():
    print("Testing create_item()")
    ex_task = "This is an example item: " + _random_text()
    create_item(ex_task, 0)
    items = get_items()
    found = False
    for item in items:
        if item[1] == ex_task:
            found = True
    assert found


def test_delete_item():
    print("Testing delete_item(id)")
    ex_task = "This is an example item: " + _random_text()
    id = create_item(ex_task, 0)
    delete_item(id)
    check = get_item(id)
    assert check == None


def test_update_status():
    print("Testing update_status(id, value)")
    ex_task = "This is an example item: " + _random_text()
    create_item(ex_task, 0)
    items = get_items()
    for item in items:
        if item[1] == ex_task:
            ex_id = item[0]
            assert item[2] == 0
    update_status(ex_id)
    tmp = get_item(ex_id)
    #print(tmp)
    assert tmp[2] == 1


#call tests if file is run by itself only
if __name__ == "__main__":
    open_database("todo.pkl")
    test_create_item()
    test_get_items()
    test_get_item()
    test_update_item()
    test_delete_item()
    test_update_status()
    print("Done")

