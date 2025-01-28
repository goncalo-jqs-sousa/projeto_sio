from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    data = request.form
    print('Dados recebidos:')
    for key, value in data.items():
        print(f'Chave: {key}')
        # Divide o valor em cookies individuais
        cookies = value.split('; ')
        for cookie in cookies:
            # Verifica se o cookie contém '='
            if '=' in cookie:
                # Divide o cookie em nome e valor
                cookie_name, cookie_value = cookie.split('=')
                print(f'Nome do Cookie: {cookie_name}, Valor do Cookie: {cookie_value}')
            else:
                print(f'Cookie sem valor: {cookie}')
    return '', 200

if __name__ == '__main__':
    app.run(port=3000)