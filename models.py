class Usuario:
    def __init__(self, login, nome, senha):
        self.__login = login
        self.__nome = nome
        self.__senha = senha
        #self.__tipo = tipo

    @property
    def login(self):
        return self.__login

    @property
    def nome(self):
        return self.__nome

    @property
    def senha(self):
        return self.__senha

class Categoria:
    pass

class Item:
    pass