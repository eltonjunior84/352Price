
import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Função para mapear as ligas
def map_to_band(league, mapping):
    for key, value in mapping.items():
        if league in key:
            return value
    return league

Origin_Lg = {
    (tuple(['Bundesliga ', 'Ligue 1', 'Ligue', 'English Premier League', 'Italian Serie A', 'Bundesliga', 'Ligue 1 ', 'La Liga ', 'La Liga'])): 'Band 1',
    (tuple(['Belgium First Division A', 'Primeira Liga de Portugal', 'English Championship', 'Eredivisie', 'Turkish Super Lig'])): 'Band 2',
    (tuple(['Brasileirao Serie A', 'Brasileirao SerieA', 'Primera Division Argentina', 'Russian Premier Liga', 'Liga MX', 'Scottish Premiership'])): 'Band 3',
    (tuple(['Croatian First League', 'Switzerland Super League', 'La Liga 2', 'Swiss Super League', 'Bundesliga 2',
             'Colombian Primera A', 'Major League Soccer', 'MLS', 'Austrian Bundesliga', 'Ligue 2 ', 'Ligue 2','Czech First League'])): 'Band 4',
    (tuple(['Danish Superligaen', 'Uruguayan Primera Division', 'Poland Ekstraklasa'])): 'Band 5',
    (tuple(['Ecuador Serie A', 'Italian Serie B', 'Brasileirao Serie B', 'Turkish Pro Lig', 'La Liga 3', 'Qatar Stars League',
            'English League One', 'Ukranian Premier Liga', 'Ecuatorian Liga Pro', 'MLS 3', 'Liga Portugal 2', 'Paraguay First Division',
            'Ligue 4', 'Brasileirao Serie C', 'England 3 ', 'Premier League 2','Italy 3', 'Belgium 2', 'France 3', 'France 5',
            'Eredivisie 2', 'Italian Serie C','Belgium 2 ', 'Ligue 3', 'Argentina 2', 'Bundesliga 3', 'Liga MX 2', 'Segunda Division Argentina',
            'Norway 1'])): 'Band 6'
}

Destination_Lg = {
    (tuple(['Bundesliga ', 'Ligue1', 'Ligue 1', 'Premier League', 'English Premier League', 'Italian Serie A', 'Italian Serie  A', 'Bundesliga', 'Ligue 1 ', 'La Liga'])): 'Band 1',
    (tuple(['Belgium First Division A', 'Primeira Liga de Portugal', 'English Championship', 'Eredivisie', 'Turkish Super Lig'])): 'Band 2',
    (tuple(['Brasileirao Serie A', 'Scottish Premiership', 'Brasileirao SerieA', 'Primera Division Argentina', 'Russian Premier Liga', 'Liga MX'])): 'Band 3',
    (tuple(['Croatian First League', 'Switzerland Super League', 'La Liga 2', 'Swiss Super League', 'Bundesliga 2', 'Colombian Primera A',
            'Major League Soccer', 'MLS', 'Austrian Bundesliga', 'Greece Super League ', 'Greek Superleague 1', 'Ligue 2 ', 'Ligue 2'])): 'Band 4',
    (tuple(['Danish Superligaen', 'Uruguayan Primera Division', 'Poland Ekstraklasa'])): 'Band 5',
    (tuple(['Ecuador Serie A', 'Italian Serie B', 'Brasileirao Serie B', 'Turkish Pro Lig', 'La Liga 3', 'Qatar Stars League',
            'English League One', 'Ukranian Premier Liga', 'Ecuatorian Liga Pro', 'MLS 3', 'Liga Portugal 2',
            'Paraguay First Division', 'Ligue 4', 'Brasileirao Serie C', 'Saudi Professional League', 'Hungary 1st', 'J League 1',
            'Egyptian Premier League', 'France 3', 'Cyprus 1', 'Sweden 1', 'Italian Serie C', 'England 3'])): 'Band 6'
}

# User Interface
st.title("Football Player Transfer Fees Evaluation")
st.sidebar.header("Enter Player Attributes and Historic Data")

