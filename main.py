import json
import pathlib
import plotly.express as px
import plotly.graph_objects as go


def correct_name(arr):
    new_arr = []
    for user in arr:
        new_arr.append(user.replace("Ä", "ć"))
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


def piechart(labels, values, name):
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=20,
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))
    fig.update_layout(title=name)
    fig.write_image("Images/{}.png".format(name), scale=10)


DATA_ADDRESS = "JSON_data"
JSON_DATA = path_iter(DATA_ADDRESS)
USERS = find_users(JSON_DATA)
TOTAL_MSGS = all_msg(JSON_DATA)
TOTAL_MSGS_PER_USER, USER_CONTENT = users_msg(JSON_DATA, USERS)

USERS = correct_name(USERS)
print(USERS)
print(TOTAL_MSGS_PER_USER)
print(USER_CONTENT)

piechart(USERS, USER_CONTENT, "Total number of characters sent per user in The Bailey")
piechart(USERS, TOTAL_MSGS_PER_USER, "Total number of messages sent per user in The Bailey")

