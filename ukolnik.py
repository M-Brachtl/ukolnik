import time
from json import loads as jloads
from json import dump as jdump
# print(time.localtime())
# print(time.asctime(time.localtime()))
def czech_asctime(the_time: time.struct_time):
    return ("Pondělí","Úterý","Středa","Čtvrtek","Pátek","Sobota","Neděle")[the_time.tm_wday] + " " + str(the_time.tm_mday) + ". " + str(the_time.tm_mon) + ". " + str(the_time.tm_year)
def valid_date(date):
    try:
        day,month,year = date.split("/") # musí být ve formátu dd/mm/yy
        day,month,year = int(day),int(month),int(year)
    except ValueError:
        return False
    if len(date) != 8 or (day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)] or not month in range(1,13) or not day in range(1,32) or ((day,month) == (29,2) and year % 4 != 0):
        return False
    return True
class User:
    def __init__(self,name,ukolniky: list = []) -> None:
        self.name = name
        self.ukolniky: list[Ukolnik] = ukolniky
    def add_ukolnik(self,name):
        self.ukolniky.append(Ukolnik(name))
    def remove_ukolnik(self,ukolnik):
        self.ukolniky.remove(ukolnik)
    def check_all_deadlines(self):
        close_deadline: list[Ukol] = []
        past_deadline: list[Ukol] = []
        for ukolnik in user.ukolniky:
            for ukol in ukolnik.ukoly:
                check = ukol.deadline_check()
                if check: # pokud je string neprázdný, pak je deadline do 3 dnů
                    if not int(check): # pokud je číslo 0, pak je deadline 0-3 dny
                        close_deadline.append(ukol)
                    # případ, kdy je po deadlinu je ošetřen v rámci metody a náseldujícího řádku
            past_deadline += ukolnik.failed # přidá všechny úkoly, které jsou po deadlinu
        return (close_deadline,past_deadline)
    def __str__(self):
        return f"""Uživatel: {self.name}
Úkolníky: {'\n\t  '.join((ukolnik.name + " - Nesplněné úkoly: " + str(len(ukolnik.ukoly)) for ukolnik in self.ukolniky))}"""

class Ukol:
    def __init__(self,title,description,ukolnik,start_date,deadline,progress = 0) -> None:
        self.title: str = title
        self.description = description
        self.ukolnik: Ukolnik = ukolnik
        if isinstance(start_date,time.struct_time):
            self.start_date = start_date
        elif not valid_date(start_date):
            raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum. (start_date)")
        else:
            day,month,year = start_date.split("/")
            day,month,year = int(day),int(month),int(year)
            self.start_date = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        if not valid_date(deadline):
            raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum. (deadline)")
        day,month,year = deadline.split("/")
        day,month,year = int(day),int(month),int(year)
        self.deadline = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        self.progress = progress
        # self.difficulty = difficulty
    def move_deadline(self,deadline):
        try:
            day,month,year = deadline.split("/") # musí být ve formátu dd/mm/yy
            day,month,year = int(day),int(month),int(year)
        except ValueError:
            raise ValueError("Datum je zadáno v neplatném formátu.")
        if len(deadline) != 8 or (day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)] or not month in range(1,13) or not day in range(1,32) or ((day,month) == (29,2) and year % 4 != 0):
            raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum.")
        self.deadline = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        if self in self.ukolnik.failed:
            self.ukolnik.failed.remove(self)
            self.ukolnik.ukoly.append(self)
        self.deadline_check()
    def add_progress(self,change):
        self.progress += change
        if self.progress >= 100:
            self.progress = 100
            self.ukolnik.done.append(self)
            if self in self.ukolnik.ukoly:
                self.ukolnik.ukoly.remove(self)
            else:
                self.ukolnik.failed.remove(self)
        return self.progress
    def deadline_check(self): # -> ""/"0"/"1" = deadline > 3 dny/deadline 0-3 dny/deadline už uběhl
        if round((time.mktime(self.deadline) - time.mktime(time.localtime()))/86400) <= 3: # 86400 je počet sekund v jednom dnu, mktime vrací počet sekund od pevného počátku
            if round((time.mktime(self.deadline) - time.mktime(time.localtime()))/86400) < 0:
                #přemísti úkol z nedokončených do po deadlinu
                self.ukolnik.failed.append(self)
                self.ukolnik.ukoly.remove(self)
                return "1"
            else:
                return "0"
        return ""
    def __str__(self):
        return f"""\nJméno: {self.title} ({self.ukolnik.name})
Popis: {self.description}
Den začátku úkolu: {czech_asctime(self.start_date)}
Deadline: {czech_asctime(self.deadline)}
"""

