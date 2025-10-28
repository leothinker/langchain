from os import getenv

import requests
from dotenv import load_dotenv
from get_token import _getToken

load_dotenv()

api_url = "https://graph.microsoft.com/v1.0"

token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ik9PQnJqVkNtUGE5aGR5dC1zM3prVXllOEljZ09NaC1uZXo1bm05ODJXZ1EiLCJhbGciOiJSUzI1NiIsIng1dCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSIsImtpZCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82YmIyZjQyMy1kMzVjLTRiMGYtYjViZi0wNGI1OTQ3OTQwZjIvIiwiaWF0IjoxNzYxNTIwOTIxLCJuYmYiOjE3NjE1MjA5MjEsImV4cCI6MTc2MTUyNTA5MSwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsicDEiXSwiYWlvIjoiQVpRQWEvOGFBQUFBTFJld3M4RHZyWDM0ZmdQN3htK0VZQWJyTDV3bzFPS3FUb2tCSTFqRGJlUS93ZDR2NjF3WHlhTm5TYVVCM0Z2RDZZeXJLdGFPeWpWcU51SEhzbm85eXVWVVhZQ3BOTjEwbWl6RlJsbytpNHpGU25aTndiNENxWkV4R2N4aHZiYldTN1hxbkJpWkpxM0trZlAzd2FPUzFybG5kaGc5QkVkYkdiaWxqTzlDaWJTTVBDamppbU5MbnQyVm9FeCsycUFIIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBfZGlzcGxheW5hbWUiOiJlbWFpbF9hc3Npc3RhbnQiLCJhcHBpZCI6IjhhZmE0YWEwLWQ1ZmUtNGQ0My05Nzk2LTc1NmMxN2RmZWEyMSIsImFwcGlkYWNyIjoiMSIsImZhbWlseV9uYW1lIjoiTkVYWCIsImdpdmVuX25hbWUiOiJBZHZpc29yIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTE2LjQ5LjE0LjE2NiIsIm5hbWUiOiJBZHZpc29yIC0gTkVYWCIsIm9pZCI6IjBiNGI3MjUzLWFmNjYtNDk4Ny04Nzk4LTM1Mzg5ZWE3OGY1MSIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwNTJGNzU2NUU4IiwicmgiOiIxLkFWWUFJX1N5YTF6VEQwdTF2d1MxbEhsQThnTUFBQUFBQUFBQXdBQUFBQUFBQUFBaUFXVldBQS4iLCJzY3AiOiJNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIwMDliZDJiOS1hYjlhLTFkYjEtYWU0My0xZjUxOGZiOGVmZDkiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiI1WXFOdUlVdDRvX2dXM01ua0pnbUNKT3lIbldaWHNJOWZOUUw3cDMtYlFVIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFTIiwidGlkIjoiNmJiMmY0MjMtZDM1Yy00YjBmLWI1YmYtMDRiNTk0Nzk0MGYyIiwidW5pcXVlX25hbWUiOiJhZHZpc29yQG5leHgtZ2xvYmFsLmNvbSIsInVwbiI6ImFkdmlzb3JAbmV4eC1nbG9iYWwuY29tIiwidXRpIjoiQmpPQzZSQndfa3llTnNGa1BScUFBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19hY2QiOjE3NjE1MTg1NzEsInhtc19hY3RfZmN0IjoiMyA5IiwieG1zX2Z0ZCI6Imh5ZDFNNFpxY2lfV0czeUVFUVNlSlpsT1VST2lXRU8wV0c4VGRMN08zNllCWVhOcFlYTnZkWFJvWldGemRDMWtjMjF6IiwieG1zX2lkcmVsIjoiMSAxMiIsInhtc19zdCI6eyJzdWIiOiJQdFFRaDFtUFl2S21Mc1A5ZXhZRi14MXRwdGlDWEhjWnlmX2pRb3ZnWXNvIn0sInhtc19zdWJfZmN0IjoiMyAxMCIsInhtc190Y2R0IjoxNjYyNzI3MjgxLCJ4bXNfdG50X2ZjdCI6IjMgMTIifQ.C4_4tdnGtogWRZx_A1E4gTzMf0EqzJO-Q_Vc029MHUDpTPtPCkxFPJNHZDZEoQWIU1P9BxWztm_ctvbOm_tlI52WmvF1_Z5xPWg8LC0lHF1u-_vw1iWM4L5kqxjnEUYDmyVuM2JDwO4z4DnE-KFvbQhi-NoN4CMBMLQrd4R9kcXqYXzWWmGDgMQ0b3M8sGJ-BM3u5mf9LRFZEIwiYMpwegRETkBRqINyBCQGnIeudVDtGn35yUPN0-Hq0su4Gem9RyqAmgo4taB_CAwS4BCyHlsCxpHLI6UpPtkt3WO9VraOdR9MOkOKZy-bo2momWjDPGuM-3-IFi2LsGt_2kmRJg"


def _get_webhook():
    if token:  # = _getToken():
        webhook_url = "https://isadora-seriocomic-jacquelyn.ngrok-free.dev/webhook"
        lifecycle_url = "https://isadora-seriocomic-jacquelyn.ngrok-free.dev/lifecycle"
        webhook_resource = "/me/mailfolders('inbox')/messages"
        # webhook_resource = f"/users/{user_id}/mailFolders('{folder_id}')/messages/"
        # webhook_resource = (
        #     "/users/advisor@nexx-global.com/mailFolders('inbox')/messages"
        # )

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        }

        subscription_data = {
            "changeType": "created,updated",
            "notificationUrl": webhook_url,
            "resource": webhook_resource,
            "expirationDateTime": "2025-10-30T11:00:00.0000000Z",
            "lifecycleNotificationUrl": lifecycle_url,
            "clientState": "9f294d2c-7396-4052-9f36-87f0548c08a4",
        }

        create_webhook = f"{api_url}/subscriptions"
        response = requests.post(
            create_webhook, headers=headers, json=subscription_data
        )

        if response.status_code == 201:
            subscription = response.json()
            print(subscription)
            print(f"Webhook Created, Subscription ID : {subscription['id']}")
        else:
            print(
                f"Failed to create webhook :  {response.status_code} - {response.text} -"
            )

    else:
        print("Access Token failed")


if __name__ == "__main__":
    _get_webhook()
