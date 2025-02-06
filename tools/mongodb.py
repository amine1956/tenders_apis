import pandas as pd 
from config_mongodb import Mycol 

def insert_data(final_df : pd.DataFrame) : 
    infos=final_df.to_dict('records')
    Mycol.insert_many(infos)    