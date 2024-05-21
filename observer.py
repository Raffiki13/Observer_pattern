import json

class Lot:
    '''
	Класс, описывающий лот аукциона
	
    :param name: Имя лота
    :type name: str
    :param price: Цена лота
    :type price: int
	'''
    def __init__(self, name, price):
        '''
        Конструктор
        '''
        self.name = name
        self.price = price
        self.observers = []
    
    def notify_new_price(self):
        '''
        Уведомление всех наблюлдателей, что цена изменилась
        '''
        for observer in self.observers:
            observer.update_new_price(self)
    
    def notify_new_participant(self):
        '''
        Уведомление всех наблюдателей, что появился новый наблюдатель
        '''
        for observer in self.observers:
            observer.update_new_participant(self)
    
    def attach(self, observer):
        '''
        Добавление нового наблюдателя
        '''
        if observer not in self.observers:
            self.observers.append(observer)

    def remove(self, observer):
        '''
        Удаление наблюдателя
        '''
        if observer in self.observers:
            self.observers.remove(observer)

class Observer:
    '''
    Класс описывающий наблюдателя

    :param name: Имя наблюдателя
    :type name: str
    '''
    def __init__(self, name):
        '''
        Конструктор
        '''
        self.name = name

    def update_new_price(self, lot):
        '''
        Уведомление надбюдателя, что установлена новая цена на лот
        '''
        print(f'Dear {self.name}, there is a new price for {lot.name} is {lot.price}')
    
    def update_new_participant(self, lot):
        '''
        Уведомление наблюдателя, что появился новый участник аукциона на этот лот
        '''
        print(f'Dear {self.name}, there is a new participant of auction')

class Auction:
    '''
    Класс описывающий аукцион

    :param lots: Список всех лотов аукциона
    :type lots: list
    '''
    def __init__(self):
        '''
        Конструктор
        '''
        with open("lots.json", "r") as f:
            self.lots = [Lot(lot['name'], lot['price']) for lot in json.load(f)]
        
    def set_new_price_for_lot(self, lot_name, new_price):
        '''
        Установка новой цены на лот
        lot_name - имя лота, на который надо поставить новую цену new_price
        Если такой лот не нашелся, выводится сообщение, что такого лота нет
        '''
        flag = False
        for lot in self.lots:
            if lot.name == lot_name:
                flag = True
                lot.price = new_price
                lot.notify_new_price()
        if not flag:
            print(f'No lot with this name: {lot_name}')

    def print_lots(self):
        '''
        Вывод всех лотов аукциона
        '''
        for lot in self.lots:
            print(f'Lot {lot.name} has price {lot.price}')
    
    def add_observer(self, lot_name, observer):
        '''
        Добавление наблюдателя на определенный лот
        Ищется лот с lot_name и к нему добавляется observer
        Если, такой лот нашелся, для каждого наблюдателя лота, будет выведено сообщение, что появился новый участник
        '''
        for lot in self.lots:
            if lot.name == lot_name:
                lot.notify_new_participant()
                lot.attach(observer)


#Пример использования
auc = Auction()
auc.print_lots()
obs = Observer("Ivan")
auc.add_observer("automobile", obs)
auc.set_new_price_for_lot("automobile", 3000)
obs2 = Observer("Alex")
auc.add_observer("automobile", obs2)
obs3 = Observer("Mary")
auc.add_observer("automobile", obs3)
auc.set_new_price_for_lot("automobile", 5000)
auc.print_lots()
