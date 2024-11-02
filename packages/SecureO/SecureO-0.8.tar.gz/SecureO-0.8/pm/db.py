from pymongo import MongoClient 
import bcrypt
from bson.objectid import ObjectId

lower_alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
capital_alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
special = ["~", "!", "@", "#", "$", "%", "^", "&", "*"]

class Database:

    def __init__(self) -> None:
        self.db_string = "mongodb+srv://admin:admin@passwordmanager.ya0ygin.mongodb.net/passwords?retryWrites=true&w=majority&appName=PasswordManager"

    def connection(self):
        client = MongoClient(self.db_string)

        db = client["password_db"]
        collection_password = db["passwords"]
        collection_users = db["users"]

        return [collection_password, collection_users]
    
    def get_user(self, name, password):
        collection = self.connection()[1]
        if not name:
            return [{"status": "error", "message": "A Name must be given"}]
        
        user = collection.find_one({ "name": name })
        if not user:
            return [{"status": "error", "message": "Your user name is not registered register it first."}]

        
        userBytes = password.encode('utf-8') 
        result_password_check = bcrypt.checkpw(userBytes, user["password"])
        if not result_password_check:
            return [{"status": "error", "message": "Invalid Credentials"}]
        
        del user["password"]

        return [{"status": "success", "message": "User Logged IN"}, user]
    
    def upload_user_details(self, user_name, user_password):
        collection = self.connection()[1]

        bytes = user_password.encode('utf-8')
        salt = bcrypt.gensalt() 
        hash = bcrypt.hashpw(bytes, salt) 

        document = { "name": user_name, "password": hash }

        user = collection.find_one({ "name": user_name })
        if user:
            return [{ "status": "error", "message": "User Already Exists." }]

        result = collection.insert_one(document=document)

        if result.inserted_id:
            current_user = self.get_user(name=user_name, password=user_password)
            return [{ "status": "success", "message": "User Created." }, current_user]
        else:
            return [{ "status": "error", "message": "Error while creating." }]

    def upload_password(self, password_dest_name, password, strength_status, user_id):
        collection = self.connection()

        document = { "destination": password_dest_name, "password": password, "strength": strength_status, "user": user_id}

        result = collection[0].insert_one(document)

        if result.inserted_id:
            return [{"status": "success", "message": "Password successfully uploaded"}]
        else:
            return [{"status": "error", "message": "Error while uploading."}]
        
    def get_passwords(self, userId):
        collection = self.connection()

        passwords = list(collection[0].find({ "user": userId }))

        for password in passwords:
            del password["user"]

        if not passwords:
            return [{"status": "error", "message": "No Password saved by you!"}]

        return [{"status": "success", "message": "Passwords Found"}, passwords]
    
    def delete_password(self, password_id):
        try:
            collection = self.connection()[0]
            _id = ObjectId(password_id)
            result = collection.find_one_and_delete({ "_id": _id })

            if result:
                return result
            else:
                print("Object not found or already deleted.")
        except Exception as e:
             print("An error occurred:", e)

    def edit_password(self, password_id, new_password, strength_status):
        try:
            collection = self.connection()[0]
            _id = ObjectId(password_id)
            result = collection.find_one_and_update({ "_id": _id }, {
                "$set": {"password": new_password, "strength": strength_status}
            }, {"new": True}, return_document=True)

            if result:
                return result
            else:
                print("Object not found or already deleted.")
        except Exception as e:
             print("An error occurred:", e)