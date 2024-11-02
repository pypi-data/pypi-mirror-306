"""Wrap response data into other data types which are easy to handle"""
from typing import Literal
import pandas as pd
from pubgapiku.api_connector import Connector

PLATFORM = Literal['steam', 'kakao', 'console', 'psn', 'stadia', 'touranment', 'xbox']

# pylint: disable=line-too-long

class DataWrapper():
    """Data wrapper class"""
    def __init__(self, api_key:str, platform:PLATFORM, timeout:int=1):
        self.conn = Connector(api_key, platform, timeout)

    def get_sample_matches(self, date_filter:str='') -> list:
        """
        Get a list of random sample match

        [Arguments]
        date_filter  |-> Target date to collect sample match list (optional). Formatted as YYYYMMDD

        [Return]
        list |-> Successfully extracted matchid list
        """

        data:dict = self.conn.sample_matches(date_filter)
        match_list:list = [
            item['id'] for item in
            data['data']['relationships']['matches']['data']
        ]
        return match_list

    def get_players_in_match(self, match_id:str) -> pd.DataFrame:
        """
        Get a dataframe containing player names and account ids of a match

        [Arguments]
        match_id:str |-> The target match's id

        [Return]
        pd.DataFrame |-> Successfully extracted player info
        """

        data:dict = self.conn.match(match_id)
        player_list:list = [
            {'accountId': item['attributes']['stats']['playerId'],
                'playerName': item['attributes']['stats']['name']}
            for item in data['included']
            if item['type'] == 'participant'
        ]
        return pd.DataFrame(player_list)

    def get_player_data(self, **kargs) -> pd.DataFrame:
        """
        Get a dataframe containing list of players and matches they played

        [Keyword arguments]
        ids:list[str]   |-> filters by player IDs
        names:list[str] |-> filters by player names

        [Return]
        pd.DataFrame |-> Successfully extracted player-match relations
        """

        data:dict = self.conn.players(**kargs)
        player_datas = []
        for player in data['data']:
            player_id = player['id']
            player_name = player['attributes']['name']
            player_bantype = player['attributes']['banType']

            for match in player['relationships']['matches']['data']:
                if match['type'] == 'match':
                    match_info = {
                        'accountId': player_id,
                        'playerName': player_name,
                        'banType': player_bantype,
                        'matchId': match['id']
                    }
                    player_datas.append(match_info)
        return pd.DataFrame(player_datas)

    def __parse_match(self, match_data:dict) -> tuple[dict, pd.DataFrame]:
        '''
        Parse a metadata and participants data from a match data

        [Arguments]
        match_data:dict |-> A match data in dictionary type

        [Return]
        tuple[dict, pd.DataFrame] |-> Extracted metadata in dictionary type, and a DataFrame of participants data
        '''
        meta_data = {
            'id': match_data['data']['id'],
            'created': match_data['data']['attributes']['createdAt'],
            'mode': match_data['data']['attributes']['gameMode'],
            'map': match_data['data']['attributes']['mapName'],
            'duration': match_data['data']['attributes']['duration']
        }
        participants = []
        rosters = {}
        for included in match_data['included']:
            if included['type'] == 'participant':
                stats = list(included['attributes']['stats'].keys())
                player_data = {
                    key: included['attributes']['stats'][key] for key in stats
                }
                player_data['id'] = included['id']
                player_data['teamId'] = ''
                player_data['teamRank'] = 0
                participants.append(player_data)
            elif included['type'] == 'roster':
                rosters[included['id']] = {
                    'rank': included['attributes']['stats']['rank'],
                    'participants': [
                        player['id'] for player
                        in included['relationships']['participants']['data']
                    ]
                }
        participants = pd.DataFrame(participants)
        for rid, rdata in rosters.items():
            pfilter = participants['id'].isin(rdata['participants'])
            participants.loc[pfilter, 'teamId'] = rid
            participants.loc[pfilter, 'teamRank'] = rdata['rank']
        return meta_data, participants

    def __parse_telemetry(self, telemetry_data:list) -> pd.DataFrame:
        def __parse_event(event_data:dict):
            event:dict = {}
            event['type'] = event_data.pop('_T')
            event['datetime'] = event_data.pop('_D')

            event['actor'] = event_data.pop('accountId', '-')
            event['subject'] = '-'
            event['co_actor'] = '-'

            actor_keys = ('character', 'attacker', 'instigator', 'finisher', 'killer', 'reviver')
            for actor_key in actor_keys:
                if actor_key in event_data:
                    if event_data[actor_key] is None:
                        continue
                    event['actor'] = event_data[actor_key]['accountId']

            coactor_keys = ('riders', 'fellowPassengers')
            for coactor_key in coactor_keys:
                if coactor_key in event_data:
                    if len(event_data[coactor_key]) < 1:
                        continue
                    event['co_actor'] = ','.join([
                        coactor['accountId'] for coactor in event_data[coactor_key]
                    ])
            if 'assists_AccountId' in event_data:
                event['co_actor'] = ','.join(event_data['assists_AccountId'])

            if 'victim' in event_data:
                event['subject'] = event_data['victim']['accountId']

            event['contents'] = event_data
            return event

        events:list = [__parse_event(event_data) for event_data in telemetry_data]
        return pd.DataFrame(events)

    def get_match_data(self, match_id:str, **kargs) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
        """
        Get a tuple of dataframe containing a match's metadata, participants list, and telemetry data

        [Arguments]
        match_id:str   |-> target match's id

        [Keyword Arguments]
        mode:list[str] |-> filter for the gamemode (refer https://github.com/pubg/api-assets/blob/master/dictionaries/gameMode.json)

        [Return]
        tuple[dict, dict] |-> Successfully acquired match and telemetry data
        """

        match_data:dict = self.conn.match(match_id, **kargs)
        if len(match_data) == 0:
            return {}, pd.DataFrame([]), pd.DataFrame([])

        telemetry_addr:str = self.conn.telemetry_addr(match_data)
        telemetry_data:list = self.conn.get_telemetry(telemetry_addr)

        meta_data, participants = self.__parse_match(match_data)
        parsed_telemetry = self.__parse_telemetry(telemetry_data)
        return meta_data, participants, parsed_telemetry
