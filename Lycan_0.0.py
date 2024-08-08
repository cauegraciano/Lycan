#Coletar dados dos players
import requests
import pprint
import pandas as pd
import time

class Funcs ():

    #Lista os champions banidos
    #print(match_data['info']['participants'][5]['kills'])
    def get_match_dataBans(match_data, champion_data):
        for team in match_data['info']['teams']:
            for ban in team['bans']:
                champion_name = champion_data.get(str(ban['championId']))  # convertendo championId para string
                print(f"  Pick Turn {ban['pickTurn']}: {champion_name}")

    def get_match_data(match_id, mass_region, api_key):
        api_url = (
            "https://" + 
            mass_region + 
            ".api.riotgames.com/lol/match/v5/matches/" +
            match_id + 
            "?api_key=" + 
            api_key
        )
        
        resp = requests.get(api_url)
        match_data = resp.json()
        print('get_match_data',api_url)
        return match_data 

    def get_current_timestamp(self):
        return int(time.time()) 
    
    def get_player_matchv5(self, puuid, count, api_key, endTime):
        #Partidas do player
        #timestamp em segundos, 7 dias = 604800 segundos
        #print(puuid)
        startTime = endTime - 604800
        api_url = (
            "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + 
            puuid +
            "/ids" + 
            "?startTime=" +
            str(startTime) +
            "&endTime=" +
            str(endTime) +
            "&queue=420" +
            "&type=ranked" +
            "&start=0" +
            "&count=" +
            str(count) +
            "&api_key=" +
            api_key
        )

        resp = requests.get(api_url)

        matchIds = resp.json()

        return matchIds

    def get_player_match_info(self, playerMatches, api_key):
        #Dados da partida
        matches_info = {}
        #playerMatches lista de partidas
        for match in playerMatches:
            api_url = r"https://americas.api.riotgames.com/lol/match/v5/matches/" + match

            api_url = api_url + '?api_key=' + api_key

            resp = requests.get(api_url)

            match_data = resp.json()

            matches_info[match] = match_data

            print('get_player_match_info', match)
        return matches_info

    def save_excel(self, matches_info_dict, teamPuuid):
        print('save_excel')
        filtered_data = []
        for role in matches_info_dict:
            for match, match_data in matches_info_dict[role].items():
                for p in match_data['info']['participants']:
                    for playerPuuid in teamPuuid:
                        #Validar duplicacoes pois os players podem jogar duo
                        if p['puuid'] in playerPuuid.values():
                            print(match, p['riotIdGameName'])
                            new_entry = {
                                    'GameId': match,
                                    'puuid': p['puuid'],
                                    'riotIdGameName': p['riotIdGameName'],
                                    'championId': p['championId'],
                                    'championName': p['championName'],
                                    'teamPosition': p['teamPosition'],
                                    'totalMinionsKilled': p['totalMinionsKilled'],
                                    'neutralMinionsKilled': p['neutralMinionsKilled'],
                                    'CS': p['totalMinionsKilled'] + p['neutralMinionsKilled'],
                                    'kills': p['kills'],
                                    'deaths': p['deaths'],
                                    'assists': p['assists'],
                                    'kda': p['challenges']['kda'],
                                    'controlWardsPlaced': p['challenges']['controlWardsPlaced'],
                                    'visionScore': p['visionScore']
                            }
                            filtered_data.append(new_entry) 

                
        
        df = pd.DataFrame(filtered_data)

        #Salvar por sheets cada player e fazer uma sheet geral

        df.to_excel('match_data.xlsx', index=False)
        print('df salvo')

class Lycan (Funcs): 

    def __init__(self):
        
        self.matches_dict = {}
        self.matches_info_dict = {}

        self.api_key = r"RGAPI-cd38d8fe-ee7b-4bf2-be99-a6e6eb75bdb9"
        #puuidCauemo
        self.puuid = r"0ErABkXREc_Do9oOKd7swFlSjDvXRuSRin7eYd74MqRvvHNNh5NUTvYBFyK_Tsl-nhYeb8WEI0LBAQ"

        #puuid dos 5 players
        self.puuidTorras = r"QxuYknHcRhNe02rDWIgqVDOPspQB75sb2-02i2wdOc2HQ72KVyog3jbRshfezhIt6SZVDKYq4uZkhQ"
        self.puuidBerus = r"VwDX_uu6jzS8GKlqfGc0AgzdeiapIw8K7elcahH3gAlxlXE36nURLgt17pTVSrdpbeatcClP3ssYyw"
        self.puiidZkyou = r"qpcgkcTI67-s4-dl0tJZxz4hpVV24ZsDXk45gtPlF7tiDGZ7KhACdv2JBbmSumJEuUhnaEeD19eyZA"
        self.puuidRobertinho = r"FW_inwTBTgVYkwJpEt2mNQyMlXHQVMlaUd_wy6-FEDFhkJfYSbEeSgyGEkqmkUdOzOrPLzm7pv_fkQ"
        #Supp

        self.teamPuuid = [
            {
                'Top': self.puuidTorras,
                'Jungle': self.puuidBerus,
                'Mid': self.puiidZkyou,
                'Adc': self.puuidRobertinho,
                #'Support': 'None'

            }
        ]

        self.timestamp_atual = self.get_current_timestamp()
        #print(self.timestamp_atual)

        for player_position in self.teamPuuid:
            for role, puuid in player_position.items():
                if puuid:  # Verifica se puuid não é None ou uma string vazia
                    match_ids = self.get_player_matchv5(puuid, 50, self.api_key, self.timestamp_atual)
                    self.matches_dict[role] = match_ids

        for role, matches in self.matches_dict.items():
            matches_info = self.get_player_match_info(matches, self.api_key)
            self.matches_info_dict[role] = matches_info


        self.save_excel(self.matches_info_dict, self.teamPuuid)
            

        #Necessario atualizar para versao atual de tempos em tempos
        urlListOfChampionId = r"https://ddragon.leagueoflegends.com/cdn/14.15.1/data/en_US/champion.json"

        respChampId = requests.get(urlListOfChampionId)

        listOfChampionId = respChampId.json()

        champion_data = {champ['key']: champ['name'] for champ in listOfChampionId['data'].values()}

        #account
        # Usar para pegar puuid
        # api_url = r"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Cauemo/EMO"



        #print(match_data)


        
Lycan()