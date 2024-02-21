from functools import reduce
l1=[1,2,3,4,5,6,7,8,9]
l2=[1,4,9,16,25,36,49,64,81]

print(sum(l1))
print(list(map(lambda x:x**2,l1)))
print(list(filter(lambda x: x%2==0 , l1)))
print(reduce(lambda x,y: x+y,l1))

def addinghi(func):
    def inner(name):
        return f"Hi {name}!!"
    return inner

@addinghi
def string1(name):
    return name

print(string1("Tarkesh"))
