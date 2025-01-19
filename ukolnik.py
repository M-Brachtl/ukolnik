import time
from json import loads as jloads
# print(time.localtime())
# print(time.asctime(time.localtime()))
def czech_asctime(the_time: time.struct_time):
    return ("Pondělí","Úterý","Středa","Čtvrtek","Pátek","Sobota","Neděle")[the_time.tm_wday] + " " + str(the_time.tm_mday) + ". " + str(the_time.tm_mon) + ". " + str(the_time.tm_year)
class User:
    def __init__(self,name,ukolniky: list = []) -> None:
        self.name = name
        self.ukolniky: list[Ukolnik] = ukolniky
    def add_ukolnik(self,name):
        self.ukolniky.append(Ukolnik(name))
    def remove_ukolnik(self,ukolnik):
        self.ukolniky.remove(ukolnik)
    def __str__(self):
        return f"""Uživatel: {self.name}
Úkolníky: {'\n\t  '.join((ukolnik.name + " - Nesplněné úkoly: " + str(len(ukolnik.ukoly)) for ukolnik in self.ukolniky))}"""

class Ukol:
    def __init__(self,title,description,ukolnik,start_date,deadline) -> None:
        self.title = title
        self.description = description
        self.ukolnik: Ukolnik = ukolnik
        # try:
        #     day,month,year = start_date.split("/") # musí být ve formátu dd/mm/yy
        #     day,month,year = int(day),int(month),int(year)
        # except KeyError:
        #     raise ValueError("Datum je zadáno v neplatném formátu.")
        # if len(start_date) != 8 or (day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)] or not month in range(1,13) or not day in range(1,32) or ((day,month) == (29,2) and year % 4 != 0):
        #     # print(len(start_date) == 8,(day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)],not month in range(1,13),not day in range(1,32),((day,month) == (29,2) and year % 4 != 0))
        #     raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum.")
        # self.start_date = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        self.start_date = start_date
        try:
            day,month,year = deadline.split("/") # musí být ve formátu dd/mm/yy
            day,month,year = int(day),int(month),int(year)
        except ValueError:
            raise ValueError("Datum je zadáno v neplatném formátu.")
        if len(deadline) != 8 or (day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)] or not month in range(1,13) or not day in range(1,32) or ((day,month) == (29,2) and year % 4 != 0):
            raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum.")
        self.deadline = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        self.progress = 0
        # self.difficulty = difficulty
    def move_deadline(self):
        pass
    def add_progress(self,change):
        pass
    def __str__(self):
        return f"""Jméno: {self.title} ({self.ukolnik})
Popis: {self.description}
Den začátku úkolu: {czech_asctime(self.start_date)}
Deadline: {czech_asctime(self.deadline)}
"""

class Ukolnik:
    def __init__(self,name,ukoly: list = []) -> None:
        self.name = name
        self.ukoly: list[Ukol] = ukoly
        self.done: list = []
        self.failed: list = []
    def add_ukol(self,title,description,deadline):
        self.ukoly.append(Ukol(title,description,self,time.localtime(),deadline))
    def delete_ukol(self,ukol):
        pass
    def load_from_JSON(self,filename):
        pass
    def __str__(self):
        return f"""{self.name}:
Nesplněné úkoly: {'\n\t' + '\n\t'.join((ukolek.title + ' - ' + str(ukolek.deadline.tm_mday) + ". " + str(ukolek.deadline.tm_mon) + ". " + str(ukolek.deadline.tm_year) for ukolek in self.ukoly))}
Dokončené úkoly: {'\n\t' + '\n\t'.join((ukolek.title for ukolek in self.ukoly))}
Úkoly po deadlinu: {'\n\t' + '\n\t'.join((ukolek.title + ' - ' + str(ukolek.deadline.tm_mday) + ". " + str(ukolek.deadline.tm_mon) + ". " + str(ukolek.deadline.tm_year) for ukolek in self.ukoly))}
"""
    def search(self,key):
        return
    

#start
choice = ''
while choice not in {'a','b'}:
    choice = input("Můžete založit nového uživatele (a) nebo načíst ze souboru 'ukolnik.json (b)")
if choice == "b":
    # načítání z JSON
    content = jloads(open("ukolnik.json","r",encoding='utf-8').read())
    if content == {}:
        print("Nemáte žádný uložený JSON.")
    elif not isinstance(content,dict):
        print("Soubor ukolnik.json je poškozený.")
    else:
        pass #načti ten json do objektů
else:
    user = User(input("Zadejte jméno:"))

