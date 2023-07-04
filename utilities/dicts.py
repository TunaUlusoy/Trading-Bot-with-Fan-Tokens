from datetime import datetime

teams = {"Lazio" : 487,
         "FC Porto" : 212,
         "Santos" : 128,
         "Galatasaray" : 645}

leagues = {"Italy" : 94,
           "Portugal" : 94,
           "Brazil" : 71,
           "Turkey" : 203}

symbols = {"Lazio" : "LAZIOTRY",         # Lazio       : 2021-10-21
           "FC Porto" : "PORTOTRY",      # Porto       : 2021-11-16
           "Santos" : "SANTOSTRY",       # Santos      : 2021-12-31
           "Galatasaray" : "GALTRY"}     # Galatasaray : 2022-05-06

startTimes = {"Lazio" : int(datetime(2021, 10, 21, 0, 0, 0).timestamp()*1000),       
              "FC Porto" : int(datetime(2021, 11, 16, 0, 0, 0).timestamp()*1000),    
              "Santos" : int(datetime(2021, 12, 31, 0, 0, 0).timestamp()*1000),      
              "Galatasaray" : int(datetime(2022, 5, 6, 0, 0, 0).timestamp()*1000)}