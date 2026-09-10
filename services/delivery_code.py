"""delivery confirmation code utilities"""

#creates random numbers
import random


def generate_delivery_code():  #generates random 6-digit number 
    return f"{random.randint(100000,999999)}" 


#function with two parameters
def verify_delivery_code(txn, code):
    #checks whether delivery code exists
    if not txn.delivery_code:
        return False
    #del and stored code is converted to string plus comparison
    return str(code).strip() == str(txn.delivery_code)
