from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, redirect, request, session, flash, jsonify
import pg, os, bcrypt, uuid
# import stripe

# Database credentials for local Database
# db = pg.DB(
#     dbname=os.environ.get("PG_DBNAME"),
#     host=os.environ.get("PG_HOST"),
#     user=os.environ.get("PG_USERNAME"),
#     passwd=os.environ.get("PG_PASSWORD")
# )
db = pg.DB(dbname="eCommerce_db")

db.debug = True

tmp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
# Initialize the Flask application
app = Flask("eCommerce", template_folder = tmp_dir)

# Secret Key to generate encrypted tokens used to verify identity
app.secret_key = os.environ.get("SECRET_KEY")


# @app.route('/')
# def home():
#     return app.send_static_file("index.html")

@app.route("/api/products")
def products():
    results = db.query('select * from product').dictresult()
    return jsonify(results)

@app.route("/api/product/<id>")
def products_details(id):
    results = db.query('select * from product where id = $1', id).dictresult()
    return jsonify(results)

@app.route("/api/user/signup", methods=["POST"])
def signup():
    username = request.get_json()["username"]
    email = request.get_json()["email"]
    first_name = request.get_json()["first_name"]
    last_name = request.get_json()["last_name"]
    password = request.get_json()["password"] # the entered password
    salt = bcrypt.gensalt() # generate a salt
    # now generate the encrypted password
    encrypted_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    db.insert (
        "customer",
        username = username,
        email = email,
        first_name = first_name,
        last_name = last_name,
        password = encrypted_password
    )
    return "OK"

@app.route("/api/user/login", methods=['POST'])
def login():
    username = request.get_json()["username"]
    password = request.get_json()["password"] # password entered by user for login
    # encrypted_password = user.password
    customer_result_dict = db.query("select * from customer where username = $1", username).dictresult()
    customer_result_dict = customer_result_dict[0]
    print "customer_result_dict %s" % customer_result_dict
    # encrypted password retrieved from database record
    encrypted_password = customer_result_dict["password"]
    print "encrypted_password %s " % encrypted_password
    # the following line will take the original salt that was used
    # in the generation of the encrypted password, which is stored as
    # part of the encrypted_password, and hash it with the entered password
    rehash = bcrypt.hashpw(password.encode('utf-8'), encrypted_password)
    # if we get the same result, that means the password was correct
    if rehash == encrypted_password:
        token  = uuid.uuid4()
        db.insert (
            "auth_token",
            token = token,
            customer_id = customer_result_dict["id"]
        )
        user_information = {
            "user": {
                "username": customer_result_dict["username"],
                "first_name": customer_result_dict["first_name"],
                "last_name": customer_result_dict["last_name"],
                "email": customer_result_dict["email"]
            },
            "auth_token": token
        }
        return jsonify(user_information)
    else:
        return "Login Failed", 401









# @app.route("/api/shopping_cart")
# def shopping_cart():
#     results = db.query("")
#     return jsonify(results)






if __name__ == "__main__":
    app.run(debug=True)
