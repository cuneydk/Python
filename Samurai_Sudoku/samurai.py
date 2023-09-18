import os
import sys
import threading
import datetime
import time
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def cross(A, B, c=''):
    return [a + b + c for a in A for b in B]

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits


matrisA = [[0] * 9 for n in range(9)]
matrisB = [[0] * 9 for n in range(9)]
matrisC = [[0] * 9 for n in range(9)]
matrisD = [[0] * 9 for n in range(9)]
matrisM = [[0] * 9 for n in range(9)]

id_var = 'a'  # sol üst
sudoku_sol_ust = cross(rows, cols, id_var)
unitlist_a = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'b'  # sağ üst
sudoku_sag_ust = cross(rows, cols, id_var)
unitlist_b = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'c'  # sol alt
sudoku_sol_alt = cross(rows, cols, id_var)
unitlist_c = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])

id_var = 'd'  # sağ alt
sudoku_sag_alt = cross(rows, cols, id_var)
unitlist_d = ([cross(rows, c, id_var) for c in cols] +
              [cross(r, cols, id_var) for r in rows] +
              [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
               for cs in ('123', '456', '789')])


def repl(c):
    a = b = 0
    s = ""
    if c[0] in 'ABCGHI' and c[1] in '123789':
        if c[0] in 'ABC':
            s += chr(ord(c[0]) + 6)
            a = 1
        elif c[0] in 'GHI':
            s += chr(ord(c[0]) - 6)
            a = 2
        if c[1] in '123':
            s += chr(ord(c[1]) + 6)
            b = 1
        elif c[1] in '789':
            s += chr(ord(c[1]) - 6)
            b = 2
    else:
        return c
    if a == 1 and b == 1:
        s += 'a'
    elif a == 1 and b == 2:
        s += 'b'
    elif a == 2 and b == 1:
        s += 'c'
    elif a == 2 and b == 2:
        s += 'd'
    return s


id_var = '+'
sudoku_orta = [repl(x) for x in cross(rows, cols, id_var)]
unitlist_mid = ([sudoku_orta[x * 9:x * 9 + 9] for x in range(0, 9)] +
                [sudoku_orta[x::9] for x in range(0, 9)] +
                [cross(rs, cs, id_var) for rs in ('ABC', 'DEF', 'GHI')
                 for cs in ('123', '456', '789')
                 if not (rs in 'ABCGHI' and cs in '123789')])

all_squares = set(sudoku_sol_ust + sudoku_sag_ust + sudoku_sol_alt + sudoku_sag_alt + sudoku_orta)
all_unitlists = unitlist_a + unitlist_b + unitlist_c + unitlist_d + unitlist_mid

units = dict((s, [u for u in all_unitlists if s in u])
             for s in all_squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in all_squares)


################  ################

def parse_grid_samurai(grid):
    values = dict((s, digits) for s in all_squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values


def flatten(arr):
    return [x for sub in arr for x in sub]


def grid_values(grid):
    a = flatten([x[:9] for x in grid[:9]])
    b = flatten([x[12:] for x in grid[:9]])
    c = flatten([x[:9] for x in grid[12:]])
    d = flatten([x[12:] for x in grid[12:]])
    mid = flatten([x[6:15] for x in grid[6:15]])
    chars = a + b + c + d + mid
    sqrs = sudoku_sol_ust + sudoku_sag_ust + sudoku_sol_alt + sudoku_sag_alt + sudoku_orta
    assert len(chars) == 405
    return dict(zip(sqrs, chars))


################  ################


def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, '')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values


################ Sudokuları 2 Boyutlu Dizi Şeklinde Gösterme ################


