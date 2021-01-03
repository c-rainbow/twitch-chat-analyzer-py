'''Model classes'''

import datetime

# Datetime format used in Twitch chat logs, e.g. '2020-10-31T19:01:03.811Z'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


# Model class for chat comment
class Comment:
  def __init__(self, comment_json):
    self._comment = comment_json
    self._commenter = comment_json['commenter']
    self._message = comment_json['message']
    self._fragments = self._message['fragments']

  @property
  def offset(self) -> float:
    return self._comment['content_offset_seconds']

  @property
  def utc_timestamp(self) -> datetime.datetime:
    return datetime.datetime.strptime(self._comment['created_at'], TIME_FORMAT)

  @property
  def username(self) -> str:
    # Twitch login username
    return self._commenter['name']
  
  @property
  def display_name(self) -> str:
    # Twitch display name in chat, which may not be in English
    return self._commenter['display_name']

  @property
  def name(self) -> str:
    # Name as is it shown in chat.
    # For display names with English alphabets, this is the same as display name.
    # For non-English display names, this is '{display_name}({username})'
    username = self.username
    display_name = self.display_name
    if username.lower() == display_name.lower():
      return display_name

    return '%s(%s)' % (display_name, username)

  @property
  def body(self) -> str:
    # Raw chat content
    return self._message['body']

  @property
  def text_body(self) -> str:
    # Chat text content excluding emotes
    texts = []
    for fragment in self._fragments:
      if 'emoticon' not in fragment:
        texts.append(fragment['text'].strip())

    return ' '.join(texts)
  
  @property
  def emotes(self) -> list[str]:
    emotes = []
    for fragment in self._fragments:
      if 'emoticon' in fragment:
        emotes.append(fragment['text'])

    return emotes

  @property
  def unique_emotes(self) -> set[str]:
    return set(self.emotes)

  @property
  def is_subscriber(self) -> bool:
    badges = self._message.get('user_badges', [])
    for badge in badges:
      if badge['_id'] == 'subscriber':
        return True
    
    return False

  @property
  def bits(self) -> int:
    return self._message.get('bits_spent', 0)
  
  @property
  def is_sub_notice(self) -> bool:
    # If this is a subscription notice message
    msg_id = self._message.get('user_notice_params', {}).get('msg_id')
    return msg_id in ('sub', 'resub')

  def __dict__(self) -> dict:
    return {
      'offset': self.offset,
      'utc_timestamp': self.utc_timestamp,
      'username': self.username,
      'display_name': self.display_name,
      'name': self.name,
      'body': self.body,
      'text_body': self.text_body,
      'is_subscriber': self.is_subscriber,
      'bits': self.bits,
      'is_sub_notice': self.is_sub_notice,
    }