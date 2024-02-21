class Robot:
    def __init__(self,name,built_year):
        self.name=name
        self.built_year=built_year

    def __repr__(self):
        return "Robot('"+self.name+"',"+str(self.built_year)+")"

if __name__=="__main__":
    o1=Robot("Tarkesh",1993)
    print(o1)
# o1_str=str(o1)
# print(o1_str)