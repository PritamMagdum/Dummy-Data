def count(a):
    result = 0
    for word in a:
        if word.lower() =="dan brown":
            result+=1 
    return result 
for t in range(int (input())):
    a=list()
    for word in range(int (input())):
        a.append(input())
# Output the variable to STDOUT
print (count(a))
