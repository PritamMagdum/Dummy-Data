import _thread
import time
print("Creating your table please wait @ChatGPT5")
time.sleep(5.0)
def sq(num):
        print("This is square function")
        for n in num:
                time.sleep(0.2)
                print(f"The square of {n} is : ",n*n)

def cb(num):
        print("This is square function")
        for n in num:
                time.sleep(0.2)
                print(f"The square of {n} is : ",n*n*n)

t1 = time.time()
arr = [5,6,8,7,2,6]
sq(arr)
cb(arr)
print("The total time elapsed of this program is : ",time.time()-t1)
