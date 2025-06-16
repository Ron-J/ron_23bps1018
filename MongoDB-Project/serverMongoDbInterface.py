from pymongo import *
CONNECTION_STRING="mongodb://localhost:27017/project"
client=MongoClient(CONNECTION_STRING)
db=client['project']
users=db['users']
ratings=db['rating']

#Accepting data from users

def inputdata(name, typep, typec, time, sideeffects, location):
    sev=typep*typec    
    userRating=1.5+sev-(int(time)+int(sideeffects))/sev
    print(userRating)
    oldRating=ratings.find_one({"name":name},{"rating":1,"numReviews":1})
    if(oldRating):
        updRating=(oldRating['rating']*oldRating['numReviews']+userRating)/(oldRating['numReviews']+1)
        ratings.update_one({"name":name},{ '$set' :{ 'rating': updRating, 'numReviews': (oldRating['numReviews']+1)} })
    else:
        ratings.insert_one({"name": name, "rating": userRating, "numReviews":1, "location": location})            
def readdata(x, filterValue): 
        #1.Show All 2. Highest Rated 3. Search Hospital 4. Search with Location
        if x==1:
            return list(ratings.find())
        elif x==2:
            return list(ratings.find().sort([('rating',-1)]).limit(1))
        elif x==3:
            return list(ratings.find({'name':filterValue}))
        elif x==4:
            return list(ratings.find({'location':filterValue}))
        return []

def addUser(username, password):
    users.insert_one({'username':username, 'password':password})

def deleteRecord(name):
    ratings.delete_one({'name': name})
def verifyUser(username, password):
    if(list(users.find({"username": username, "password":password}))):
        return True
    else:
        return False