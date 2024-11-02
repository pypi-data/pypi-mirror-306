"""KRAFTON API Request sender"""
from datetime import datetime
from typing import Literal
import requests

PLATFORM = Literal['steam', 'kakao', 'console', 'psn', 'stadia', 'touranment', 'xbox']

# pylint: disable=line-too-long

class Connector:
    """API Request sender class"""
    def __init__(self, api_key:str, platform:PLATFORM, timeout:int=1):
        """
        Initialize API request sender

        [Arguments]
        api_key:str        |-> An API key of the PUBG Developer Portal
        platform:PLATFORM  |-> Target platform to collect data
                               (steam, kakao, console, psn, stadia, tournament, xbox)
        timeout:int        |-> Timeout limitation (sec)
        """
        self.timeout:int = timeout
        self.api_base:str = f"https://api.pubg.com/shards/{platform}"
        self.header:dict = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/vnd.api+json'
        }
        self.header_nokey:dict = {
            'Accept': 'application/vnd.api+json'
        }

    def __chk_err(self, response:requests.Response) -> dict|list:
        """
        Check the status code of the response
        If the status code is not 200, the function raises an assertion error

        [Arguments]
        response:requests.Response |-> target response to check

        [Return]
        json |-> When the status code of the response is 200
        """
        assert response.status_code == 200,\
            'Got a response with bad status code'
        return response.json()

    def __chk_cls_str(self, subject:object, tgt_class:type) -> str:
        return f'Inappropriate data type received ({type(subject)}). It must be {tgt_class}'

    def sample_matches(self, date_filter:str='') -> dict:
        """
        Get sample match list

        [Arguments]
        date_filter  |-> Target date to collect sample match list (optional). Formatted as YYYYMMDD

        [Return]
        dict |-> A json response which includes a list of sample matches within
        """

        if date_filter != '':
            try:
                dt:datetime = datetime.strptime(date_filter, '%Y%m%d')
            except ValueError as exc:
                warning:str = 'Invalid date format. It should be YYYYMMDD (without dashes).'
                raise ValueError(warning) from exc
            date_filter = f'?filter[createdAt-start]={dt.strftime("%Y-%m-%dT%H%%3A%M%%3A%SZ")}'

        api = f'{self.api_base}/samples{date_filter}'
        response:requests.Response = requests.get(api, headers=self.header, timeout=self.timeout)
        output = self.__chk_err(response)
        assert isinstance(output, dict), self.__chk_cls_str(output, dict)
        return output

    def players(self, **kargs) -> dict:
        """
        Get players information

        [Keyword arguments]
        ids:list[str]   |-> filters by player IDs
        names:list[str] |-> filters by player names

        [Return]
        dict |-> A json response which includes target players' information
        """

        fil_by_id:bool = ('ids' in kargs) and (len(kargs['ids']) > 0)
        fil_by_name:bool = ('names' in kargs) and (len(kargs['ids']) > 0)

        assert fil_by_id or fil_by_name, 'You have to use one of filters'
        assert not (fil_by_id and fil_by_name), 'You cannot use both filters at the same time'

        if fil_by_id:
            filter_:str = 'playerIds'
            filter_elements:str = ','.join(kargs['ids'])
        else:
            filter_:str = 'playerNames'
            filter_elements:str = ','.join(kargs['names'])

        api:str = self.api_base + f'/players?filter[{filter_}]={filter_elements}'
        response:requests.Response = requests.get(api, headers=self.header, timeout=self.timeout)
        output = self.__chk_err(response)
        assert isinstance(output, dict), self.__chk_cls_str(output, dict)
        return output

    def match(self, match_id:str, **kargs) -> dict:
        """
        Get a match's information

        [Argument]
        match_id:str |-> target match's ID

        [Keyword Arguments]
        mode:list[str] |-> filter for the gamemode (refer https://github.com/pubg/api-assets/blob/master/dictionaries/gameMode.json)

        [Return]
        dict |-> A json response which includes target match's information (if the data doesn't satisfy the filter, return value will be an empty dict)
        """
        api = self.api_base + f'/matches/{match_id}'
        response:requests.Response = requests.get(
            api, headers=self.header_nokey, timeout=self.timeout
        )
        output = self.__chk_err(response)
        assert isinstance(output, dict), self.__chk_cls_str(output, dict)

        # mode filter: when the extracted game mode is not satisfy the filter, return tuple of empty dict and dataframes
        if ('mode' in kargs) and (len(kargs['mode']) > 0):
            mode = output['data']['attributes']['gameMode']
            if not mode in kargs['mode']:
                return {}

        return output

    def telemetry_addr(self, match_data:dict) -> str:
        """
        Get the address of telemetry data from a match data

        [Argument]
        match_data:dict |-> A match data which is obtained through *match* function

        [Return]
        str |-> The address of the match's telemetry data
        """
        output = None
        included:list[dict] = match_data['included']
        for item in included:
            if item['type'] == 'asset':
                output = item['attributes']['URL']
                break
        assert isinstance(output, str), 'Failed to search the address of telemetry data'
        return output

    def get_telemetry(self, addr:str) -> list:
        """
        Get telemetry data of a match

        [Argument]
        addr:str |-> The address of the telemetry data

        [Return]
        list |-> The target match's telemetry data
        """
        response:requests.Response = requests.get(
            addr, headers=self.header_nokey, timeout=self.timeout
        )
        output = self.__chk_err(response)
        assert isinstance(output, list), self.__chk_cls_str(output, list)
        return output