# User Inputs
age = st.sidebar.number_input("Age", min_value=10, max_value=50, step=1, value=25)
height = st.sidebar.number_input("Height (cm)", min_value=140, max_value=210, step=1, value=180)
league_origin = st.sidebar.selectbox("Origin League", list(Origin_Lg.keys()))
league_dest = st.sidebar.selectbox("Destination League", list(Destination_Lg.keys()))
deal_type = st.sidebar.selectbox("Deal Type", ["Free", "Transfer"])
Position = st.sidebar.selectbox("Position", ["DF", "FB", "DM", "MF", "AM", "WR", "FW"])
Remaining_Contract_Months = st.sidebar.number_input("Remaning Contract Time", min_value=0, step=1)
Injured_Games_Missed = st.sidebar.number_input("Games Unavailable", min_value=0, step=1, value=25)
U23_INT_Appearances = st.sidebar.number_input("International U-23 Caps", min_value=0, step=1, value=25)
INT_Appearances = st.sidebar.number_input("Senior International Caps", min_value=0, step=1, value=25)
Min = st.sidebar.number_input("Minutes Played", min_value=0, step=1, value=2000)
goals = st.sidebar.number_input("Goals Scored", min_value=0, step=1, value=10)
xG = st.sidebar.number_input("Expected Goals (xG)", min_value=0.0, step=0.1, value=8.5)
Yellow_Cards = st.sidebar.number_input("Yellow Cards", min_value=0, step=1, value=8)
Red_Cards = st.sidebar.number_input("Red Cards", min_value=0, step=1, value=8)
Progressive_Carries = st.sidebar.number_input("Progressive Carries", min_value=0, step=1, value=8)
Progressive_Passes = st.sidebar.number_input("Progressive Passes", min_value=0, step=1, value=8)
Progressive_Passes_Received = st.sidebar.number_input("Progressive Passes Received", min_value=0, step=1, value=8)
Shots_Total = st.sidebar.number_input("Shots Total", min_value=0, step=1, value=8)
Shots_on_Target = st.sidebar.number_input("Shots on Target", min_value=0, step=1, value=8)
Passes_Completed = st.sidebar.number_input("Passes Completed", min_value=0, step=1, value=8) 
Passes_Attempted = st.sidebar.number_input("Passes Attempted", min_value=0, step=1, value=8)
Assists = st.sidebar.number_input("Assists", min_value=0, step=1, value=5)
xA = st.sidebar.number_input("Expected Assists (xA)", min_value=0.0, step=0.1, value=6.0)
Shot_Creating_Actions = st.sidebar.number_input("Shot Creating Actions", min_value=0, step=1, value=8)
Goal_Creation_Actions = st.sidebar.number_input("Goal Creating Actions", min_value=0, step=1, value=8)
Tackles = st.sidebar.number_input("Tackles", min_value=0, step=1, value=8)
Tackles_won = st.sidebar.number_input("Tackles Won", min_value=0, step=1, value=8)
Interceptions = st.sidebar.number_input("Interceptions", min_value=0, step=1, value=8)
Blocks = st.sidebar.number_input("Blocks", min_value=0, step=1, value=8)
Clearances = st.sidebar.number_input("Clearances", min_value=0, step=1, value=8)
Attempted_Take_Ons = st.sidebar.number_input("Attempted Take Ons", min_value=0, step=1, value=8)
Successful_Take_Ons = st.sidebar.number_input("Successful Take Ons", min_value=0, step=1, value=8)
Touches_Att_Pen = st.sidebar.number_input("Touches in Attacking Penalty Area", min_value=0, step=1, value=8)
Aerials_Won = st.sidebar.number_input("Aerial Duels Won", min_value=0, step=1, value=8)
Aerials_Lost = st.sidebar.number_input("Aerial Duels Lost", min_value=0, step=1, value=8)
WC = st.sidebar.number_input("World Cups", min_value=0, step=1, value=8)
FIFA_U23 = st.sidebar.number_input("U-23 World Cups or Olympics", min_value=0, step=1, value=8)
UEFA_CONMEBOL_U23 = st.sidebar.number_input("UEFA or CONMEBOL U-23 Tournaments", min_value=0, step=1, value=8)
OTHERS_U23 = st.sidebar.number_input("U-23 Continental Tournaments of Other Confederations", min_value=0, step=1, value=8)
UEFA_CAM = st.sidebar.number_input("UEFA Cup or Copa America", min_value=0, step=1, value=8)
Other_Nation_Continental = st.sidebar.number_input("Other Confederation Senior Tournaments", min_value=0, step=1, value=8)
CWC = st.sidebar.number_input("Club World Championship", min_value=0, step=1, value=8)
UEFA_CL = st.sidebar.number_input("UEFA Champions League", min_value=0, step=1, value=8)
COPA_LIBERTADORES = st.sidebar.number_input("Copa Libertadores da America", min_value=0, step=1, value=8)
UEFA_EL = st.sidebar.number_input("UEFA Europa League", min_value=0, step=1, value=8)
COPA_SUDAMERICANA = st.sidebar.number_input("Copa Sudamericana", min_value=0, step=1, value=8)
Other_Club_Continental = st.sidebar.number_input("Other Club Continental Tournaments", min_value=0, step=1, value=8)
DL1 = st.sidebar.number_input("Domestic Leagues - Band 1", min_value=0, step=1, value=8)
DL2 = st.sidebar.number_input("Domestic Leagues - Band 2", min_value=0, step=1, value=8)
DL3 = st.sidebar.number_input("Domestic Leagues - Band 3", min_value=0, step=1, value=8)
DL4 = st.sidebar.number_input("Domestic Leagues - Band 4", min_value=0, step=1, value=8)
DL5 = st.sidebar.number_input("Domestic Leagues - Band 5", min_value=0, step=1, value=8)
DL6 = st.sidebar.number_input("Domestic Leagues - Band 6", min_value=0, step=1, value=8)


