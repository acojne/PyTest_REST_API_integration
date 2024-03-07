import random

import requests

ENDPOINT = "https://todo.pixegami.io"


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def get_list_task(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def new_payload_task(content, user_id, is_done = False):
    return {
        "content": content,
        "user_id": user_id,
        "is_done": is_done,
    }

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def test_todo_api():
    response = requests.get(ENDPOINT)
    print(response)
    data = response.json()
    print(data)

    status_code = response.status_code
    assert status_code == 200


def test_create_task():
    payload = {
        "content": "New Task",
        "user_id": "test_user111",
        "is_done": False,
    }
    create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    create_task_data = create_task_response.json()
    # print(create_task_data)

    task_id = create_task_data['task']['task_id']
    # Check newly added data
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    get_task_data = get_task_response.json()
    print(get_task_data)
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]
    assert get_task_data["task_id"] == create_task_data['task']["task_id"]


def test_update_task():
    # create new task
    payload = new_payload_task("new_task_01","User_01", True)
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    print(get_task(task_id).json())

    # update task
    new_payload = {
        "content": "Updated New Task 1 ",
        "task_id": task_id,
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200
    print(update_task_response.json())

    # get and validate task
    get_updated_data = get_task(task_id).json()
    print(get_updated_data)
    assert get_updated_data["content"] == new_payload["content"]
    assert get_updated_data["user_id"] == payload["user_id"]
    assert get_updated_data["is_done"] == True


def test_tasks_per_userid():
    all_tasks = get_list_task("User_02").json()

    for item in all_tasks["tasks"]:
        print(item["task_id"])
        delete_task(item["task_id"])

    print(get_list_task("User_01").json())

def test_delete_all_tasks():
    n = 3

    for _ in range(n):
        content = "Task" + "_" + str(random.randint(0, 1000))
        create_task(new_payload_task(content, "User_01", True))

    all_tasks = get_list_task("User_01").json()

    for item in all_tasks["tasks"]:
        delete_task(item["task_id"])

    print(get_list_task("User_01").json())