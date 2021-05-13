import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import pandas as pd
import json

#csv contains MD5 hash of lowercase version of list member's email address
mailchimp = pd.read_csv("YOUR_CSV")
mailchimp = mailchimp.astype(str)

actions=[]
timestamps=[]
types=[]
campaign_ids=[]
titles=[]
open_activity=[]
signup_category=[]
emailid=[]

for n in mailchimp.Hash:
    try:
      client = MailchimpMarketing.Client()
      client.set_config({
        "api_key": "YOUR_API_KEY",
        "server": "YOUR_SERVER_PREFIX"
      })

      response = client.lists.get_list_member_activity_feed("list_id", n)
      # print(n)
    except ApiClientError as error:
      print("Error: {}".format(error.text))

    for i in response['activity']:
        if i['activity_type'] == 'sent':
            actions.append(i['activity_type'])
            timestamps.append(i['created_at_timestamp'])
            types.append(' ')
            open_activity.append(' ')
            campaign_ids.append(i['campaign_id'])
            titles.append(i['campaign_title'])
            signup_category.append(' ')
            emailid.append(response['email_id'])
        elif i['activity_type'] == 'bounce':
            actions.append(i['activity_type'])
            timestamps.append(i['created_at_timestamp'])
            types.append(i['bounce_type'])
            open_activity.append(i['bounce_has_open_activity'])
            campaign_ids.append(i['campaign_id'])
            titles.append(i['campaign_title'])
            signup_category.append(' ')
            emailid.append(response['email_id'])
        else:
            actions.append(i['activity_type'])
            timestamps.append(i['created_at_timestamp'])
            types.append(' ')
            open_activity.append(' ')
            campaign_ids.append(' ')
            titles.append(' ')
            signup_category.append(i['signup_category'])
            emailid.append(response['email_id'])
        
        
mailchimpdf = pd.DataFrame()
mailchimpdf['action'] = actions
mailchimpdf['timestamp'] = timestamps
mailchimpdf['type'] = types
mailchimpdf['campaign_id'] = campaign_ids
mailchimpdf['title'] = titles
mailchimpdf['open activities'] = open_activity
mailchimpdf['signup category'] = signup_category
mailchimpdf['emailid'] = emailid
mailchimpdf.to_csv("OUTPUT_FILE")
