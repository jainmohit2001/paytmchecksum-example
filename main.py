import json
import os
import uuid

import requests
from dotenv import load_dotenv
from paytmchecksum import PaytmChecksum

load_dotenv()

PAYTM_MID = os.environ["PAYTM_MID"]
PAYTM_MERCHANT_KEY = os.environ["PAYTM_MERCHANT_KEY"]
IS_STAGING = False
PAYTM_WEBSITE_NAME = "DEFAULT"


def create_order_id():
    return f"ORDERID_{uuid.uuid4().hex}"


def main():
    order_id = create_order_id()
    amount = 1.00

    if IS_STAGING:
        callback_url = "https://securegw-stage.paytm.in/theia/paytmCallback?ORDER_ID="
    else:
        callback_url = "https://securegw.paytm.in/theia/paytmCallback?ORDER_ID="

    paytm_params = {
        "body": {
            "requestType": "Payment",
            "mid": PAYTM_MID,
            "websiteName": PAYTM_WEBSITE_NAME,
            "orderId": order_id,
            "callbackUrl": callback_url + order_id,
            "txnAmount": {
                "value": str(amount),
                "currency": "INR",
            },
            "userInfo": {
                "custId": str("test"),
            },
        },
    }

    checksum = PaytmChecksum.generateSignature(
        json.dumps(paytm_params["body"]), PAYTM_MERCHANT_KEY
    )

    paytm_params["head"] = {"signature": checksum}
    post_data = json.dumps(paytm_params)

    if IS_STAGING:
        url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MID}&orderId={order_id}"
    else:
        url = f"https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MID}&orderId={order_id}"

    try:
        response = requests.post(
            url, data=post_data, headers={"Content-type": "application/json"}
        ).json()
        print(response["body"])
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
