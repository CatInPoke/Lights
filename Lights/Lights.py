from tkinter import *

rectWidth = 30      #Ширина одного квадрата
widthOfField = 21   #Ширина поля (в квадратах)
heightOfField = 16  #Высота поля
step = 0            #Номер текущего момента времени
root = Tk()         #Переменная окна
root.title("Traffic ligths")
c = Canvas(root, width = widthOfField*rectWidth, height = heightOfField*rectWidth, bg = "white")

    #Функция, возвращающая строку ячейки по ее номеру
def getRow(cell): 
    return cell // land.width
    
    #Функция, возвращающая столбец ячейки по ее номеру
def getColumn(cell):
    return cell - land.width * getRow(cell)

    #Функция, рисующая квадраты
def drawSquare(column, row, suqareColour, _tag = ''):
    c.create_rectangle(column*rectWidth, row*rectWidth, (column+1)*rectWidth, (row+1)*rectWidth, fill = suqareColour, tag = _tag)
    return

    #Обработчик нажатия
def onClick(event):
    global step
    if step < 20:
        animateCarsMoving(moveTable.table)
        step += 1

    #Функция, отрисовывающая движение машин
def animateCarsMoving(moveTable):
    for i in range(len(moveTable)):
            currentCell = moveTable[i][step]
            nextCell = moveTable[i][step+1]
            if nextCell != 0:
                c.move('car' + str(i), (getColumn(nextCell) - getColumn(currentCell)) * rectWidth, (getRow(nextCell) - getRow(currentCell)) * rectWidth)
            else:
                c.delete('car' + str(i))

def checkSpeed(currentSpeed, currentRow, currentColumn):
    if car.turning:
    #Проверка попадания на перекресток
        if land.table[currentRow][currentColumn + currentSpeed][2] == 3 and currentColumn < car.destinationColumn:
            return 1
        if land.table[currentRow][currentColumn - currentSpeed][2] == 3 and currentColumn > car.destinationColumn:
            return 1
        if land.table[currentRow + currentSpeed][currentColumn][2] == 3 and currentRow < car.destinationRow:
            return 1
        if land.table[currentRow - currentSpeed][currentColumn][2] == 3 and currentRow > car.destinationRow:
            return 1
    #Проверка выхода с перекрестка
        if currentSpeed != car.speed:
            if land.table[currentColumn - currentSpeed][currentRow][2] == 2 and currentColumn > car.destinationColumn:
                return car.speed
            if land.table[currentColumn + currentSpeed][currentRow][2] == 2 and currentColumn < car.destinationColumn:
                return car.speed
            if land.table[currentColumn][currentRow + currentSpeed][2] == 1 and currentRow < car.destinationRow:
                return car.speed
            if land.table[currentColumn][currentRow - currentSpeed][2] == 1 and currentRow > car.destinationRow:
                return car.speed
    return currentSpeed

class Car:
    
    currentPoint = 0
    #Конструктор
    def __init__(self, initialPoint, destination, speed):
        #Начальная точка
        self.initialPoint = initialPoint
        currentPoint = initialPoint
        #Цель
        self.destination = destination
        #Скорость
        self.speed = speed
        #Будет ли машина поворачивать на перекрестке
        self.turning = 0
        #Повернула ли машина уже
        self.turned = 0
        #Достигнута ли целевая ячейка
        self.achieved = 0
    
    #Функция приблизительного подсчета необходимого времени (количество столбцов в таблице движения)
    def calculateTime(self):
        self.initialRow = getRow(self.initialPoint)
        self.initialColumn = getColumn(self.initialPoint)
        self.destinationRow = getRow(self.destination)
        self.destinationColumn = getColumn(self.destination)
        self.time = abs(self.initialColumn - self.destinationColumn) + abs(self.initialRow - self.destinationRow)

    #Проверка, будет ли машина поворачивать
    def ifTurning(self):
        if self.initialRow != self.destinationRow and self.initialColumn != self.destinationColumn:
            self.turning = 1

