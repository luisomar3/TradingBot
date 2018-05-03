config = {

    "adx_window" : 18,
    
    "monedaSimulacion": 'ETH',

    "fechaInicio" : "1 Jan, 2018", #los meses son en inglés, JAN FEB MAR APR MAY JUN JUL AUG SEP NOV DIC

    "capitalSimulacion" : 1,
    
    "MonedaBase": 'BTC', #Moneda base con cual se realizaran los Trades. USDT, BTC, ETH, etc..

    'monedas': ['ETH'],#,'BNB','XVG','XRP','EOS','ADA','NEO','ICX','BCC','NANO','IOST','BNB','TRX','ONT'],

    'interval' : '8h', #Los intervalos disponibles son : 1d 1h 1M (month) 30m etc.+

    'capital' : 10,  #EL CAPITAL EXPRESADO EN BTC 
    
    "cron_intervals" : {"1m": "*/1", "1M": "*/5", 'thirtyMin' : '*/30','4h':'2', 'hour':'*/30 ','day':'*/1'} 


}