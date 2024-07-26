# Ari_bot.py

Greetings, I decided to make an open source bot. It's currently under development. Not which commands are available.

Example:

-   1.!info
-   2.!join
-   2.1.!play
-  2.2.!stop
-  2.3.!pause 
-  2.4.!level 
-   3.!creator
-   4.!shop
-   4.1.!balance
-   4.2.!buy
-   4.3.!add_role
-   5.!hello

```pip install yt_dlp pynacl discord.py aiohttp```

`config/config.py`
```python
#[CONFIG]
TOKEN = "token" #token bota discord 
#[ID]
Channels = id# command 
Channels1 = id # level 
Channels_admin = id
#[LEVEL_ROLE]
level1 = id
level2 = id
```
- token- [token bot](https://discord.com/developers)
- channels -id channel 
- level - id Roley

```python 
@is_in_allowed_channel
@is_in_allowed_channel_admin
```
This method works checks.py.config.py you can put the channel id there. On which commands will work. Same as admin 