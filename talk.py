import pya3rt

def create_reply(user_text):
    apikey = "DZZPKSBU5XUE5wY9tfXf4QCEuOdg36C1"
    client = pya3rt.TalkClient(apikey)

    res = client.talk(user_text)
    return res['results'][0]['reply']
