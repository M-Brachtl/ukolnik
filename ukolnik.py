import time
# print(time.localtime())
# print(time.asctime(time.localtime()))
class User:
    def __init__(self,name,user_id,ukolniky: list = []) -> None:
        self.name = name
        self.user_id = user_id
        self.ukolniky = ukolniky # list[Ukol]
    def add_ukolnik(self,ukolnik):
        self.ukolniky.append(ukolnik)
    def remove_ukolnik(self,ukolnik):
        self.ukolniky.remove(ukolnik)
    def list_ukoly(self,ordering = "abc"): # abc, dead(line), start, diff
        return

class Ukol:
    def __init__(self,title,description,start_date,deadline) -> None:
        self.title = title
        self.description = description
        try:
            day,month,year = start_date.split("/") # musí být ve formátu dd/mm/yy
            day,month,year = int(day),int(month),int(year)
        except KeyError:
            raise ValueError("Datum je zadáno v neplatném formátu.")
        if len(start_date) != 8 or (day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)] or not month in range(1,13) or not day in range(1,32) or ((day,month) == (29,2) and year % 4 != 0):
            # print(len(start_date) == 8,(day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)],not month in range(1,13),not day in range(1,32),((day,month) == (29,2) and year % 4 != 0))
            raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum.")
        self.start_date = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        try:
            day,month,year = deadline.split("/") # musí být ve formátu dd/mm/yy
            day,month,year = int(day),int(month),int(year)
        except KeyError:
            raise ValueError("Datum je zadáno v neplatném formátu.")
        if len(deadline) != 8 or (day,month) in [(30,2),(31,2),(31,4),(31,6),(31,9),(31,11)] or not month in range(1,13) or not day in range(1,32) or ((day,month) == (29,2) and year % 4 != 0):
            raise ValueError("Datum je zadáno v neplatném formátu nebo jde o neexistující datum.")
        self.deadline = time.localtime(time.mktime(time.struct_time((2000+year,month,day,23,59,59,-1,-1,-1))))
        self.progress = 0
        # self.difficulty = difficulty
    def move_deadline(self):
        pass
    def add_progress(self):
        pass
    def __str__(self):
        return f"""    Jméno: {self.title}
        Popis: {self.description}
        Den začátku úkolu: {("Pondělí","Úterý","Středa","Čtvrtek","Pátek","Sobota","Neděle")[self.start_date.tm_wday] + " " + str(self.start_date.tm_mday) + ". " + str(self.start_date.tm_mon) + ". " + str(self.start_date.tm_year)}
        Deadline: {("Pondělí","Úterý","Středa","Čtvrtek","Pátek","Sobota","Neděle")[self.deadline.tm_wday] + " " + str(self.deadline.tm_mday) + ". " + str(self.deadline.tm_mon) + ". " + str(self.deadline.tm_year)}
"""

class Ukolnik:
    def __init__(self,name,ukoly: list = []) -> None:
        self.name = name
        self.ukoly = ukoly
        self.done = []
        self.failed = []
    def add_ukol(self,title,description,deadline,difficulty):
        self.ukoly.append(Ukol(title,description,time.localtime(),deadline,difficulty))
    def delete_ukol(self,some_info):
        pass
    def load_from_JSON(self,filename):
        pass
    def __str__(self):
        return f"""{self.name}:
Nesplněné úkoly: {'\n' + '\n\t'.join((ukolek.title + ' - ' + str(ukolek.deadline.tm_mday) + ". " + str(ukolek.deadline.tm_mon) + ". " + str(ukolek.deadline.tm_year) for ukolek in self.ukoly))}
Dokončené úkoly: {'\n' + '\n\t'.join((ukolek.title for ukolek in self.ukoly))}
Úkoly po deadlinu: {'\n' + '\n\t'.join((ukolek.title + ' - ' + str(ukolek.deadline.tm_mday) + ". " + str(ukolek.deadline.tm_mon) + ". " + str(ukolek.deadline.tm_year) for ukolek in self.ukoly))}
"""
    def plot_it(self):
        pass
    def notification(self):
        pass
    def search(self,key):
        return
    
# testing data

tester = User("Testér",0,[Ukolnik("CAD",[Ukol("Hák 2","Udělej druhý hák nebo to vezmi od Adama","10/01/25","25/01/25"),Ukol("Ryba","Rys vodního tvora, za pomoci kót inženýra Dudy","08/01/25","14/01/25")])])
print(tester.ukolniky[0])

# try loading Ukolniky from ukolnik.json
# else create a new one
# Ukolnik(input("Zadejte jméno svého prvního Úkolníku."))