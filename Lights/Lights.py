from tkinter import *

rectWidth = 30      #������ ��������
widthOfField = 21   #������ ����
heightOfField = 16  #������ ����
step = 0            #����� ���� ��� ��������� �������
root = Tk()         #���������� ����
root.title("Traffic ligths")
c = Canvas(root, width = widthOfField*rectWidth, height = heightOfField*rectWidth, bg = "white")

    #�������, ������������ ����� ������� � ����� ������ �� ������ ������
def getRow(cell): 
    return cell // land.width

def getColumn(cell):
    return cell - land.width * getRow(cell)

    #�������, �������� ������� ��������� ����� � �������� ������
def drawSquare(column, row, suqareColour):
    c.create_rectangle(column*rectWidth, row*rectWidth, (column+1)*rectWidth, (row+1)*rectWidth, fill = suqareColour)
    return

    #���������� �������
def onClick(event):
    global step
    if step < 20:
        animateCarsMoving(moveTable.table)
        step += 1

    #�������� �������
def animateCarsMoving(moveTable):
    for i in range(len(moveTable)):
            currentCell = moveTable[i][step]
            nextCell = moveTable[i][step+1]
            if nextCell != 0:
                drawSquare(getColumn(currentCell), getRow(currentCell), "green")
                drawSquare(getColumn(nextCell), getRow(nextCell), "blue")

def checkSpeed(currentSpeed, currentRow, currentColumn):
    if car.turning:
    #�������� ��������� �� �����������
        if land.table[currentRow][currentColumn + currentSpeed][2] == 3 and currentColumn < car.destinationColumn:
            return 1
        if land.table[currentRow][currentColumn - currentSpeed][2] == 3 and currentColumn > car.destinationColumn:
            return 1
        if land.table[currentRow + currentSpeed][currentColumn][2] == 3 and currentRow < car.destinationRow:
            return 1
        if land.table[currentRow - currentSpeed][currentColumn][2] == 3 and currentRow > car.destinationRow:
            return 1
    #�������� ������ � �����������
        if currentSpeed != car.speed:
            if land.table[currentRow][currentColumn + currentSpeed][2] == 2 and currentColumn > car.destinationColumn:
                return car.speed
            if land.table[currentRow][currentColumn - currentSpeed][2] == 2 and currentColumn < car.destinationColumn:
                return car.speed
            if land.table[currentRow + currentSpeed][currentColumn][2] == 1 and currentRow < car.destinationRow:
                return car.speed
            if land.table[currentRow - currentSpeed][currentColumn][2] == 1 and currentRow > car.destinationRow:
                return car.speed
    return currentSpeed

class Car:
    
    currentPoint = 0
    #�����������
    def __init__(self, initialPoint, destination, speed):
        #��������� �����
        self.initialPoint = initialPoint
        currentPoint = initialPoint
        #����
        self.destination = destination
        #��������
        self.speed = speed
        #����� �� ������ ������������ �� �����������
        self.turning = 0
    
    #������� ���������������� �������� ������������ ������� (���������� �������� � ������� ��������)
    def calculateTime(self):
        self.initialRow = getRow(self.initialPoint)
        self.initialColumn = getColumn(self.initialPoint)
        self.destinationRow = getRow(self.destination)
        self.destinationColumn = getColumn(self.destination)
        self.time = abs(self.initialColumn - self.destinationColumn) + abs(self.initialRow - self.destinationRow)

    #��������, ����� �� ������ ������������
    def ifTurning(self):
        if self.initialRow != self.destinationRow and self.initialColumn != self.destinationColumn:
            self.turning = 1        

