from flask_login import UserMixin

# Define the User class
# User class is responsible to store users imformation temporarily after the user logs in it gets it's imformation from the user loader function and it stores the detail so you can use current_user attribute of flask login 

class User(UserMixin): 
        def __init__(self, id, username, password):
            self.id = id
            self.username = username
            self.password = password
        
        #Basically if the following username and passwords are given following items returns following value

        def get_id(self):
            return str(self.id)
    
        def is_authenticated(self):
            return True

        def is_active(self):
            return True

        def is_anonymous(self):
            return False