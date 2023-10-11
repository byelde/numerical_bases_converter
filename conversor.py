import dash
from dash import dcc, Input, Output, html, State
import dash_bootstrap_components as dbc
from styles import Styles

def parab10(num, bi):

    num = num.split('.')
    db = '0123456789abcdefghijklmnopqrstuvwxyz'
    na10 = 0

    
    num_int = num[0][::-1]

    for idx_digito, digito in enumerate(num_int):

        if digito.isalpha():
            digito = digito.lower()

        for idx_db, db_digito in enumerate(db):
            if digito == db_digito:
                na10 += ((int(bi)**idx_digito)*int(idx_db))
    

    if len(num) != 1:
        num_frac = num[1]

        for idx_digito, digito in enumerate(num_frac):

            if digito.isalpha():
                digito = digito.lower()

            for idx_db, digito_db in enumerate(db):
                if digito == digito_db:
                    na10 += (bi**(-(idx_digito+1)))*idx_db


    return na10

def parabf(na10, bf, qtde_digitos=4):

    # Para a base final (bf)

    db = '0123456789abcdefghijklmnopqrstuvwxyz'[:bf+1]
    parte_inteira = na10//1
    parte_frac = na10%1
    nabf = ''

    while True:
        
        if parte_inteira < bf:
            for idx_db, db_digito in enumerate(db):

                if str(int(parte_inteira)) == str(idx_db):
                    nabf += db_digito.upper()
                    break

            break

        
        for idx_db, db_digito in enumerate(db):

            if idx_db == parte_inteira%bf:
                nabf += str(db_digito).upper()
                parte_inteira = parte_inteira//bf
                break
            
    nabf = nabf[::-1]
    nabf += '.'

    for contador in range(qtde_digitos):

        parte_frac = parte_frac*bf
        pi_pf = str(int(parte_frac//1))

        for idx_db, db_digito in enumerate(db):

            if pi_pf == db_digito:
                nabf += str(idx_db).upper()

        parte_frac -= int(parte_frac//1)


    return nabf

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
 
    # Header
    html.Div([
        dbc.Label('Laboratório ICC', style=Styles.headerText),
        html.A([
            html.Img(src=r'assets/github_logo.png', alt='image', style={'width':'48px',})
        ], href='https://github.com/byelde/numerical_bases_converter', style={'padding-right':'1%'}),
    ], style=Styles.header),

    # Card
    html.Div([

        html.Div([
            
            # Title
            html.Div([

                html.Img(src=r'assets/logo.png', alt='image'),
                html.H3('Conversor de bases numéricas', style={'padding-left':'1%'})

            ], style=Styles.title),

            # Inputs
            html.Div([
                html.Div([

                    dbc.Label('Número:', style=Styles.inputsLabels),
                    dbc.Input(placeholder = 'Digite um valor inteiro', valid = False, id = 'input-num', type = 'text'),
                    dbc.FormText('*Valores entre as bases 2-36')

                ], style=Styles.inputs),

                html.Div([

                    dbc.Label('Base Inicial:', style=Styles.inputsLabels),
                    dbc.Input(placeholder = 'Digite um valor inteiro', valid = False, id = 'input-baseI', type = 'number'),
                    dbc.FormText('*Valor entre 2-36')

                ], style=Styles.inputs),

                html.Div([

                    dbc.Label('Base Final:', style=Styles.inputsLabels),
                    dbc.Input(placeholder = 'Digite um valor inteiro', valid = False, id = 'input-baseF', type = 'number'),
                    dbc.FormText('*Valor entre 2-36')
                ], style=Styles.inputs),

            ], style=Styles.inputsParent),

            # Buttons
            html.Div([

                html.Div([
                    dbc.Label(
                        'Qtde. digitos fracionários:',
                        style=Styles.inputsLabels
                    ),
                    dcc.Slider(
                        id='frac_picker',
                        min=1,
                        max=15,
                        step=1,
                        marks={ 1:'1', 3:'3', 6:'6', 9:'9', 12:'12', 15:'15' },
                        value=1,
                    ),
                ], style={'width':'20%'}),
                dbc.Button('CALCULAR', color = 'danger', id = 'Calcular', style=Styles.buttons, n_clicks=0),
                dbc.Button('RESETAR', color = 'danger', id = 'Resetar', outline = True, style=Styles.buttons, n_clicks=0)

            ], style=Styles.buttonsParent),

            # Output
            html.Div([

                dbc.Label(
                    'Resultado: ',
                    style=Styles.outputTitle
                ),
                dbc.Label(
                    children = 'Resultado',
                    id = 'output_result',
                    style=Styles.outputText
                )

            ], style=Styles.outputParent),

        ], style=Styles.cardChildren)

    ], style=Styles.card)

], style=Styles.page)

@app.callback([
    Output('output_result', 'children', allow_duplicate=True),
    [Input('Calcular','n_clicks'),
     State('input-num', 'value'),
     State('input-baseI', 'value'),
     State('input-baseF', 'value'),
     State('input-num', 'valid'),
     State('input-baseI', 'valid'),
     State('input-baseF', 'valid'),
     State('frac_picker', 'value')],
],prevent_initial_call = True,)
def converter(nclicks, num, bi, bf, valnum, valbasei, valbasef, qtde_frac):

    if valnum and valbasei and valbasef:
        num, bi, bf = str(num), int(bi), int(bf)

        na10 = parab10(num,bi)
        nabf = parabf(na10, bf, qtde_frac)

        return[nabf]

    
    else:
        return['Valores inválidos']

@app.callback([
    Output('input-num', 'value', allow_duplicate=True),
    Output('input-baseI', 'value', allow_duplicate=True),
    Output('input-baseF', 'value', allow_duplicate=True),
    Output('output_result', 'children'),
    Output('input-num', 'valid', allow_duplicate=True),
    Output('input-baseI', 'valid', allow_duplicate=True),
    Output('input-baseF', 'valid', allow_duplicate=True),
    [Input('Resetar', 'n_clicks')]
],prevent_initial_call = True,)
def reset(n_clicks):
    return (None, None, None, 'Resultado', False, False, False)

@app.callback([
    Output('input-num', 'valid'),
    Output('input-baseI', 'valid'),
    Output('input-baseF', 'valid'),
    [Input('input-num', 'value'),
     Input('input-baseI', 'value'),
     Input('input-baseF', 'value'),]
], prevent_initial_call = True)
def validateInputs(input_num, input_baseI, input_baseF):

    db = '0123456789abcdefghijklmnopqrstuvwxyz'

    try:
        retnum, retbasei, retbasef = True, True, True

        for letra in input_num:
            if letra not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.':
                retnum = False
                break
        
        if input_baseI not in range(2,37):
            retbasei = False
        
        if input_baseF not in range(2,37):
            retbasef = False

        return [retnum, retbasei, retbasef]

    except:
        return [False, False, False]

if __name__ == '__main__':
    app.run_server(debug = True)