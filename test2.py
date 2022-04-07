def test_dic():
    me={
        "first":"Arturo",
        "last":"Martinez",
        "age":21,
        "hobbies":[],
        "address":{
            "street":"main 101",
            "city":"San Ysidro",
        }
    }

    # Best practice 
    address=me["address"]
    print(address["street"])

    # In single line 
    # print(me["address"]["street"])

    #Add new keys
    me["color"]="red"

    #Modify existing keys
    me["age"]=22

    #Check if a key exist
    if "age" in me:
        print("Age already exist in this dictionary") 
        print(me["age"],me["color"])
    



print("----- Dictionary Test -----")
test_dic()

