from tkinter import *

rectWidth = 30      #Ширина квадрата
widthOfField = 21   #Ширина поля
heightOfField = 16  #Высота поля
step = 0            #Номер шага для отрисовки машинок
root = Tk()         #Переменная окна
root.title("Traffic ligths")
c = Canvas(root, width = widthOfField*rectWidth, height = heightOfField*rectWidth, bg = "white")

    #Функции, возвращающие номер столбца и номер строки по номеру ячейки
def getRow(cell): 
    return cell // land.width

def getColumn(cell):
    return cell - land.width * getRow(cell)

    #Функция, рисующая квадрат заданного цвета в заданной ячейке
def drawSquare(column, row, suqareColour):
    c.create_rectangle(column*rectWidth, row*rectWidth, (column+1)*rectWidth, (row+1)*rectWidth, fill = suqareColour)
    return

    #Обработчик события
def onClick(event):
    global step
    if step < 20:
        animateCarsMoving(moveTable.table)
        step += 1

    #Движение машинок
def animateCarsMoving(moveTable):
    for i in range(len(moveTable)):
            currentCell = moveTable[i][step]
            nextCell = moveTable[i][step+1]
            if nextCell != 0:
                drawSquare(getColumn(currentCell), getRow(currentCell), "green")
                drawSquare(getColumn(nextCell), getRow(nextCell), "blue")

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
            drawSquare(self.carColumn, self.carRow, "blue")
            
                
        
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
        self.table[self.currentCar] = [0] * 20 #(car.time + 1)
        self.table[self.currentCar][0] = car.initialPoint
        self.counter = 1
        self.currentRow = car.initialRow
        self.currentColumn = car.initialColumn
        self.currentSpeed = car.speed
        #Пока не достигли конечной точки
        while self.currentColumn != car.destinationColumn or self.currentRow != car.destinationRow: 
            #Если находимся на вертикальном участке
            if land.table[self.currentColumn][self.currentRow][2] == 1:
                #Пока номер текущей строки не станет равным номеру целевой
                while self.currentRow != car.destinationRow:    
                    #Если номер текущей строки больше целевого    
                    if self.currentRow > car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                        self.currentRow -= self.currentSpeed
                    #Если меньше
                    else:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + land.width * self.currentSpeed
                        self.currentRow += self.currentSpeed
                    self.counter += 1
                    #Проверка приближения к перекрестку
                    self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
            #Если находимся на горизонтальном участке
            if land.table[self.currentColumn][self.currentRow][2] == 2:
                #Пока номер текущего столбца не станет равным номеру целевого
                 while self.currentColumn != car.destinationColumn:
                    #Если номер текущего столбца больше целевого
                    if self.currentColumn > car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                        self.currentColumn -= self.currentSpeed
                    #Если меньше
                    else:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                        self.currentColumn += self.currentSpeed
                    self.counter += 1
                    #Проверка приближения к перекрестку
                    self.currentSpeed = checkSpeed(self.currentSpeed, self.currentRow, self.currentColumn)
            #Если находимся на перекрестке
            if land.table[self.currentColumn][self.currentRow][2] == 3:
                #Пока не достигнем целевого столбца ИЛИ целевой строки
                while self.currentColumn != car.destinationColumn or self.currentRow != car.destinationRow:
                    #Если номер текущего столбца больше целевого
                    if self.currentColumn > car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - self.currentSpeed
                        self.currentColumn -= self.currentSpeed
                    #Если меньше
                    if self.currentColumn < car.destinationColumn:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] + self.currentSpeed
                        self.currentColumn += self.currentSpeed
                    #Если номер текущей строки больше номера целевой
                    if self.currentRow > car.destinationRow:
                        self.table[self.currentCar][self.counter] = self.table[self.currentCar][self.counter - 1] - land.width * self.currentSpeed
                        self.currentRow -= self.currentSpeed
                    #Если меньше
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