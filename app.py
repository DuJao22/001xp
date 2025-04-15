from flask import Flask, render_template, request, jsonify, url_for, redirect, session
from produtos_extraidos import produtos, produto_promocao
import sqlite3

app = Flask(__name__)
app.secret_key = 'E_MUITO_E_MASSA'  # Necessário para usar sessions

def criar_tabela_carrinho():
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS carrinho (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER,
            titulo TEXT,
            preco TEXT,
            quantidade INTEGER,
            imagem TEXT
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela_carrinho()

@app.route('/')
def index():
    return render_template("cacau2.html", produtos=produtos, produto_promocao=produto_promocao)

@app.route('/adicionar_carrinho', methods=['POST'])
def adicionar_carrinho():
    data = request.get_json()

    produto_id = data.get('id')
    
    titulo = data.get('titulo')
    preco = data.get('preco')
    print(preco)
    imagem = data.get('imagem')
    quantidade = data.get('quantidade', 1)

    conn = sqlite3.connect('banco.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO carrinho (produto_id, titulo, preco, quantidade, imagem)
        VALUES (?, ?, ?, ?, ?)
    ''', (produto_id, titulo, preco, quantidade, imagem))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Produto adicionado com sucesso!'})

@app.route('/quantidade_carrinho')
def quantidade_carrinho():
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()
    c.execute('SELECT SUM(quantidade) FROM carrinho')
    total = c.fetchone()[0]
    conn.close()
    return jsonify({'quantidade': total or 0})

@app.route('/carrinho')
def carrinho():
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()
    c.execute("SELECT id, produto_id, titulo, preco, quantidade, imagem FROM carrinho")
    carrinho_itens = c.fetchall()
    conn.close()

    carrinho_detalhado = []
    total = 0.0

    for item in carrinho_itens:
        id_carrinho, produto_id, titulo, preco, quantidade, imagem = item

        # Converter preço string para float
        try:
            preco_float = float(str(preco).replace('R$', '').replace('.', '').replace(',', '.').strip())
        except:
            preco_float = 0.0

        subtotal = preco_float * quantidade
        total += subtotal

        # Procurar informações adicionais do produto
        produto_info = next((p for p in produtos if p['id'] == produto_id), None)
        preco_antigo = produto_info.get('preco_antigo') if produto_info else None
        etiquetas = produto_info.get('etiquetas', []) if produto_info else []

        carrinho_detalhado.append({
            "id_carrinho": id_carrinho,
            "produto_id": produto_id,
            "titulo": titulo,
            "preco": preco_float,
            "quantidade": quantidade,
            "imagem": imagem,
            "preco_antigo": preco_antigo,
            "etiquetas": etiquetas,
            "subtotal": subtotal
        })

    total = round(total, 2)
    return render_template("venda.html", carrinho=carrinho_detalhado, total=total)


@app.route('/remover_carrinho/<int:id>', methods=["POST"])
def remover_carrinho(id):
    conn = sqlite3.connect('banco.db')
    c = conn.cursor()
    c.execute("DELETE FROM carrinho WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/carrinho')

@app.route('/alterar_quantidade/<int:id>', methods=["POST"])
def alterar_quantidade(id):
    acao = request.form.get("acao")
    quantidade = int(request.form.get("quantidade"))

    if acao == "aumentar":
        quantidade += 1
    elif acao == "diminuir" and quantidade > 1:
        quantidade -= 1

    conn = sqlite3.connect('banco.db')
    c = conn.cursor()
    c.execute("UPDATE carrinho SET quantidade=? WHERE id=?", (quantidade, id))
    conn.commit()
    conn.close()
    return redirect('/carrinho')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
