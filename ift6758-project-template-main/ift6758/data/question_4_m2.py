import pandas as pd
import numpy as np
import math
import os

data = "tidy_df.csv"

def get_df(data):
    df = pd.read_csv(data)
    return df

def get_new_features(data_frame):
    df = data_frame
    df['game_seconds'] = df['period_time']
    df1 = df['game_seconds'].str.split(':',expand=True).astype(int)
    df['game_seconds'] = df1[0]*60+df1[1]
    df['game_seconds'] = ((df['period']-1)*(60*20) + df['game_seconds'])
    df['previous_event_game_seconds'] = df['previous_event_period_time']
    df2 = df['previous_event_game_seconds'].str.split(':',expand=True).astype(int)
    df['previous_event_game_seconds'] = df2[0]*60+df2[1]
    df['previous_event_game_seconds'] = ((df['previous_event_period']-1)*(60*20) + df['previous_event_game_seconds'])
    df['time_since_last_event'] = df['game_seconds']-df['previous_event_game_seconds']
    df['distance_from_last_event'] = np.sqrt((df['x_coordinates']**2 - df['previous_event_x_coordinates'])**2 + (df['y_coordinates'] - df['previous_event_y_coordinates'])**2)
    df['distance_from_last_event'] = df['distance_from_last_event'].round(decimals=2)
    df['distance_from_net'] = df['distance_from_net'].round(decimals=2)
    rebound = np.empty(len(df.index),dtype=bool)
    for index, row in df.iterrows():
        if row['previous_event_type']=='Shot':
            rebound[index]=True
        else:
            rebound[index]=False
    df['rebound'] = rebound.tolist()
    df['speed'] = (df['distance_from_last_event']/df['time_since_last_event']).round(decimals=2)
    
    return df

def get_angle_change(data_frame):
    df = data_frame
    list_angle = []
    for index, row in df.iterrows():
        if row['previous_event_type']=='Shot':
            if df.attacking_team_side[index] == "right":
                if df.previous_event_y_coordinates[index] == 0:
                    list_angle.append(np.absolute(df.angle_from_net[index]))
                else:
                    distance_from_net = np.sqrt(df.previous_event_y_coordinates[index]**2+df.previous_event_x_coordinates[index]**2)
                    angle = np.arcsin(df.previous_event_y_coordinates[index]/distance_from_net)*-180/math.pi
                    sign = np.sign([angle,df.angle_from_net[index]])
                    change_in_angle = 0
                    if sign[0]!=sign[1]:
                        change_in_angle = np.absolute(angle) + np.absolute(df.angle_from_net[index])
                    else:
                        change_in_angle = np.absolute(angle-df.angle_from_net[index])
                    list_angle.append(change_in_angle)
                    
            if df.attacking_team_side[index] == "left":
                if df.previous_event_y_coordinates[index] == 0:
                    list_angle.append(np.absolute(df.angle_from_net[index]))
                else:
                    distance_from_net = np.sqrt(df.previous_event_y_coordinates[index]**2+df.previous_event_x_coordinates[index]**2)
                    angle = np.arcsin(df.previous_event_y_coordinates[index]/distance_from_net)*180/math.pi
                    sign = np.sign([angle,df.angle_from_net[index]])
                    change_in_angle = 0
                    if sign[0]!=sign[1]:
                        change_in_angle = np.absolute(angle) + np.absolute(df.angle_from_net[index])
                    else:
                        change_in_angle = np.absolute(angle-df.angle_from_net[index])
                    list_angle.append(change_in_angle)  
        else:
            list_angle.append(0)
            
    df['change_in_angle'] = list_angle
    df['change_in_angle'] = df['change_in_angle'].round(decimals=2)
    
    return df

                    
                    

