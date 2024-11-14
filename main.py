from flask import Flask, render_template, redirect, url_for, flash, request, session
import fdb
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'grupo2'

host = 'localhost'
database = r'C:\Users\Aluno\Desktop\siteFinanceiroBanco\BANCODADOS.FDB'
user = 'SYSDBA'
password = 'sysdba'

# Conexão
con = fdb.connect(host=host, database=database, user=user, password=password)

class Usuario:
    def __init__(self, id_usuario, nome, email, senha):
        self.id = id_usuario
        self.nome = nome
        self.email = email
        self.senha = senha

class Despesa:
    def __init__(self, id_usuario, id_despesa, nome, valor, data_despesa, descricao):
        self.id_usuario = id_usuario
        self.id_despesa = id_despesa
        self.nome = nome
        self.valor = valor
        self.data_despesa = data_despesa
        self.descricao = descricao


class Receita:
    def __init__(self, id_usuario, id_receita, nome, valor, data_receita, descricao):
        self.id_usuario = id_usuario
        self.id_receita = id_receita
        self.nome = nome
        self.valor = valor
        self.data_receita = data_receita
        self.descricao = descricao

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute("SELECT ID_DESPESA, NOME, VALOR, DATA_DESPESA, DESCRICAO FROM DESPESA")
    despesas = cursor.fetchall()
    cursor.execute("SELECT ID_RECEITA, NOME, VALOR, DATA_RECEITA, DESCRICAO FROM RECEITA")
    receitas = cursor.fetchall()
    cursor.close()
    return render_template('index.html', despesas=despesas, receitas=receitas)

@app.route('/cadastroDespesa')
def cadastroDespesa():
    cursor = con.cursor()
    cursor.execute("SELECT ID_DESPESA, NOME, VALOR, DATA_DESPESA, DESCRICAO FROM DESPESA")
    despesa = cursor.fetchall()
    cursor.close()
    return render_template('cadastroDespesa.html', despesa=despesa)


@app.route('/cadastroReceita')
def cadastroReceita():
    cursor = con.cursor()
    cursor.execute("SELECT ID_RECEITA, NOME, VALOR, DATA_RECEITA, DESCRICAO FROM RECEITA")
    receita = cursor.fetchall()
    cursor.close()
    return render_template('cadastroReceita.html', receita=receita)

@app.route('/criarDespesa', methods=['POST'])
def criarDespesa():
    nome = request.form['nome']
    valor = request.form['valor']
    data_despesa = request.form['data_despesa']
    descricao = request.form['descricao']
    cursor = con.cursor()
    try:
        cursor.execute("SELECT 1 FROM despesa WHERE VALOR = ?", (valor,))
        if cursor.fetchone():
            flash('Erro: O valor da despesa já foi cadastrado neste dia!', "error")
            return redirect(url_for('cadastroDespesa'))  # Corrigido aqui
        cursor.execute("INSERT INTO despesa (NOME, VALOR, DATA_DESPESA, DESCRICAO) VALUES (?, ?, ?, ?)",
                       (nome, valor, data_despesa, descricao))
        con.commit()
    except Exception as e:
        flash(f"Erro ao criar despesa: {e}", "error")
        return redirect(url_for('cadastroDespesa'))  # Corrigido aqui
    finally:
        cursor.close()
        flash("Despesa cadastrada com sucesso!", "success")
        return redirect(url_for('index'))  # Corrigido aqui

@app.route('/criarReceita', methods=['POST'])
def criarReceita():
    nome = request.form['nome']
    valor = request.form['valor']
    data_receita = request.form['data_receita']
    descricao = request.form['descricao']
    cursor = con.cursor()
    try:
        cursor.execute("SELECT 1 FROM receita WHERE NOME = ? AND DATA_RECEITA = ?", (nome, data_receita))
        if cursor.fetchone():
            flash('Erro: O valor da receita já foi cadastrado neste dia!', "error")
            return redirect(url_for('cadastroReceita'))  # Corrigido aqui
        cursor.execute("INSERT INTO receita (NOME, VALOR, DATA_RECEITA, DESCRICAO) VALUES (?, ?, ?, ?)",
                       (nome, valor, data_receita, descricao))
        con.commit()
    except Exception as e:
        flash(f"Erro ao criar receita: {e}", "error")
        return redirect(url_for('cadastroReceita'))  # Corrigido aqui
    finally:
        cursor.close()
        flash("Receita cadastrada com sucesso!", "success")
        return redirect(url_for('index'))  # Corrigido aqui

@app.route('/editarDespesa/<int:id>', methods=['GET', 'POST'])
def editarDespesa(id):
    cursor = con.cursor()
    cursor.execute("SELECT id_despesa, nome, valor, data_despesa, descricao FROM despesa WHERE id_despesa = ?", (id,))
    despesa = cursor.fetchone()
    if not despesa:
        cursor.close()
        flash("Despesa não encontrada", "error")
        return redirect(url_for('index'))  # Corrigido aqui
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        data_despesa = request.form['data_despesa']
        descricao = request.form['descricao']
        cursor.execute("UPDATE despesa SET nome = ?, valor = ?, data_despesa = ?, descricao = ? WHERE id_despesa = ?",
                       (nome, valor, data_despesa, descricao, id))
        con.commit()
        cursor.close()
        flash("Despesa atualizada com sucesso!", "success")
        return redirect(url_for('cadastroDespesa'))  # Corrigido aqui
    cursor.close()
    return render_template('editarDespesa.html', despesa=despesa, valor='Editar Despesa')

