from flask import Flask, render_template, request, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore

app = Flask(__name__)

# Initialize Firebase Admin
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/")
def dashboard():
    return render_template("admin.html")

@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.json
    name     = data.get("name")
    email    = data.get("email")
    password = data.get("password")
    role     = data.get("role")  # "doctor", "patient", "counselor"

    # Basic validation
    if not all([name, email, password, role]):
        return jsonify({"error": "All fields are required"}), 400

    if role not in ["doctor", "patient", "counselor"]:
        return jsonify({"error": "Invalid role"}), 400

    try:
        # Create user in Firebase Auth
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )

        # Save role + name in Firestore
        db.collection("users").document(user.uid).set({
            "name": name,
            "email": email,
            "role": role,
            "uid": user.uid
        })

        return jsonify({"success": True, "uid": user.uid}), 201

    except auth.EmailAlreadyExistsError:
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list-users", methods=["GET"])
def list_users():
    users = db.collection("users").stream()
    result = [u.to_dict() for u in users]
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)