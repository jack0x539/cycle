from flask import Flask, render_template, request, session, redirect
from api import MySqlApiContext as ApiContext
import configparser as config

conf = config.ConfigParser()
conf.read("app.config")

api = ApiContext("127.0.0.1", "cycle", conf["database"]["username"], conf["database"]["password"])
app = Flask(__name__)
app.secret_key = "m;oimHLJKFDNLc9p8oiASchncsn98jdsc[pomdsoc987()*&)USHHC98auiscn"

alert_bad = "alert-danger"
alert_good = "alert-success"

def alert(message, kind):
    if not "alerts" in session:
        session["alerts"] = []
    session["alerts"].append((message, kind))

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html")

@app.route("/users/")
def users():
    users = api.get_users(False)
    if not users:
        alert(api.last_error, alert_bad)
        return login()
    return render_template("users.html", users=users)

@app.route("/users/<id>")
def user(id):
    user = None

    if id:
        user = api.get_user(id)
        if not user:
            alert(api.last_error, alert_bad)
    
    data = {
        "id": user.id,
        "username": user.username,
        "forename": user.forename,
        "surname": user.surname,
        "emailaddress": user.email_address,
        "dob": user.dob,
        "primaryrole": user.primary_event_role.id if user.primary_event_role else 0,
        "address": user.address,
        "roles": api.get_event_roles()
    }

    return render_template("user.html", **data)

@app.route("/users/<id>", methods=["POST"])
def user_post(id):
    username = request.form["username"].strip() if request.form["username"] else ""
    forename = request.form["forename"].strip() if request.form["forename"] else ""
    surname = request.form["surname"].strip() if request.form["surname"] else ""
    email_address = request.form["emailaddress"] if request.form["emailaddress"] else ""
    dob = request.form["dob"] if request.form["dob"] else ""
    primary_role_id = request.form["primaryrole"] if request.form["primaryrole"] else None

    data = {
        "username": username,
        "forename": forename,
        "surname": surname,
        "emailaddress": email_address,
        "dob": dob,
        "primaryrole": primary_role_id
    }

    if not username or not forename or not surname or not email_address or not dob:
        alert("all fields are required", alert_bad)
        return render_template("user.html", **data)
    
    user = api.update_user(id, username, forename, surname, email_address, dob, primary_role_id)
    if not user:
        alert("failed to update user; {}".format(api.last_error), alert_bad)
        return render_template("user.html", **data) 
    
    alert("user updated", alert_good)
    return redirect("/users/{}".format(id))

@app.route("/users/create")
def user_create():
    return render_template("user.html")

@app.route("/users/create", methods=["POST"])
def user_create_post():
    username = request.form["username"].strip() if request.form["username"] else ""
    forename = request.form["forename"].strip() if request.form["forename"] else ""
    surname = request.form["surname"].strip() if request.form["surname"] else ""
    email_address = request.form["emailaddress"] if request.form["emailaddress"] else ""
    dob = request.form["dob"] if request.form["dob"] else ""

    data = {
        "username": username,
        "forename": forename,
        "surname": surname,
        "emailaddress": email_address,
        "dob": dob
    }

    if not username or not forename or not surname or not email_address or not dob:
        alert("all fields are required", alert_bad)
        return render_template("user.html", **data)
    
    user = api.create_user(username, forename, surname, email_address, dob)
    if not user:
        alert("failed to create user; {}".format(api.last_error), alert_bad)
        return render_template("user.html", **data)

    alert("user created", alert_good)
    return redirect("/users/{}".format(user.id))

@app.route("/users/<id>/address/create")
def user_address(id):
    user = api.get_user(id, False)

    if not user:
        if api.erred:
            alert("Failed to load <strong>User</strong>; {}".format(api.last_error), alert_bad)
        else:
            alert("<strong>User</strong> not found.", alert_bad)
        return redirect("/users")

    return render_template("address.html", user=user, address=user.address)

