#import flask library
from flask_cors import CORS
from flask import Flask,abort,request
from mock_data import catalog
import json
from config import db 
from bson import ObjectId

#create the application "server"
app= Flask("Server")
CORS(app)
 
## App routes
 #Root route
@app.route("/")
def home():
    return "Hello from flask"

#Me route
@app.route("/me")
def about_me():
    return "Arturo Martinez Jr"


################################################################################
################################# API ENDPOINTS ################################
################################# RETURN JSON ################################
################################################################################

#Retrive the catalog 
@app.route("/api/products",methods=['GET'])
def get_catalog():    
    
    products=[]
    cursor=db.products.find({}) # cursor is collection
    
    for prod in cursor:
        prod["_id"] = str(prod["_id"])
        products.append(prod)

    return json.dumps(products)

#Post method test
@app.route("/api/products",methods=['POST'])
def save_catalog():
    prod=request.get_json() # return data (payload) from the request
    
    db.products.insert_one(prod)
                             
    print(prod)
    prod["_id"] = str(prod["_id"])
    return json.dumps(prod)

#Count every product in the catalog
@app.route("/api/products/count",methods=['GET'])
def count_products():

    cursor=db.products.find({}) # cursor is collection 
    c=0
    for item in cursor:
        c+=1
    print(c)
    
    return json.dumps(c)

#Get the sum of all products
@app.route("/api/products/total",methods=['GET'])
def total_products():

    cursor= db.products.find({})
    total=0
    for x in cursor:
        total=x['price']+total  

    print(total)
    return json.dumps(total)

#Get the product by ID <Sending the ID>
@app.route("/api/products/<id>",methods=['GET'])
def id_products(id):
    
    
    prod= db.products.find_one({"_id":ObjectId(id)})

    if not prod:
        return abort(404,"There is no product with such ID")

    prod["_id"]=str(prod["_id"])
    return json.dumps(prod)
    
    

#Return the product with the lowest price
@app.route("/api/products/cheapest")
def cheap_product():
    solution = catalog[0]
    for prod in catalog:
        if prod["price"] < solution["price"]:
            solution = prod

    return json.dumps(solution)

#GET /api/categories

@app.get("/api/categories")
def unique_categories():
    categories = []
    for prod in catalog:
        category = prod["category"]
        if not category in categories:
            categories.append(category)
    
    return json.dumps(categories)



@app.get("/api/catalog/<category>")
def prods_by_pcategory(category):
    
    products=[]
    cursor= db.products.find({"category":category})
    for item in cursor:
        # We HAVE to parse the id to string always fron ObjectId
        item["_id"]=str(item["_id"])
        products.append(item)

    return json.dumps(products)


   
@app.get('/api/someNumbers')
def someNumbers():
    Numbers=[]
    for n in range(1,51):
        Numbers.append(n)

    return json.dumps(Numbers)

##############################################################################
################################# COUPON CODE ENDPOINTS ######################
################################# RETURN JSON ################################
##############################################################################

allCoupons=[]

#GET METHOD TO REGISTER A NEW COUPON
@app.post("/api/couponCode")
def coupons():
    
    coupon=request.get_json()
    coupon["_id"]=1
    allCoupons.append(coupon)
    
    return json.dumps(allCoupons)
    
#POST METHOD TO RETRIEVE THE COUPON LIST
@app.get("/api/couponCode")
def retrieve_couponlist():
    return json.dumps(allCoupons)



# Get all coupons
@app.route("/api/allcoupons", methods=["GET"])
def getall_coupons():

    cursor = db.coupons.find({})
    allDBCoupons=[]
  
    for coup in cursor:
        coup["_id"] = str(coup["_id"])
        allDBCoupons.append(coup)
                 
   
    return json.dumps(allDBCoupons)


#add a new coupon ton the data base
@app.route("/api/allcoupons",methods=["POST"])
def addnew_coupon():
    coup=request.get_json() # return data (payload) from the request
    
    #coupon validation zone

    #validates the coupon code length
    if not "code" in coup:
        return abort(400,"The coupon must contain a code")
    
    #validates the coupon code length 
    if len(coup["code"])<5:
        return abort(400,"The coupon must contain 5 characters")
    
    #validates the coupon code discount no more than 50 or lower than 5 percent
    if coup["discount"]<5 or coup["discount"]>50:
        return abort(400,"Discount not valid")


    ##Adds the coupon to the database
    db.coupons.insert_one(coup)
    coup["_id"] = str(coup["_id"])
     
    return json.dumps(coup)

#Get the COUPON by CODE <Sending the CODE>
@app.route("/api/allcoupons/<code>",methods=['GET'])
def coupon_code(code):

    coup= db.coupons.find_one({"code":code})

    if not coup:
        return abort(404,"There is no coupon with such code")
    
    coup["_id"]=str(coup["_id"])

    return json.dumps(coup)


##############################################################################
################################# users Endpoints ######################
################################# RETURN JSON ################################
##############################################################################

##get all users from the database
@app.route("/api/users", methods=["GET"])
def getall_users():
    
    cursor = db.users.find({})
    dbUsers=[]
    for user in cursor:
        user["_id"] = str(user["_id"])
        dbUsers.append(user)
    
    return json.dumps(dbUsers)


#Get the user by email <Sending the email>
@app.route("/api/users/<email>",methods=['GET'])
def user_email(email):

    user= db.users.find_one({"email":email})

    if not user:
        return abort(404,"There is no coupon with such code")
    
    user["_id"]=str(user["_id"])

    return json.dumps(user)

##register a new user from the database
@app.route("/api/users", methods=["POST"])
def register_users():
    
    user=request.get_json()
    ##validate te user before inserting one user
    if not "name" in user or not "password" in user or not "email" in user:
        abort(400,"Credentials must contain name,password and email")
   
    ##check empty values in the dictionary
    if len(user["name"])<1:
        return "Thats not a valid user name"

    if len(user["password"])<1:
        return "Thats not a valid password"
    
    if len(user["email"])<1:
        return "Thats not a valid email"

    db.users.insert_one(user)
    user["_id"]=str(user["_id"])

    return json.dumps(user)

@app.route("/api/login",methods=["POST"])
def validate_user():
    data=request.get_json() # <= dict with user and password

    if not "name" in data:
        return abort(401,"User name required")
    
    if not "password" in data:
        return abort(401,"Password required")

    user=db.users.find_one({"name":data["name"],"password":data["password"]})

    if not user:
        abort(401," There is no user with that password")    
    
    user.pop('password') #<=== remove the password from the payload
    user["_id"]=str(user["_id"])
    return json.dumps(user) 


#Run the app on debug mode 
app.run(debug=True)
