def younger_person():
    ages = [77,42,32,50,56,14,78,30,51,89,12,38,67,10]

    lower=ages[0]

    for x in ages:
        if lower>x:
            lower=x
    print(lower)
    

def stats():

    data = [12,-1,123,345,412,4.55,123,23.4,123,4587,-129,94,956,14565,32, 0.001, 123]
    sum=0
    nsum=0
    gfive=0

    for x in data:
        sum=sum+x


    for x in data:
        if x<0:
            nsum+=x
    
    for x in data:
        if x>500:
            gfive+=1

            


    print(f"Total items in the array: {len(data)}\n")
    print(f"The sum of all the items is equal to : {sum} \n")
    print(f"The sum of all the NEGTAIVE items is equal to : {nsum} \n")
    print(f"Total items OVER 500 in the array: {gfive}\n")


def print_some_numbers():
    
    for x in range(10,110,10):
        print(x)




# print("test")
# younger_person()
stats()
print_some_numbers()