# Calculate derived attributes
ninety_minutes = round(Min / 90, 4) if Min > 0 else 0
Goals_90 = round(goals / ninety_minutes, 4) if ninety_minutes > 0 else 0
xG_90 = round(xG / ninety_minutes, 4) if ninety_minutes > 0 else 0
Progressive_Carries_90 = round(Progressive_Carries / ninety_minutes, 4) if ninety_minutes > 0 else 0
Progressive_Passes_90 = round(Progressive_Passes / ninety_minutes, 4) if ninety_minutes > 0 else 0
Progressive_Passes_Received_90 = round(Progressive_Passes_Received / ninety_minutes, 4) if ninety_minutes > 0 else 0
Shots_Total_90 = round(Shots_Total / ninety_minutes, 4) if ninety_minutes > 0 else 0
Shots_on_Target_90 = round(Shots_on_Target / ninety_minutes, 4) if ninety_minutes > 0 else 0
Passes_Completed_90 = round(Passes_Completed / ninety_minutes, 4) if ninety_minutes > 0 else 0
Passes_Attempted_90 = round(Passes_Attempted / ninety_minutes, 4) if ninety_minutes > 0 else 0
Pass_Completion_perc_90 = round((Passes_Completed_90 / Passes_Attempted_90) * 100, 4) if Passes_Attempted_90 > 0 else 0
Assists_90 = round(Assists / ninety_minutes, 4) if ninety_minutes > 0 else 0
xA_90 = round(xA / ninety_minutes, 4) if ninety_minutes > 0 else 0
GxG = Goals_90 - xG_90
AxA = Assists_90 - xA_90
Shot_Creating_Actions_90 = round(Shot_Creating_Actions / ninety_minutes, 4) if ninety_minutes > 0 else 0
Goal_Creation_Actions_90 = round(Goal_Creation_Actions / ninety_minutes, 4) if ninety_minutes > 0 else 0
Tackles_90 = round(Tackles / ninety_minutes, 4) if ninety_minutes > 0 else 0
Tackles_won_90 = round(Tackles_won / ninety_minutes, 4) if ninety_minutes > 0 else 0
Tackles_Won_perc_90 = round((Tackles_won_90 / Tackles_90) * 100, 4) if Tackles_90 > 0 else 0
Interceptions_90 = round(Interceptions / ninety_minutes, 4) if ninety_minutes > 0 else 0
Blocks_90 = round(Blocks / ninety_minutes, 4) if ninety_minutes > 0 else 0
Clearances_90 = round(Clearances / ninety_minutes, 4) if ninety_minutes > 0 else 0
Attempted_Take_Ons_90 = round(Attempted_Take_Ons / ninety_minutes, 4) if ninety_minutes > 0 else 0
Successful_Take_Ons_90 = round(Successful_Take_Ons / ninety_minutes, 4) if ninety_minutes > 0 else 0
Successful_Take_On_perc_90 = round((Successful_Take_Ons_90 / Attempted_Take_Ons_90) * 100, 4) if Attempted_Take_Ons_90 > 0 else 0
Touches_Att_Pen_90 = round(Touches_Att_Pen / ninety_minutes, 4) if ninety_minutes > 0 else 0
Aerials_Won_90 = round(Aerials_Won / ninety_minutes, 4) if ninety_minutes > 0 else 0
Aerials_Lost_90 = round(Aerials_Lost / ninety_minutes, 4) if ninety_minutes > 0 else 0
Aerials_Total_90 = round(Aerials_Won_90 + Aerials_Lost_90, 4)
Aerials_Won_perc_90 = round((Aerials_Won_90 / Aerials_Total_90) * 100, 4) if Aerials_Total_90 > 0 else 0

