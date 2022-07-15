from models import Usuario
SQL_SELECT_USUARIO_POR_LOGIN = "SELECT login, nome from usuario where login = '{}'"
SQL_USUARIO_AUTENTICACAO = "SELECT login, nome, senha from usuario where login = '{}'  and senha = md5('{}')"
SQL_SELECT_USUARIOS = "SELECT login, nome FROM usuario ORDER BY nome"
SQL_INSERT_USUARIO = "INSERT INTO usuario (login, nome, senha) VALUES ('{}', '{}', md5('{}'))"
SQL_DELETE_USUARIO = "DELETE FROM usuario WHERE login LIKE '{}'"
SQL_UPDATE_USUARIO = "UPDATE usuario SET nome = '{}' WHERE login = '{}' "
SQL_UPDATE_SENHA = "UPDATE usuario SET senha = md5('{}') WHERE login = '{}'"

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def autenticacao(self, login, senha):
        cursor = self.__db.connection.cursor()
        sql = SQL_USUARIO_AUTENTICACAO.format(login, senha)
        cursor.execute(sql)
        dados = cursor.fetchone()
        if(dados):
            usuario = Usuario(dados[0], dados[1], dados[2])#traduz_usuario(dados) if dados else None
        #Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
        else:
            usuario = None
        return usuario

    def busca_por_login(self, login):
        cursor = self.__db.connection.cursor()
        sql = SQL_SELECT_USUARIO_POR_LOGIN.format(login)
        cursor.execute(sql)
        dados = cursor.fetchone()
        usuario = Usuario(dados[0], dados[1], None)#traduz_usuario(dados) if dados else None
        #Usuario(tupla[0], tupla[1], tupla[2], tupla[3])
        return usuario

    def listar(self):
        cursor = self.__db.connection.cursor()
        #print(SQL_SELECT_USUARIOS)
        cursor.execute(SQL_SELECT_USUARIOS)
        usuarios = traduz_usuarios(cursor.fetchall())
        return usuarios

    def inserir(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_INSERT_USUARIO.format(usuario.login, usuario.nome, usuario.senha))
        self.__db.connection.commit()
        return usuario

    def atualizar(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_UPDATE_USUARIO.format(usuario.nome, usuario.login))
        self.__db.connection.commit()
        return usuario

    def atualizar_senha(self, usuario):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_UPDATE_SENHA.format(usuario.senha, usuario.login))
        self.__db.connection.commit()
        return usuario

    def deletar(self, login):
        self.__db.connection.cursor().execute(SQL_DELETE_USUARIO.format(login))
        self.__db.connection.commit()

    def iniciar_sessao(self, login):
        #self.__db.connection.cursor().execute(SQL_START_SESSION.format(login))
        self.__db.connection.cursor().callproc('p_start_session', [login])
        self.__db.connection.commit()

    def finalizar_sessao(self, login):
        #self.__db.connection.cursor().execute(SQL_END_SESSION.format(login))
        self.__db.connection.cursor().callproc('p_end_session', [login])
        self.__db.connection.commit()

def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])

def traduz_usuarios(usuarios):
    def cria_usuario_com_tupla(tupla):
        return Usuario(tupla[0], tupla[1], '')
    return list(map(cria_usuario_com_tupla, usuarios))
