import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from vaccin_datahantering import Datahantering
from vaccin_database import Vaccin_database
from vaccin_visualization import Visual_extract

if __name__ == '__main__':
    
    user_vacc_path = "vaccin_covid.csv"
   
    
    data_vaccin = Datahantering(user_vacc_path)

    database_vaccin = Vaccin_database(data_vaccin)
    
    vaccin_visual_data = Visual_extract(database_vaccin.get_db_path())
    
    vaccin_visual_data._extract_country_data()

    vaccin_visual_data.plot_daily_vaccination()
    
       