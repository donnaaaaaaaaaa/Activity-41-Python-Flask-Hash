from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# In-memory storage for demonstration purposes
hash_storage = {}
user_storage = {}


# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.route('/gethash', methods=['GET'])
def get_hash():
    # Retrieve the stored hash if available
    return jsonify(hash_storage), 200


@app.route('/sethash', methods=['POST'])
def set_hash():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        hash_storage[username] = hash_password(password)
        return jsonify({"message": "Hash set successfully"}), 201
    return jsonify({"error": "Username and password are required"}), 400


@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username in hash_storage:
        if hash_storage[username] == hash_password(password):
            return jsonify({"message": "Login successful"}), 200
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({"error": "User not found"}), 404


@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username')
    password = request.args.get('password')

    if username and password:
        if username not in hash_storage:
            hash_storage[username] = hash_password(password)
            user_storage[username] = password
            return jsonify({"message": "User registered successfully"}), 201
        return jsonify({"error": "Username already exists"}), 409
    return jsonify({"error": "Username and password are required"}), 400


if __name__ == '__main__':
    app.run(debug=True)