def yazdir(values, sqr, tip):

    width = 1 + max(len(values[s]) for s in sqr)
    line = '+'.join(['-' * (width * 3)] * 3)
    satir = ""
    counter = 0
    temp = ""
    for r in rows:
        satir = ''.join(
            values[sqr[(ord(r) - 65) * 9 + int(c) - 1]].center(width) + ('|' if c in '36' else '') for c in cols)
        satirBolme = satir.split("|")
        index = 0
        for i in satirBolme:
            uclu = i.split(" ")
            temp += uclu[0] + " - " + uclu[1] + " - " + uclu[2] + " | "
            if tip == "a":
                matrisA[counter][index] = uclu[0]
                matrisA[counter][index + 1] = uclu[1]
                matrisA[counter][index + 2] = uclu[2]
            elif tip == "b":
                matrisB[counter][index] = uclu[0]
                matrisB[counter][index + 1] = uclu[1]
                matrisB[counter][index + 2] = uclu[2]
            elif tip == "c":
                matrisC[counter][index] = uclu[0]
                matrisC[counter][index + 1] = uclu[1]
                matrisC[counter][index + 2] = uclu[2]
            elif tip == "d":
                matrisD[counter][index] = uclu[0]
                matrisD[counter][index + 1] = uclu[1]
                matrisD[counter][index + 2] = uclu[2]
            elif tip == "m":
                matrisM[counter][index] = uclu[0]
                matrisM[counter][index + 1] = uclu[1]
                matrisM[counter][index + 2] = uclu[2]
            index += 3

        temp = ""
        counter += 1


def yazdir_samurai(vals):

    listezaman = []

    if not vals:
        print("Çözüm bulunamadı. Samurai Sudokunuzun geçerli olup olmadığını kontrol ediniz.")
        return

    def run():
        yazdir(vals, sudoku_sol_ust, "a")
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)
        time.sleep(3)
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)

    def run2():
        yazdir(vals, sudoku_sag_ust, "b")
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)
        time.sleep(3)
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)

    def run3():
        yazdir(vals, sudoku_sol_alt, "c")
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)
        time.sleep(3)
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)

    def run4():
        yazdir(vals, sudoku_sag_alt, "d")
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)
        time.sleep(3)
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)

    def run5():
        yazdir(vals, sudoku_orta, "m")
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)
        time.sleep(3)
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        #print(result)

    #localtime = time.localtime()
    #result1 = time.strftime("%I:%M:%S %p", localtime)
    a = datetime.datetime.now()

    t1 = threading.Thread(target=run)
    time.sleep(1)
    t2 = threading.Thread(target=run2)
    time.sleep(1)
    t3 = threading.Thread(target=run3)
    time.sleep(1)
    t4 = threading.Thread(target=run4)
    time.sleep(1)
    t5 = threading.Thread(target=run5)
    time.sleep(1)

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    t3.start()
    t3.join()

    t4.start()
    t4.join()

    t5.start()
    t5.join()

    #localtime2 = time.localtime()
    #result2 = time.strftime("%I:%M:%S %p", localtime2)

    b = datetime.datetime.now()

    sonuc5thread = b - a
    listezaman.append(sonuc5thread.seconds)

    #print(b - a)
    #print(float(sonuc5thread.seconds))

    threadLock = threading.Lock()
    threadLock.acquire()

    c = datetime.datetime.now()

    t1 = threading.Thread(target = run)
    time.sleep(1)
    t2 = threading.Thread(target = run2)
    time.sleep(1)
    t3 = threading.Thread(target = run3)
    time.sleep(1)
    t4 = threading.Thread(target = run4)
    time.sleep(1)
    t5 = threading.Thread(target = run5)
    time.sleep(1)
    t6 = threading.Thread(target = run)
    time.sleep(1)
    t7 = threading.Thread(target = run2)
    time.sleep(1)
    t8 = threading.Thread(target = run3)
    time.sleep(1)
    t9 = threading.Thread(target = run4)
    time.sleep(1)
    t10 = threading.Thread(target = run5)
    time.sleep(1)

    t1.start()
    t1.join()

    t2.start()
    t2.join()

    t3.start()
    t3.join()

    t4.start()
    t4.join()

    t5.start()
    t5.join()

    t6.start()
    t6.join()

    t7.start()
    t7.join()

    t8.start()
    t8.join()

    t9.start()
    t9.join()

    t10.start()
    t10.join()

    d = datetime.datetime.now()

    sonuc10thread = d - c
    listezaman.append(sonuc10thread.seconds)
    #print(sonuc10thread.seconds)
    return listezaman


################ Arama ################

def solve(grid):
    return search(parse_grid_samurai(grid))