## testing
user.ukolniky.append(Ukolnik("Testovanie",[]))
user.ukolniky[0].add_ukol("Test1","Slouží k testování úkolu s blízkým deadlinem","20/01/25")
user.ukolniky[0].add_ukol("Test2","Slouží k testování úkolu s dalekým deadlinem","20/02/25")
user.ukolniky[0].add_ukol("Test3","Slouží k testování úkolu s uběhlým deadlinem","17/01/25")
##

print(f"\nVítejte {user.name}")
#kontrola blízkých deadlinů
if user.ukolniky == []:
    print("Nemáte žádné úkolníky. Založte si svůj první úkolník.")
    user.add_ukolnik(input("Zadejte jméno úkolníku."))
    print("Založili jste svůj první úkolník!")
else:
    close_deadline: list[Ukol] = []
    past_deadline: list[Ukol] = []
    for ukolnik in user.ukolniky:
        for ukol in ukolnik.ukoly:
            if round((time.mktime(ukol.deadline) - time.mktime(time.localtime()))/86400) <= 3: # 86400 je počet sekund v jednom dnu, mktime vrací počet sekund od pevného počátku
                if round((time.mktime(ukol.deadline) - time.mktime(time.localtime()))/86400) < 0:
                    #přemísti úkol z nedokončených do po deadlinu
                    ukolnik.failed.append(ukol)
                    ukolnik.ukoly.remove(ukol)
                else:
                    close_deadline.append(ukol)
        past_deadline += ukolnik.failed # přidá všechny úkoly, které jsou po deadlinu
    if not close_deadline == []:
        print("\nMáte nesplněné úkoly, které mají deadline do 3 dnů!")
        for ukol in close_deadline:
            print(f"{ukol.title} - {ukol.ukolnik.name}: {czech_asctime(ukol.deadline)}")
    if not past_deadline == []:
        print("\nMáte nesplněné úkoly, které jsou po deadlinu!")
        for ukol in past_deadline:
            print(f"{ukol.title} - {ukol.ukolnik.name}: {czech_asctime(ukol.deadline)}")
    print()

# základní možnosti při ovládání
command = -1 # neutrální hodnota, která nemá za následek ukončení
while command:
    ##content
    if command == 1: # přidat úkol
        command = -1
        subcommand = -1
        while subcommand not in range(len(user.ukolniky)):
            try:
                print("Napište číslo úkolníku, do kterého chcete úkol přidat.")
                subcommand = int(input("\n".join([str(num+1) + " - " + ukolnik.name for num, ukolnik in enumerate(user.ukolniky)]) + "\n")) - 1
            except ValueError:
                subcommand = -1
        ukolnik = user.ukolniky[subcommand]
        try: ukolnik.add_ukol(input("Zadejte název úkolu: "),input("Zadejte popis úkolu: "),input("Zadejte datum deadlinu ve formátu dd/mm/yy: "))
        except ValueError as error:
            print(error) # neplatný formát atd. více v __int__ classy Ukol
    if content == 2: # přidat úkolník
        command = -1
        user.add_ukolnik(input("Zadejte jméno úkolníku: "))
    if content == 3: # progress
        command = -1
        subcommand = -1
        while subcommand not in range(len(user.ukolniky)):
            try:
                print("Napište číslo úkolníku, do kterého chcete úkol přidat.")
                subcommand = int(input("\n".join([str(num+1) + " - " + ukolnik.name for num, ukolnik in enumerate(user.ukolniky)]) + "\n")) - 1
            except ValueError:
                subcommand = -1
        subcommand2 = -1
        while subcommand2 not in range(len(user.ukolniky[subcommand])):
            try:
                print("Napište číslo úkolníku, do kterého chcete úkol přidat.")
                subcommand2 = int(input("\n".join([str(num+1) + " - " + ukol.title for num, ukol in enumerate(user.ukolniky[subcommand].ukoly)]) + "\n")) - 1
            except ValueError:
                subcommand2 = -1
        ukol = user.ukolniky[subcommand].ukoly[subcommand2]
        change = 0
        while not change:
            try:
                change = int(input(f"Zadejte, kolik chcete přidat k dosavadnímu progresu úkolu ({ukol.progress})"))
            except ValueError:
                change = 0
        ukol.add_progress(change)
    while command not in range(9):
        try:
            command = int(input("""Zadejte příkaz:
            0 - ukončení programu
            1 - přidání nového úkolu
            2 - přidání nového ukolníku
            3 - změna úrovně postupu plnění úkolu
            4 - trvalé smazání úkolu
            5 - změna deadlinu
            6 - nahrání Ukolníku samostatně ze souboru
            7 - uložit uživatele
            8 - uložit úkolník odděleně
            """))
        except ValueError:
            command = -1