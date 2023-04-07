#!/bin/env python3

from datetime import date, datetime, timedelta
from icalendar import Calendar, Event # requires python-icalendar

# von Wikipedia
beschreibungen = {
        'Neujahr':                          'Neujahr (auch Neujahrstag) ist der erste Tag des Kalenderjahres. Wegen der teils in einzelnen Kulturen und Religionen unterschiedlichen Zeitrechnungen und damit auch Kalender ist der Jahresbeginn zu unterschiedlichen Zeitpunkten.', # https://de.wikipedia.org/wiki/Neujahr
        'Heilige Drei Könige':              'Die eigentliche Bezeichnung dieses Festes ist dagegen Erscheinung des Herrn. Die Kirche feiert an diesem Tag das Sichtbarwerden der Göttlichkeit Jesu in der Anbetung durch die Sterndeuter, bei seiner Taufe im Jordan und durch das von ihm bei der Hochzeit zu Kana bewirkte Wunder der Verwandlung von Wasser in Wein.', # https://de.wikipedia.org/wiki/Heilige_Drei_K%C3%B6nige#Feiertag
        'Valentinstag':                     'In Westdeutschland wurde der Valentinstag nach dem Zweiten Weltkrieg durch im Land stationierte US-Soldaten bekannt. 1950 wurde in Nürnberg der erste „Valentinsball“ veranstaltet. Allgemein bekannt wurde der Valentinstag durch die vor dem 14. Februar verstärkt einsetzende Werbung der Floristik- und Süßwarenindustrie.', # https://de.wikipedia.org/wiki/Valentinstag#Deutschland
        'Frauentag':                        'Er entstand als Initiative sozialistischer Organisationen in der Zeit vor dem Ersten Weltkrieg im Kampf um die Gleichberechtigung, das Wahlrecht für Frauen sowie die Emanzipation von Arbeiterinnen. Erstmals fand der Frauentag am 19. März 1911 statt. 1921 wurde sein Datum durch einen Beschluss der Zweiten Internationalen Konferenz kommunistischer Frauen in Moskau endgültig auf den 8. März gelegt.', # https://de.wikipedia.org/wiki/Internationaler_Frauentag
        'Tag der Arbeit':                   'Der Erste Mai wird als Tag der Arbeit, Tag der Arbeiterbewegung, Internationaler Kampftag der Arbeiterklasse oder auch als Maifeiertag bezeichnet. [...] Anfang 1886 rief die nordamerikanische Arbeiterbewegung zur Durchsetzung des Achtstundentags zum Generalstreik am 1. Mai auf – in Anlehnung an die Massendemonstration am 1. Mai 1856 in Australien, welche ebenfalls den Achtstundentag forderte.', # https://de.wikipedia.org/wiki/Erster_Mai
        'Tag der Befreiung':                'Der 8. Mai ist als Tag der Befreiung in einigen europäischen Ländern ein Gedenktag, an dem als Jahrestag zum 8. Mai 1945 der bedingungslosen Kapitulation der deutschen Wehrmacht und damit des Endes des Zweiten Weltkrieges in Europa und der Befreiung vom Nationalsozialismus gedacht wird.', # https://de.wikipedia.org/wiki/Tag_der_Befreiung
        'Internationaler Kindertag':        'Der Kindertag, auch Weltkindertag, Internationaler Kindertag oder Internationaler Tag des Kindes, ist ein in über 145 Staaten der Welt begangener Tag, um auf die besonderen Bedürfnisse der Kinder und speziell auf die Kinderrechte aufmerksam zu machen. [...] In Deutschland und Österreich wird am 20. September der Weltkindertag ausgerichtet, aber auch der 1. Juni als Internationaler Kindertag gefeiert.', # https://de.wikipedia.org/wiki/Kindertag
        'Augsburger Hohes Friedensfest':    'Ursprünglich feierten die Augsburger Protestanten damit das 1648 durch den Westfälischen Frieden eingeleitete Ende der Rekatholisierungsmaßnahmen während des Dreißigjährigen Krieges.', # https://de.wikipedia.org/wiki/Augsburger_Hohes_Friedensfest
        'Maria Himmelfahrt':                'Christi Himmelfahrt [...] bezeichnet im christlichen Glauben die Rückkehr Jesu Christi als Sohn Gottes zu seinem Vater in den Himmel. Christi Himmelfahrt wird am 40. Tag der Osterzeit, also 39 Tage nach dem Ostersonntag gefeiert. Deshalb fällt das Fest immer auf einen Donnerstag.', # https://de.wikipedia.org/wiki/Christi_Himmelfahrt
        'Weltkindertag':                    'Der Kindertag, auch Weltkindertag, Internationaler Kindertag oder Internationaler Tag des Kindes, ist ein in über 145 Staaten der Welt begangener Tag, um auf die besonderen Bedürfnisse der Kinder und speziell auf die Kinderrechte aufmerksam zu machen. [...] In Deutschland und Österreich wird am 20. September der Weltkindertag ausgerichtet, aber auch der 1. Juni als Internationaler Kindertag gefeiert.', # https://de.wikipedia.org/wiki/Kindertag
        'Tag der Deutschen Einheit':        'Der 3. Oktober wurde als Tag der Deutschen Einheit im Einigungsvertrag 1990 zum gesetzlichen Feiertag in Deutschland bestimmt. Als deutscher Nationalfeiertag erinnert er an die deutsche Wiedervereinigung, die „mit dem Wirksamwerden des Beitritts der Deutschen Demokratischen Republik zur Bundesrepublik Deutschland […] am 3. Oktober 1990“ „vollendet“ wurde.', # https://de.wikipedia.org/wiki/Tag_der_Deutschen_Einheit
        'Reformationstag':                  'Der Reformationstag, das Reformationsfest oder der Gedenktag der Reformation wird von evangelischen Christen in Deutschland und Österreich am 31. Oktober im Gedenken an den Beginn der Reformation der Kirche durch Martin Luther im Jahr 1517 gefeiert.', # https://de.wikipedia.org/wiki/Reformationstag
        'Allerheiligen':                    'Allerheiligen ist ein christliches Fest, an dem aller Heiligen gedacht wird, der „verherrlichten Glieder der Kirche, die schon zur Vollendung gelangt sind“, der bekannten wie der unbekannten.', # https://de.wikipedia.org/wiki/Allerheiligen
        'Martinstag':                       'Der Martinstag ist in Mitteleuropa von zahlreichen Bräuchen geprägt, darunter das Martinsgansessen, der Martinszug und das Martinssingen. [...] An einem Tag im Winter begegnete Martin am Stadttor von Amiens einem armen, unbekleideten Mann. In einer barmherzigen Tat teilte er seinen Mantel mit dem Schwert und gab eine Hälfte dem Armen. [...] Eine weitere Überlieferung besagt, dass Martin im Jahr 371 in der Stadt Tours von den Einwohnern zum Bischof ernannt werden sollte. Martin, der sich des Amtes unwürdig empfand, habe sich in einem Gänsestall versteckt. Die aufgeregt schnatternden Gänse verrieten aber seine Anwesenheit, und er musste das Bischofsamt annehmen.', # https://de.wikipedia.org/wiki/Martinstag, https://de.wikipedia.org/wiki/Martin_von_Tours
        'Nikolaustag':                      'Der Gedenktag des [Nikolaus von Myra] ist mit vielen Bräuchen verbunden. Einige hingen ursprünglich mit der Perikopenordnung der Kirche zusammen. Am 6. Dezember war verbindlich die Perikope vom Gleichnis von den anvertrauten Talenten vorgesehen. Der bekannte Brauch der Befragung der Kinder durch den Nikolaus, ob sie denn auch brav und fromm gewesen seien, geht auf dieses Gleichnis zurück.', # https://de.wikipedia.org/wiki/Nikolaus_von_Myra#Brauchtum
        'Heiligabend':                      'Der Heilige Abend, auch Heiligabend oder Weihnachtsabend genannt, ist der Vorabend des Weihnachtsfestes (Fest der Geburt Jesu Christi); vielerorts wird auch der ganze Vortag so bezeichnet. Am Abend findet unter anderem in Deutschland, der Schweiz, in Liechtenstein und in Österreich traditionell die Bescherung statt.', # https://de.wikipedia.org/wiki/Heiliger_Abend
        'Erster Weihnachtsfeiertag':        'In Finnland und Estland wird am Heiligen Abend der „Weihnachtsfrieden“ ausgerufen. Früher erhielten Menschen, die während des Weihnachtsfriedens in Finnland eine Straftat begingen, eine doppelt so hohe Strafe wie üblich.',
        'Zweiter Weihnachtsfeiertag':       'Das Weihnachtsfest erhielt in der Liturgie etwa ab dem 8. Jahrhundert eine Oktav, eine einwöchige Festzeit, in der aber die in diese Zeit fallenden bestehenden Heiligenfeste erhalten blieben. Vor der Reformation gab es in den einzelnen deutschen Herrschaften je nach dem jeweiligen Landesfürsten bis zu fünf Weihnachtsfeiertage.', # https://de.wikipedia.org/wiki/Zweiter_Weihnachtsfeiertag
        'Ostersonntag':                     'Der Ostersonntag ist im Christentum der Festtag der Auferstehung Jesu Christi, der nach dem Neuen Testament als Sohn Gottes den Tod überwunden hat.', # https://de.wikipedia.org/wiki/Ostersonntag
        'Palmsonntag':                      'Am Palmsonntag wird des Einzugs Jesu Christi in Jerusalem gedacht. Zum Zeichen seines Königtums jubelte das Volk ihm zu und streute dem nach Jerusalem Kommenden Palmzweige.', # https://de.wikipedia.org/wiki/Palmsonntag#Kirchliche_Tradition
        'Gründonnerstag':                   'An ihm gedenken die Christen des letzten Abendmahles Jesu mit den zwölf Aposteln am Vorabend seiner Kreuzigung.', # https://de.wikipedia.org/wiki/Gr%C3%BCndonnerstag
        'Karfreitag':                       'Christen gedenken an diesem Tag des Leidens und Sterbens Jesu Christi am Kreuz. Der Karfreitag wird auch stiller Freitag oder hoher Freitag genannt. ', # https://de.wikipedia.org/wiki/Karfreitag
        'Karsamstag':                       'Die Christen gedenken am Karsamstag, dem Tag der Grabesruhe Jesu Christi, seines Abstiegs in die Unterwelt, bei dem er nach seiner Kreuzigung die Seelen der Gerechten seit Adam aus dem Limbus patrum befreit habe.', # https://de.wikipedia.org/wiki/Karsamstag
        'Ostermontag':                      'Zwei Jünger Jesu sind am dritten Tag nach der Kreuzigung Jesu aus Jerusalem fortgegangen, um nach Emmaus zurückzukehren. Auf dem Weg dorthin schließt sich ihnen ein dritter, unbekannter Mann an. [...] Er bricht am Tisch das Brot, und in diesem Moment erkennen sie Jesus, der aber vor ihren Augen verschwindet.', # https://de.wikipedia.org/wiki/Ostermontag#Liturgische_Bedeutung
        'Christi-Himmelfahrt':              'Christi Himmelfahrt bezeichnet im christlichen Glauben die Rückkehr Jesu Christi als Sohn Gottes zu seinem Vater in den Himmel.', # https://de.wikipedia.org/wiki/Christi_Himmelfahrt
        'Pfingstsonntag':                   'Pfingsten ist ein christliches Fest. Der Festinhalt ist die Sendung des Geistes Gottes zu den Jüngern Jesu und seine bleibende Gegenwart in der Kirche. Der Pfingstsonntag ist der 50. Tag der Osterzeit.', # https://de.wikipedia.org/wiki/Pfingsten
        'Pfingstmontag':                    'Der Pfingstmontag wurde in einigen Ländern als zweiter Feiertag und Tag der früheren Pfingstoktav beibehalten, zählt aber nach der Liturgiereform formal nicht mehr zur Osterzeit, sondern bereits zur Zeit im Jahreskreis.', # https://de.wikipedia.org/wiki/Pfingsten#R%C3%B6mische_Praxis_seit_dem_2._Vatikanischen_Konzil
        'Fronleichnam':                    'Als Festgedanken gelten heute die Feier der Gegenwart Christi in der Eucharistie als „Sakrament der Einheit“ und der „Mitte, aus der wir leben“, das öffentliche Bekenntnis des Christseins und das Bild der pilgernden Kirche (Unterwegssein mit Christus), ferner die Segnung der Schöpfung, des Alltags und der Lebenswelt der Menschen.', # https://de.wikipedia.org/wiki/Fronleichnam
        'Aschermittwoch':                   'Mit dem Aschermittwoch beginnt in der Westkirche seit dem Pontifikat Gregors des Großen die vierzigtägige Fastenzeit.', # https://de.wikipedia.org/wiki/Aschermittwoch
        'Faschingsdienstag':                'Als letzter Tag vor dem Beginn der Fastenzeit am Aschermittwoch kommt ihm im Brauchtum oftmals eine besondere Bedeutung zu. In einigen Regionen, in denen Karneval gefeiert wird, stellt er den Höhepunkt der Feiertage dar. International ist dieser Tag auch als Mardi Gras („fetter Dienstag“) oder „Shrove“ oder „Pancake (Tues)day“ bekannt.', # https://de.wikipedia.org/wiki/Fastnachtsdienstag
        'Rosenmontag':                      'Der Rosenmontag ist insbesondere im Rheinland und Rheinhessen der Höhepunkt der Karnevalszeit.',
        'Silvester':                        'Als Silvester (regional auch Altjahrstag oder Altjahrestag) wird in einigen europäischen Sprachen der 31. Dezember, der letzte Tag des Jahres im gregorianischen Kalender, bezeichnet. Nach dem Heiligenkalender der römisch-katholischen Kirche ist dies der Gedenktag des heiligen Papstes Silvester I.', # https://de.wikipedia.org/wiki/Silvester
        'Buß- und Bettag':                  'Der Buß- und Bettag in Deutschland ist ein Feiertag der evangelischen Kirche, der auf Notzeiten zurückgeht. Im Lauf der Geschichte wurden Buß- und Bettage immer wieder aus aktuellem Anlass angesetzt. Angesichts von Notständen und Gefahren wurde die ganze Bevölkerung zu Umkehr und Gebet aufgerufen.', # https://de.wikipedia.org/wiki/Bu%C3%9F-_und_Bettag
        'Beginn Sommerzeit':                'Benjamin Franklin erklärte 1784 im Journal de Paris, dass das ausgedehnte Nachtleben Energie durch künstliches Licht vergeude. Dagegen helfe früheres Aufstehen und Zubettgehen. Die Idee einer staatlich verordneten Sommerzeit kam Ende des 19. Jahrhunderts auf.', # https://de.wikipedia.org/wiki/Sommerzeit#Geschichte
        'Beginn Winterzeit':                'Zur Unterscheidung von der Sommerzeit wird die „normalerweise“ als gesetzliche Zeit dienende Zonenzeit offiziell Normalzeit oder Standardzeit genannt, alternativ auch Winterzeit.', # https://de.wikipedia.org/wiki/Sommerzeit#Grundlagen
        'Muttertag':                        'Der Muttertag ist ein Tag zu Ehren der Mutter und der Mutterschaft. Er hat sich seit 1914, beginnend in den Vereinigten Staaten, in der westlichen Welt etabliert. [...] Die Ursprünge des Muttertags lassen sich bis zu den Verehrungsritualen der Göttin Rhea im antiken Griechenland sowie dem Kybele- und Attiskult bei den Römern zurückverfolgen. Der Muttertag in seiner heutigen Form wurde in der englischen und US-amerikanischen Frauenbewegung geprägt.', # https://de.wikipedia.org/wiki/Muttertag
        'Vierter Advent':                   '„Freut euch in dem Herrn allewege, und abermals sage ich: Freuet euch! [..] Der Herr ist nahe!“ Anders als bei den ersten drei Adventssonntagen scheint hier schon die (Vor-)Freude auf das Christfest durch.', # https://de.wikipedia.org/wiki/Advent#Advent_in_der_evangelischen_Kirche
        'Dritter Advent':                   '„Bereitet dem HERRN den Weg, denn siehe, der HERR kommt gewaltig.“ Im Mittelpunkt steht Johannes der Täufer als Wegbereiter Christi; als Evangelium wird das Benedictus gelesen.', # https://de.wikipedia.org/wiki/Advent#Advent_in_der_evangelischen_Kirche
        'Zweiter Advent':                   '„Steht auf und erhebt eure Häupter, weil sich eure Erlösung naht.“', # https://de.wikipedia.org/wiki/Advent#Advent_in_der_evangelischen_Kirche
        'Erster Advent':                    '„Siehe, dein König kommt zu dir, ein Gerechter und ein Helfer.“ Das Evangelium vom Einzug in Jerusalem prägt in Verbindung mit Psalm 24 den Sonntag, was sich in einigen Adventsliedern ausdrückt.', # https://de.wikipedia.org/wiki/Advent#Advent_in_der_evangelischen_Kirche
        'Totensonntag':                     'Der Totensonntag oder Ewigkeitssonntag ist in den evangelischen Kirchen in Deutschland und der Schweiz ein Gedenktag für die Verstorbenen.', # https://de.wikipedia.org/wiki/Totensonntag
        'Volkstrauertag':                   'Der Volkstrauertag ist in Deutschland ein staatlicher Gedenktag und gehört zu den sogenannten stillen Tagen. [...] Eine Zeremonie im Deutschen Bundestag erinnert an die Opfer von Gewalt und Krieg aller Nationen.', # https://de.wikipedia.org/wiki/Volkstrauertag
        }


