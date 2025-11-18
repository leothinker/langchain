from os import getenv

import requests
from dotenv import load_dotenv
from get_token import _getToken

load_dotenv()

api_url = "https://graph.microsoft.com/v1.0"

token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6Ijl5cm5iTXpJeFB2aS1KZ1c5TTZRZWMwV2Zua092Z2ZsWS00aW9uQWlVNGciLCJhbGciOiJSUzI1NiIsIng1dCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSIsImtpZCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82YmIyZjQyMy1kMzVjLTRiMGYtYjViZi0wNGI1OTQ3OTQwZjIvIiwiaWF0IjoxNzYxODg0Mjc4LCJuYmYiOjE3NjE4ODQyNzgsImV4cCI6MTc2MTg4OTU5MiwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsicDEiXSwiYWlvIjoiQVpRQWEvOGFBQUFBS0pmTWh5ZHdkYXN6NHYyMjM4djBvb3dLanJCVWxRWVFHVEVsT1ZWVlhNUFZDVlVUNFZUWDg0cnBFTkxuT3VyL0RpLzZiUlhadGF5VGhIM3IxNTZNbTV4VFdXTDFQcy9UQTlHaldOQVo0bS9aeUU1M2IwbFlscExhS0NacWNXcy9ub1RhWW9ZUW5oeFkyWWs5ZmlEUlAvYUJiNkVDSVZ4ZVlIYlV0Zm0vbDRVQnNDWm4xMVJXWit1dzRVaHJFTzc0IiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBfZGlzcGxheW5hbWUiOiJlbWFpbF9hc3Npc3RhbnQiLCJhcHBpZCI6IjhhZmE0YWEwLWQ1ZmUtNGQ0My05Nzk2LTc1NmMxN2RmZWEyMSIsImFwcGlkYWNyIjoiMSIsImZhbWlseV9uYW1lIjoiTkVYWCIsImdpdmVuX25hbWUiOiJBZHZpc29yIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTE2LjQ5LjE0LjE2NiIsIm5hbWUiOiJBZHZpc29yIC0gTkVYWCIsIm9pZCI6IjBiNGI3MjUzLWFmNjYtNDk4Ny04Nzk4LTM1Mzg5ZWE3OGY1MSIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwNTJGNzU2NUU4IiwicmgiOiIxLkFWWUFJX1N5YTF6VEQwdTF2d1MxbEhsQThnTUFBQUFBQUFBQXdBQUFBQUFBQUFBaUFXVldBQS4iLCJzY3AiOiJNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbC5TZW5kIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgZW1haWwiLCJzaWQiOiIwMDliZDJiOS1hYjlhLTFkYjEtYWU0My0xZjUxOGZiOGVmZDkiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiI1WXFOdUlVdDRvX2dXM01ua0pnbUNKT3lIbldaWHNJOWZOUUw3cDMtYlFVIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFTIiwidGlkIjoiNmJiMmY0MjMtZDM1Yy00YjBmLWI1YmYtMDRiNTk0Nzk0MGYyIiwidW5pcXVlX25hbWUiOiJhZHZpc29yQG5leHgtZ2xvYmFsLmNvbSIsInVwbiI6ImFkdmlzb3JAbmV4eC1nbG9iYWwuY29tIiwidXRpIjoiV0hLRmNpRTRwRS11MjVsQ2IxTUdBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19hY2QiOjE3NjE1MTg1NzEsInhtc19hY3RfZmN0IjoiMyA5IiwieG1zX2Z0ZCI6IjRxOHRlMFVtdEFodEFTR1FLYm42QVJwRzhYQ3huNTZjcHR2RVVmeE5JWUVCWVhOcFlYTnZkWFJvWldGemRDMWtjMjF6IiwieG1zX2lkcmVsIjoiMSAyMCIsInhtc19zdCI6eyJzdWIiOiJQdFFRaDFtUFl2S21Mc1A5ZXhZRi14MXRwdGlDWEhjWnlmX2pRb3ZnWXNvIn0sInhtc19zdWJfZmN0IjoiMTIgMyIsInhtc190Y2R0IjoxNjYyNzI3MjgxLCJ4bXNfdG50X2ZjdCI6IjMgMTAifQ.BiMKnw_xfQWnMU3xQyxvf0tkXBEHUQkLvLGGvuCvzRZ5J6hm_fEcCwBIj0iBYiwWGKIq_ccaN438QElHC1YVHmGEVvcuQGKvyLsN50U5OP0aPHag7uoeYkEqSzl1WNEp2RsXM_pchN5hxDZ-C2TV6lJCkQoMCwY2xpVM5C59m2h5-hunIAZ973fmzlrYc6p8vIYlTOLKMJd7pmg0mUhskAxkb9_RVOl6kGAzw1lzrgf2mFPZg1THgeL-Q7Hae157386QuKI-DMRDoMDMojmn8bMpIfaVxWBvsNKPt72r8U-XAl9yTvN9rsoa8UfG6QzQQAd1GdXmtEftQoAsZp54Ow"


def _get_webhook():
    if token:  # = _getToken():
        webhook_url = (
            "https://isadora-seriocomic-jacquelyn.ngrok-free.dev/email/webhook"
        )
        lifecycle_url = (
            "https://isadora-seriocomic-jacquelyn.ngrok-free.dev/email/lifecycle"
        )
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
            "expirationDateTime": "2025-11-07T11:00:00.0000000Z",
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
