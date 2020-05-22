# coding=utf8

import unicodedata
from collections import OrderedDict
import tkinter as tk
import tkinter.font as tkfont

c_lightshade = '#EEF1EE'
c_lightaccent = '#979B7E'
c_brand = '#A3B1A7'
c_darkaccent = '#767682'
c_darkshade = '#374251'

data = {'文禄' : {'start': 1592, 'length': 4, 'hepburn': 'Bunroku'}, # 桃山時代
'慶長' : {'start': 1596, 'length': 19, 'hepburn': 'Keichō'}, # 桃山時代
'元和' : {'start': 1615, 'length': 9, 'hepburn': 'Genna'}, # 江戸時代
'寛永' : {'start': 1624, 'length': 20, 'hepburn': 'Kan\'ei'},
'正保' : {'start': 1644, 'length': 4, 'hepburn': 'Shōhō'},
'慶安' : {'start': 1648, 'length': 4, 'hepburn': 'Keian'},
'承応' : {'start': 1652, 'length': 3, 'hepburn': 'Jōō'},
'明暦' : {'start': 1655, 'length': 3, 'hepburn': 'Meireki'},
'万治' : {'start': 1658, 'length': 3, 'hepburn': 'Manji'},
'寛文' : {'start': 1661, 'length': 12, 'hepburn': 'Kanbun'},
'延宝' : {'start': 1673, 'length': 8, 'hepburn': 'Enpō'},
'天和' : {'start': 1681, 'length': 3, 'hepburn': 'Tenna'},
'貞享' : {'start': 1684, 'length': 4, 'hepburn': 'Jōkyō'},
'元禄' : {'start': 1688, 'length': 16, 'hepburn': 'Genroku'},
'宝永' : {'start': 1704, 'length': 7, 'hepburn': 'Hōei'},
'正徳' : {'start': 1711, 'length': 5, 'hepburn': 'Shōtoku'},
'享保' : {'start': 1716, 'length': 20, 'hepburn': 'Kyōhō'},
'元文' : {'start': 1736, 'length': 5, 'hepburn': 'Genbun'},
'寛保' : {'start': 1741, 'length': 3, 'hepburn': 'Kanpō'},
'延享' : {'start': 1744, 'length': 4, 'hepburn': 'Enkyō'},
'寛延' : {'start': 1748, 'length': 3, 'hepburn': 'Kan\'en'},
'宝歴' : {'start': 1751, 'length': 13, 'hepburn': 'Hōreki'},
'明和' : {'start': 1764, 'length': 8, 'hepburn': 'Meiwa'},
'安永' : {'start': 1772, 'length': 9, 'hepburn': 'An\'ei'},
'天明' : {'start': 1781, 'length': 8, 'hepburn': 'Tenmei'},
'寛政' : {'start': 1789, 'length': 12, 'hepburn': 'Kansei'},
'享和' : {'start': 1801, 'length': 3, 'hepburn': 'Kyōwa'},
'文化' : {'start': 1804, 'length': 14, 'hepburn': 'Bunka'},
'文政' : {'start': 1818, 'length': 12, 'hepburn': 'Bunsei'},
'天保' : {'start': 1830, 'length': 14, 'hepburn': 'Tenpō'},
'弘化' : {'start': 1844, 'length': 4, 'hepburn': 'Kōka'},
'嘉永' : {'start': 1848, 'length': 6, 'hepburn': 'Ka\'ei'},
'安政' : {'start': 1854, 'length': 6, 'hepburn': 'Ansei'},
'万延' : {'start': 1860, 'length': 1, 'hepburn': 'Man\'en'},
'文久' : {'start': 1861, 'length': 3, 'hepburn': 'Bunkyū'},
'元治' : {'start': 1864, 'length': 1, 'hepburn': 'Genji'},
'慶応' : {'start': 1865, 'length': 3, 'hepburn': 'Keiō'},
'明治' : {'start': 1868, 'length': 33, 'hepburn': 'Meiji'} } # Meiji
data = OrderedDict(sorted(data.items(), key= lambda x: x[1]['start']))

def normalizeEdoperiodname(text):
    """
    >>> normalizeEdoperiodname("Shōhō")
    Shoho
    """
    text = unicodedata.normalize("NFD", text)
    text = text.encode("ascii", "ignore")
    text = text.lower()
    return text

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
        startyear = data[period]['start']
        length = data[period]['length']
        if startyear <= year and year <= startyear + length - 1:
            return (period, year - startyear + 1)

    return ("Not found", 1)

def westernFromEdo(edoyear):
    """
    >>> westernFromEdo("正保1")
    1644
    """
    period = edoyear[:2]
    year = int(edoyear[2:])

    if period in data:
        startyear = period['start']
        length = period['length']

        if 1 <= year and year <= length:
            return startyear + year - 1
        else:
            raise ValueError("Year %2d is not within periods span %2d" %(year, length))
    else:
        raise ValueError("Didn't find period %s" % period)

