import sys
from random import randint


#Populates array with zeroes
def populate(x):
    w, h = x,x
    Matrix = [[0 for i in range(w)] for j in range(h)] 
    return Matrix

#Populates array with Xs
def populateDis(x):
    w, h = x,x
    Matrix = [['x' for i in range(w)] for j in range(h)] 
    return Matrix

#Plants bombs
def plantBomb(field):
    i = randint(1,9)
    j = randint(1,9)
    if field[i][j] == 0:
        field[i][j] = -1
        return field
    else:
        plantBomb(field)


#left         [i-1][j]
#top left     [i-1][j-1]
#bottom left [i-1][j+1]


#top          [i][j-1]
#bottom       [i][j+1]

#top right    [i+1][j-1]
#right        [i+1][j]
#bottom right [i+1][j+1]

#Enumerates cells around the bombs

def enumField(field):
    for i in range(1,10):
        for j in range(1,10):
            if field[i][j] == -1:  
                #top
                if field[i-1][j] != -1:
                    field[i-1][j] += 1
                
                #top left
                if field[i-1][j-1] != -1:
                    field[i-1][j-1] += 1

                #top right
                if field[i-1][j+1] != -1:
                    field[i-1][j+1] += 1

                #bottom left
                if field[i+1][j-1] != -1:
                    field[i+1][j-1] += 1
                
                #left
                if field[i][j-1] != -1:
                    field[i][j-1] += 1


                #rigt
                if field[i][j+1] != -1:
                    field[i][j+1] += 1

                #bottom
                if field[i+1][j] != -1:
                    field[i+1][j] += 1

                #bottom right 
                if field[i+1][j+1] != -1:
                    field[i+1][j+1] += 1
    return field


#Reveals cells 

def reveal(dis,field,i,j):
    if field[i][j] == 0:
        dis[i][j] = field[i][j]
        
        #top
        if  i > 1 and dis[i-1][j] == 'x':
            dis[i-1][j] = field[i-1][j]
            reveal(dis,field,i-1,j)
        #top left
        if  i > 1 and j > 1 and dis[i-1][j-1] == 'x':
            dis[i-1][j-1] = field[i-1][j-1]
            reveal(dis,field,i-1,j-1)
        #top right
        if i > 1 and j < 9 and dis[i-1][j+1] == 'x':
            dis[i-1][j+1] = field[i-1][j+1]
            reveal(dis,field,i-1,j+1)
        
        #left
        if j >1 and dis[i][j-1] == 'x':
            dis[i][j-1] = field[i][j-1]
            reveal(dis,field,i,j-1)

        #rigt
        if j < 9 and dis[i][j+1] == 'x':
            dis[i][j+1]  = field[i][j+1]
            reveal(dis,field,i,j+1)

        #bottom
        if i < 9 and dis[i+1][j] == 'x':
            dis[i+1][j] = field[i+1][j]
            reveal(dis,field,i+1,j)
        #bottom right 
        if i < 9 and j < 9 and dis[i+1][j+1] == 'x':
            dis[i+1][j+1] = field[i+1][j+1]
            reveal(dis,field,i+1,j+1)
        
        #bottom left 
        if i < 9 and j >1 and dis[i+1][j-1] == 'x':
            dis[i+1][j-1] = field[i+1][j-1]
            reveal(dis,field,i+1,j-1)
    elif field[i][j] > 0:
           dis[i][j] = field[i][j]
    
    return dis
    

#Prints tables

def printTables():
    # for i in range(1,len(field)-1):
    #     for j in range(1,len(field)-1):
    #         print("{:^3}".format(field[i][j]),end = '')
    #     print ("")

    # print ("====================================")

    for i in range(1,len(field)-1):
        for j in range(1,len(field)-1):
            sys.stdout.write("{:^3}".format(dis[i][j]))
        sys.stdout.write ("\n")
    

if __name__ == '__main__':
    

    field = populate(11)



    for i in range(5):
        plantBomb(field)


    field = enumField(field)

    dis = populateDis(10)
    undis = dis
    for i in range(1,len(field)-1):
        for j in range(1,len(field)-1):
            dis[i][j] = 'x'

    printTables()



    while True:
        
        

        try:
            r = input("Enter a row number or 'm' to mark a cell : ")
            r = int(r)
            c = input("Enter column : ")
            c = int(c)
            
            if field[r][c] == -1 :
                print ("******************************")
                print ("**********  BOOM  ************")
                print ("******************************")
                print ("##YOU HAVE TREADED ON A BOMB##") 
                break

            
            undis = reveal(dis,field,r,c)
            count = 0
            for n in range(1,len(undis)):
                for m in range(1,len(undis)):
                    if undis[n][m] == 'x':
                        count += 1
                    if undis[n][m] == 'm':
                        count += 1

            
            
            

            print(count)

            printTables()

            if count == 5 :
                print ("******************************")
                print ("******   YOU WON !!!  ********")
                print ("******************************")
                for i in range(1,len(undis)):
                    for j in range(1,len(undis)):
                        if undis[i][j] == 'x' or undis[i][j] == 'm':
                            undis[i][j] = 'B'
                printTables()
                break
        except ValueError:
            if (r == 'm'):
                r = input("Enter a row for marking : ")
                c = input("Enter a column for marking : ")
                
                undis[int(r)][int(c)] = 'm'
                printTables()

        
        

        #print (field[r][c])
        #print(undis)