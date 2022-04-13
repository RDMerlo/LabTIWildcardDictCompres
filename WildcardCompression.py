# -*- coding: utf-8 -*-
# Подключаемые модули

import math

# Константы

nMethodLZ77 = 0 # Метод LZ77
tMethodLZ77 = 'Метод LZ77'
nMethodLZSS = 1 # Метод LZSS
tMethodLZSS = 'Метод LZSS'
# Список методов
listMethod = (tMethodLZ77, tMethodLZSS)

sizeSymbol = 8 # Размер 1-го символ в битах

# Функции и классы
# Используем 36-ричную систему счисления для смещения и длины строки
def str36(num36):
    if (num36 >= 0) and (num36 <= 9):
        strNum = str(num36)
    elif (num36 >= 10) and (num36 <= 36):
        strNum = chr(0x0041 + num36 - 10) # ord(’A’) = 0x0041
    else:
        strNum = 'Error'
    return strNum

def int36(num36):
    if (num36 >= '0') and (num36 <= '9'):
        intNum = int(num36)
    elif (num36 >= 'A') and (num36 <= 'Z'):
        intNum = ord(num36) - 0x0041 + 10 # ord(’A’) = 0x0041
    else:
        intNum = -1
    return intNum

# Создание LZ77 кода
def makeLZ77(d, ld, b, lb):
    print('1')
    i = d.find(b[0])
    # Первый символ буфера в словаре не найден
    # ИЛИ это последний символ буфера
    if (i == -1) or (0 == len(b) - 1):
        i = 0 # Смещение
        n = 0 # Длина подстроки
        Code = str36(i) + str36(n) + b[n] # Код LZ77
        # Первый символ буфера в словаре найден, смещение - i
    else:
        n = 1 # Длина подстроки
        Code = ''
        # ...
        # ...
        # ... # Код LZ77
    sizeCode = ld + lb + sizeSymbol # Размер 1-го LZ77 кода в битах
    # Сдвиг курсора, код и размер кода
    print('2')
    print('n = ', n+1,  ' sizeCode = ', sizeCode)
    return n+1, Code, sizeCode

# Декодирование LZ77 кода
def makeDeLZ77(d, c):
    # Одиночный символ
    if c[1] == '0':
        n = 0
        deCode = c[2] # Значение кода
        # Подстрока из словаря И символ
    else:
        i = int36(c[0]) # Смещение
        n = int36(c[1]) # Длина
        deCode = d[i:i+n] + c[2] # Значение кода
    d = d[n+1:] + deCode # Сдвиг словаря
    n = 3 # Сдвиг курсора по сжатому сообщению
    # Сдвиг курсора, код, его значение и словарь
    return n, c, deCode, d

# Создание LZSS кода
def makeLZSS(d, ld, b, lb):
    i = d.find(b[0])
    # Первый символ буфера в словаре не найден
    if (i == -1):
        n = 1 # Сдвиг курсора
        Code = '0' + b[0] # Код LZSS
        sizeCode = 1 + sizeSymbol # Размер 1-го LZSS кода в битах
    # Первый символ буфера в словаре найден, смещение - i
    else:
        #TODO: Сделать
        n = 1 # Длина подстроки И сдвиг курсора
        Code = 'hello world'
        # ...
        # ...
        # ... # Код LZSS
        sizeCode = 1 + ld + lb # Размер 1-го LZSS кода в битах
    # Сдвиг курсора, код и размер кода
    return n, Code, sizeCode

# Декодирование LZSS кода
def makeDeLZSS(d, c):
    # Одиночный символ
    if c[0] == '0':
        n = 1
        deCode = c[1] # Значение кода
        d = d[n:] + deCode # Сдвиг словаря
        n = 2 # Сдвиг курсора по сжатому сообщению
    # Подстрока из словаря
    else:
        i = int36(c[1]) # Смещение
        n = int36(c[2]) # Длина
        deCode = d[i:i+n] # Значение кода
        d = d[n:] + deCode # Сдвиг словаря
        n = 3 # Сдвиг курсора по сжатому сообщению
    c = c[0:n]
    # Сдвиг курсора, код, его значение и словарь
    return n, c, deCode, d

# Параметры кодирования
class makeCode:
    def __init__(self, nMethod, tInputText, nDict, nBuff):
        self.nMethod = nMethod # Метод сжатия
        self.tInputText = tInputText # Исходный текст
        self.Index = 0 # Смещение курсора
        self.nDict = nDict # Размер словаря (в символах)
        self.nBuff = nBuff # Размер буфера (в символах)
        self.tOutputText = '' # Сжатый тект
        self.sizeOutputText = 0 # Размер сжатого текста (в битах)
        pass

    def makeNextCode(self):
        tDict, tBuff, tCode = '', '', ''
        # Если не достигли конца сообщения
        if self.Index < len(self.tInputText):
            # Определение содержимого словаря
            if self.Index < self.nDict:
                tDict = self.tInputText[0: self.Index]
            else:
                tDict = self.tInputText[self.Index-self.nDict: self.Index]
            # Символ пустого места - 0x02f3, также - 0x02da
            tDict = tDict.rjust(self.nDict, chr(0x02f3))
            # Определение содержимого буфера
            tBuff = self.tInputText[self.Index: self.Index+self.nBuff]
            # Получение сдвига курсора, кода и его размера в битах
            if self.nMethod == nMethodLZ77:
                shift, tCode, sizeCode = makeLZ77(tDict, \
                        math.ceil(math.log2(self.nDict)), \
                        tBuff, math.ceil(math.log2(self.nBuff)))
            elif self.nMethod == nMethodLZSS:
                shift, tCode, sizeCode = makeLZSS(tDict, \
                        math.ceil(math.log2(self.nDict)), \
                        tBuff, math.ceil(math.log2(self.nBuff)))
            # Сдвиг курсора
            self.Index += shift
            # Накопление сжатого текста
            self.tOutputText += tCode
            # и его размера
            self.sizeOutputText += sizeCode
            # Дополним буфер до заданной длины символом пустого места
            tBuff = tBuff.ljust(self.nBuff, chr(0x02da))
        return tDict, tBuff, tCode

# Параметры декодирования
class makeDeCode:
    def __init__(self, nMethod, tInputText, nDict):
        self.nMethod = nMethod # Метод сжатия
        self.tInputText = tInputText # Исходный текст
        self.Index = 0 # Смещение курсора
        self.nDict = nDict # Размер словаря (в символах)
        self.tDict = ''.rjust(nDict, chr(0x02f3)) # Словарь
        # 0x02f3 - символ пустого места
        self.tOutputText = '' # Сжатый тект
        pass

    def makeNextDeCode(self):
        tCode, tDeCode = '', ''
        # Если не достигли конца сообщения
        if self.Index < len(self.tInputText):
            # Чтение очередного кода
            tCode = self.tInputText[self.Index: self.Index+3]
            # Получение сдвига курсора, кода, его значения и
            # следующего значения словаря
            if self.nMethod == nMethodLZ77:
                shift, tCode, tDeCode, self.tDict = \
                        makeDeLZ77(self.tDict, tCode)
            elif self.nMethod == nMethodLZSS:
                shift, tCode, tDeCode, self.tDict = \
                        makeDeLZSS(self.tDict, tCode)
            # Сдвиг курсора
            self.Index += shift
            # Накопление исходного текста
            self.tOutputText += tDeCode
        return tCode, tDeCode