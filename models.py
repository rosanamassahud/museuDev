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
    def __init__(self, desc, ordem, id= None):
        self.__desc = desc
        self.__ordem = ordem
        self.__id = id

    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def ordem(self):
        return self.__ordem

    @ordem.setter
    def ordem(self, ordem):
        self.__ordem = ordem

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

class Item:
    def __init__(self, desc, data_aquisicao, data_cadastro, tipo, nome_arquivo, extensao_arquivo, usuario, categoria, codigo = None):
        self.__codigo = codigo
        self.__desc = desc
        self.__data_aquisicao = data_aquisicao
        self.__data_cadastro = data_cadastro
        self.__tipo = tipo
        self.__nome_arquivo = nome_arquivo
        self.__extensao_arquivo = extensao_arquivo
        self.__usuario = usuario
        self.__categoria = categoria

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        self.__codigo = codigo

    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def data_aquisicao(self):
        return self.__data_aquisicao

    @data_aquisicao.setter
    def data_aquisicao(self, data_aquisicao):
        self.__data_aquisicao = data_aquisicao

    @property
    def data_cadastro(self):
        return self.__data_cadastro

    @data_cadastro.setter
    def data_cadastro(self, data_cadastro):
        self.__data_cadastro = data_cadastro

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        self.__tipo = tipo

    @property
    def nome_arquivo(self):
        return self.__nome_arquivo

    @nome_arquivo.setter
    def nome_arquivo(self, nome_arquivo):
        self.__nome_arquivo = nome_arquivo

    @property
    def extensao_arquivo(self):
        return self.__extensao_arquivo

    @extensao_arquivo.setter
    def extensao_arquivo(self, extensao_arquivo):
        self.__extensao_arquivo = extensao_arquivo

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario):
        self.__usuario = usuario

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        self.__categoria = categoria