@app.route("/users/<id>/address/create", methods=["POST"])
def user_address_post(id):
    address1 = request.form["address1"].strip() if request.form["address1"] else ""
    address2 = request.form["address2"].strip() if request.form["address2"] else ""
    address3 = request.form["address3"].strip() if request.form["address3"] else ""
    county = request.form["county"].strip() if request.form["county"] else ""
    postcode = request.form["postcode"].strip() if request.form["postcode"] else ""

    address = api.create_user_address(id, address1, address2, address3, county, postcode)

    if address:
        alert("Address created.", alert_good)
        return redirect("/users/{}".format(id))
    
    alert("Failed to create address; {}".format(api.last_error), alert_bad)
    return redirect("/users/{}/address/create".format(id))

@app.route("/eventroles/<id>")
def event_role(id):
    role = None

    if id:
        role = api.get_event_role(id)
        if not role:
            alert("Failed to load <strong>EventRole</strong>; {}".format(api.last_error), alert_bad)
            return redirect("/eventroles")
    
    data = {
        "id": role.id,
        "name": role.name,
        "description": role.description
    }

    return render_template("event_role.html", **data)

@app.route("/eventroles/<id>", methods=["POST"])
def event_role_post(id):
    name = request.form["name"] if "name" in request.form else ""
    description = request.form["description"] if "description" in request.form else ""

    data = {
        "id": id,
        "name": name,
        "description": description
    }

    if not name:
        alert("The <strong>name</strong> field is required.", alert_bad)
        return render_template("event_role.html", **data)
    
    role = api.update_event_role(id, name, description)
    if not role:
        alert("Failed to update <strong>EventRole</strong>; {}".format(api.last_error), alert_bad)
        return render_template("event_role.html", **data)

    alert("Updated EventRole <strong>{}</strong>.".format(name), alert_good)
    return redirect("/eventroles/{}".format(id))

@app.route("/eventroles/create")
def event_role_create():
    return render_template("event_role.html")

@app.route("/eventroles/create", methods=["POST"])
def event_role_create_post():
    name = request.form["name"] if "name" in request.form else ""
    description = request.form["description"] if "description" in request.form else ""

    data = {
        "name": name,
        "description": description
    }

    if not name:
        alert("The <strong>name</strong> field is required.", alert_bad)
        return render_template("event_role.html", **data)
    
    role = api.create_event_role(name, description)
    if not role:
        alert("Failed to create <strong>EventRole</strong>; {}".format(api.last_error), alert_bad)
        return render_template("event_role.html", **data)

    alert("New event role '<strong>{}</strong>' created.".format(name), alert_good)
    return redirect("/eventroles")

@app.route("/eventroles/<id>/delete")
def event_role_delete(id):
    role = api.get_event_role(id)

    if not role:
        alert("Failed to load <strong>EventRole</strong>; {}".format(api.last_error), alert_bad)
        return redirect("/eventroles")
    
    data = {
        "id": role.id,
        "name": role.name,
        "description": role.description
    }

    return render_template("event_role_delete.html", **data)

@app.route("/eventroles/<id>/delete", methods=["POST"])
def event_role_delete_post(id):
    role = api.get_event_role(id)
    success = api.delete_event_role(id)

    if role and success:
        alert("Deleted EventRole <strong>{}</strong>".format(role.name), alert_good)
    elif role:
        alert("Failed to delete EventRole <strong>{}</strong>; {}".format(role.name, api.last_error), alert_bad)
    else:
        alert("Failed to delete <strong>EventRole</strong>; {}".format(api.last_error), alert_bad)
        
    return redirect("/eventroles")
    
@app.route("/eventroles/")
def event_roles():
    roles = api.get_event_roles(False)
    if not roles and api.erred:
        alert("Failed to load <strong>Event Roles</strong>; {}".format(api.last_error), alert_bad)
    return render_template("event_roles.html", event_roles=roles)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    session["username"] = username
    session["password"] = password

    api.username = username
    api.password = password

    return redirect("/eventroles")

@app.route("/init")
def init():
    api.install()
    if api.erred:
        alert("install failed; {}".format(api.last_error), alert_bad)
    else:
        alert("installed", alert_good)
    return redirect("/")

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
    