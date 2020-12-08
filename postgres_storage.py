import psycopg2
import dataset
#from bottle import template

db = dataset.connect("postgresql://todouser1:todopassword1@drdelozier-1880.postgres.pythonanywhere-services.com:11880/tododb")
#db = dataset.connect("sqlite://:memory:")


def get_items():
    items = list(db['todo'].all())
    results = [(item['id'], item['task'], item['status']) for item in items]
    return results


def update_status(id, value):
    db['todo'].update(dict(id=id, status=value), ['id'])


def create_item(task, status):
    id = db['todo'].insert(dict(task=task, status=status))
    return id


def get_item(id):
    items = list(db['todo'].find(id=id))
    if len(items) == 0:
        return None
    results = [(item['id'], item['task'], item['status']) for item in items]
    return results[0]


def delete_item(id):
    db['todo'].delete(id=id)


def update_item(update, id):
    db['todo'].update(dict(id=id, task=update), ['id'])


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
    update_status(ex_id, 1)
    tmp = get_item(ex_id)
    #print(tmp)
    assert tmp[2] == 1


#call tests if file is run by itself only
if __name__ == "__main__":
    test_get_items()
    test_get_item()
    test_update_item()
    test_create_item()
    test_delete_item()
    test_update_status()
    print("Done")

