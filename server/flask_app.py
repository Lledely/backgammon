from flask import Flask, request, redirect, url_for
import json
import random

from data import db_session
from data.sessions import Sessions


app = Flask(__name__)


@app.route("/update/<int:id>", methods=["POST"])
def update(id) -> None:
    data = request.json
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id)
    session.state = data["state"]
    session.prev_move = data["prev_move"]
    session.dice = f"{random.randint(1, 6)} {random.randint(1, 6)}"


@app.route("/get/<int:id>")
def get(id) -> json:
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id)
    next = (["w", "b"].index(session.prev_move) + 1) % 2
    response = {
        "id": id,
        "state": session.state,
        "next": ['w', 'b'][next],
        "dice": session.dice
    }
    return json.dumps(response)


@app.route("/join/<int:id>")
def join(id):
    return redirect(url_for(f"get/{id}"))


@app.route("/start")
def start() -> None:
    db_sess = db_session.create_session()
    session = Sessions()
    session.state = ('w' * 15) + (' ' * 22) + ('b' * 15)
    session.prev_move = random.choice(['w', 'b'])
    session.dice = f"{random.randint(1, 6)} {random.randint(1, 6)}"
    db_sess.add(session)
    db_sess.commit()
    get()


def main():
    db_session.global_init("db/server.db")
    app.run()


if __name__ == '__main__':
    main()
