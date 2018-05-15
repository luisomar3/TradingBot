config = {

    "api_key":'AIc1YLwGtRDJzy4wpMRe7CcAUBxTMIIfT1ddhQOhTJbHRP2xqhMkIyt5EABHLPZt',

    "secret_key":"I3S3KFNBanZStUpXHhPKTgWAxHrUUtGgBjuU7XIL2Eb1bct83nKqEMucjfR6q7qe",

    "ventana" : 14,  #Cantidad de dias con que se hara el promedio movil
    
    "monedaSimulacion": 'IOTA',  #moneda para simular y graficar ganancias.

    "fechaInicio" : "1 APR, 2018",
   
    "fechaFinal"  : "30 APR, 2018 "	,	 #los meses son en inglés, JAN FEB MAR APR MAY JUN JUL AUG SEP NOV DIC

    "capitalSimulacion" : 1, #Posicion a invertir para la optimizacion del portafolio
    
    "MonedaBase": 'BTC', #Moneda base con cual se realizaran los Trades. USDT, BTC, ETH, etc..

    'monedas': ['ETH'],#,'BNB','XVG','XRP','EOS','ADA','NEO','ICX','BCC','NANO','IOST','BNB','TRX','ONT'],

    'interval' : '4h', #Los intervalos disponibles son : 1d 1h 1M (month) 30m etc.+

    'posicion' : 0.001,  #Porcentaje del capital para tomar posicion
    
    "cron_intervals" : {'1m':'*/1',"1h": "*/1", "2h": "*/2", '3h' : '*/3','4h':'*/4', '5h': '*/5', '6h':'*/6'} 


}


#avisar que el volumen esta subiendo 