import sys
import ml

def myTest(param1, param2):
    result = f"Function myTest was called with {param1} and {param2}!"
    return result

def anotherFunction(param1, param2):
    result = f"Another function was called with {param1} and {param2}!"    
    return result
    
def linearReg():
    result = ml.linearReg()
    print(result)       

def simpleFunction():
    print("simpleFunction was called!")  # This function prints directly instead of returning

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "run-mytest":
        param1 = sys.argv[2]
        param2 = sys.argv[3]
        result = myTest(param1, param2)
        print(result)
    elif command == "run-another":
        param1 = sys.argv[2]
        param2 = sys.argv[3]
        result = anotherFunction(param1, param2)
        print(result)
    elif command == "run-simple":
        simpleFunction()
    elif command == "linearReg":
        linearReg()
