from models import Usuario, Categoria, Item

FORMATO_DATA_INV = '%Y-%m-%d'
FORMATO_DATE = '%d/%m/%Y'

SQL_SELECT_USUARIO_POR_LOGIN = "SELECT login, nome from usuario where login = '{}'"
SQL_USUARIO_AUTENTICACAO = "SELECT login, nome, senha from usuario where login = '{}'  and senha = md5('{}')"
SQL_SELECT_USUARIOS = "SELECT login, nome FROM usuario ORDER BY nome"
SQL_INSERT_USUARIO = "INSERT INTO usuario (login, nome, senha) VALUES ('{}', '{}', md5('{}'))"
SQL_DELETE_USUARIO = "DELETE FROM usuario WHERE login LIKE '{}'"
SQL_UPDATE_USUARIO = "UPDATE usuario SET nome = '{}' WHERE login = '{}' "
SQL_UPDATE_SENHA = "UPDATE usuario SET senha = md5('{}') WHERE login = '{}'"

SQL_SELECT_CATEGORIA = "SELECT idCategoria, descricaoCategoria, ordemPainel FROM categoria ORDER BY ordemPainel"
SQL_INSERT_CATEGORIA = "INSERT INTO categoria(descricaoCategoria, ordemPainel) VALUES ('{}', {})"
SQL_UPDATE_CATEGORIA = "UPDATE categoria SET descricaoCategoria = '{}', ordemPainel = {} WHERE idCategoria = {}"
SQL_DELETE_CATEGORIA = "DELETE FROM categoria WHERE idCategoria = {}"
SQL_SELECT_CATEGORIA_POR_ID = "SELECT idCategoria, descricaoCategoria, ordemPainel FROM categoria WHERE idCategoria = {} ORDER BY ordemPainel"

SQL_SELECT_ITEM = "SELECT codigoItem, descricaoItem, " \
                  "DATE_FORMAT(dataAquisicao, '%d/%m/%Y') AS dataAquisicao, " \
                  "dataCadastro, tipoItem+0 AS tipoItem, nomeArquivo, extensaoArquivo, " \
                  "u.login, u.nome, u.senha, " \
                  "c.descricaoCategoria, c.ordemPainel, c.idCategoria " \
                  "FROM item " \
                  "INNER JOIN categoria c ON item.idCategoria = c.idCategoria " \
                  "INNER JOIN usuario u ON item.login = u.login " \
                  "ORDER BY c.ordemPainel, item.dataCadastro"
SQL_SELECT_ITEM_POR_ID = "SELECT codigoItem, descricaoItem, " \
                  "DATE_FORMAT(dataAquisicao, '%d/%m/%Y') AS dataAquisicao, " \
                  "dataCadastro, tipoItem+0 AS tipoItem, nomeArquivo, extensaoArquivo, " \
                  "u.login, u.nome, u.senha, " \
                  "c.descricaoCategoria, c.ordemPainel, c.idCategoria " \
                  "FROM item WHERE codigoItem = {} " \
                  "INNER JOIN categoria c ON item.idCategoria = c.idCategoria " \
                  "INNER JOIN usuario u ON item.login = u.login " \
                  "ORDER BY c.ordemPainel, item.dataCadastro"

SQL_INSERT_ITEM = "INSERT INTO item (descricaoItem, dataAquisicao, dataCadastro, tipoItem, nomeArquivo, extensaoArquivo, login, idCategoria) " \
                  "VALUES ('{}', {}, now(), {}, '{}', '{}', '{}', {})"

SQL_UPDATE_ITEM = "UPDATE item SET descricaoItem = '{}', dataAquisicao = {}, tipoItem = {}, " \
                  "nomeArquivo = '{}', extensaoArquivo = '{}', " \
                  "login = '{}', idCategoria = {} " \
                  "WHERE codigoItem = {}"
SQL_DELETE_ITEM = "DELETE FROM item WHERE codigoItem = {}"
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

class CategoriaDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, categoria):
        cursor = self.__db.connection.cursor()
        if (categoria.id):
            cursor.execute(SQL_UPDATE_CATEGORIA.format(categoria.desc.capitalize(), categoria.ordem, categoria.id))
        else:
            sql_insert = SQL_INSERT_CATEGORIA.format(categoria.desc.capitalize(), categoria.ordem)
            cursor.execute(sql_insert)
            categoria.id = cursor.lastrowid
        self.__db.connection.commit()
        return categoria

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SELECT_CATEGORIA)
        categorias = traduz_categorias(cursor.fetchall())
        return categorias

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SELECT_CATEGORIA_POR_ID.format(id,))
        tupla = cursor.fetchone()
        return Categoria(tupla[1], tupla[2], id=tupla[0])

    def deletar(self, id):
        sql_delete = SQL_DELETE_CATEGORIA.format(id,)
        self.__db.connection.cursor().execute(sql_delete)
        self.__db.connection.commit()

class ItemDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, item):
        cursor = self.__db.connection.cursor()
        data = """str_to_date('{}',{})""".format(item.data_aquisicao, FORMATO_DATA_INV)
        tipo_item = item.tipo
        if (tipo_item == None or tipo_item == ''):
            tipo_item == None

        if (item.codigo):
            sql_update_item = SQL_UPDATE_ITEM.format(item.desc, item.data_aquisicao, item.tipo, item.nome_arquivo, item.extensao_arquivo, item.usuario.login, item.categoria.id, item.id)
            cursor.execute(sql_update_item)
        else:
            sql_insert_item = SQL_INSERT_ITEM.format(item.desc, item.data_aquisicao, item.tipo, item.nome_arquivo, item.extensao_arquivo, item.usuario.login, item.categoria.id)
            cursor.execute(sql_insert_item)
            item.codigo = cursor.lastrowid
        self.__db.connection.commit()
        return item

    def listar(self):
        cursor = self.__db.connection.cursor()

        sql_recurso_lista = SQL_SELECT_ITEM

        #print(sql_recurso_lista)
        cursor.execute(sql_recurso_lista)
        itens = traduz_itens(cursor.fetchall())
        return itens

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        sql_recurso_id = SQL_SELECT_ITEM_POR_ID.format(FORMATO_DATA_INV, id)

        cursor.execute(sql_recurso_id)

        tupla = cursor.fetchone()
        return Item(tupla[1], tupla[2], tupla[3], tupla[4],tupla[5], tupla[6], Usuario(tupla[7], tupla[8], tupla[9]), Categoria(tupla[10], tupla[11], id=tupla[12]),id=tupla[0])

    def deletar(self, id):
        try:
            self.__db.connection.cursor().execute(SQL_DELETE_ITEM, (id, ))
            self.__db.connection.commit()
        except (self.__db.connection.Error) as e:
            return e


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])

def traduz_usuarios(usuarios):
    def cria_usuario_com_tupla(tupla):
        return Usuario(tupla[0], tupla[1], '')
    return list(map(cria_usuario_com_tupla, usuarios))

def traduz_categorias(categorias):
    def cria_categoria_com_tupla(tupla):
        return Categoria(tupla[1], tupla[2], id=tupla[0])
    return list(map(cria_categoria_com_tupla, categorias))

def traduz_itens(categorias):
    def cria_item_com_tupla(tupla):
        return Item(tupla[1], tupla[2], tupla[3], tupla[4],tupla[5], tupla[6], Usuario(tupla[7], tupla[8], tupla[9]), Categoria(tupla[10], tupla[11], id=tupla[12]),id=tupla[0])
    return list(map(cria_item_com_tupla, categorias))
