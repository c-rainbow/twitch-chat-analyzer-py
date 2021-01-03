import time
import sys
import os
import json

from twitch_chat_analyzer import kraken

CLIENT_ID = "s2frr164040bp9l6mgurxaz32i6rm1"  # Test client ID 


def downloadChat(video_id, save_to_file=True):
  client = kraken.TwitchClient(CLIENT_ID)
  video_json = client.GetVideo(video_id)
  if not video_json:
    return
  # print(json.dumps(video_json, indent=2))

  print('Downloading chat of', video_json['title'], 'by', video_json['channel']['display_name'])

  total_seconds = float(video_json['length'])

  start_time = time.time()
  comments_generator = client.GetComments(video_id)
  comments = []
  for comments_batch in comments_generator:
    comments.extend(comments_batch)
    comment_count = len(comments)
    if comment_count:
      draw_progress(comments[-1]['content_offset_seconds'], total_seconds, comment_count)

  draw_progress(100, 100, len(comments))
  end_time = time.time()
  sys.stdout.write('\nDownload complete in %d seconds' % (end_time - start_time))

  data_json = {"video": video_json, "comments": comments}
  if save_to_file:
    save_chat(video_id, data_json)

  return data_json


def draw_progress(offset, total, comment_count):
  progress = min(100, offset / total * 100)
  sys.stdout.write('Total %d chats downloaded. %.2f%% complete\r' % (comment_count, progress))
  sys.stdout.flush()

def save_chat(video_id, data_json):
  video_json = data_json['video']
  streamer_username = video_json['channel']['name']
  path_dir = os.path.join('.', 'chatlogs', streamer_username)
  if not os.path.exists(path_dir):
    os.makedirs(path_dir)
  filepath = os.path.join(path_dir, str(video_id) + '.json')
  content = json.dumps(data_json, indent=2, ensure_ascii=False)
  with open(filepath, 'w', encoding='utf8') as f:
    f.write(content)
  print('\nChat saved to ', filepath, '\n')


if __name__ == '__main__':
  data = downloadChat('past_broadcast_number')

