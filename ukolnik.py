import time
# print(time.localtime())
# print(time.asctime(time.localtime()))
class User:
    def __init__(self,name,user_id,ukolniky) -> None:
        self.name = name
        self.user_id = user_id
        self.ukolniky = ukolniky
    def add_ukolnik(self,ukolnik):
        self.ukolniky.append(ukolnik)
    def remove_ukolnik(self,ukolnik):
        self.ukolniky.remove(ukolnik)
    def list_ukoly(self,ordering = "abc"): # abc, dead(line), start, diff
        return

class Ukol:
    def __init__(self,title,description,start_date,deadline,difficulty) -> None:
        self.title = title
        self.description = description
        self.start_date = start_date
        self.deadline = deadline
        self.progress = 0
        self.difficulty = difficulty
    def move_deadline(self):
        pass
    def add_progress(self):
        pass
    def all_info(self):
        return

class Ukolnik:
    def __init__(self,name) -> None:
        self.name = name
        self.ukoly = []
        self.done = []
        self.failed = []
    def add_ukol(self,title,description,deadline,difficulty):
        self.ukoly.append(Ukol(title,description,time.localtime(),deadline,difficulty))
    def delete_ukol(self,some_info):
        pass
    def load_from_JSON(self,filename):
        pass
    def list_ukoly(self,ordering = "abc"): # abc, dead(line), start, diff
        return
    def plot_it(self):
        pass
    def notification(self):
        pass
    def search(self,key):
        return
    
# try loading Ukolniky from ukolnik.json
# else create a new one
# Ukolnik(input("Zadejte jméno svého prvního Úkolníku."))