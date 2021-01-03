import typing
import requests

BASE_URL = 'https://api.twitch.tv/v5/%s'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'


CLIENT_ID = 's2frr164040bp9l6mgurxaz32i6rm1'


class TwitchClient:

  def __init__(self, client_id: str = CLIENT_ID):
    self.client_id = client_id
    self.session = requests.Session()
    self.headers = {
      'Client-ID': client_id,
      'Accept': 'application/vnd.twitchtv.v5+json'
    }

  def GetUsernameFromVideo(self, video_id) -> str:
    video_json = self.GetVideo(video_id)
    if not video_json:
      return None

    return video_json['channel']['name']

  def GetVideo(self, video_id) -> dict[str, typing.Any]:
    url = BASE_URL % 'videos/' + str(video_id)
    return self._GetUrl(url)

  def GetComments(self, video_id):
    cursor = ''
    while cursor is not None:
      url = BASE_URL % 'videos/' + str(video_id) + '/comments?cursor=' + cursor
      comments_batch = self._GetUrl(url)
      cursor = comments_batch.get('_next')
      yield comments_batch['comments']

  def _GetUrl(self, url):
    response = self.session.get(url, headers=self.headers)
    if response.status_code >= 400:
      print('Request to', url, 'failed with status code', response.status_code)
      return None

    try:
      return response.json()
    except Exception as e:
      print('JSON parsing error', e)
      return None