class Ukolnik:
    def __init__(self,name,ukoly = None) -> None:
        self.name = name
        if ukoly is None:
            self.ukoly: list[Ukol] = []
        else:
            self.ukoly: list[Ukol] = ukoly
        self.done: list = []
        self.failed: list = []
    def add_ukol(self,title,description,deadline):
        self.ukoly.append(Ukol(title,description,self,time.localtime(),deadline))
        if self.name == "JSONing":
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    def delete_ukol(self,ukol: Ukol,ukol_list: list):
        ukol_list.remove(ukol)
    def __str__(self):
        return f"""{self.name}:
Nesplněné úkoly: {'\n\t' + '\n\t'.join((str(i+1) + ': ' + ukolek.title + ' - ' + str(ukolek.deadline.tm_mday) + ". " + str(ukolek.deadline.tm_mon) + ". " + str(ukolek.deadline.tm_year) for i, ukolek in enumerate(self.ukoly)))}
Dokončené úkoly: {'\n\t' + '\n\t'.join((str(i+self.list_lengths()[0]+1) + ': ' + ukolek.title for i, ukolek in enumerate(self.done)))}
Úkoly po deadlinu: {'\n\t' + '\n\t'.join((str(i+self.list_lengths()[0]+self.list_lengths()[1]+1) + ': ' + ukolek.title + ' - ' + str(ukolek.deadline.tm_mday) + ". " + str(ukolek.deadline.tm_mon) + ". " + str(ukolek.deadline.tm_year) for i, ukolek in enumerate(self.failed)))}
"""
    def list_lengths(self):
        return (len(self.ukoly),len(self.done),len(self.failed))
    

#start
choice = ''
while choice not in {'a','b'}:
    choice = input("Můžete založit nového uživatele (a) nebo načíst ze souboru 'ukolnik.json (b)")
if choice == "b":
    # načítání z JSON
    content: dict = jloads(open("ukolnik.json","r",encoding='utf-8').read())
    if content == {}:
        print("Nemáte žádný uložený JSON.")
    elif not isinstance(content,dict):
        print("Soubor ukolnik.json je poškozený.")
    else:
        user = User(content["name"])
        for ukolnik_data in content["ukolniky"]:
            ukolnik = Ukolnik(ukolnik_data["name"])
            for ukol_data in ukolnik_data["ukoly"]:
                ukol = Ukol(ukol_data["title"],ukol_data["description"],ukolnik,ukol_data["start_date"],ukol_data["deadline"],ukol_data["progress"])
                ukolnik.ukoly.append(ukol)
            for ukol_data in ukolnik_data["done"]:
                ukol = Ukol(ukol_data["title"],ukol_data["description"],ukolnik,ukol_data["start_date"],ukol_data["deadline"],ukol_data["progress"])
                ukolnik.done.append(ukol)
            for ukol_data in ukolnik_data["failed"]:
                ukol = Ukol(ukol_data["title"],ukol_data["description"],ukolnik,ukol_data["start_date"],ukol_data["deadline"],ukol_data["progress"])
                ukolnik.failed.append(ukol)
            user.ukolniky.append(ukolnik)
            del ukolnik
else:
    user = User(input("Zadejte jméno:"))

## testing
# user.ukolniky.append(Ukolnik("Testovanie",[]))
# user.ukolniky[0].add_ukol("BIGGO","Slouží k testování úkolu s blízkým deadlinem","22/01/25")
# user.ukolniky[0].add_ukol("Test2","Slouží k testování úkolu s dalekým deadlinem","20/02/25")
# user.ukolniky[0].add_ukol("Test3","Slouží k testování úkolu s uběhlým deadlinem","17/01/25")
##

print(f"\nVítejte {user.name}")
#kontrola blízkých deadlinů
if user.ukolniky == []:
    print("Nemáte žádné úkolníky. Založte si svůj první úkolník.")
    user.add_ukolnik(input("Zadejte jméno úkolníku."))
    print("Založili jste svůj první úkolník!")
