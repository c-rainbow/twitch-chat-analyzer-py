
import json
import collections
import typing
from matplotlib import pyplot as plt
import math
import os
import pandas as pd

from twitch_chat_analyzer import kraken
from twitch_chat_analyzer import downloader
from twitch_chat_analyzer import models as tca_models


class ChatAnalyzer:
  def __init__(self, video_json, comments_json):
    self.video = video_json
    self.comments = [tca_models.Comment(comment_json) for comment_json in comments_json]

  def DrawChatPerMinute(self, minute: int = 5):
    chat_counts = self.GetChatPerMinute(minute)
    x = [str(index * minute) for index in range(len(chat_counts))]

    plt.bar(x, chat_counts, color='pink')
    plt.show()

  def GetChatPerMinute(self, minute: int = 5) -> typing.List[int]:
    total_seconds = minute * 60
    total_slots = int(math.ceil(self.video['length'] / total_seconds))
    counts = [0] * total_slots
    for comment in self.comments:
      index = int(comment.offset / total_seconds)
      counts[index] += 1

    return counts

  def DrawTopEmotes(self, top: int = 10):
    emote_counts = self.GetEmoteCounts()[:top]
    names, counts = zip(*emote_counts)

    plt.xticks(rotation=45, ha='right')
    plt.bar(names, counts, color='#00917C')
    plt.show()

  def GetEmoteCounts(self) -> typing.List[typing.Tuple[str, int]]:
    emote_dict: typing.Dict[str, int] = collections.defaultdict(int)
    for comment in self.comments:
      emotes = comment.emotes
      for emote in emotes:
        emote_dict[emote] += 1
    
    return self._SortedByCount(emote_dict)
  
  def DrawTopUniqueEmotes(self, top: int = 10):
    unique_emote_counts = self.GetUniqueEmoteCounts()[:top]
    names, counts = zip(*unique_emote_counts)

    plt.xticks(rotation=45, ha='right')
    plt.bar(names, counts, color='#61B15A')
    plt.show()

  def GetUniqueEmoteCounts(self) -> typing.List[typing.Tuple[str, int]]:
    unique_emote_dict: typing.Dict[str, int] = collections.defaultdict(int)
    for comment in self.comments:
      unique_emotes = comment.unique_emotes
      for emote in unique_emotes:
        unique_emote_dict[emote] += 1

    return self._SortedByCount(unique_emote_dict)

  def DrawTopChatters(self, top: int = 10):
    chat_counts = self.GetTopChatters()[:top]
    names, counts = zip(*chat_counts)

    plt.xticks(rotation=45, ha='right')
    plt.bar(names, counts, color='#79A3B1')
    plt.show()

  def GetTopChatters(self) -> typing.List[typing.Tuple[str, int]]:
    chat_count: typing.Dict[str, int] = collections.defaultdict(int)
    for comment in self.comments:
      chat_count[comment.display_name] += 1

    return self._SortedByCount(chat_count)

  def ToDataFrame(self) -> pd.DataFrame:
    return pd.DataFrame([comment.ToDict() for comment in self.comments])  

  def _SortedByCount(self, counts: typing.Dict[str, int]) -> typing.List[typing.Tuple[str, int]]:
    sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_counts


def FromFile(filepath) -> ChatAnalyzer:
  with open(filepath, 'r', encoding='utf8') as f:
    try:
      data_json = json.load(f)
      return ChatAnalyzer(data_json['video'], data_json['comments'])
    except Exception as e:
      print('Cannot load the file', filepath, '. Reason:', e)
      raise e


def FromVideoId(video_id) -> ChatAnalyzer:
  # First check if the chat log was already downloaded
  client = kraken.TwitchClient()
  username = client.GetUsernameFromVideo(video_id)
  path = 'chatlogs/{username}/{video_id}.json'.format(username=username, video_id=video_id)
  if os.path.exists(path):
    return FromFile(path)
  
  # If not already downloaded, download the chat
  data_json = downloader.downloadChat(video_id)
  return ChatAnalyzer(data_json['video'], data_json['comments'])


ann = FromVideoId(857482176)

#df = ann.ToDataFrame()