def search(values):

    if values is False:
        return False
    if all(len(values[s]) == 1 for s in all_squares):
        return values

    n, s = min((len(values[s]), s) for s in all_squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))
                for d in values[s])


################ Araçlar ################

def some(seq):
    for e in seq:
        if e: return e
    return False


def from_file(filename, sep='\n'):
    return open(filename, 'r').read().strip().split(sep)


def shuffled(seq):
    seq = list(seq)
    random.shuffle(seq)
    return seq


class GUI(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("SAMURAI SUDOKU SOLVER")
        self.resize(630, 630)

        for i in range(0, 270, 30):
            for j in range(0, 270, 30):
                self.label = QLabel(str(matrisA[(int)(i / 30)][(int)(j / 30)]), self)
                self.label.setGeometry(j + 14, i, 30, 30)
            pass
        pass

        for i in range(0, 270, 30):
            for j in range(360, 630, 30):
                self.label = QLabel(str(matrisB[(int)(i / 30)][(int)((j - 360) / 30)]), self)
                self.label.setGeometry(j + 14, i, 30, 30)
            pass
        pass

        for i in range(360, 630, 30):
            for j in range(0, 270, 30):
                self.label = QLabel(str(matrisC[(int)((i - 360) / 30)][(int)(j / 30)]), self)
                self.label.setGeometry(j + 14, i, 30, 30)
            pass
        pass

        for i in range(360, 630, 30):
            for j in range(360, 630, 30):
                self.label = QLabel(str(matrisD[(int)((i - 360) / 30)][(int)((j - 360) / 30)]), self)
                self.label.setGeometry(j + 14, i, 30, 30)
            pass
        pass

        for i in range(180, 450, 30):
            for j in range(180, 450, 30):
                self.label = QLabel(str(matrisM[(int)((i - 180) / 30)][(int)((j - 180) / 30)]), self)
                self.label.setGeometry(j + 14, i, 30, 30)
            pass
        pass

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QPen(Qt.blue, 2))

        for i in range(30, 271, 30):
            painter.drawLine(i, 0, i, 270)

        for i in range(30, 271, 30):
            painter.drawLine(i, 360, i, 630)

        for i in range(360, 640, 30):
            painter.drawLine(i, 0, i, 270)

        for i in range(360, 640, 30):
            painter.drawLine(i, 360, i, 630)

        painter.setPen(QPen(Qt.cyan, 2))

        for i in range(30, 271, 30):
            painter.drawLine(0, i, 270, i)

        for i in range(30, 271, 30):
            painter.drawLine(360, i, 630, i)

        for i in range(360, 640, 30):
            painter.drawLine(0, i, 270, i)

        for i in range(360, 640, 30):
            painter.drawLine(360, i, 630, i)

        # middle
        painter.setPen(QPen(Qt.cyan, 2))
        for i in range(180, 480, 30):
            painter.drawLine(180, i, 450, i)

        painter.setPen(QPen(Qt.blue, 2))
        for i in range(180, 480, 30):
            painter.drawLine(i, 180, i, 450)

        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)


class GUI2(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("THREAD COMPARING GUI")
        self.resize(630, 630)



    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QPen(Qt.black, 2))

        painter.drawLine(10, 10, 10, 620)
        painter.drawLine(10, 620, 620, 620)

        painter.setPen(QPen(Qt.blue, 2))
        painter.drawLine(10, 620, thread5 * 4, 80)

        painter.setPen(QPen(Qt.red, 2))
        painter.drawLine(10, 620, thread10 * 4, 80)

        vertical_layout = QVBoxLayout()
        self.setLayout(vertical_layout)


if __name__ == '__main__':
    prompt = 1
    while prompt:
        txt = input("Samurai Sudoku txt dosyasının bulunduğu dosya yolunu giriniz: ")
        try:
            f = open(txt, 'r')
            prompt = 0
        except FileNotFoundError:
            print("Dosya bulunamadı.")
    samurai_grid = f.read().split('\n')
    ans = solve(samurai_grid)
    yazdir_samurai(ans)
    thread5 = yazdir_samurai(ans)[0]
    thread10 = yazdir_samurai(ans)[1]

    app = QApplication([])

    widget = GUI()
    widget.show()

    widget2 = GUI2()
    widget2.show()

    app.exec_()