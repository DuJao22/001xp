from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    produtos = [
        {
            "nome": "Ovo de Páscoa ao Leite Pantufa Ursinhos Carinhosos Ursinha Carinhosa G 170g",
            "imagem": "https://www.cacaushow.com.br/on/demandware.static/-/Sites-masterCatalog_CacauShow/default/dw26676210/medium/1003515_1.png",
            "preco_antigo": "179.99",
            "preco": "169.99",
            "etiquetas": [{"texto": "8 CACAUS", "cor": "500"}, {"texto": "Promoção de Páscoa", "cor": "100"}]
        },
        {
            "nome": "Ovo de Páscoa laCreme Mezzo ao Leite e Branco 200g",
            "imagem": "https://www.cacaushow.com.br/on/demandware.static/-/Sites-masterCatalog_CacauShow/default/dw6925db9f/medium/1002505_1.png",
            "preco": "49.99",
            "etiquetas": [{"texto": "8 CACAUS", "cor": "500"}, {"texto": "Promoção de Páscoa", "cor": "100"}]
        }
    ]
    return render_template("cacau2.html", produtos=produtos)


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=5000)