def get_ostern(jahr: int) -> date:
    # https://de.wikipedia.org/wiki/Gau%C3%9Fsche_Osterformel#Eine_erg%C3%A4nzte_Osterformel
    k = jahr // 100
    m = 15 + (3*k + 3) // 4 - (8*k + 13) // 25
    s = 2 - (3*k + 3) // 4
    a = jahr % 19
    d = (19*a + m) % 30
    r = (d + a // 11) // 29
    og = 21 + d - r
    sz = 7 - (jahr + jahr // 4 + s) % 7
    oe = 7 - (og - sz) % 7
    res = og + oe
    return date(jahr, 3, 1) + timedelta(days=res-1)


def main():

    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    i = 1

    for jahr in range(2023, 2023+30):
        feiertage = {}
        feiertage['Neujahr'] = date(jahr, 1, 1)
        feiertage['Heilige Drei Könige'] = date(jahr, 1, 6)
        feiertage['Valentinstag'] = date(jahr, 2, 14)
        feiertage['Frauentag'] = date(jahr, 3, 8)
        feiertage['Tag der Arbeit'] = date(jahr, 5, 1)
        feiertage['Tag der Befreiung'] = date(jahr, 5, 8)
        feiertage['Internationaler Kindertag'] = date(jahr, 6, 1)
        feiertage['Augsburger Hohes Friedensfest'] = date(jahr, 8, 8)
        feiertage['Maria Himmelfahrt'] = date(jahr, 8, 15)
        feiertage['Weltkindertag'] = date(jahr, 9, 20)
        feiertage['Tag der Deutschen Einheit'] = date(jahr, 10, 3)
        feiertage['Reformationstag'] = date(jahr, 10, 31)
        feiertage['Allerheiligen'] = date(jahr, 11, 1)
        feiertage['Martinstag'] = date(jahr, 11, 11)
        feiertage['Nikolaustag'] = date(jahr, 12, 6)
        feiertage['Heiligabend'] = date(jahr, 12, 24)
        feiertage['Erster Weihnachtsfeiertag'] = date(jahr, 12, 25)
        feiertage['Zweiter Weihnachtsfeiertag'] = date(jahr, 12, 26)

        feiertage['Ostersonntag'] = get_ostern(jahr)
        feiertage['Palmsonntag'] = feiertage['Ostersonntag'] - timedelta(days=7)
        feiertage['Gründonnerstag'] = feiertage['Ostersonntag'] - timedelta(days=3)
        feiertage['Karfreitag'] = feiertage['Ostersonntag'] - timedelta(days=2)
        feiertage['Karsamstag'] = feiertage['Ostersonntag'] - timedelta(days=1)
        feiertage['Ostermontag'] = feiertage['Ostersonntag'] + timedelta(days=1)
        feiertage['Christi-Himmelfahrt'] = feiertage['Ostersonntag'] + timedelta(days=39)
        feiertage['Pfingstsonntag'] = feiertage['Ostersonntag'] + timedelta(days=49)
        feiertage['Pfingstmontag'] = feiertage['Pfingstsonntag'] + timedelta(days=1)
        feiertage['Fronleichnam'] = feiertage['Ostersonntag'] + timedelta(days=60)

        feiertage['Aschermittwoch'] = feiertage['Ostersonntag'] - timedelta(days=46)
        feiertage['Faschingsdienstag'] = feiertage['Aschermittwoch'] - timedelta(days=1)
        feiertage['Rosenmontag'] = feiertage['Aschermittwoch'] - timedelta(days=2)

        feiertage['Silvester'] = date(jahr, 12, 31)

        # Buß- und Bettag: Mittwoch vor dem 23.11.
        # 23.11.:   Montag:     -5 = (0 + 4) % 7) + 1) * -1
        #           Dienstag:   -6 = (1 + 4) % 7) + 1) * -1
        #           Mittwoch:   -7 = (2 + 4) % 7) + 1) * -1
        #           Donnerstag: -1 = (3 + 4) % 7) + 1) * -1
        #           Freitag:    -2
        #           Samstag:    -3
        #           Sonntag:    -4
        offset = ((date(jahr, 11, 23).weekday() + 4) % 7) + 1
        feiertage['Buß- und Bettag'] = date(jahr, 11, 23) - timedelta(days=offset)

        # Beginn Sommerzeit: letzter Sonntag im März
        # 31.3.: Sonntag:       0   (6 + 1) % 7) * -1
        # 31.3.: Montag:        -1  (0 + 1) % 7) * -1
        # 31.3.: Dienstag:      -2
        # 31.3.: Mittwoch:      -3
        # 31.3.: Donnerstag:    -4
        # 31.3.: Freitag:       -5
        # 31.3.: Samstag:       -6
        offset = ((date(jahr, 3, 31).weekday() + 1) % 7)
        feiertage['Beginn Sommerzeit'] = date(jahr, 3, 31) - timedelta(days=offset)

        # Ende Sommerzeit: letzter Sonntag im Oktober
        offset = ((date(jahr, 10, 31).weekday() + 1) % 7)
        feiertage['Beginn Winterzeit'] = date(jahr, 10, 31) - timedelta(days=offset)

        # Zweiter Sonntag im Mai: Muttertag
        # 1.5.: Sonntag:    0 + 7 = (6 - 6) + 7 = 13 - 6
        # 1.5.: Montag:     6 + 7 = (6 - 0) + 7 = 13 - 0
        # 1.5.: Dienstag:   5 + 7 = (6 - 1) + 7 = 13 - 1
        # 1.5.: Mittwoch:   4 + 7 = (6 - 2) + 7 = 13 - 2
        # 1.5.: Donnerstag: 3 + 7 = (6 - 3) + 7 = 13 - 3
        # 1.5.: Freitag:    2 + 7 = (6 - 4) + 7 = 13 - 4
        # 1.5.: Samstag:    1 + 7 = (6 - 5) + 7 = 13 - 5
        offset = 13 - date(jahr, 5, 1).weekday()
        feiertage['Muttertag'] = date(jahr, 5, 1) + timedelta(days=offset)

        # 1. - 4. Advent: die 4 Sonntage vor Weihnachten... (4. Advent kann auch der 24. sein!!!)
        # 4. Advent
        # 25.12.: Sonntag:      -7 = 0 - 7 = (6 - 6) - 7 = 6 + 1
        # 25.12.: Montag:       -1 = 6 - 7 = (6 - 0) - 7 = 0 + 1
        # 25.12.: Dienstag:     -2 = 5 - 7 = (6 - 1) - 7 = 1 + 1
        # 25.12.: Mittwoch:     -3 = 4 - 7 = (6 - 2) - 7 = 2 + 1
        # 25.12.: Donnerstag:   -4 = 3 - 7 = (6 - 3) - 7 = 3 + 1
        # 25.12.: Freitag:      -5 = 2 - 7 = (6 - 4) - 7 = 4 + 1
        # 25.12.: Samstag:      -6 = 1 - 7 = (6 - 5) - 7 = 5 + 1
        offset = date(jahr, 12, 25).weekday() + 1
        feiertage['Vierter Advent'] = date(jahr, 12, 25) - timedelta(days=offset)

        feiertage['Dritter Advent'] = feiertage['Vierter Advent'] - timedelta(days=7)
        feiertage['Zweiter Advent'] = feiertage['Dritter Advent'] - timedelta(days=7)
        feiertage['Erster Advent'] = feiertage['Zweiter Advent'] - timedelta(days=7)

        # Einen Sonntag vor 1. Advent: Totensonntag
        feiertage['Totensonntag'] = feiertage['Erster Advent'] - timedelta(days=7)

        # Zwei Sonntage vor 1. Advent: Volkstrauertag
        feiertage['Volkstrauertag'] = feiertage['Totensonntag'] - timedelta(days=7)

        for name, day in feiertage.items():
            ev = Event()

            ev.add('summary', name)
            ev.add('dtstart', day)
            ev.add('dtend', day + timedelta(days=1))
            ev.add('dtstamp', datetime.utcnow())
            ev.add('uid', i)
            i += 1
            if name not in beschreibungen.keys():
                print(f'WARNUNG: `{name}` hat keine Beschreibung!')
            else:
                ev.add('description', beschreibungen[name])

            cal.add_component(ev)


    with open('output.ics', 'wb') as f:
        f.write(cal.to_ical())

if __name__ == '__main__':
    main()
