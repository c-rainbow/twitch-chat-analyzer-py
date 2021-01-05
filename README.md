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
# Video ID is the last part of the video URL (1234567890 in https://www.twitch.tv/videos/1234567890)
# If the chat log was not downloaded before, it will download automatically and create an analyzer.
ann = analyzer.FromVideoId('REPLACE_HERE_TO_VIDEO_ID')

# Some pre-built statistics functions to draw graph
ann.DrawChatPerMinute(10)  # Chat counts for each N-minute interval
ann.DrawTopChatters(20)  # Top N viewers with most chats
ann.DrawTopEmotes(15)  # Top N most used emotes

# If you just want to get the data
ann.GetChatPerMinute(10)  # Chat counts for each 10-minute interval, list of (offset, count)
ann.GetTopChatters()  # Viewer names and chat counts, list of (name, chat_count), sorted by chat count
ann.GetEmoteCounts()  # Emotes and usage counts, list of (emote_name, count), sorted by count

# If you want to handle dataframe yourself
df = ann.ToDataFrame()

# Some useful functions to deal with dataframe
df[df['is_sub_notice']]  # Show new/renew subscription notice messages
df[df['bits'] > 0]  # Show messages with bits
df['text_body'].apply(len).mean()  # Average chat length (excluding emotes)

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