class Field:
    #Конструктор таблицы поля [номер ячейки, номер машины (0 - отсутствие машины), 
    #тип дороги (0 - отсутствие дороги, 1 - вертикальная дорога, 2 - горизонтальная дорога, 3 - перекресток)]
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
                
    #Создание ячеек дороги
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
    #Размещение машин на дороге
    def placeCars(self, *cars):
        self.numberOfCar = 1
        self.cars = cars
        for i in range(len(self.cars[0])):
            self.carRow = getRow(self.cars[0][i].initialPoint)
            self.carColumn = getColumn(self.cars[0][i].initialPoint)
            self.table[self.carColumn][self.carRow][1] = self.numberOfCar
            self.numberOfCar += 1
            drawSquare(self.carColumn, self.carRow, "blue", 'car' + str(i))
            
        
class MoveTable:
    #Создание таблицы движения
    def __init__(self, initialTime, numberOfCars):
        self.numberOfCars = numberOfCars
        self.currentCar = 0
        self.table = [0] * self.numberOfCars
        self.initialTime = initialTime
        self.efficiency = 0
    #Добавление машины в таблицу и расчет ее движения без учета пересечений с другими машинами
    def addCar(self, car):
        self.car = car
        self.table[self.currentCar] = [0] * 20 #(self.car.time + 1)
        self.table[self.currentCar][0] = car.initialPoint
        self.counter = 1
        self.currentRow = car.initialRow
        self.currentColumn = car.initialColumn
        self.currentSpeed = car.speed
        #Пока не достигли края поля
        while self.currentColumn > 1 and self.currentRow > 1 and self.currentColumn < widthOfField and self.currentRow < heightOfField: #self.currentColumn != car.destinationColumn or self.currentRow != car.destinationRow: 
            if self.currentColumn == self.car.destinationColumn and self.currentRow == self.car.destinationRow:
                self.car.achieved = 1
            #Если находимся на вертикальном участке
            if land.table[self.currentColumn][self.currentRow][2] == 1:
                if self.currentRow > self.car.destinationRow or self.car.achieved:
                    if self.car.turned:
                        while self.currentRow > 0:    
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                            self.currentRow -= self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                    else:
                        while self.currentRow != self.car.destinationRow:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                            self.currentRow -= self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                else:
                    if self.car.turned:
                        while self.currentRow < heightOfField:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + land.width * self.currentSpeed
                            self.currentRow += self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                    else:
                        while self.currentRow != self.car.destinationRow:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + land.width * self.currentSpeed
                            self.currentRow += self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                #Проверка приближения к перекрестку
                self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
            #Если находимся на горизонтальном участке
            if land.table[self.currentColumn][self.currentRow][2] == 2:
                if self.currentColumn > self.car.destinationColumn or self.car.achieved:
                    if self.car.turned:
                        while self.currentColumn > 0:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                            self.currentColumn -= self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                    else:
                        while self.currentColumn != self.car.destinationColumn:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                            self.currentColumn -= self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                else:
                    if self.car.turned:
                        while self.currentColumn < widthOfField:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                            self.currentColumn += self.currentSpeed
                            self.counter += 1
                    else:
                        while self.currentColumn != self.car.destinationColumn:
                            self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                            self.currentColumn += self.currentSpeed
                            self.counter += 1
                            self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                
            #Если находимся на перекрестке
            if land.table[self.currentColumn][self.currentRow][2] == 3:
                #Пока не достигнем целевого столбца ИЛИ целевой строки
                while self.currentColumn != self.car.destinationColumn or self.currentRow != self.car.destinationRow:
                    #Если номер текущего столбца больше целевого
                    if self.currentColumn > self.car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                        self.currentColumn -= self.currentSpeed
                    #Если меньше
                    if self.currentColumn < self.car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                        self.currentColumn += self.currentSpeed
                    #Если номер текущей строки больше номера целевой
                    if self.currentRow > self.car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                        self.currentRow -= self.currentSpeed
                    #Если меньше
                    if self.currentRow < self.car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + land.width * self.currentSpeed
                        self.currentRow += self.currentSpeed
                    self.counter += 1
                    self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
                self.car.turned = 1
        self.currentCar += 1

        def optmizeTable(self, table):
            self.table = table
            resultTable = [0] * len(self.table)
            for i in range(len(self.table)):
                resultTable = [0] * 20
            
        
        def isOptimal(self, table):
            self.table = table                        
            for i in range(len(self.table) - 1):
                for j in range(i + 1, len(self.table)):
                    for k in range(len(self.table[i])):
                        if self.table[i][k] == self.table[j][k]:
                            return False
            return True

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