config = {

    #"api_key":'QHvkyX9fCPQ6P68nXyTSLqRaLkjtd3mul2PTJ7neiSoWDeceUSrfOUE9apMSVUFc',

    #"secret_key":"nKsPGSiU5vXyLWbQk9KmxCfxmRtPjKjiS2xwnFs3E9xDzfDElHZQbc7yWVR6fYQu",
    
    "api_key":'tOyXPMfuayT2xwhPsETFIgmXNfLDi44ULRJdPjejoWpsPYzN0149VUEajR2RxjqR',

    "secret_key":"Ggy0klNu9JOsPLDbhb7hMOQw20X5xo8Hi10Nv7jSg7asM2qvlVmEzkAjcQ5pXDHA",

    "estrategia":1, #Las estrategias actuales son 1-ADX+DI Y 2-DM+AROON

    "ventana" :14,  #Cantidad de dias con que se hara el promedio movil

    "ventanaAroon" : 5,

    "ventanaVWMA" : 14 ,

    "velaVWMA" : 'L' ,

    "stopLoss" : 0 , #1 para si 0 para no.
    
    "monedaSimulacion": 'BTC',  #moneda para simular y graficar ganancias.
    
    "umbralOptimizador":10, #umbral para optimizador

    "modo" : 1,  # 1 para simulacion, 2 para bot

    "fechaInicio" : "1 Jan , 2017",
   
    "fechaFinal"  : ""	,	 #los meses son en inglés, JAN FEB MAR APR MAY JUN JUL AUG SEP NOV DIC

    "capitalSimulacion" : 0.001, #Posicion a invertir para la optimizacion del portafolio
    
    "MonedaBase": 'USDT', #Moneda base con cual se realizaran los Trades. USDT, BTC, ETH, etc..

    'monedas': ['POE'],#'BNB','MANA','BCN'],#,'BNB','XVG','XRP','EOS','ADA','NEO','ICX','BCC','NANO','IOST','BNB','TRX','ONT'],

    'posicion' : 0.0012,  # posicion

    'interval' : '4',
        
    'frame' : 'h',

    'retraso' : 2, # CANTIDAD DE MINUTOS ANTES DE ANALIZAR EL MERCADO
    
    "cron_intervals" : {'1':'*/1', "2": "*/2", '3' : '*/3','4':'*/4', '5': '*/5', '6':'*/6','7':'*/6','8':'*/8','9':'*/9','10':'*/10','15':'*/15','30':'*/30'} ,
    
    "email": "luisomar242@gmail.com",

    "email_password" : "omarhl$8",
    "destinatarios" : ["luisomar242@gmail.com","hermesramirezfonseca@gmail.com"]#"hermesramirezfonseca@gmail.com"


}



#avisar que el volumen esta subiendo 
