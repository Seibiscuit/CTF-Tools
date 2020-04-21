"""
Author: Austin Caddell
e-mail: austincaddell.business@gmail.com
forked code from: https://github.com/mzfr/ctf-writeups/blob/master/picoCTF-2018/Cryptography/rsa-madlibs/calculate-d.py
"""

def egcd(e, phi):
    """
    Euclid's Extended GCD algorithm.
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    """

    if e == 0:
        return phi, 0, 1
    else:
        g, y, x = egcd(phi % e, e)

    return g, x - (phi // e) * y, y



def modinv(e, phi):
    """
    Modular inverse using the e-GCD algorithm.
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Computing_multiplicative_inverses_in_modular_structures
    """

    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % phi
    
    
    
def getInfo(varDict):
    """
    Runs through the different variables that come in challenges.
    """
    
    print("Paste values into prompt or enter q to reset or quit\n\
          If value not given then enter 0.\n\nValues in parenthesis\n\
          will be passed if user presses enter to go to the next line\n")

    case = []

    for key, value in varDict.items():
        temp = input(f"What is the value of {key}? ({value})\n")
        if temp == "q": break
        elif temp != "" and temp != "0": 
            varDict[key] = temp
            case.append("1")
        else:
            case.append("0")
   
    return varDict, case


                
def case_solver(varDict,case):
    """
    Tries to solve what it can with what variables it has based on case
    """
    # case = 8 numbers based on if they have a value = p,q,n,phi,e,d,c,m == 11010010
    # 1 is on 0 is off - Basically a bunch of booleans saved as an int that looks like binary
    
    i = 0
    while True:
        intCase = int("".join(case))     
        if str(intCase)[:3] == "110": 
            varDict["n"] = findN(varDict)
            intCase += 100000
        elif str(intCase)[:4] == "1110":
            varDict["phi"] = findPhi(varDict)
            intCase += 10000
        elif str(intCase)[:3] == "101":
            varDict["q"] = findQ(varDict)
            intCase += 1000000
        elif str(intCase)[:3] == "011":
            varDict["p"] = findP(varDict)
            intCase += 10000000
        elif str(intCase)[4] == "0":
            varDict["e"] = findE(varDict)
            intCase += 1000
        elif str(intCase)[3] == "1" and str(intCase)[4:6] == "10":
            varDict["d"] = findD(varDict)
            intCase += 100
        elif str(intCase)[2] == "1" and str(intCase)[5:7] == "11":
            varDict["m"] = findM(varDict)
            varDict["message"] = printMessage(varDict)
            intCase += 1
#        elif str(intCase)[7] == "1":
#            printMessage(varDict)
        else: break
        case = list(str(intCase))
        i+=1
        if i == 10: break
    return varDict
    

            
def findN(varDict): return str(int(varDict['p']) * int(varDict['q']))
"""
Takes in P and Q and returns N
"""



def findPhi(varDict): return str((int(varDict['p']) - 1) * (int(varDict['q']) - 1))
"""
Takes in P and Q and returns PHI
"""



def findQ(varDict): return str(int(varDict['n']) // int(varDict['p']))
"""
Takes in N and P and returns Q
"""



def findP(varDict): return str(int(varDict['n']) // int(varDict['q']))
"""
Takes in N and Q and returns P
"""



def findE(varDict):
    """
    Takes in the varDict to assign the list to the E dictionary listing.
    """
    #the list is cited as being the fastest E values to compute because they are 2^n + 1
    #citation is here https://www.di-mgt.com.au/rsa_alg.html
    print("E was not found.\n\
     ...using the fastest E values")
    varDict["e"] = [3,5,17,257,65537]
    


    
def findD(varDict):return str(modinv(int(varDict["e"]),int(varDict["phi"])))
"""
takes in PHI and E and returns D
"""
    
    

def findM(varDict):
#    import pdb; pdb.set_trace()
    return str(pow(int(varDict["c"]),int(varDict["d"]),int(varDict["n"])))
"""
Takes C, D, and N and creates the plaintext Decimal of M
"""


    
def printMessage(varDict): return(bytearray.fromhex(hex(int(varDict["m"])).strip("0x")).decode())
"""
Takes a given plaintext decimal and returns ASCII
"""    



def output(varDict):
    print(f"p: {varDict['p']}\n\
                q: {varDict['q']}\n\
                n: {varDict['n']}\n\
                phi: {varDict['phi']}\n\
                e: {varDict['e']}\n\
                d: {varDict['d']}\n\
                c: {varDict['c']}\n\
                m: {varDict['m']}\n\
                message: {varDict['message']}\n")

    

def main():
    varDict = {"p":"0","q":"0","n":"0","phi":"0","e":"0","d":"0","c":"0","m":"0"}
    while True:
        varDict, case = getInfo(varDict)
        varDict = case_solver(varDict,case)
        output(varDict)
        userInput = input("Type quit to exit or press Enter to continue\n")
        if userInput == "quit":
            break


if __name__ == '__main__':
    main()