def checkEntry(*event):
    entry = yearentry.get()

    if isWesternYear(entry):
        westernyear = int(entry)
        period, year = edoFromWestern(westernyear)
        showPeriod(period, year)
    else:
        period, year = "", "0"
        for c in entry:
            if c in "0123456789０１２３４５６７８９":
                year += str(unicodedata.digit(c))
            else:
                period += c
        
        showPeriod(period, int(year))

def highlightButton(periodname):
    for period, perioddata in data.items():
        b = perioddata['button']
        if period == periodname:
            b.configure(background=c_darkaccent, activebackground=c_darkaccent, foreground=c_lightshade, activeforeground=c_lightshade)
        else:
            b.configure(background=c_lightshade, activebackground=c_lightshade, foreground=c_darkshade, activeforeground=c_darkshade)
            b.underline = -1

def showPeriod(period: str, year: int):
    if period in data:
        startyear = data[period]['start']
        length = data[period]['length']
        transcription = data[period]['hepburn']
        endyear = startyear + length - 1
        highlightButton(period)
    # Search in hepburn transcription
    elif normalizeEdoperiodname(period) in [normalizeEdoperiodname(d['hepburn']) for d in data.values()]:
        for key, value in data.items():
            if normalizeEdoperiodname(period) == normalizeEdoperiodname(value['hepburn']):
                period = key
                startyear = value['start']
                length = value['length']
                transcription = value['hepburn']
                endyear = startyear + length - 1
                highlightButton(period)
    else:
        period = "not found"
        startyear, length, transcription = 0, 0, ""
        endyear = 0

    for widget in resultFrame.winfo_children():
        widget.destroy()

    labelPeriod = tk.Label(resultFrame, text=period, font=bigFont, bg=c_lightshade)
    labelPeriod.pack()
    labelPeriodTranslation = tk.Label(resultFrame, text=transcription, font=smallFont, bg=c_lightshade)
    labelPeriodTranslation.pack()
    labelSpan = tk.Label(resultFrame, text="%s - %s" % (startyear, endyear), font=smallFont, bg=c_lightshade)
    labelSpan.pack(pady=(5, 20))

    tableFrame = tk.Frame(resultFrame, bg=c_lightshade)
    tableFrame.pack()
    for i in range(length):
        col_edoyear = tk.Label(tableFrame, text=period + str(i+1), bg=c_lightshade)
        col_year = tk.Label(tableFrame, text=str(startyear + i), bg=c_lightshade)
        if i + 1 == year:
            col_edoyear.configure(font=normalFont, fg=c_lightaccent)
            col_year.configure(font=normalFont, fg=c_lightaccent)
        else:
            col_edoyear.configure(font=smallFont)
            col_year.configure(font=smallFont)
        col_edoyear.grid(column=0, row=i, padx=(10, 10))
        col_year.grid(column=1, row=i, padx=(10, 10))

def getFunction_InsertEdoperiodInEntry(edoperiod):
    def f(event):
        yearentry.delete(0, tk.END)
        yearentry.insert(0, edoperiod + "1")
        yearentry.focus()
        yearentry.event_generate("<Return>", when="tail")
    return f

if __name__ == "__main__":
    window = tk.Tk()
    window.title("江戸時代 → 西年")
    window.configure(bg=c_lightshade)
    smallFont = tkfont.Font(family="Lucida Grande", size=12)
    normalFont = tkfont.Font(family="Lucida Grande", size=16)
    bigFont = tkfont.Font(family="Lucida Grande", size=20)
    window.geometry("700x800")
    inputFrame = tk.Frame(bg=c_lightshade)
    inputFrame.pack(pady=(10, 10))
    buttonFrame = tk.Frame(bg=c_lightshade)
    buttonFrame.pack(pady=(10, 10))
    resultFrame = tk.Frame(bg=c_lightshade)
    resultFrame.pack(pady=(10, 10))

    yearentryLabel = tk.Label(inputFrame, text="年", font=normalFont, bg=c_lightshade)
    yearentryLabel.grid(column=0, row=0, padx=(0, 10))
    yearentry = tk.Entry(inputFrame, width=10, font=normalFont)
    yearentry.grid(column=1, row=0)
    yearentry.bind("<Return>", checkEntry)

    buttontablewidth = 10
    for i, period in enumerate(data.keys()):
        
        button = tk.Button(buttonFrame, text=period, font=smallFont)
        button.grid(column = i % buttontablewidth, row = i // buttontablewidth + 1)
        f = getFunction_InsertEdoperiodInEntry(period)
        button.bind("<Button-1>", f)
        data[period]['button'] = button
    highlightButton("")

    window.mainloop()
