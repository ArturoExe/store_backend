from mock_data import catalog


def lower_than(price):
    c=0
    for item in catalog:
        if item["price"]<price:
            c+=1
    print(c)

def greater_than(price):
    c=0
    for item in catalog:
        if item["price"]>price:
            c+=1
    print(c)


lower_than(100)
greater_than(90)