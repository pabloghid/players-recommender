import pandas as pd
import numpy as np
import os
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import json

class PlayerRecommendation:
    METRICS_TO_TRAIN = ['90s', 'Goals', 'Assists', 'Acc_Passes_Percentage', 'Key_Passes-n', 'Tackles', 'Blocks', 
                        'Interceptations', 'Tackles_Interceptations', 'Duels_Won_Percentage', 'Shots',
                        'ShotsOnTarget', 'ShotsOnTarget_Percentage', 'Goals_Shot', 
                        'Goals_ShotsOnTarget', 'Fouls_Draw-n', 'Fouls_Committed-n', 'Save_Percentage', 
                        'Goals_Conceded-n'
                        ]

    def __init__(self, directory='core\data'):
        self.directory = directory
        self.df = None
        self.distances = None
        self.indices = None
    
    def group_csv_df(self):
        dataframes = []
        players_directory = self.directory + '\players'
        for filename in os.listdir(self.directory + '\players'):
            if filename.endswith('.csv'):
                filepath = os.path.join(players_directory, filename)
                df = pd.read_csv(filepath)
                dataframes.append(df)

        combined_df = pd.concat(dataframes, ignore_index=True)

        new_csv = self.directory + '/players_data.csv'
        combined_df.to_csv(new_csv, index=False)
        
        self.df = combined_df

    def clean_data(self, dataset):
        ## carregar o dataset
        df = dataset
        ## limpar dribbles past (está zerado)
        df = df.drop(columns=['Dribbles_Past'])
        ## limpar dados zero
        df = df.fillna(0)
        ## remover com menos de 3 partidas
        df = df[df['Minutes'] >= 270]
        ## juntar jogadores iguais (ver se existem dados com o mesmo id e com clube diferente)

        self.df = df

    def group_players(self):
        self.df['Count'] = self.df.groupby('Id')['Id'].transform('count')
        different_teams = self.df.groupby('Id')['Team'].nunique()
        self.df['Different_Team'] = (different_teams > 1) & (self.df['Count'] == 1)
        filtered_df = self.df[self.df['Different_Team'] | ~self.df.duplicated('Id', keep='first')]
        filtered_df = filtered_df.drop(columns=['Different_Team', 'Count'])
        new_df = filtered_df.groupby('Id').agg({
            'Name': 'first','Age': 'first','Nationality': 'first','Injured': 'first','Team': 'first',
            'Position': 'first','Games': 'sum', 'Minutes': 'sum', 'Accuracy_Passes': 'sum', 'Key_Passes': 'sum', 'Total_Passes': 'sum',
            'Shots_On': 'sum', 'Shots_Total': 'sum', 'Dribbles_Attempts': 'sum',
            'Dribbles_Success': 'sum', 'Fouls_Drawn': 'sum', 'Fouls_Committed': 'sum', 'Tackled_Block': 'sum',
            'Tackled_Intercept': 'sum', 'Tackled_Total': 'sum', 'Duels_Won': 'sum', 'Duels_Total': 'sum',
            'Goals_Assist': 'sum', 'Goals_Total': 'sum', 'Goals_Conceded': 'sum', 'Goals_Saves': 'sum', 'Photo':'first','Logo_Team':'first','Rating': 'mean',
            'Yellow_Cards': 'sum', 'Red_Cards': 'sum', 'Yellow_Red_Cards': 'sum', 'Weight_kg': 'sum', 'Height_cm': 'sum'
        }).reset_index()
        new_df['player_name_team'] = new_df['Name'] + ' - ' + new_df['Team']
        self.df = new_df

    def new_metrics(self):
        d90s = (self.df['Minutes']/90)
        self.df['90s'] = d90s.round(1)
        self.df['Goals'] = (self.df['Goals_Total']/d90s).round(2)
        self.df['Assists'] = (self.df['Goals_Assist']/d90s).round(2)
        self.df['Acc_Passes_Percentage'] = self.df['Accuracy_Passes']
        self.df['Key_Passes-n'] = (self.df['Key_Passes']/d90s).round(2)
        self.df['Tackles'] = (self.df['Tackled_Total']/d90s).round(2)
        self.df['Blocks'] = (self.df['Tackled_Block']/d90s).round(2)
        self.df['Interceptations'] = (self.df['Tackled_Intercept']/d90s).round(2)
        self.df['Tackles_Interceptations'] = (self.df['Tackled_Intercept']+self.df['Tackled_Block']/d90s).round(2)
        self.df['Duels_Won_Percentage'] = (self.df['Duels_Won']/self.df['Duels_Total']*100).round(1)
        self.df['Shots'] = (self.df['Shots_Total']/d90s).round(2)
        self.df['ShotsOnTarget'] = (self.df['Shots_On']/d90s).round(2)
        self.df['ShotsOnTarget_Percentage'] = (self.df['Shots_On']/self.df['Shots_Total']*100).round(1)
        self.df['Goals_Shot'] = (self.df['Goals']-self.df['Shots']/d90s).round(2)
        self.df['Goals_ShotsOnTarget'] = (self.df['Goals']-self.df['ShotsOnTarget']/d90s).round(2)
        self.df['Fouls_Draw-n'] = (self.df['Fouls_Drawn']/d90s).round(2)
        self.df['Fouls_Committed-n'] = (self.df['Fouls_Committed']/d90s).round(2)
        self.df['Save_Percentage'] = (self.df['Goals_Saves']/(self.df['Goals_Saves']+self.df['Goals_Conceded'])*100).round(1)
        self.df['Goals_Conceded-n'] = (self.df['Goals_Conceded']/d90s).round(2)
        #self.df['Penalty_Percentage'] = (self.df['Goals_Conceded']/self.df['Goals_Conceded']*100)
        self.df = self.df.fillna(0)
        return self.df

    def train_nearest_neighbors(self):
        metrics = ['Goals', 'Assists', 'Acc_Passes_Percentage', 'Key_Passes-n', 'Tackles', 'Blocks', 'Interceptations', 'Tackles_Interceptations', 'Duels_Won_Percentage', 'Shots','ShotsOnTarget', 'ShotsOnTarget_Percentage', 'Goals_Shot', 'Goals_ShotsOnTarget', 'Fouls_Draw-n', 'Fouls_Committed-n', 'Save_Percentage', 'Goals_Conceded-n']
        stats = self.df[metrics].values
        data = StandardScaler().fit_transform(stats)

        X = np.array(data)
        self.nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(X)
        self.distances, self.indices = self.nbrs.kneighbors(X)


    def initialize(self):
        self.group_csv_df()
        self.clean_data(self.df)
        self.group_players()
        self.new_metrics()
        self.train_nearest_neighbors()
    
    def get_all_players(self):
        return self.df.to_dict(orient='records')

    def find_player_neighbors(self, player_id):
        result_json = {}

        self.df.loc[self.df["Id"] == player_id]
        # Obtenha as informações do jogador alvo
        target_info = {
            'name': self.df['Name'].loc[self.df["Id"] == player_id].values[0],
            'team': self.df['Team'].loc[self.df["Id"] == player_id].values[0]
        }

        result_json['player'] = {'id': str(player_id), 'name': target_info['name'], 'team': target_info['team']}

        target_index = self.df[self.df["Id"] == player_id].index[0]

        neighbor_list = [{'id': str(self.df['Id'].iloc[idx]), 'name': self.df['Name'].iloc[idx], 'team': self.df['Team'].iloc[idx], 'distance': self.distances[target_index, j]} for j, idx in enumerate(self.indices[target_index])]
        ## Remove o primeiro pois é o próprio jogador
        result_json['neighbors'] = neighbor_list[1:]
        
        return json.dumps(result_json, indent=2)
    