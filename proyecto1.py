# -*- coding: utf-8 -*-
# ################################################################################################## #
# PROYECTO 1 - MINERÍA DE DATOS 																	 #
# DIEGO RESTREPO/ANDRES MOTTA/DAVID FAJARDO 														 #
# ################################################################################################## #

# ################################################################################################## #
# Packages reading																	 				 #														 #
# ################################################################################################## #
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import category_encoders as ce
import pickle
import os.path

# ################################################################################################## #
# Carga del modelo																	 				 #														 #
# ################################################################################################## #

encode = pickle.load( open( 'encoder2.sav', "rb" ) )
rf = pickle.load(open('rf.sav', 'rb'))

# ################################################################################################## #
# Visualización																	 				 	 #														 #
# ################################################################################################## #
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True

app.layout = html.Div(children=[
    html.Div([
        html.Div([##Título
            html.H1(children='CAR PRICING',style={'margin':'auto','width': "50%",'color': 'brown', 'fontSize': 40}),
            html.Div(children='''
                Aplicación para el cálculo del precio de vehículos usados'''
			,style={'margin':'auto','width': "40%",'color': 'brown', 'fontSize': 20}),
        ]),
    ],style={'width': '100%', 'display': 'inline-block','color': 'brown', 'fontSize': 40}),              
     html.Div([##Solicitud de información
               html.Label('Ingrese la siguiente información:'),
               html.Label('\n'),
             html.Div([##cuad1                                    
					html.Label('Marca del vehículo:'),
					dcc.Input(id='marca2',
						placeholder='Enter a value...',
						type='text',
						value='Ford'
					),
                    
                   html.Label('Dropdown'),
                   dcc.Dropdown(id='marca',
                                options=[
                                         {'value': 'Nissan'},
                                         {'value': 'Chevrolet'},
                                         {'value': 'Hyundai'},
                                         {'value': 'Jeep'},
                                         {'value': 'Ford'},
                                         {'value': 'Kia'},
                                         {'value': 'Mercedes-Benz'},
                                         {'value': 'Dodge'},
                                         {'value': 'GMC'},
                                         {'value': 'Toyota'},
                                         {'value': 'Honda'},
                                         {'value': 'Volkswagen'},
                                         {'value': 'Cadillac'},
                                         {'value': 'Volvo'},
                                         {'value': 'BMW'},
                                         {'value': 'Subaru'},
                                         {'value': 'Chrysler'},
                                         {'value': 'Buick'},
                                         {'value': 'Ram'},
                                         {'value': 'Lexus'},
                                         {'value': 'Porsche'},
                                         {'value': 'Audi'},
                                         {'value': 'Lincoln'},
                                         {'value': 'MINI'},
                                         {'value': 'INFINITI'},
                                         {'value': 'Scion'},
                                         {'value': 'Land'},
                                         {'value': 'Acura'},
                                         {'value': 'Mazda'},
                                         {'value': 'Mercury'},
                                         {'value': 'Mitsubishi'},
                                         {'value': 'Pontiac'},
                                         {'value': 'Jaguar'},
                                         {'value': 'Bentley'},
                                         {'value': 'Suzuki'},
                                         {'value': 'FIAT'},
                                         {'value': 'Tesla'},
                                         {'value': 'Freightliner'},
                                         {'value': 'Saturn'}
                                         ],
                                value='Nissan'
                                ),
                       
                    html.Label(' '),
					html.Label('Modelo del vehículo:'),
					dcc.Input(id='modelo',
						placeholder='Enter a value...',
						type='text',
						value='EscapeFWD'
					),
                    html.Label(' '),
					html.Label('Año del vehículo:'),
					dcc.Input(id='year',
						placeholder='Enter a value...',
						type='number',
						value='2015'
					),
                    html.Label(' '),
					html.Label('Millaje del vehículo:'),
					dcc.Input(id='millas',
						placeholder='Enter a value...',
						type='number',
						value='23388'
					),
                    
                   html.Label('Dropdown'),
                   dcc.Dropdown(id='estado',
                                options=[
                                         {'label': 'Ohio', 'value': 'OH'},
                                         {'label': 'California', 'value': 'CA'},
                                         {'label': 'San Francisco', 'value': 'SF'}
                                         ],
                                value='OH'
                                ),
                       
                    html.Label(' '),
					html.Label('Estado:'),
					dcc.Input(id='estado2',
						placeholder='Enter a value...',
						type='text',
						value='OH'
					)			
            ],style={'margin':'auto','width': '50%', 'display': 'inline-block'}
            )             
    ]),
    html.Label(' '),
    html.Div([## Envío de información
           html.Label('Presione el botón para cargar su información'), 
            html.Button('BOTÓN DE CARGA', id='button',style={'margin':'auto','width': "20%", 'backgroundColor': 'yellow'})
    ]),
    html.Label(' '),
	html.Div([##Respuesta
					html.Div([ ##cuad3.1
						html.Label('El precio estimado es:'),
						html.Div([
							html.Div(id='precio_pred', style={'color': 'blue', 'fontSize': 30}),
						], style={'marginBottom': 50, 'marginTop': 25,'fontSize': 25})
					],style={'width': '20%', 'display': 'inline-block','fontSize': 18}
					) ##cierre cuad3.1
	]),##Respuesta
    html.Div(id = 'hidden_coords')                            
]
)

# ################################################################################################## #
# Interactividad																	 				 #														 #
# ################################################################################################## #

@app.callback(
     dash.dependencies.Output('precio_pred', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('marca', 'value'),
     dash.dependencies.State('modelo', 'value'),
     dash.dependencies.State('year', 'value'),
     dash.dependencies.State('millas', 'value'),
     dash.dependencies.State('estado', 'value'),
    ])

# ################################################################################################## #
# Predicción																	 				 	 #														 #
# ################################################################################################## #

def prediccion_precio (	n_clicks, marca,modelo,year, millas,estado):
	entrada_datos = {'Make':marca,'Mileage':millas,'Model':modelo,'Price':0,'State':estado,'Year':year, 'set':0} 
	print(entrada_datos)	
	df = pd.DataFrame(entrada_datos,index=[1])
	df = encode.transform(df)
	df.drop(['Price','set'],axis=1,inplace=True)
	precio_pred = rf.predict(df)	
	return np.round(precio_pred,2)


# ################################################################################################## #
# Deployment																	 				 	 #														 #
# ################################################################################################## #
if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True, host='0.0.0.0', port=8888)
