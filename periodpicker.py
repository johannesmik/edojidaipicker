# coding=utf8

import unicodedata
from collections import OrderedDict

def normalizeEdoperiodname(text):
    """
    >>> normalizeEdoperiodname("Shōhō")
    Shoho
    """
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore")
    text = text.lower()
    return text

data = {'文禄' : (1592, 4, ''),
'慶長' : (1596, 19, 'Keichō'),
'元和' : (1615, 9, 'Genna'),
'寛永' : (1624, 20, 'Kan\'ei'),
'正保' : (1644, 4, 'Shōhō'),
'慶安' : (1648, 4, 'Keian'),
'承応' : (1652, 3, 'Jōō'),
'明暦' : (1655, 3, 'Meireki'),
'万治' : (1658, 3, 'Manji'),
'寛文' : (1661, 12, 'Kanbun'),
'延宝' : (1673, 8, 'Enpō'),
'天和' : (1681, 3, 'Tenna'),
'貞享' : (1684, 4, 'Jōkyō'),
'元禄' : (1688, 16, 'Genroku'),
'宝永' : (1704, 7, 'Hōei'),
'正徳' : (1711, 5, 'Shōtoku'),
'享保' : (1716, 20, 'Kyōhō'),
'元文' : (1736, 5, 'Genbun'),
'寛保' : (1741, 3, 'Kanpō'),
'延享' : (1744, 4, 'Enkyō'),
'寛延' : (1748, 3, 'Kan\'en'),
'宝歴' : (1751, 13, 'Hōreki'),
'明和' : (1764, 8, 'Meiwa'),
'安永' : (1772, 9, 'An\'ei'),
'天明' : (1781, 8, 'Tenmei'),
'寛政' : (1789, 12, 'Kansei'),
'享和' : (1801, 3, 'Kyōwa'),
'文化' : (1804, 14, 'Bunka'),
'文政' : (1818, 12, 'Bunsei'),
'天保' : (1830, 14, 'Tenpō'),
'弘化' : (1844, 4, 'Kōka'),
'嘉永' : (1848, 6, 'Ka\'ei'),
'安政' : (1854, 6, 'Ansei'),
'万延' : (1860, 1, 'Man\'en'),
'文久' : (1861, 3, 'Bunkyū'),
'元治' : (1864, 1, 'Genji'),
'慶応' : (1865, 3, 'Keiō'),
'明治' : (1868, 33, 'Meiji') }
data = OrderedDict(sorted(data.items(), key= lambda x: x[1][0]))
translation = {normalizeEdoperiodname(value[2]) : key  for key, value in data.items()}

def checkdata(data):
    nextyear = ""
    for value in data.values():
        year, span, _ = value
        if nextyear != "":
            if nextyear != year:
                return False
        nextyear = year + span
    return True


def isWesternYear(year):
    for c in year:
        if c not in "0123456789":
            return False
    return True

def edoFromWestern(year):
    """
    >>> edoFromWestern(1830)
    ("天保", 3)
    """

    for period in data:
        startyear, span, _ = data[period]
        if startyear <= year and year <= startyear + span - 1:
            return (period, year - startyear + 1)

    return ("Not found", 1)

def westernFromEdo(edoyear):
    """
    >>> westernFromEdo("正保1")
    1644
    >>> westernFromEdo("天保3")
    1832
    """
    period = edoyear[:2]
    year = int(edoyear[2:])

    if period in data:
        startyear, span = data[period]

        if 1 <= year and year <= span:
            return startyear + year - 1
        else:
            raise ValueError("Year %2d is not within periods span %2d" %(year, span))
    else:
        raise ValueError("Don't know period %s" % period)

def checkEntry(*event):
    print(yearentry.get())

    entry = yearentry.get()

    if isWesternYear(entry):
        westernyear = int(entry)
        createResultFromWestern(westernyear)
    else:
        edoperiod, year = "", ""
        for c in entry:
            if c in "0123456789０１２３４５６７８９":
                year += str(unicodedata.digit(c))
            else:
                edoperiod += c
        
        createResultFromEdo(edoperiod, int(year))

