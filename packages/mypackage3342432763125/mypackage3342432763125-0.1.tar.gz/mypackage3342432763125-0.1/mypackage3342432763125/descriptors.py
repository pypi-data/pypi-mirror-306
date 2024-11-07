import math

class ShowAccess:
    def __set_name__(self, owner, name):
        self.name = name  # Сохраняем имя атрибута

    def __get__(self, instance, owner):
        value = instance.__dict__.get(self.name)
        print(f"Get {self.name} = {value}")
        return value

    def __set__(self, instance, value):
        print(f"Set {self.name} = {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        value = instance.__dict__.get(self.name)
        print(f"Delete {self.name} = {value}")
        del instance.__dict__[self.name]

class Circle:
    radius = ShowAccess()  # Используем дескриптор для управления атрибутом

    def __init__(self, radius):
        self.radius = radius  # Устанавливаем значение radius
    
    @property
    def area(self):
        return math.pi * self.radius ** 2

if __name__ == "__main__":  
    c = Circle(100)
    print(c.area)  # Вызовет __get__ дескриптора
    del c.radius  # Вызовет __delete__ дескриптора