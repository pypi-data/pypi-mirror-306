# PUBG API Wrapper for Pandas
This package is under development; thus, some features may not work correctly or exist.   

## Installation
#### Using PyPI
You can download this project from PyPI using pip (pip3).   
```bash
pip install pubgapi-ku
```

#### Install directly from the source code
You can also install this project directly from the source code. In this case, you need to install ***setuptools***.   
The instruction assumes that you already installed the required tools.

##### 1. Install after build
```bash
python -m build
pip install ./dist/pubgapi_ku-0.17.5-py3-none-any.whl
```

##### 2. Install without build
```bash
pip install . # Normal mode
pip install -e . # Development mode
```

## Modules
### 1. API Connector
The module contains **Connector** class which has functions to get raw JSON data using *PUBG API* provided by *PUBG Developer Portal* (https://developer.pubg.com/).   
All data which can be collected using this module can also be collected by the **DataWrapper** class, which provides data as *Pandas DataFrame* type using **Connector** class internally.   
Therefore, there is no need to necessarily use **API Connector** module and **Connector** class in most cases.   

#### Usage
To use Connector class, you must generate a PUBG API key. Refer instruction of PUBG Developer Portal (https://documentation.pubg.com/en/getting-started.html).   
```Python
from pubgapiku.api_connector import Connector

conn = Connector(<your_api_key>, 'steam')
sample_matches:dict = conn.sample_matches()
```
#### Functions
> ***\_\_init\_\_*** *(self, api_key:str, platform:PLATFORM, timeout:int=1)*

Initialize API request sender.   

##### Arguments
***`api_key:str`*** An API key of the PUBG Developer Portal   
***`platform:PLATFORM`*** Target platform to collect data (steam, kakao, console, psn, stadia, tournament, xbox)   
***`timeout:int`*** Timeout limitation (sec), default=1   
&nbsp;

> ***sample_matches*** *(self, date_filter:str='') -> dict*

Return dictionary-type data containing a list of sample matches within 24 hours in UTC starting from the targeted date.   
When the API request is unsuccessful (the response code was not 200), an assertion error will be occurred.   
   
*The use of this function is subject to the request rate limitation of your PUGB Developer Portal account.*   

##### Arguments
***`date_filter:str`*** Target date to collect sample match list (optional). Formatted as YYYYMMDD   
&nbsp;

> ***players*** *(self, \*\*kargs) -> dict*

Return a dictionary-type value containing players information.   
When the API request was not successful (the response code was not 200), an assertion error will be occurred.   
   
*The use of this function is subject to the request rate limitation of your PUGB Developer Portal account.*   

##### Keyword Arguments
***`ids:list[str]`*** Filters by player ID   
***`names:list[str]`*** Filters by player names   
&nbsp;

> ***match*** *(self, match_id:str) -> dict*

Return a dictionary-type value containing a match's information.   
When the API request was not successful (the response code was not 200), an assertion error will be occurred.   

##### Arguments
***`match_id:str`*** The ID of the match for which you want to collect information   

##### Keyword Arguments
***`mode:list[str]`*** filter for the gamemode (refer https://github.com/pubg/api-assets/blob/master/dictionaries/gameMode.json)    
&nbsp;

> ***telemetry_addr*** *(self, match_data:dict) -> str*

Return the address of telemetry data of a match from the match's data.   
When the address of telemetry data was not found, an assertion error will be occurred.   

##### Arguments
***`match_data:dict`*** A match data which is obtained from ***match*** function   
&nbsp;

> ***get_telemetry*** *(self, addr:str) -> list*

Return a dictionary-type value containing a match's telemetry data of the target match.   
When the request was not successful (the response code was not 200), an assertion error will be occurred.   

##### Arguments
***`addr:str`*** The address of the target telemetry data obtained from telemetry_addr function   
&nbsp;

---
### 2. Data Wrapper
The module contains **DataWrapper** class, which has functions to get PUBG data from *PUBG API* as *Pandas DataFrame* data type.   
Since **DataWrapper** class works based on **Collector** class, a PUBG API key is also needed to use **DataWrapper** class.   

#### Usage
```Python
import pandas as pd
from pubgapiku.data_wrapper import DataWrapper

wrapper = DataWrapper(<your_api_key>, 'steam')
sample_matches:list = wrapper.get_sample_matches()
players:pd.DataFrame = wrapper.get_players_in_match(sample_matches[0])
```
#### Functions
> ***\_\_init\_\_*** *(self, api_key:str, platform:PLATFORM, timeout:int=1)*

Initialize a data wrapper instance, which contains a **Connector** instance.   

##### Arguments
***`api_key:str`*** An API key of the PUBG Developer Portal   
***`platform:PLATFORM`*** Target platform to collect data (steam, kakao, console, psn, stadia, tournament, xbox)   
***`timeout:int`*** Timeout limitation (sec), default=1   
&nbsp;

> ***get_sample_matches*** *(self, date_filter:str='') -> list*

Return a list of sample matches within 24 hours in UTC starting from the targeted date.   
   
*The use of this function is subject to the request rate limitation of your PUGB Developer Portal account.*   

##### Arguments
***`date_filter:str`*** Target date to collect sample match list (optional). Formatted as YYYYMMDD   
&nbsp;

> ***get_players_in_match*** *(self, match_id:str) -> pd.DataFrame*

Get a dataframe containing player names and account ids of a match.   
   
*The use of this function is subject to the request rate limitation of your PUGB Developer Portal account.*   

##### Arguments
***`match_id:str`*** The target match's id   
&nbsp;

> ***get_player_data*** *(self, \*\*kargs) -> pd.DataFrame*

Get a dataframe containing list of players and matches they played.   
   
*The use of this function is subject to the request rate limitation of your PUGB Developer Portal account.*   

##### Keyword Arguments
***`ids:list[str]`*** filters by player IDs   
***`names:list[str]`*** filters by player names   
&nbsp;

> ***get_match_data*** *(self, match_id:str) -> tuple[dict, pd.DataFrame, pd.DataFrame]*

Get a tuple of dataframe containing a match's metadata, participants list, and telemetry data.   

##### Arguments
***`match_id:str`*** target match's id   

##### Keyword Arguments
***`mode:list[str]`*** filter for the gamemode (refer https://github.com/pubg/api-assets/blob/master/dictionaries/gameMode.json)    
&nbsp;