from flask import render_template, request, redirect, session
from flask_app import app
from flask import flash
from flask_app.Models.user_model import Users

from flask_bcrypt import Bcrypt        


@app.route("/")
def altlandingPage():

    # if not session['user_id']:
    #     flash ('You must be logged in to access the dash board')
    #     redirect ('/join_ninja')
    return render_template("landing.html")


@app.route("/Landing")
def landingPage():

    # if not 'userName' in session:
    #     flash ('You must be logged in to view profiles', 'profile_access_error')
    #     return redirect('/Landing/Login')
    # else:
        return redirect("/")

@app.route("/Landing/Register")
def registerUser():
    
    return render_template ("register_user.html")

@app.route('/Landing/authorize_user', methods = ['POST'])
def authorizeUser():

    if Users.validate_user(request.form):
        Users.create(request.form)  
        session['userName'] = request.form['userName']   
        return redirect('/Landing/Profiles')
    else:
        return redirect ('/Landing/Register')

@app.route('/Landing/Login')
def login():

    return render_template('login.html')

@app.route('/Landing/authorize_Login', methods = ['POST'])
def verifylogin():
    user = Users.login_user(request.form) #should return true with a user instance or false
    
    if user:
        return redirect ('/Landing/Profiles')
    else:
        return redirect('/Landing/Login')

@app.route('/Landing/Profiles/<int:id>')
def profile(id):
    users = Users.get_all()
    user = Users.get_one_by_id(id)
    if not 'userName' in session:
        flash ('You must be logged in to view profile', 'profile_access_error')
        return redirect ('/')

    return render_template("profile.html", user = user, users = users)

@app.route('/Landing/Profiles')
def profiles():
    users = Users.get_all()
    
    if not 'userName' in session:
        flash ('You must be logged in to access the dash board', 'profile_access_error')
        return redirect ('/Landing/Login')

    return render_template("profiles.html", users = users)

@app.route('/logout')
def logout():
    session['userName'] = None
    return redirect('/')





















    # Ninjas.create(request.form)
    
    # # Call the save @classmethod on User
    # user_id = Ninjas.save(request.form)
    # # store user id into session
    # session['user_id'] = user_id

    # if not Ninjas.validate_ninja(request.form):
    #     return redirect('/join_ninja')
    # else:
    #     Ninjas.create(request.form)
    #     print(request.form)
    #     session['user_id'] = ninja_user.id
    #     return redirect ("/")




# @app.route('/login', methods=['POST'])
# def login():

#     ninja_user = Ninjas.login_user(request.form)
#     if ninja_user:
#         session['user_id'] = ninja_user.id
#         return redirect ('/ninjas')
#     else:
#         return redirect('/join_ninja')
# @app.rout('/logout')
# def logout():
#     session.clear()
#     return redirect('/')

# @app.route('/ninjas/update/<int:id>')
# def update_ninja(id):
#     print(Ninjas.update(request.form))
#     dojos = Dojos.get_all()
#     ninjas = Ninjas.get_all()
#     update_ninja = Ninjas.update_ninja(id)
#     return render_template('update_ninja.html', dojos = dojos, ninjas = ninjas )

# @app.route('/ninjas/delete/<int:id>')
# def delete(id):
#     print(Ninjas.delete(request.form))
#     return redirect('/ninjas')


# def login():
#     # see if the username provided exists in the database
    
#     data = { "email" : request.form["email"] }
#     user_in_db = Ninjas.get_by_email(data)
#     # user is not registered in the db
#     if not user_in_db:
#         flash("Invalid Email/Password")
#         return redirect("/")
#     if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
#         # if we get False after checking the password
#         flash("Invalid Email/Password")
#         return redirect('/')
#     # if the passwords matched, we set the user_id into session
#     session['user_id'] = Ninjas.id
#     # never render on a post!!!
#     return redirect("/ninjas")