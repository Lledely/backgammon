from flask import Flask, request, jsonify
import json
import random
# import os

from data import db_session
from data.sessions import Sessions


app = Flask(__name__)
db_session.global_init('/home/Lledely/mysite/server.db')


@app.route("/update/<int:id>", methods=["POST", "GET"])
def update(id):
    data = request.json
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id).first()
    session.state = data["state"]
    session.prev_move = data["moven"]
    session.dice = f"{random.randint(1, 6)} {random.randint(1, 6)}"
    db_sess.commit()
    responce = {
        "id": session.id,
        "state": session.state,
        "moven": session.prev_move,
        "dice": session.dice
    }
    return jsonify(responce)


@app.route("/get/<int:id>", methods=["POST", "GET"])
def get(id) -> json:
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id).first()
    response = {
        "id": id,
        "state": session.state,
        "moven": session.prev_move,
        "dice": session.dice
    }
    return jsonify(response)


@app.route("/join/<int:id>", methods=["POST", "GET"])
def join(id) -> json:
    db_sess = db_session.create_session()
    session = db_sess.query(Sessions).filter(Sessions.id == id).first()
    responce = {
        "id": session.id,
        "state": session.state,
        "moven": session.prev_move,
        "dice": session.dice
    }
    return json.dumps(responce)


@app.route("/start", methods=["POST", "GET"])
def start() -> json:
    db_sess = db_session.create_session()
    session = Sessions()
    session.state = ' '.join(['w' * 15] + ['e'] * 11 + ['b' * 15] + ['e'] * 11)
    session.prev_move = '1'
    session.dice = f"{random.randint(1, 6)} {random.randint(1, 6)}"
    db_sess.add(session)
    db_sess.commit()
    responce = {
        "id": session.id,
        "state": session.state,
        "moven": session.prev_move,
        "dice": session.dice
    }
    return jsonify(responce)


def main():
    # db_session.global_init(os.path.join(os.path.dirname(os.path.abspath(__file__)), '/home/Lledely/mysite/db/server.db'))
    # db_session.global_init('/home/Lledely/mysite/server.db')
    app.run()


if __name__ == '__main__':
    main()
# db_session.global_init('/home/Lledely/mysite/server.db')
# app.run()
