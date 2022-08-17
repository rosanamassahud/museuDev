from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
#from flask_weasyprint import HTML, render_pdf
#from weasyprint import HTML
import errorcode
from models import Usuario, Categoria
from dao import UsuarioDao, CategoriaDao


import time
from datetime import datetime, timedelta
#from helpers import recupera_imagem, deleta_arquivo
from app import server, db#, app_dash

#import json
import locale
locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
usuario_dao = UsuarioDao(db)
categoria_dao = CategoriaDao(db)

@server.route('/')
@server.route('/index')
def index():
    #lista = jogo_dao.listar()
    return render_template('index.html', titulo='Museu Virtual')

@server.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo='bla',proxima=proxima)

@server.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.method == 'POST' and 'usuario' in request.form and 'senha' in request.form:
        usuario = usuario_dao.autenticacao(request.form['usuario'], request.form['senha'])
        if usuario:
            #if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.login
            session['usuario_nome'] = usuario.nome
            #session['usuario_tipo'] = usuario.tipo
            usuario_dao.iniciar_sessao(usuario.login)
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            print(proxima_pagina)
            if proxima_pagina == '/' or proxima_pagina == '/index':
                proxima_pagina = url_for('home')
            return redirect(proxima_pagina)
        else:
            flash('Não logado, tente denovo!')
            return redirect(url_for('login'))

@server.route('/logout')
def logout():
    usuario_dao.finalizar_sessao(session['usuario_logado'])
    session.pop('usuario_logado')
    session.pop('usuario_nome')
    session.pop('id_propriedade',None)
    session.pop('nome_propriedade', None)
    '''
    session['usuario_logado'] = None
    session['usuario_nome'] = None
    session['id_propriedade'] = None
    session['nome_propriedade'] = None
    '''
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@server.route('/lista_usuarios')
def lista_usuarios():
    #id = session['id_propriedade']

    lista = usuario_dao.listar()
    tit_lista = 'Usuários do sistema'
    return render_template('lista_usuarios.html', titulo=tit_lista, lista=lista)

@server.route('/novo_usuario')
def novo_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo_usuario')))
    return render_template('novo_usuario.html', titulo='Cadastro de Usuários do Sistema')


@server.route('/criar_usuario', methods=['POST',])
def criar_usuario():
    login = request.form['loginUsuario']
    nome = request.form['nomeUsuario']
    senha = request.form['senhaUsuario']
    #tipo = request.form['tipo']
    usuario = Usuario(login, nome, senha)
    usuario = usuario_dao.inserir(usuario)
    flash('Usuário {} cadastrado com sucesso!'.format(usuario.nome))
    return redirect(url_for('lista_usuarios'))

@server.route('/deletar_usuario/<login>')
def deletar_usuario(login):
    usuario_dao.deletar(login)
    flash('Usuário removido com sucesso!')
    return redirect(url_for('lista_usuarios'))

@server.route('/editar_usuario/<login>')
def editar_usuario(login):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_usuario')))
    usuario = usuario_dao.busca_por_login(login)
    return render_template('editar_usuario.html', titulo='Editando usuário', usuario=usuario)

@server.route('/atualizar_usuario', methods=['POST',])
def atualizar_usuario():
    login = request.form['loginUsuario']
    nome = request.form['nomeUsuario']
    #tipo = request.form['tipo']
    usuario = Usuario(login, nome, None)
    usuario = usuario_dao.atualizar(usuario)
    return redirect(url_for('lista_usuarios'))

@server.route('/alterar_senha_usuario/<login>')
def alterar_senha_usuario(login):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_usuario')))
    usuario = usuario_dao.busca_por_login(login)
    return render_template('alterar_senha_usuario.html', titulo='Alteração de senha de usuário', usuario=usuario)

@server.route('/atualizar_senha', methods=['POST',])
def atualizar_senha():
    login = request.form['loginUsuario']
    senha = request.form['senhaUsuario']

    usuario = Usuario(login, None, senha)
    usuario = usuario_dao.atualizar_senha(usuario)
    return redirect(url_for('lista_usuarios'))

@server.route('/creditos')
def creditos():
    return render_template('creditos.html', titulo='Créditos')

@server.route('/home')
def home():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('/')))
    return render_template('sim_home.html', titulo='Sistema de Informação do Museu Virtual')

@server.route('/lista_categorias')
def lista_categorias():
    #id = session['id_propriedade']
    lista = categoria_dao.listar()
    tit_lista = 'Categorias'
    return render_template('lista_categorias.html', titulo=tit_lista, lista=lista)

@server.route('/nova_categoria')
def nova_categoria():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('nova_categoria')))
    return render_template('nova_categoria.html',
                           titulo='Cadastro de Categorias do Site')

@server.route('/criar_categoria', methods=['POST',])
def criar_categoria():
    desc = request.form['descCategoria']
    ordem = request.form['ordem']

    categoria = Categoria(desc,ordem)
    categoria = categoria_dao.salvar(categoria)
    flash('Categoria {} cadastrada com sucesso!'.format(categoria.desc))
    return redirect(url_for('lista_categorias'))

@server.route('/editar_categoria/<int:id>')
def editar_categoria(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar_categoria')))
    categoria = categoria_dao.busca_por_id(id)
    return render_template('editar_categoria.html', titulo='Editando categoria', categoria=categoria)

@server.route('/atualizar_categoria', methods=['POST',])
def atualizar_categoria():
    id = request.form['idCategoria']
    desc = request.form['descCategoria']
    ordem= request.form['ordem']

    categoria = Categoria(desc, ordem, id=id)
    categoria_dao.salvar(categoria)
    return redirect(url_for('lista_categorias'))

@server.route('/deletar_cultura/<int:id>')
def deletar_categoria(id):
    categoria_dao.deletar(id)
    flash('Categoria removida com sucesso!')
    return redirect(url_for('lista_categorias'))
