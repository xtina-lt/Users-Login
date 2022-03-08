###############
''' IMPORTS '''
###############
from flask_app.config.mysqlconnection import connectToMySQL
# 1) import query metthod
from flask import flash
# 2) import flash
from flask_bcrypt import Bcrypt
# 3) import bcrypt hashing
from flask_app import app
# 3) import app
bcrypt = Bcrypt(app) 
# 3) access to app to pass to bcrypt
import re
# 4) import regex compiler
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
# 4) re.compile characters_numbers@characters_numbers.com
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
# 4) re.compile  one letter and one number, upper and lower, 1 special character atleast 8 characters


###############
'''  CLASS  '''
###############
class User:
    db = 'users_schema'
    # global variable
    # SQL: schema.table == users_schema.users

    def __init__(self, data):
    # {'first_name': 'xxxxx', 'last_name': 'xxxx', 'email':'xxxx@xxxx.com', 'password':'xxxxxxxx'}
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]




    ############
    ''' READ '''
    ############
    '''READ ALL'''
    @classmethod
    def select_all(cls):
        query="SELECT * FROM users"
        results = connectToMySQL(cls.db).query_db(query)
        return [cls(i) for i in results]
        # returns User class with each dictionary from list of resutls

    '''READ ONE'''
    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM users WHERE id=%(id)s"
        result=connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])
        # returns a User of the first dictionary in result list
    
    @classmethod
    def is_email(cls,data):
        query="SELECT * FROM users WHERE email=%(email)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return results[0]
        else:
            return False
            # either [{user:details}] 
            # or
            # ()
    
    @classmethod
    def get_password(cls, data):
        query="SELECT password FROM users WHERE email=%(id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result[0])
        return result[0]



    
    ############
    '''LOGIN'''
    ############
    @staticmethod
    def validate_login(e):
        is_valid = True
        # 1) set is_valid to Ture
        # 1) change if validation is False
        email=User.is_email(e)
        # 2) check to see if an email is in the sytsem
        
        if email:
        # 3) IF EMAIL IN DB
            check_me=User.select_one(email)
            # 3a) use the first and only email
            if not bcrypt.check_password_hash(check_me.password, e["password"]):
            # 3b) hash form password
            # 3b) comapre to already hashed password from db
                flash("Incorrect password")
                is_valid=False
        else:
        # 3) IF NO EMAIL IN DB
            flash("Not a valid email")
            is_valid=False

        return is_valid




    #######################
    '''CREATE / REGISTER'''
    #######################
    '''VALIDATE'''
    @staticmethod
    def validate_insert(e):
        is_valid=True
        '''name lengths'''
        if len(e["first_name"]) < 3:
        # A) condition
            flash("First name should be greater than 3 characters")
            # B) flash message
            is_valid=False
            # C) change is_valid
        if len(e["last_name"]) < 3:
            flash("Last name should be greater than 3 characters")
            is_valid=False
        '''email'''
        if not EMAIL_REGEX.match(e["email"]):
        # 1) if not email regex from global varials
        # 1) must match data dict from form email 
            flash("Not a valid email")
            is_valid=False
        if e["email"] != e["check_email"]:
        # 2) check if emails match
            flash("Emails are not the same🤷‍♀️")
            is_valid=False
        if User.is_email(e):
        # 3) make sure email is not in use
            flash("Email in use 😞")
            is_valid=False
        '''password'''
        if e["password"] != e["check_pword"]:
        # 1) if both passwords are the same
            flash("Passwords do not match")
            is_valid=False
        if not PASSWORD_REGEX.match(e["password"]):
        # 2) 1 upper, 1 lower, 1 special character, 1 number
            flash("Password must contain: 1 upper, 1 lower, 1 special character, 1 number.")
            is_valid=False
        return is_valid
    

    '''QUERY'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.db).query_db(query,data)
        # returns id
    



    ############
    '''UPDATE'''
    ############
    '''VALIDATE'''
    @staticmethod
    def validate_update(e):
        print(e)
        is_valid=True
        found_email = User.is_email(e)
        found_user = User.select_one(e)

        '''name lengths'''
        if len(e["first_name"]) < 3:
            # A) condition
            flash("First name should be greater than 3 characters")
            # B) flash message
            is_valid=False
            # C) change is_valid
        if len(e["last_name"]) < 3:
            flash("Last name should be greater than 3 characters")
            is_valid=False
        '''email'''
        if found_email and found_email["email"] != found_user.email:
        # 1) if input email is found
        # 1) and inputed email != the email found when searching the data id
            flash("Email taken, and not by you🤷‍♀️")
            is_valid=False
        if not EMAIL_REGEX.match(e["email"]):
        # 1) if it is not email format
            flash("Invalid email")
            is_valid=False
        if e["email"] != e["confirm_email"]:
        # 3) if email's don't match
            flash("Email's are not the same🤷‍♀️")
            is_valid=False
        '''password'''
        if not bcrypt.check_password_hash(found_user.password, e["password"]):
        # 1) check current user
        # 1) hash the password inputted, compare with the select_one(data(id:id)) password
            flash("Present password doesn't match")
            is_valid=False
        if e["new_pass"]:
        # 2) if there is a new password
            if e["new_pass"] != e["new_pass_check"]:
            # 2) check new password matches confirm pass
                flash("Passwords do not match🤷‍♀️")
                is_valid=False
            if not PASSWORD_REGEX.match(e["new_pass"]):
            # 2) check new password format
                flash("Password must contain: 1 upper, 1 lower, 1 special character, 1 number.")
                is_valid=False
        return is_valid

    '''QUERY'''
    @classmethod
    def update(cls, data):
        query="UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    



    ############
    '''DELETE'''
    ############
    @classmethod
    def delete(cls, data):
        query="DELETE FROM users WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query,data)