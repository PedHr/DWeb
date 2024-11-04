from flask import Blueprint, render_template, request, redirect, url_for, flash
import mysql.connector
from config import Config, datacfg

contato = Blueprint('contato', __name__)

@contato.route('/')
def contatoPage():
    return render_template("contatos.html")

@contato.route("/addContato", methods=['POST'])
def adicionar_contato():
    if request.method == "POST":
        nome = request.form['nomeCompleto']
        email = request.form['email']
        telefone = request.form['telefone']
        texto = request.form['mensagem']
        
        sql = "INSERT INTO tb_contato (cont_nome, cont_email, cont_telefone, cont_mensagem) VALUES (%s, %s, %s, %s)"
        try:
            con = mysql.connector.connect(**datacfg)
            cur = con.cursor()
            cur.execute(sql, (nome, email, telefone, texto))
            con.commit()
            cur.close()
            con.close()
            flash('Contato adicionado com sucesso!', "success")
            return redirect(url_for('contato.contatoPage'))
        except mysql.connector.Error as erro:
            if erro.errno == 1062:
              flash('E-mail já cadastrado!', 'danger')
              cur.close()
              con.close()
              return redirect(url_for('contato.contatoPage')) 

@contato.route("/listarContatos")
def listarContatos():
  sql = "select * from tb_contato"
  con = mysql.connector.connect(**datacfg)
  cur = con.cursor()
  cur.execute(sql)
  contatos = cur.fetchall()
  print(contatos)
  cur.close()
  con.close()
  
  return render_template("contatosListagem.html", contatos = contatos)
