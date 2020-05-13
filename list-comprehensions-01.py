'''
This program is to demonstrate list comprehensions,
Goal : You are given three integers  and  representing the dimensions of a cuboid along with an integer .
      You have to print a list of all possible coordinates given by  on a 3D grid where the sum of  is not equal to .
      Here,
'''
try:
    X = int(input("Enter the value of X : "))
    Y = int(input("Enter the value of Y : "))
    Z = int(input("Enter the value of Z : "))
    N = int(input("Enter the number for comparison : "))
except ValueError as e:
    print("Please Enter only integer and try again ...... Bye for now ....")

'''
for i in range(X+1):
    for j in range(Y+1):
        for k in range(Z+1):
            if i+j+z != N
                print("[", i, ",", j,", ",k, "]")
'''
myList = [(i,j,k) for i in range(X+1) for j in range(Y+1) for k in range(Z+1) if i+j+k != N ]
print(myList)