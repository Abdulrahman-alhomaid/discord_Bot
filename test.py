class Characters:
    def __init__(self , url  , name , point):
        self.url = url
        self.name = name
        self.point = point
        self.des = "this is  the car des"
    def msg(self):
        return self.name +"\n" + self.point

def create():
    characters = {}
    with open("charcters.txt" , "r") as myFile:
        for x , line in enumerate(myFile.readlines()):
            detalis = line.split(",")
            characters.update( {x :  Characters(url=detalis[0] , name = detalis[1] , point=detalis[2]) } )
    return characters



if __name__ == "__main__":
    
    create()