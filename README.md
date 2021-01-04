# twitch-chat-analyzer-py

Twitch chat analyzer from past broadcasts, designed for Jupyter notebook.


## Getting Started

### Installation

The package can be installed by ```pip``` command in terminal 

```pip install --upgrade twitch-chat-analyzer```

### Run Jupyter Notebook

The package is mainly intended to be used in Jupyter notebook, but it can still be used in standard Python environment

Instruction to install Jupyter notebook (or newer JupyterLab) is [here](https://jupyter.org/install)

After installation, run the following command in terminal to start Jupyter

```jupyter notebook``` or ```jupyter-lab```

### Download chats from past broadcast

notebook.ipynb has examples of statistics functions. 

```python
from twitch_chat_analyzer import analyzer

# Create an analyzer object from video ID.
# If the chat log was not downloaded before, it will download automatically and create an analyzer.
ann = analyzer.FromVideoId('REPLACE_HERE_TO_VIDEO_ID')

# Some pre-built statistics functions to draw graph
ann.DrawChatPerMinutes(10)  # Chat counts for each 10-minute interval
ann.DrawTopChatters(20)  # Top 20 viewers with most chats
ann.DrawTopEmotes(15)  # Top 15 most used emotes

# If you want to handle dataframe yourself
df = ann.ToDataFrame()
```

### DataFrame

The dataframe returned from ToDataFrame() has the following columns

| Column name | type | meaning |
| :---------: | :--: | :-----: |
| offset | float | Time of the chat, in seconds after stream started |
| username | str | Twitch login username |
| display_name | str | Display name in chat, which may not be in English |
| name | str | Combined name of username and display_name, as displayed in Twitch chat |
| body | str | Raw chat content, including emote text |
| text_body | str | Chat content excluding emotes |
| is_subscriber | bool | if the chatter is a subscriber |
| bits | int | Amount of bits spent in the chat |
| is_sub_notice | bool | if the chat is new/renew subscription notice | 

