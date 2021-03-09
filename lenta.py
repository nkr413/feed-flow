from telethon import TelegramClient, events, sync

lenta_id = 3081639
lenta_hash = "956797cee84ce327876b7465c01a066f"
subs_base = []
feed_flow = "@feed_flow"

client = TelegramClient('lenta_nkr', lenta_id, lenta_hash).start()

# @client.on(events.NewMessage(chats=(subs_base)))
# async def handler(event):
#   await client.forward_messages(feed_flow, event.message)

async def handler(event):
	await client.forward_messages(feed_flow, event.message)

@client.on(events.NewMessage(chats=(feed_flow)))
async def new_handler(event):
  data = event.message.to_dict()['message']

  if data == "/subs":
  	txt = "Подписанные каналы:\n\n"
  	
  	if len(subs_base) == 0:
  		await client.send_message(feed_flow, "Отсутствует подписка на каналы")
  	else:
  		txt += '\n'.join(subs_base)
  		await client.send_message(feed_flow, txt)

  if data[0] == "+" and data[1] == "@":
    subs_base.append(data[1:])

    client.add_event_handler(handler, events.NewMessage(chats=(subs_base)))

  if data[0] == "-" and data[1] == "@":
  	txt = data[1:]
  	for i in subs_base:
  		if txt == i:
  			subs_base.remove(i)
  			client.remove_event_handler(handler)

  			client.add_event_handler(handler, events.NewMessage(chats=(subs_base)))
  				
client.run_until_disconnected()