def getInformationOnPeriod(period):
    pass

def createResultFromWestern(year: int):
    period, edoyear = edoFromWestern(year)
    startyear, span, translation = data[period]
    endyear = startyear + span - 1

    for widget in resultFrame.winfo_children():
        widget.destroy()

    labelPeriod = tk.Label(resultFrame, text=period, font=bigFont)
    labelPeriod.pack()
    labelPeriodTranslation = tk.Label(resultFrame, text=translation, font=normalFont)
    labelPeriodTranslation.pack()
    labelSpan = tk.Label(resultFrame, text="%s - %s" % (startyear, endyear), font=smallFont)
    labelSpan.pack()
    labelYear = tk.Label(resultFrame, text="%s%d = %d" % (period, edoyear, year), font=normalFont)
    labelYear.pack()

    tableFrame = tk.Frame(resultFrame)
    tableFrame.pack()
    for i in range(span):
        col_edoyear = tk.Label(tableFrame, text=period + str(i+1), font=smallFont)
        col_edoyear.grid(column=0, row=i)
        col_year = tk.Label(tableFrame, text=str(startyear + i), font=smallFont)
        col_year.grid(column=1, row=i)

def createResultFromEdo(period: str, year: int):
    if normalizeEdoperiodname(period) in translation and normalizeEdoperiodname(period) != b'':
        period = translation[normalizeEdoperiodname(period)]
    startyear, span, transcription = data[period]
    endyear = startyear + span - 1

    for widget in resultFrame.winfo_children():
        widget.destroy()

    labelPeriod = tk.Label(resultFrame, text=period, font=bigFont)
    labelPeriod.pack()
    labelPeriodTranslation = tk.Label(resultFrame, text=transcription, font=normalFont)
    labelPeriodTranslation.pack()
    labelSpan = tk.Label(resultFrame, text="%s - %s" % (startyear, endyear), font=smallFont)
    labelSpan.pack()
    labelYear = tk.Label(resultFrame, text="%s%d = %d" % (period, year, startyear+year-1), font=normalFont)
    labelYear.pack()

    tableFrame = tk.Frame(resultFrame)
    tableFrame.pack()
    for i in range(span):
        col_edoyear = tk.Label(tableFrame, text=period + str(i+1), font=smallFont)
        col_edoyear.grid(column=0, row=i)
        col_year = tk.Label(tableFrame, text=str(startyear + i), font=smallFont)
        col_year.grid(column=1, row=i)

import tkinter as tk
import tkinter.font as tkfont


def insertInYearentry(text):
    def f(event):
        yearentry.delete(0, tk.END)
        yearentry.insert(0, text + "1")
        yearentry.focus()
        yearentry.event_generate("<Return>", when="tail")
    return f

if __name__ == "__main__":
    if not checkdata(data):
        print("Data check failed")

    window = tk.Tk()
    window.title("江戸時代 → 西年")
    smallFont = tkfont.Font(family="Lucida Grande", size=12)
    normalFont = tkfont.Font(family="Lucida Grande", size=16)
    bigFont = tkfont.Font(family="Lucida Grande", size=20)
    window.geometry("800x400")
    inputFrame = tk.Frame()
    inputFrame.pack()
    buttonFrame = tk.Frame()
    buttonFrame.pack()
    resultFrame = tk.Frame()
    resultFrame.pack()

    label1 = tk.Label(inputFrame, text="年", font=normalFont)
    label1.grid(column=0, row=0)
    yearentry = tk.Entry(inputFrame, width=10, font=bigFont)
    yearentry.grid(column=1, row=0)
    yearentry.bind("<Return>", checkEntry)

    buttontablewidth = 10
    for i, period in enumerate(data.keys()):
        
        button = tk.Button(buttonFrame, text=period, font=bigFont)
        button.grid(column = i % buttontablewidth, row = i // buttontablewidth + 1)
        f = insertInYearentry(period)
        button.bind("<Button-1>", f)

    window.mainloop()



