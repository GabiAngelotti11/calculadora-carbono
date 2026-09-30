from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------------------------------------
# DICIONÁRIOS DE SUPORTE
# -------------------------------------------------------------
FATORES_EMISSAO = {
    'pe_bike': 0.00,
    'carro_eletrico': 0.05,
    'onibus': 0.07,
    'moto': 0.10,
    'carro_gasolina': 0.20
}

NOMES_TRANSPORTE = {
    'pe_bike': 'Bicicleta ou a pé',
    'carro_eletrico': 'Carro elétrico',
    'onibus': 'Ônibus (por passageiro)',
    'moto': 'Moto',
    'carro_gasolina': 'Carro a gasolina'
}

@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# Aceita tanto /calcular como /calcular/ sem dar erro 404
@app.route('/calcular', methods=['GET', 'POST'])
@app.route('/calcular/', methods=['GET', 'POST'])
def calcular():
    erros = []
    resultado = None
    
    dados_form = {
        'distancia': '',
        'dias': '',
        'transporte': ''
    }

    if request.method == 'POST':
        # Captura os dados brutos (texto) enviados do HTML
        distancia_str = request.form.get('distancia', '').strip()
        dias_str = request.form.get('dias', '').strip()
        transporte = request.form.get('transporte', '').strip()

        # Guarda no dicionário para manter os campos preenchidos
        dados_form['distancia'] = distancia_str
        dados_form['dias'] = dias_str
        dados_form['transporte'] = transporte

        distancia_num = None
        dias_num = None

        # 1. Validação da Distância
        if not distancia_str:
            erros.append('Informe a distância percorrida por dia.')
        else:
            try:
                distancia_num = float(distancia_str.replace(',', '.'))
                if distancia_num <= 0:
                    erros.append('A distância diária deve ser maior que 0.')
            except ValueError:
                erros.append('A distância diária deve ser um valor numérico válido.')

        # 2. Validação dos Dias da Semana
        if not dias_str:
            erros.append('Informe a quantidade de dias de deslocamento por semana.')
        else:
            try:
                dias_num = int(dias_str)
                if dias_num < 1 or dias_num > 7:
                    erros.append('Os dias de deslocamento por semana devem estar entre 1 e 7.')
            except ValueError:
                erros.append('Os dias de deslocamento devem ser um número inteiro.')

        # 3. Validação do Meio de Transporte
        if not transporte:
            erros.append('Selecione um meio de transporte.')
        elif transporte not in FATORES_EMISSAO:
            erros.append('Meio de transporte inválido.')

        # Cálculo e classificação se não houver erros
        if not erros:
            km_mes = distancia_num * dias_num * 4
            fator = FATORES_EMISSAO[transporte]
            emissao_mensal = km_mes * fator

            # Classificação por faixas (if / elif / else)
            if emissao_mensal <= 20.0:
                faixa = 'Baixo impacto'
                classe_alerta = 'alert-success'
                icone = '🟢'
            elif emissao_mensal <= 60.0:
                faixa = 'Impacto moderado'
                classe_alerta = 'alert-warning'
                icone = '🟡'
            elif emissao_mensal <= 120.0:
                faixa = 'Alto impacto'
                classe_alerta = 'alert-danger'
                icone = '🟠'
            else:
                faixa = 'Impacto crítico'
                classe_alerta = 'alert-dark'
                icone = '🔴'

            resultado = {
                'distancia': distancia_num,
                'dias': dias_num,
                'transporte_nome': NOMES_TRANSPORTE[transporte],
                'km_mes': km_mes,
                'emissao_mensal': emissao_mensal,
                'faixa': faixa,
                'classe_alerta': classe_alerta,
                'icone': icone
            }

    return render_template(
        'calcular.html',
        erros=erros,
        resultado=resultado,
        dados_form=dados_form
    )

if __name__ == '__main__':
    app.run(debug=True)