else:
    close_deadline, past_deadline = user.check_all_deadlines()
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
                print(subcommand)
                subcommand = -1
        ukolnik = user.ukolniky[subcommand]
        try:
            ukolnik.add_ukol(input("Zadejte název úkolu: "),input("Zadejte popis úkolu: "),input("Zadejte datum deadlinu ve formátu dd/mm/yy: "))
            check = ukolnik.ukoly[-1].deadline_check()
            if check:
                if int(check):
                    print("Pozor, tento úkol už je po deadlinu!")
                else:
                    print("Pozor, tento úkol má deadline do tří dnů.")
        except ValueError as error:
            print(error) # neplatný formát atd. více v __int__ classy Ukol
    elif command == 2: # přidat úkolník
        command = -1
        user.add_ukolnik(input("Zadejte jméno úkolníku: "))
    elif command == 3: # progress
        command = -1
        subcommand = -1
        ukol_list_choice = (user.ukolniky[subcommand].ukoly,user.ukolniky[subcommand].failed)[bool(input("Pokud chcete měnit postup plnění u úkolu po deadlinu, napište 1. Jinak nepište nic. "))]
        while subcommand not in range(len(user.ukolniky)):
            try:
                print("Napište číslo úkolníku, ze kterého chcete úkol vybrat.")
                subcommand = int(input("\n".join([str(num+1) + " - " + ukolnik.name for num, ukolnik in enumerate(user.ukolniky)]) + "\n")) - 1
            except ValueError:
                subcommand = -1
        subcommand2 = -1
        while subcommand2 not in range(len(ukol_list_choice)):
            try:
                print("Napište číslo úkolu, který chcete upravit.")
                subcommand2 = int(input("\n".join([str(num+1) + " - " + ukol.title for num, ukol in enumerate(ukol_list_choice)]) + "\n")) - 1
            except ValueError:
                subcommand2 = -1
        ukol = ukol_list_choice[subcommand2]
        change = 0
        while not change:
            try:
                change = int(input(f"Zadejte, kolik % chcete přidat k dosavadnímu progresu úkolu ({ukol.progress})"))
            except ValueError:
                change = 0
        result = ukol.add_progress(change)
        if result < 100:
            print(f"Momentální úroveň splnění je {result} %.")
        else:
            print("Výborně! Úkol máte splněn!")
    elif command == 4: # kontrola deadlinů
        command = -1
        close_deadline, past_deadline = user.check_all_deadlines()
        if not close_deadline == []:
            print("\nMáte nesplněné úkoly, které mají deadline do 3 dnů!")
            for ukol in close_deadline:
                print(f"{ukol.title} - {ukol.ukolnik.name}: {czech_asctime(ukol.deadline)}")
        if not past_deadline == []:
            print("\nMáte nesplněné úkoly, které jsou po deadlinu!")
            for ukol in past_deadline:
                print(f"{ukol.title} - {ukol.ukolnik.name}: {czech_asctime(ukol.deadline)}")
        print()
    elif command == 5 or command == 7: #trvalý delete NEBO změna deadlinu
        command = -1
        subcommand = -1
        while subcommand not in range(len(user.ukolniky)):
            try:
                print("Napište číslo úkolníku, ze kterého chcete úkol vybrat.")
                subcommand = int(input("\n".join([str(num+1) + " - " + ukolnik.name for num, ukolnik in enumerate(user.ukolniky)]) + "\n")) - 1
            except ValueError:
                subcommand = -1
        subcommand2 = -1
        list_choice_command = -1
        while list_choice_command not in range(1,4):
            try:
                print("Napište číslo seznamu úkolů v úkolníku, ze kterého chcete úkol vybrat.")
                list_choice_command = int(input("""1 - Nesplněné úkoly
2 - Hotové úkoly
3 - Nesplěné úkoly po deadlinu"""))
            except ValueError:
                list_choice_command = -1
        ukol_list_choice = (user.ukolniky[subcommand].ukoly,user.ukolniky[subcommand].done,user.ukolniky[subcommand].failed)[list_choice_command-1]
        while subcommand2 not in range(len(ukol_list_choice)+1):
            try:
                print("Napište číslo úkolu.")
                subcommand2 = int(input("\n".join([str(num+1) + " - " + ukol.title for num, ukol in enumerate(ukol_list_choice)]) + "\n")) - 1
            except ValueError:
                subcommand2 = -1
        ukol: Ukol = ukol_list_choice[subcommand2]
        if command == 5:
            user.ukolniky[subcommand].delete_ukol(ukol,ukol_list_choice)
        else:
            try:
                ukol.move_deadline(input("Zadejte nové datum ve formátu dd/mm/yy: "))
            except ValueError as error:
                print(error)
    elif command == 6: #printování
        command = -1
        subcommand = -1
        while subcommand not in range(len(user.ukolniky)):
            try:
                print("Napište číslo úkolníku, do kterého chcete úkol přidat.")
                subcommand = int(input("\n".join([str(num+1) + " - " + ukolnik.name for num, ukolnik in enumerate(user.ukolniky)]) + "\n")) - 1
            except ValueError:
                subcommand = -1
        print(user.ukolniky[subcommand])
        list_lengths = user.ukolniky[subcommand].list_lengths()
        subcommand2 = -1
        while subcommand2 not in range(sum(list_lengths)+1):
            try:
                subcommand2 = int(input("Napište číslo úkolu, který chcete zobrazit. Pokud nechcete zobrazit žádný, napište 0. "))
            except ValueError:
                subcommand2 = -1
        if subcommand2:
            subcommand2 -= 1
            if subcommand2 < list_lengths[0]:
                print(user.ukolniky[subcommand].ukoly[subcommand2])
            elif subcommand2 < list_lengths[0]+list_lengths[1]:
                print(user.ukolniky[subcommand].done[subcommand2-list_lengths[0]])
            elif subcommand2 < sum(list_lengths):
                print(user.ukolniky[subcommand].failed[subcommand2-list_lengths[0]-list_lengths[1]])
    elif command == 8: # uložit
        command = 0
        content = {
            "name":user.name,
            "ukolniky":[
                {
                    "name":ukolnik.name,
                    "ukoly":[
                        {
                            "title":ukol.title,
                            "description":ukol.description,
                            "start_date":f"{ukol.start_date.tm_mday:02}/{ukol.start_date.tm_mon:02}/{ukol.start_date.tm_year-2000:02}",
                            "deadline":f"{ukol.deadline.tm_mday:02}/{ukol.deadline.tm_mon:02}/{ukol.deadline.tm_year-2000:02}",
                            "progress":ukol.progress
                        } for ukol in ukolnik.ukoly # projede po jednom úkoly a vyplní je
                    ],
                    "done":[
                        {
                            "title":ukol.title,
                            "description":ukol.description,
                            "start_date":f"{ukol.start_date.tm_mday:02}/{ukol.start_date.tm_mon:02}/{ukol.start_date.tm_year-2000:02}",
                            "deadline":f"{ukol.deadline.tm_mday:02}/{ukol.deadline.tm_mon:02}/{ukol.deadline.tm_year-2000:02}",
                            "progress":ukol.progress
                        } for ukol in ukolnik.done
                    ],
                    "failed":[
                        {
                            "title":ukol.title,
                            "description":ukol.description,
                            "start_date":f"{ukol.start_date.tm_mday:02}/{ukol.start_date.tm_mon:02}/{ukol.start_date.tm_year-2000:02}",
                            "deadline":f"{ukol.deadline.tm_mday:02}/{ukol.deadline.tm_mon:02}/{ukol.deadline.tm_year-2000:02}",
                            "progress":ukol.progress
                        } for ukol in ukolnik.failed
                    ]
                } for ukolnik in user.ukolniky
            ]
        }
        jdump(content,open("ukolnik.json","w",encoding='utf-8'))
    while command not in range(9):
        input("Pro návrat do menu zmáčkněte ENTER")
        try:
            command = int(input("""Zadejte příkaz:
            0 - ukončení programu
            1 - přidání nového úkolu
            2 - přidání nového ukolníku
            3 - změna úrovně postupu plnění úkolu
            4 - kontrola deadlinů
            5 - trvalé smazání úkolu
            6 - zobrazení úkolníku/úkolu
            7 - změna deadlinu
            8 - uložit a ukončit
            """))
        except ValueError:
            command = -1