from flask import Flask, render_template, request

app = Flask(__name__)

# -------------------------------------------------------------
# 1. DICIONÁRIOS DE SUPORTE
# Guardam os valores e os nomes para não 'chumbar' texto no código
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

# Rotas simples do seu projeto
@app.route('/')
def pagina_inicial():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# -------------------------------------------------------------
# 2. ROTA DA CALCULADORA (Processa GET para exibir e POST para calcular)
# -------------------------------------------------------------
@app.route('/calcular', methods=['GET', 'POST'])
def calcular():
    erros = []
    resultado = None
    
    # Dicionário que guarda o que o usuário digitou para não perder o texto ao recarregar a tela
    dados_form = {
        'distancia': '',
        'dias_semana': '',
        'transporte': ''
    }

    if request.method == 'POST':
        # Passo A: Captura os valores digitados no formulário HTML (sempre chegam como texto/string)
        distancia = request.form.get('distancia', '').strip()
        dias = request.form.get('dias', '').strip()
        transporte = request.form.get('transporte', '').strip()

        # Salva em dados_form para reenviar ao HTML
        dados_form['distancia'] = distancia
        dados_form['dias'] = dias
        dados_form['transporte'] = transporte

        distancia = None
        dias = None

        # -------------------------------------------------------------
        # Passo B: VALIDAÇÃO NO SERVIDOR (Acumula erros na lista 'erros')
        # -------------------------------------------------------------
        
        # Validação 1: Distância
        if not distancia:
            erros.append('Informe a distância percorrida por dia.')
        else:
            try:
                # Troca vírgula por ponto (ex: '12,5' vira '12.5') antes de converter
                distancia = float(distancia.replace(',', '.'))
                if distancia <= 0:
                    erros.append('A distância diária deve ser maior que 0.')
            except ValueError:
                erros.append('A distância diária deve ser um valor numérico válido.')

        # Validação 2: Dias da Semana
        if not dias:
            erros.append('Informe a quantidade de dias de deslocamento por semana.')
        else:
            try:
                dias = int(dias)
                if dias < 1 or dias > 7:
                    erros.append('Os dias de deslocamento por semana devem estar entre 1 e 7.')
            except ValueError:
                erros.append('Os dias de deslocamento devem ser um número inteiro.')

        # Validação 3: Meio de Transporte
        if not transporte:
            erros.append('Selecione um meio de transporte.')
        elif transporte not in FATORES_EMISSAO:
            erros.append('Meio de transporte inválido.')

        # -------------------------------------------------------------
        # Passo C: CÁLCULO E CLASSIFICAÇÃO (Só se NÃO houver nenhum erro)
        # -------------------------------------------------------------
        if not erros:
            # Fórmula pedida no simulado:
            km_mes = distancia * dias * 4
            fator = FATORES_EMISSAO[transporte]
            emissao_mensal = km_mes * fator

            # Classificação por faixas usando obrigatoriamente if / elif / else
            if emissao_mensal <= 20.0:
                faixa = 'Baixo impacto'
                classe_alerta = 'alert-success'  # Verde
                icone = '🟢'
            elif emissao_mensal <= 60.0:
                faixa = 'Impacto moderado'
                classe_alerta = 'alert-warning'  # Amarelo
                icone = '🟡'
            elif emissao_mensal <= 120.0:
                faixa = 'Alto impacto'
                classe_alerta = 'alert-danger'   # Laranja/Vermelho
                icone = '🟠'
            else:
                faixa = 'Impacto crítico'
                classe_alerta = 'alert-dark'     # Escuro/Crítico
                icone = '🔴'

            # Agrupa os resultados em um dicionário para enviar de forma organizada ao HTML
            resultado = {
                'distancia': distancia,
                'dias': dias,
                'transporte_nome': NOMES_TRANSPORTE[transporte],
                'km_mes': km_mes,
                'emissao_mensal': emissao_mensal,
                'faixa': faixa,
                'classe_alerta': classe_alerta,
                'icone': icone
            }

    # Devolve a página enviando as variáveis
    return render_template(
        'calcular.html',
        erros=erros,
        resultado=resultado,
        dados_form=dados_form
    )

if __name__ == '__main__':
    app.run(debug=True)