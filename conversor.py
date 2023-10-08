import dash
from dash import dcc, Input, Output, html, State
import dash_bootstrap_components as dbc
from styles import Styles

def parab10(num, bi):
    num = num[::-1]

    db = '0123456789abcdefghijklmnopqrstuvwxyz'[:bi+1]

    # Para base 10

    na10 = 0

    for idx_digito, digito in enumerate(num):

        if digito.isalpha():
            digito = digito.lower()

        for idx_db, db_digito in enumerate(db):
            if digito == db_digito:
                na10 += ((int(bi)**idx_digito)*int(idx_db))
    
    return na10

def parabf(na10, bf):

    # Para a base final (bf)

    db = '0123456789abcdefghijklmnopqrstuvwxyz'[:bf+1]

    nabf = ''

    while True:
        
        if na10 < bf:
            for idx_db, db_digito in enumerate(db):
                if str(na10) == str(idx_db):
                    nabf += db_digito.upper()
                    break
            break

        
        for idx_db, db_digito in enumerate(db):
            if idx_db == na10%bf:
                nabf += str(db_digito).upper()
                na10 = na10//bf
                break
    
    
    return [nabf[::-1]]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
 
    # Header
    html.Div([
        dbc.Label('Laboratório ICC', style=Styles.headerText)
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
     State('input-baseF', 'valid'),],
],prevent_initial_call = True,)
def converter(nclicks, num, bi, bf, valnum, valbasei, valbasef):

    if valnum and valbasei and valbasef:
        num, bi, bf = str(num), int(bi), int(bf)

        na10 = parab10(num,bi)
        nabf = parabf(na10, bf)

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
            if letra not in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
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