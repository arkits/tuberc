from app.models import User, Channel 
from app import app, db

def get(client, current_user_id):
    
    response = client.subscriptions().list(part='snippet,contentDetails',mine=True).execute()

    more = True
    nextPageToken = False    
    subs_channel_id = []
    
    while more: 
        if nextPageToken:
            response = client.subscriptions().list(pageToken = nextPageToken, part='snippet',mine=True).execute()
        else:
            print ("Calling yt ")
            response = client.subscriptions().list(maxResults=50, part='snippet',mine=True).execute()
    
        items = response.get('items')
    
        for item in items:
            snippet = item.get('snippet')        
            resourceId = snippet.get('resourceId')
            channelId = resourceId.get('channelId') 
            channelId = str(channelId)
            subs_channel_id.append(channelId)
            
        nextPageToken = response.get('nextPageToken')
    
        if nextPageToken:
            more = True
        else:
            more = False 

    print ("Final subs_channel_id is " +  str(subs_channel_id))

    u = User.query.get(current_user_id)
    u.sub_chans = str(subs_channel_id)
    db.session.add(u)
    db.session.commit()

    print ("Commited succeffully....")



    

