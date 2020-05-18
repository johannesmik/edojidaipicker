import periodpicker

def test_checkdata():
    nextyear = ""
    for value in periodpicker.data.values():
        year, span, _ = value
        if nextyear != "":
            assert nextyear == year
        nextyear = year + span