import json
import pathlib
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def correct_name(arr):
    new_arr = []
    for user in arr:
        user = user.replace("Ä", "ć")
        user = user.replace("Ä", "č")
        user = user.replace("Å ", "Š")
        user = user.replace("Å¡", "š")
        user = user.replace("Å½", "Ž")
        user = user.replace("Å¾", "ž")
        new_arr.append(user)
    return new_arr


def path_iter(address):
    data = []
    for path in pathlib.Path(address).iterdir():
        f = open(path, encoding="utf-8")
        data.append(json.load(f))
        f.close()
    return data


def find_users(data):
    users = []
    for file in data:
        for participant in file["participants"]:
            users.append(participant["name"])
    users = set(users)
    # users = correct_name(users)
    return users


def all_msg(data):
    msg_count = 0
    for file in data:
        for message in file["messages"]:
            msg_count += 1
    return msg_count


def users_msg(data, users):
    user_arr = []
    user_content = []
    for user in users:
        msg_count = 0
        content = ""
        for file in data:
            for message in file["messages"]:
                if message["sender_name"] == user:
                    msg_count += 1
                    if "content" in message:
                        content += message["content"]
        user_arr.append(msg_count)
        user_content.append(len(content))
    return user_arr, user_content


def selection_sort(x, y, z):
    for i in range(len(x)):
        swap = i + np.argmin(x[i:])
        (x[i], x[swap]) = (x[swap], x[i])
        (y[i], y[swap]) = (y[swap], y[i])
        (z[i], z[swap]) = (z[swap], z[i])
    return x, y, z


def revert_array(arr):
    res = arr[::-1]
    return res


def reduce_array(arr):
    new_arr = []
    if len(arr) > 10:
        other = 0
        for j in range(0, 9):
            new_arr.append(arr[j])
        for j in range(10, len(arr)):
            other += arr[j]
        new_arr.append(other)
    else:
        new_arr = arr
    return new_arr


def piechart(labels, values, title):
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'royalblue', ]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=15,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title=title)
    fig.write_image("Images/{}.png".format(title), scale=10)


GROUP_NAME = "OI 2019-2020"
DATA_ADDRESS = "Testing2"
JSON_DATA = path_iter(DATA_ADDRESS)
USERS = find_users(JSON_DATA)
TOTAL_MSGS = all_msg(JSON_DATA)
TOTAL_MSGS_PER_USER, USER_CONTENT = users_msg(JSON_DATA, USERS)

USERS = correct_name(USERS)

USER_CONTENT, USERS, TOTAL_MSGS_PER_USER = selection_sort(USER_CONTENT, USERS, TOTAL_MSGS_PER_USER)
USERS = revert_array(USERS)
USER_CONTENT = revert_array(USER_CONTENT)
TOTAL_MSGS_PER_USER = revert_array(TOTAL_MSGS_PER_USER)

TOTAL_MSGS_PER_USER = reduce_array(TOTAL_MSGS_PER_USER)
USER_CONTENT = reduce_array(USER_CONTENT)

for i in range(9, len(USERS)):
    USERS.pop()
USERS.append('Other')

print(USERS)
print(TOTAL_MSGS_PER_USER)
print(USER_CONTENT)

piechart(USERS, USER_CONTENT, "Total number of CHARACTERS sent per user in {}".format(GROUP_NAME))
piechart(USERS, TOTAL_MSGS_PER_USER, "Total number of MESSAGES sent per user in {}".format(GROUP_NAME))
