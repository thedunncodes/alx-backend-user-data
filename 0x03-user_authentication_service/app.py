from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home() -> str:
    """ Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register() -> str:
    email, password = request.form.get("email"), request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"})
    return jsonify({"email": "{}".format(user.email),
                    "message": "user created"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
