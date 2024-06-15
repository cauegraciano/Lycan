#Coletar dados dos players
import requests
import pprint
#import pandas

api_key = r"RGAPI-8bf97cb7-bdd6-45cd-96f6-fe54a2d26a80"
puuid = r"0ErABkXREc_Do9oOKd7swFlSjDvXRuSRin7eYd74MqRvvHNNh5NUTvYBFyK_Tsl-nhYeb8WEI0LBAQ"
#account
# Usar para pegar puuid
# api_url = r"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/Cauemo/EMO"

#parametro com puuid
api_url = r"https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/0ErABkXREc_Do9oOKd7swFlSjDvXRuSRin7eYd74MqRvvHNNh5NUTvYBFyK_Tsl-nhYeb8WEI0LBAQ"

api_url = api_url + '&api_key=' + api_key
resp = requests.get(api_url)

#Partidas do player
api_url = r"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/0ErABkXREc_Do9oOKd7swFlSjDvXRuSRin7eYd74MqRvvHNNh5NUTvYBFyK_Tsl-nhYeb8WEI0LBAQ/ids?start=0&count=20"

api_url = api_url + '&api_key=' + api_key

resp = requests.get(api_url)

#Dados da partida
api_url = r"https://americas.api.riotgames.com/lol/match/v5/matches/BR1_2946987516"

api_url = api_url + '?api_key=' + api_key

resp = requests.get(api_url)

match_data = resp.json()

match_data.keys()
print(match_data['info']['participants'][5])

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
    return match_data 


#Salvar em excel
    #Players individual
    #Time como todo