class Field:
    #����������� ������� ���� [����� ������, ����� ������ (0 - ���������� ������), 
    #��� ������ (0 - ���������� ������, 1 - ������������ ������, 2 - �������������� ������, 3 - �����������)]
    def __init__(self, width, height):
        numberOfCell = 0 
        self.width = width
        self.height = height
        self.table = [0] * self.width
        for i in range(self.width):
            self.table[i] = [0] * self.height
        for i in range(self.width):
            for j in range(self.height):
                self.table[i][j] = [numberOfCell,0,0]
                c.create_rectangle(i*rectWidth, j*rectWidth, (i+1)*rectWidth, (j+1)*rectWidth, fill = "red")
                numberOfCell += 1
                
    #�������� ����� ������
    def makeRoad(self, firstRow, lastRow, firstColumn, lastColumn):
        self.firstRow = firstRow
        self.lastRow = lastRow
        self.firstColumn = firstColumn
        self.lastColumn = lastColumn
        for i in range(self.firstRow, self.lastRow + 1):
            for j in range(self.height):
                self.table[i][j][2] = 1
                drawSquare(i, j, "green")
        for j in range(self.firstColumn, self.lastColumn + 1):
            for i in range(self.width):
                self.table[i][j][2] += 2
                drawSquare(i, j, "green")
    #���������� ����� �� ������
    def placeCars(self, *cars):
        self.numberOfCar = 1
        self.cars = cars
        for i in range(len(self.cars[0])):
            self.carRow = getRow(self.cars[0][i].initialPoint)
            self.carColumn = getColumn(self.cars[0][i].initialPoint)
            self.table[self.carColumn][self.carRow][1] = self.numberOfCar
            self.numberOfCar += 1
            drawSquare(self.carColumn, self.carRow, "blue")
            
                
        
class MoveTable:
    #�������� ������� ��������
    def __init__(self, initialTime, numberOfCars):
        self.numberOfCars = numberOfCars
        self.currentCar = 0
        self.table = [0] * self.numberOfCars
        self.initialTime = initialTime
        self.efficiency = 0
    #���������� ������ � ������� � ������ �� �������� ��� ����� ����������� � ������� ��������
    def addCar(self, car):
        self.car = car
        self.table[self.currentCar] = [0] * 20 #(car.time + 1)
        self.table[self.currentCar][0] = car.initialPoint
        self.counter = 1
        self.currentRow = car.initialRow
        self.currentColumn = car.initialColumn
        self.currentSpeed = car.speed
        #���� �� �������� �������� �����
        while self.currentColumn != car.destinationColumn or self.currentRow != car.destinationRow: 
            #���� ��������� �� ������������ �������
            if land.table[self.currentColumn][self.currentRow][2] == 1:
                #���� ����� ������� ������ �� ������ ������ ������ �������
                while self.currentRow != car.destinationRow:    
                    #���� ����� ������� ������ ������ ��������    
                    if self.currentRow > car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                        self.currentRow -= self.currentSpeed
                    #���� ������
                    else:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + land.width * self.currentSpeed
                        self.currentRow += self.currentSpeed
                    self.counter += 1
                    #�������� ����������� � �����������
                    self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
            #���� ��������� �� �������������� �������
            if land.table[self.currentColumn][self.currentRow][2] == 2:
                #���� ����� �������� ������� �� ������ ������ ������ ��������
                 while self.currentColumn != car.destinationColumn:
                    #���� ����� �������� ������� ������ ��������
                    if self.currentColumn > car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                        self.currentColumn -= self.currentSpeed
                    #���� ������
                    else:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                        self.currentColumn += self.currentSpeed
                    self.counter += 1
                    #�������� ����������� � �����������
                    self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
            #���� ��������� �� �����������
            if land.table[self.currentColumn][self.currentRow][2] == 3:
                #���� �� ��������� �������� ������� ��� ������� ������
                while self.currentColumn != car.destinationColumn or self.currentRow != car.destinationRow:
                    #���� ����� �������� ������� ������ ��������
                    if self.currentColumn > car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                        self.currentColumn -= self.currentSpeed
                    #���� ������
                    if self.currentColumn < car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                        self.currentColumn += self.currentSpeed
                    #���� ����� ������� ������ ������ ������ �������
                    if self.currentRow > car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                        self.currentRow -= self.currentSpeed
                    #���� ������
                    if self.currentRow < car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + land.width * self.currentSpeed
                        self.currentRow += self.currentSpeed
                    self.counter += 1
        self.currentCar += 1

land = Field(widthOfField, heightOfField)
land.makeRoad(5, 7, 5, 7)


cars = list()
cars.append(Car(149, 90, 1))
cars.append(Car(279, 127, 2))
cars.append(Car(144, 126, 3))

land.placeCars(cars)

times = list()
for car in cars:
    car.calculateTime()
    times.append(car.time)
    car.ifTurning()
initialTime = max(times)

moveTable = MoveTable(initialTime, len(cars))
for car in cars:
    moveTable.addCar(car)
c.pack()
root.bind('<Button-1>', onClick)
root.mainloop()