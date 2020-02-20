import json
def configurate():
  token = input("Enter Discord Bot Token\n")
  prefix = input("Enter Bot Prefix\n")
  ownerid = input("Enter your Discord ID (Optional)\n")
  welcomechannel = input("Enter the channel ID of your welcome channel (Optional)\n")
  welcomeimage = input("Enter a custom welcome image (Optional)\n")
  generalchannel = input("Enter general channel ID (Optional)\n")
  if ownerid == "":
    ownerid = 0
  data = {
    'prefix': prefix,
    'token': token,
    'ownerid': ownerid,
    'welcomechannel': welcomechannel,
    'welcomeimage': welcomeimage,
    'generalchannel': generalchannel,
    'config': true
    }
  with open('config.json', 'w') as f:
    json.dump(data, f)