Weighted_Trophees = round((
    WC * 10 + FIFA_U23 * 3 + UEFA_CONMEBOL_U23 * 2 + OTHERS_U23 * 1 +
    UEFA_CAM * 8 + Other_Nation_Continental * 4 + CWC * 5 + UEFA_CL * 7 +
    COPA_LIBERTADORES * 5 + UEFA_EL * 3 + COPA_SUDAMERICANA * 2 + Other_Club_Continental * 1
) / 72, 4)

# Mapear ligas para bandas
origin_band = map_to_band(league_origin, Origin_Lg)
dest_band = map_to_band(league_dest, Destination_Lg)

# Loading the Model Pipeline
with open("player_price_pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

# Criar DataFrame para predição
input_data = pd.DataFrame({
    "Age": [age],
    "Height_cm": [height],
    "Remaining_Contract_Months": [Remaining_Contract_Months],
    "Injured_Games_Missed": [Injured_Games_Missed],
    "U23_INT_Appearances": [U23_INT_Appearances],
    "INT_Appearances": [INT_Appearances],
    "Min": [Min],
    "Yellow_Cards": [Yellow_Cards],
    "Red_Cards": [Red_Cards],
    "Weighted_Trophees": [Weighted_Trophees],
    "Progressive_Carries_90": [Progressive_Carries_90],
    "Progressive_Passes_90": [Progressive_Passes_90],
    "Progressive_Passes_Received_90": [Progressive_Passes_Received_90],
    "Shots_Total_90": [Shots_Total_90],
    "Shots_on_Target_90": [Shots_on_Target_90],
    "Passes_Completed_90": [Passes_Completed_90],
    "Passes_Attempted_90": [Passes_Attempted_90],
    "Pass_Completion_perc_90": [Pass_Completion_perc_90],
    "Shot_Creating_Actions_90": [Shot_Creating_Actions_90],
    "Goal_Creation_Actions_90": [Goal_Creation_Actions_90],
    "Tackles_90": [Tackles_90],
    "Tackles_won_90": [Tackles_won_90],
    "Tackles_Won_perc_90": [Tackles_Won_perc_90],
    "Interceptions_90": [Interceptions_90],
    "Blocks_90": [Blocks_90],
    "Clearances_90": [Clearances_90],
    "Attempted_Take_Ons_90": [Attempted_Take_Ons_90],
    "Successful_Take_Ons_90": [Successful_Take_Ons_90],
    "Successful_Take_On_perc_90": [Successful_Take_On_perc_90],
    "Touches_Att_Pen_90": [Touches_Att_Pen_90],
    "Aerials_Won_90": [Aerials_Won_90],
    "Aerials_Lost_90": [Aerials_Lost_90],
    "Aerials_Total_90": [Aerials_Total_90],
    "Aerials_Won_perc_90": [Aerials_Won_perc_90],
    "GxG": [GxG],
    "AxA": [AxA],
    "Origin_League_Band 1": [1 if origin_band == "Band 1" else 0],
    "Origin_League_Band 2": [1 if origin_band == "Band 2" else 0],
    "Origin_League_Band 3": [1 if origin_band == "Band 3" else 0],
    "Origin_League_Band 4": [1 if origin_band == "Band 4" else 0],
    "Origin_League_Band 5": [1 if origin_band == "Band 5" else 0],
    "Origin_League_Band 6": [1 if origin_band == "Band 6" else 0],
    "Destination_League_Band 1": [1 if dest_band == "Band 1" else 0],
    "Destination_League_Band 2": [1 if dest_band == "Band 2" else 0],
    "Destination_League_Band 3": [1 if dest_band == "Band 3" else 0],
    "Destination_League_Band 4": [1 if dest_band == "Band 4" else 0],
    "Destination_League_Band 5": [1 if dest_band == "Band 5" else 0],
    "Destination_League_Band 6": [1 if dest_band == "Band 6" else 0],
    "Deal_Type_Free": [1 if deal_type == "Free" else 0],
    "Deal_Type_Transfer": [1 if deal_type == "Transfer" else 0],
    "Position_AM": [1 if Position == "AM" else 0],
    "Position_DF": [1 if Position == "DF" else 0],
    "Position_DM": [1 if Position == "DM" else 0],
    "Position_FB": [1 if Position == "FB" else 0],
    "Position_FW": [1 if Position == "FW" else 0],
    "Position_MF": [1 if Position == "MF" else 0],
    "Position_WR": [1 if Position == "WR" else 0]
})

if st.button("Prever Preço"):
    prediction = pipeline.predict(input_data)
    st.subheader(f"Preço Previsto: €{prediction[0]:,.2f}")