@app.route('/editarReceita/<int:id>', methods=['GET', 'POST'])
def editarReceita(id):
    cursor = con.cursor()
    cursor.execute("SELECT id_receita, nome, valor, data_receita, descricao FROM receita WHERE id_receita = ?", (id,))
    receita = cursor.fetchone()
    if not receita:
        cursor.close()
        flash("Receita não encontrada", "error")
        return redirect(url_for('index'))  # Corrigido aqui
    if request.method == 'POST':
        nome = request.form['nome']
        valor = request.form['valor']
        data_receita = request.form['data_receita']
        descricao = request.form['descricao']
        cursor.execute("UPDATE receita SET nome = ?, valor = ?, data_receita = ?, descricao = ? WHERE id_receita = ?",
                       (nome, valor, data_receita, descricao, id))
        con.commit()
        cursor.close()
        flash("Receita atualizada com sucesso!", "success")
        return redirect(url_for('cadastroReceita'))  # Corrigido aqui
    cursor.close()
    return render_template('editarReceita.html', receita=receita, valor='Editar Receita')

@app.route('/deletarDespesa/<int:id>', methods=['POST'])
def deletarDespesa(id):
    cursor = con.cursor()
    try:
        cursor.execute('DELETE FROM despesa WHERE id_despesa = ?', (id,))
        con.commit()
        flash("Despesa excluída com sucesso!", "success")
    except Exception as e:
        con.rollback()
        flash('Erro ao excluir despesa.', 'error')
    finally:
        cursor.close()
        return redirect(url_for('index'))  # Corrigido aqui

@app.route('/deletarReceita/<int:id>', methods=['POST'])
def deletarReceita(id):
    cursor = con.cursor()
    try:
        cursor.execute('DELETE FROM receita WHERE id_receita = ?', (id,))
        con.commit()
        flash("Receita excluída com sucesso!", "success")
    except Exception as e:
        con.rollback()
        flash('Erro ao excluir receita.', 'error')
    finally:
        cursor.close()
        return redirect(url_for('index'))  # Corrigido aqui

@app.route('/inicio', methods=['GET'])
def inicio():
    total_receita = 0
    total_despesa = 0
    total_perda_lucro = 0  # Inicialize a variável aqui

    if 'id_usuario' not in session:
        flash('Você precisa estar logado no sistema.')
        return redirect(url_for('login'))

    id_usuario = session['id_usuario']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT coalesce(VALOR,0) FROM RECEITA WHERE id_usuario = ?', (id_usuario,))
        for row in cursor.fetchall():
            total_receita += row[0]

        cursor.execute('SELECT coalesce(VALOR,0) FROM DESPESA WHERE id_usuario = ?', (id_usuario,))
        for row in cursor.fetchall():
            total_despesa += row[0]

        total_perda_lucro = total_receita - total_despesa  # Calcule o total_perda_lucro

    except Exception as e:
        total_receita = 0
        total_despesa = 0
        total_perda_lucro = 0  # Em caso de erro, garanta que o valor de total_perda_lucro seja 0
        print(f"Erro ao buscar total_receita: {str(e)}")
        print(f"Tipo do erro: {type(e)}")

    finally:
        cursor.close()

    # Formate as variáveis para exibição
    total_receita = f"{total_receita:.2f}"
    total_despesa = f"{total_despesa:.2f}"
    total_perda_lucro = f"{total_perda_lucro:.2f}"

    return render_template('index.html', total_receita=total_receita, total_despesa=total_despesa, total_perda_lucro=total_perda_lucro)


@app.route('/cria_usuario', methods=['GET'])
def cria_usuario():
    return render_template('cadastro.html')

# Rota para adicionar usuário
@app.route('/adiciona_usuario', methods=['POST'])
def adiciona_usuario():
    data = request.form
    nome = data['nome']
    email = data['email']
    senha = data['senha']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT FIRST 1 id_usuario FROM USUARIO WHERE EMAIL = ?', (email,))
        if cursor.fetchone() is not None:
            flash('Este email já está sendo usado!')
            return redirect(url_for('cria_usuario'))

        cursor.execute("INSERT INTO Usuario (nome, email, senha) VALUES (?, ?, ?)",
                       (nome, email, senha))
        con.commit()
    finally:
        cursor.close()
    flash('Usuario adicionado com sucesso!')
    return redirect(url_for('login.html'))

# Rota de Login
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        cursor = con.cursor()
        try:
            cursor.execute("SELECT id_usuario,nome FROM Usuario WHERE email = ? AND senha = ?", (email, senha,))
            usuario = cursor.fetchone()
        except Exception as e:
            flash(f'Erro ao acessar o banco de dados: {e}')  # Mensagem de erro para o usuário
            return redirect(url_for('login'))  # Redireciona de volta ao login
        finally:
            cursor.close()

        if usuario:
            session['id_usuario'] = usuario[0]  # Armazena o ID do usuário na sessão
            session['nome'] = usuario[1] #nome do mané
            return redirect(url_for('inicio'))
        else:
            flash('Email ou senha incorretos!')

    return render_template('login.html')

# Rota de Logout
@app.route('/logout')
def logout():
    session.pop('id_usuario', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
