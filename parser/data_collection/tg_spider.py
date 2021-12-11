# from telethon import TelegramClient
from telethon.sync import TelegramClient

api_id = 12465126
api_hash = '6f41fc346203d98715395048cff3e1eb'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

entity = client.get_entity('https://t.me/tass_agency')
print(entity.stringify()) #All paratmeters
print(entity.id)
msg = client.get_messages(entity.id, limit=10)
print(msg[7].stringify())

