from flask_app.Config.mysqlconnection import connectToMySQL
from flask import flash # flash needs session!
import datetime
import re
from flask_app import app, DATABASE
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt, 
                         # which is made by invoking the function Bcrypt with our app as an argument

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Users:

    def __init__(self, data):

        self.id = data['id']
        self.userName = data['userName']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def create(cls, data):

        hashedPassword = bcrypt.generate_password_hash(data['password'])

        new_user_data = {
            ** data,
                "password" : hashedPassword,
            }

        query = """
            INSERT INTO users (userName, firstName, lastName, email, password)
            VALUES (%(userName)s, %(firstName)s, %(lastName)s, %(email)s, %(password)s) 
        """

        new_user_data = connectToMySQL('dojogram_db').query_db(query, new_user_data)

        # since our INSERTS will return the id of the created row, so we will return new_user_data
        return new_user_data

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"

        results = connectToMySQL('dojogram_db').query_db(query)
        # Create an empty list to append our instances of Users
        users = []
        # Iterate over the db results and create instances of user with cls.
        for row in results:
            newUser = cls(row)
            users.append(newUser)
        return users

    # the update method will be used when we need to update a friend in our database
    @classmethod
    def get_one_by_id(cls, id):

        data = {
            id:id
        }
        
        query = """
            SELECT * FROM users
            WHERE id = %(id)s
        """

        results = connectToMySQL('dojogram_db').query_db(query, data)

        if results:
            row = results[0]
            return cls(row)

    # The login method requires a true or false check from get_one_by_email to see if user exits
    @classmethod
    def get_one_by_email(cls, email):
        data = {
            'email':'email'
        }
        query = """
            SELECT * FROM users
            WHERE email = %(email)s
        """

        results = connectToMySQL('dojogram_db').query_db(query, data)

        # results returns a list of dictionaries requiring us to loop through to obtain 1 result!
        # However, if results wasnt found, search would be empty, therefore requiring an "if" condition to filter results

        if len(results) > 0:
            row = results[0]
            return cls(row)
        else:
            flash("user not found", 'name_error')
            return False

    # The login method requires a true or false check from get_one_by_email to see if user exits
    @classmethod
    def login_user(cls, creds):

        found_user = cls.get_one_by_email(creds['email'])

        if found_user:
            if bcrypt.check_password_hash(found_user.password, creds['password']):
                return found_user
            else:
                flash ('invalid login attempt', 'login_error')
                return False
        else:
            flash ("invalid login attempt", 'login_error')
            return False

    @classmethod
    def update_user(cls, data):

        query = """
            UPDATE users SET

            userName = %(firstName)s, firstName = %(firstName)s, lastName = %(lastName)s, email = %(email)s, password = %(password)s

            WHERE id = %(id)s
        """
        connectToMySQL(cls.dojogram_db).query_db(query,data )

    @classmethod
    def delete_user(cls, id):

        data = {
            id:id
        }

        query  = """
            DELETE FROM users 
            WHERE id = %(id)s;
        """
    

        connectToMySQL(cls.dojogram_db).query_db(query, data)

    @staticmethod
    def validate_user(form):

        isValid = True
        validEmail = True

        if len(form['firstName']) < 2 or len(form['lastName']) < 2:
            flash("Name is too short", 'name_error')
            isValid = False
        if len(form['email']) < 2:
            flash('email is invalid', 'email_error')
            validEmail = False
        if not EMAIL_REGEX.match(form['email']):
            flash('email format is invalid', 'bad_email_format_error')
            validEmail = False
        if Users.get_one_by_email(form['email']):
            flash('user already exits')
            isValid = False   
        if len(form['password']) < 2:
            flash('password is required', 'password_error')
            isValid = False
        
        # if form['password'] != form['confirm_password']:
        #     flash('password must match')
        #     isValid = False
        # if len(form['password']) < 7:
        #     flash('password too short', 'password_error')
        #     isValid = False

        return isValid



    @classmethod
    def save(cls, data):

        # data = {
        #     email:email
        #     password:password
        # }

        query = """
            INSERT INTO users
            (username, password)
            VALUES (%(email)s, %(password)s)
        """

        return connectToMySQL("dojogram_db").query_db(query, data)
