import itertools
import collections
import sys
import math

class Molecule(object):     # класс молекулы
    def __init__(self, name : int, x : float, y : float, z : float):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '({}, {}, {}, {})'.format(self.name, self.x, self.y, self.z)

    def __repr__(self):
        return '({}, {}, {}, {})'.format(self.name, self.x, self.y, self.z)

def distance(m1 : Molecule, m2 : Molecule):     # вычисление расстояния
    return math.sqrt(math.pow(float(m1.x) - float(m2.x), 2) \
                   + math.pow(float(m1.y) - float(m2.y), 2) \
                   + math.pow(float(m1.z) - float(m2.z), 2))

def getComboList(array : list, count : int):    # получения списка комбинаций молекул
    temp = []
    for j in itertools.combinations(array, count):
        for i in itertools.permutations(j):
            temp.append(i)
    return temp

def readFromFile(path : str):   # чтение из файла
    vec = []
    try:
        with open(path, "r") as file:
            data = file.readlines()[7:]
            for line in data:
                temp = line.split()
                vec.append(Molecule(temp[0], temp[1], temp[2], temp[3]))  
    except IOError:
        print("An IOError has occurred! - ", path)
    return vec

def isomorphic(vec1 : list, vec2 : list, isPercent : bool, bias : float):   # поиск изоморфных структур
    result = []
    first = {}
    second = {}

    for el in vec1:     # список молекул в большой структуре
        if el.name in first:
            first[el.name] += 1
        else:
            first[el.name] = 1  
    
    for el in vec2:     # список молекул в маленькой структуре
        if el.name in second:
            second[el.name] += 1
        else:
            second[el.name] = 1

    for key in second:  # проверка на возможность сравнения
        if key in first:
            if first[key] < second[key]:
                print("Not enough number of molecules in big struct")
                print(first[key], "<", second[key], "; molecules -", key)
                return result
        else:
            print("Missing molecule", key, "in big struct")
            return result
        
    vec2.sort(key = lambda x : x.name)
    second = collections.OrderedDict(sorted(second.items()))

    dist2 = []      # список с расстояниями малой структуры
    for el in itertools.combinations(vec2, 2):
        dist2.append(distance(el[0], el[1]))

    array = []  # создания массива с возможными комбинациями сравнения
    for name in second:
        temp = []
        for el in vec1:
            if el.name == name:
                temp.append(el)
        array.append(getComboList(temp, second[name]))

#    cp = []
#    try:    # все комбинации сравнения
#        cp = list(itertools.product(*array))  
#    except:
#        pass

    for struct in itertools.product(*array):
        sortStruct = list(itertools.chain.from_iterable(struct))
        correct = True
        i = 0
        for elements in itertools.combinations(sortStruct, 2):  # сравнения расстояния
            if abs(distance(elements[0], elements[1]) - dist2[i]) \
                    > (bias * dist2[i] / 100 if isPercent else bias):
                correct = False
                break
            i += 1
        if correct: # если подходит, то проверяем на уникальность
            for res in result: 
                for el in sortStruct:
                    if el in res:
                        correct = False
                    else:
                        correct = True
                        break
                if not correct:
                    break
            if correct: # добавление в список результата
                result.append(sortStruct)          
    return result

if __name__ == "__main__":

    path1 = ""
    path2 = ""
    isPercent = False
    bias = 0.01
    # ввод данных
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg.startswith("big="):
                path1 = arg[4:]
            if arg.startswith("small="):
                path2 = arg[6:]
            if arg.startswith("percent="):
                if arg[8:] == "y":
                    isPercent = True
                else:
                    isPercent = False
            if arg.startswith("bias="):
                bias = float(arg[5:])
    else:
        path1 = input("First struct: ")
        path2 = input("Second struct: ")
        isPercentAnswer = input("bias in percent (y/n)?")
        if isPercentAnswer == "y":
            isPercent = True
        else:
            isPercent = False
        bias = float(input("bias:"))

    vec1 = readFromFile(path1)
    vec2 = readFromFile(path2)

    res = isomorphic(vec1, vec2, isPercent, bias)
    print("Result:")    # вывод результата
    for el in res:
        print(el)
    print("Found", len(res), "elements")