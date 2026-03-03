salesforceTestAccountActivities.py:
"""
Fetch activity history and emails (last 2 months) for a single Salesforce account.
Uses OAuth2 + httpx (no simple_salesforce). Outputs raw JSON for viewing.
"""

import json
import os
import urllib.parse
from datetime import datetime, timedelta

import httpx
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = "0018000000ufgnjAAA"
OUTPUT_FILE = f"account_{ACCOUNT_ID}_activities.json"
API_VERSION = "v60.0"


def _token_url() -> str:
    domain = (os.getenv("SF_DOMAIN") or "").strip().lower()
    if "test" in domain:
        return "https://test.salesforce.com/services/oauth2/token"
    return "https://login.salesforce.com/services/oauth2/token"


def _password_for_auth() -> str:
    password = os.getenv("SF_PASSWORD") or ""
    token = os.getenv("SF_TOKEN") or ""
    if token:
        return password + token
    return password


def _get_access_token_sync() -> tuple[str, str]:
    client_id = (os.getenv("SF_CLIENT_ID") or os.getenv("SF_CONSUMER_KEY") or "").strip()
    client_secret = (os.getenv("SF_CLIENT_SECRET") or os.getenv("SF_CONSUMER_SECRET") or "").strip()
    username = (os.getenv("SF_USERNAME") or "").strip()
    if not all([client_id, client_secret, username]):
        raise RuntimeError(
            "Missing Salesforce OAuth2 credentials: set SF_CLIENT_ID, SF_CLIENT_SECRET, SF_USERNAME, SF_PASSWORD in .env"
        )
    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": _password_for_auth(),
    }
    with httpx.Client(timeout=30.0) as c:
        r = c.post(_token_url(), data=data)
        r.raise_for_status()
        body = r.json()
        return body["access_token"], body["instance_url"]


def _normalize_soql(soql: str) -> str:
    return " ".join(soql.split()).strip()


def _query_sync(instance_url: str, access_token: str, soql: str) -> dict:
    path = f"/services/data/{API_VERSION}/query"
    url = instance_url.rstrip("/") + path + "?q=" + urllib.parse.quote(_normalize_soql(soql))
    with httpx.Client(timeout=60.0) as c:
        r = c.get(url, headers={"Authorization": f"Bearer {access_token}"})
        r.raise_for_status()
        return r.json()


def _query_more_sync(instance_url: str, access_token: str, next_records_url: str) -> dict:
    """Follow nextRecordsUrl (path only, e.g. /services/data/v60.0/query/01g...)"""
    url = instance_url.rstrip("/") + next_records_url
    with httpx.Client(timeout=60.0) as c:
        r = c.get(url, headers={"Authorization": f"Bearer {access_token}"})
        r.raise_for_status()
        return r.json()


def _strip_attributes(record: dict) -> None:
    if "attributes" in record:
        del record["attributes"]
    if record.get("Owner") and isinstance(record["Owner"], dict) and "attributes" in record["Owner"]:
        del record["Owner"]["attributes"]


def _strip_attributes_recursive(obj):
    """Strip attributes from a record and from nested records (e.g. ActivityHistories.records)."""
    if isinstance(obj, dict):
        if "attributes" in obj:
            del obj["attributes"]
        if obj.get("Owner") and isinstance(obj["Owner"], dict) and "attributes" in obj["Owner"]:
            del obj["Owner"]["attributes"]
        for v in obj.values():
            _strip_attributes_recursive(v)
    elif isinstance(obj, list):
        for item in obj:
            _strip_attributes_recursive(item)


def main():
    print("Connecting to Salesforce...")
    access_token, instance_url = _get_access_token_sync()
    print("Connected. Fetching account and activity history...")

    # 1. Account + ActivityHistories (last 6 months). Try WITH WHERE first.
    q_account = f"""
        SELECT Id, Name, Website, BillingCity, BillingCountry,
               (SELECT Id, ActivityDate, ActivityType, Description, Subject
                FROM ActivityHistories
                WHERE ActivityDate = LAST_N_DAYS:60
                ORDER BY ActivityDate DESC
                LIMIT 500)
        FROM Account
        WHERE Id = '{ACCOUNT_ID}'
    """
    try:
        res = _query_sync(instance_url, access_token, q_account)
    except Exception as e:
        if "ActivityHistories" in str(e) or "WHERE" in str(e):
            # Fallback: no WHERE in subquery, filter in Python
            q_account = f"""
                SELECT Id, Name, Website, BillingCity, BillingCountry,
                       (SELECT Id, ActivityDate, ActivityType, Description, Subject
                        FROM ActivityHistories
                        ORDER BY ActivityDate DESC
                        LIMIT 500)
                FROM Account
                WHERE Id = '{ACCOUNT_ID}'
            """
            res = _query_sync(instance_url, access_token, q_account)
        else:
            raise

    if res.get("totalSize", 0) == 0:
        print("Account not found.")
        return

    account = res["records"][0].copy()
    _strip_attributes_recursive(account)

    # Optionally filter ActivityHistories by date in Python (if we used fallback without WHERE)
    cutoff = (datetime.now() - timedelta(days=60)).date()
    if "ActivityHistories" in account and account["ActivityHistories"].get("records"):
        records = account["ActivityHistories"]["records"]
        filtered = []
        for r in records:
            ad = r.get("ActivityDate")
            if ad is None:
                filtered.append(r)
                continue
            if isinstance(ad, str) and "T" in ad:
                ad = datetime.fromisoformat(ad.replace("Z", "+00:00")).date()
            elif isinstance(ad, str):
                ad = datetime.strptime(ad, "%Y-%m-%d").date()
            if ad >= cutoff:
                filtered.append(r)
        account["ActivityHistories"]["records"] = filtered
        account["ActivityHistories"]["totalSize"] = len(filtered)

    # 2. Contact IDs (and optionally Case IDs) for this account
    q_contacts = f"SELECT Id FROM Contact WHERE AccountId = '{ACCOUNT_ID}'"
    contact_ids = []
    try:
        cont_res = _query_sync(instance_url, access_token, q_contacts)
        contact_ids = [r["Id"] for r in cont_res.get("records", []) if r.get("Id")]
    except Exception as e:
        print(f"Contact query warning: {e}")

    q_cases = f"SELECT Id FROM Case WHERE AccountId = '{ACCOUNT_ID}'"
    case_ids = []
    try:
        case_res = _query_sync(instance_url, access_token, q_cases)
        case_ids = [r["Id"] for r in case_res.get("records", []) if r.get("Id")]
    except Exception:
        pass

    related_ids = contact_ids + case_ids
    emails = []

    if related_ids:
        id_list = "','".join(related_ids)
        q_emails = f"""
            SELECT Id, MessageDate, Subject, FromAddress, ToAddress, TextBody, HtmlBody, RelatedToId
            FROM EmailMessage
            WHERE RelatedToId IN ('{id_list}')
            AND MessageDate = LAST_N_DAYS:60
            ORDER BY MessageDate DESC
        """
        try:
            em_res = _query_sync(instance_url, access_token, q_emails)
            emails.extend(em_res.get("records", []))
            while not em_res.get("done", True) and em_res.get("nextRecordsUrl"):
                em_res = _query_more_sync(instance_url, access_token, em_res["nextRecordsUrl"])
                emails.extend(em_res.get("records", []))
        except Exception as e:
            print(f"EmailMessage query warning (feature may be disabled): {e}")

    for rec in emails:
        _strip_attributes(rec)

    # Count "Email" type activities (these are Task records — your logged emails live here)
    ah = account.get("ActivityHistories", {})
    ah_records = ah.get("records", []) if isinstance(ah, dict) else []
    ah_count = len(ah_records)
    email_activity_count = sum(1 for r in ah_records if r.get("ActivityType") == "Email")

    payload = {"account": account, "emails": emails}

    out_path = os.path.abspath(OUTPUT_FILE)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, default=str)

    print(f"SUCCESS! Raw JSON saved to: {out_path}")
    print(f"  Account: {account.get('Name', '?')} (Id: {account.get('Id', '?')})")
    print(f"  Activity history records (Tasks/Events, last 2 months): {ah_count}")
    print(f"  — of which Email-type activities (logged emails in ActivityHistory): {email_activity_count}")
    print(f"  EmailMessage records (Enhanced Email / Email-to-Case object): {len(emails)}")


if __name__ == "__main__":
    main()



Output Data:
{
  "account": {
    "Id": "0018000000ufgnjAAA",
    "Name": "Premia Solutions Limited",
    "Website": "www.premiasolutions.com",
    "BillingCity": "Warwick",
    "BillingCountry": "United Kingdom",
    "ActivityHistories": {
      "totalSize": 14,
      "done": true,
      "records": [
        {
          "Id": "00TOF00000hil5h2AA",
          "ActivityDate": "2026-02-10",
          "ActivityType": "Meeting",
          "Description": null,
          "Subject": "Azure Platform Cost Review"
        },
        {
          "Id": "00TOF00000k2JCE2A2",
          "ActivityDate": "2026-02-10",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Re: [peer1.com #2410043] [7008621]  Aptum Order 279799 Confirmation\nBody:\nHi Neil\n\nThe link doesn\u2019t work for me, but I\u2019m guessing it\u2019s a couple of orders that have appeared in your portal ?\n\nIf so, we\u2019re going to cover off in our call at 2.\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Tuesday, 10 February 2026 at 13:26\n\nTo: Darren Wells <darren.wells@aptum.com>\n\nSubject: FW: [peer1.com #2410043] [7008621] Aptum Order 279799 Confirmation\n\nHi Darren,\n\nQuick question - what is this for? Has it been sent in error?\n\nRegards,\n\nNeil\n\nNeil Turner\n\nIT Director\n\nMobile: 07711 886890\n\nEmail: neil@premiasolutions.com\n\nWeb: \nhttps://can01.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.premiasolutions.com%2F&data=05%7C02%7Cdarren.wells%40aptum.com%7Cc918888916ca47b820c508de68a7f115%7Cad69d4224fa742b0a4d3f58410f311ed%7C1%7C0%7C639063267734821407%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=wp0%2FMWtSV%2BrnGpiXw628l6MOFzw2bgfArGhREOfcnsw%3D&reserved=0\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use it, or any part of it, in any form whatsoever. If you have received this e-mail\n in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are solely those of the author and do not necessarily represent those of Premia Solutions\n Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n-----Original Message-----\n\nFrom: support@aptum.com <support@aptum.com>\n\nSent: 10 February 2026 11:51\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nSubject: [peer1.com #2410043] [7008621] Aptum Order 279799 Confirmation\n\nExternal email. Use caution.\n\nDear Neil Turner\n\nThank you for choosing Aptum. To begin working on your solution:\n\n\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 DRaaS\n\nPlease review the 4 simple steps below to get your new solution started.\n\n=== Step 1 - Review and Accept Order ===\n\nLog in to the Aptum portal with the username below:\n\nhttps://can01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fmypeer1.com%2Fmy-account%2Forders.php%3Fid%3D279799&data=05%7C02%7Cdarren.wells%40aptum.com%7Cc918888916ca47b820c508de68a7f115%7Cad69d4224fa742b0a4d3f58410f311ed%7C1%7C0%7C639063267734854260%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=mLC%2F1BOAHin%2Fb0vPV9WYj6uJQUOoX5rQlJzD3ghVc60%3D&reserved=0\n\nUsername = neilturner\n\nA unique password was emailed to you separately, please change it once have logged in.\n\nNote: If the link to the order does not work for you, login to the portal and select menu options My Account -> Account Summary -> Order History to list unapproved orders.\n\nOnce you have logged in, please review the order details. If you agree to and accept the order, press APPROVE. If the order is not accurate, please call your Account Manager.\n\n=== Step 2 - Order Provisioning ===\n\nAfter the order is approved, our provisioning team will start building your solution. Standard solutions generally take three to five business days to provision. Complex orders may take longer. Please contact your Account Manager for an estimated build-time.\n\n=== Step 3 - Welcome Email ===\n\nOnce your new hosting solution is ready, you will receive an email alert notifying you.\n\n=== Step 4 - Order Complete ===\n\nCongratulations! You are now ready to begin using your new Aptum solution. If you have any further questions, please contact your Account Manager.\n\nUS (Toll Free): 888 978 7251\n\nUK (Toll Free): 0800 840 7499\n\nFrance: 0805 210 280\n\nAll other countries: 001 646 396 0422\n\nThank you for choosing Aptum as your IT hosting provider.\n\nSincerely,\n\nAptum\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office at Building\n 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments, and do not\n use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy policy outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Re: [peer1.com #2410043] [7008621]  Aptum Order 279799 Confirmation"
        },
        {
          "Id": "00TOF00000jyrQx2AI",
          "ActivityDate": "2026-02-08",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Re: [peer1.com #2410014] [7008621][7337471 :: Premia.DRaaS]  Your cancellation request has been received.\nBody:\nSorry Neil, yes it is.\u00a0\nI raised it internally as it seems it was overlooked on the original ticket.\u00a0\nDarren WellsSenior Strategic Account Manager+44 7852 926026\naptum.com | LinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\nSent: Sunday, February 8, 2026 3:19:36 PM\nTo: Darren Wells <darren.wells@aptum.com>\nSubject: FW: [peer1.com #2410014] [7008621][7337471 :: Premia.DRaaS] Your cancellation request has been received. \u00a0Hi Darren,\n\nJust checking that this was in response to the email I sent the other day?\n\nRegards,\n\nNeil\n\nNeil Turner\nIT Director\n\nMobile: 07711 886890\nEmail: neil@premiasolutions.com\nWeb: https://can01.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.premiasolutions.com%2F&data=05%7C02%7Cdarren.wells%40aptum.com%7Cf19e053fe8074a2edbb108de67257ac0%7Cad69d4224fa742b0a4d3f58410f311ed%7C1%7C0%7C639061607867944219%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=3D%2Fx%2FwLYHhRjpGluEqOMLiNhFefWXo9xRbmNtrp0p1I%3D&reserved=0\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\nRegistered number: 4088720\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a result of any viruses being passed on.\nPlease consider the Environment before printing this email.\n\n-----Original Message-----\nFrom: Apache <tickets@peer1.com>\nSent: 05 February 2026 17:15\nTo: Neil Turner <neil@premiasolutions.com>\nSubject: [peer1.com #2410014] [7008621][7337471 :: Premia.DRaaS] Your cancellation request has been received.\n\nExternal email. Use caution.\n\nGreetings,\n\nThis message has been automatically generated in response to the creation of a trouble ticket regarding:\n\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 \"[7008621][7337471 :: Premia.DRaaS]\u00a0 Your cancellation request has been received.\", a summary of which appears below.\n\nYour ticket has been assigned an ID of [peer1.com #2410014].\n\nAll updates can be viewed or submitted online at https://can01.safelinks.protection.outlook.com/?url=https%3A%2F%2Fmypeer1.com%2F&data=05%7C02%7Cdarren.wells%40aptum.com%7Cf19e053fe8074a2edbb108de67257ac0%7Cad69d4224fa742b0a4d3f58410f311ed%7C1%7C0%7C639061607867958240%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=h4oaQoYEejQnSl8MaIXMtfQe5QdRuyww43oURW6oJVw%3D&reserved=0.\n\nIf you choose to reply to this ticket via email, please include the string:\n\n\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0\u00a0 [peer1.com #2410014]\n\nin the subject line of all correspondence about this issue.\n\nBest regards,\n\nPEER 1 Hosting\n-------------------------------------------------------------------------\nYour cancellation request has been received.\n\nCancellation details\n\nService:\n7337471 :: Premia.DRaaS\n\nReason: Not leaving, just moving to another Product Additional comments: https://aptum.atlassian.net/browse/APTUM-48673\noffline date Dec 20, 2025\nno etf\n\nYou may be contacted by a Aptum employee to discuss your reasons for canceling.\n\nSincerely,\nAptum Managed Hosting Team",
          "Subject": "Email: Re: [peer1.com #2410014] [7008621][7337471 :: Premia.DRaaS]  Your cancellation request has been received."
        },
        {
          "Id": "00TOF00000joyaE2AQ",
          "ActivityDate": "2026-02-05",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: accounts@premiasolutions.com; steve.watts@premiasolutions.com\nBCC: \nAttachment: --none--\n\nSubject: Re: Your Aptum  Invoice is Ready 9125505\nBody:\nMorning Neil\n\nI\u2019ll investigate and get back to you.\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Thursday, 5 February 2026 at 09:18\n\nTo: Darren Wells <darren.wells@aptum.com>\n\nCc: Accounts <accounts@premiasolutions.com>, Steve Watts <steve.watts@premiasolutions.com>\n\nSubject: RE: Your Aptum Invoice is Ready 9125505\n\nMorning Darren,\n\n\u00a0\n\nI hope that you are well.\n\n\u00a0\n\nThere was a DrasS line on our invoice to cover the period for March. Is this correct? I thought that we had removed DR because we are only on self-hosted and only require backups to be taken?\n\n\u00a0\n\nRegards,\n\n\u00a0\n\nNeil\n\n\u00a0\n\n\u00a0\n\n\u00a0\n\n\u00a0\n\nNeil Turner\n\nIT Director\n\n\u00a0\n\n\u00a0\n\nMobile: 07711 886890\n\nEmail:\nneil@premiasolutions.com\n\nWeb: www.premiasolutions.com\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\u00a0\u00a0\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\n\u00a0\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use\n it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are\n solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a\n result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n\u00a0\n\nFrom:\u00a0Aptum Billing <billing@aptum.com>\n\nSent:\u00a004 February 2026 17:42\n\nTo:\u00a0Neil Turner <neil@premiasolutions.com>; Accounts <accounts@premiasolutions.com>\n\nSubject:\u00a0Your Aptum Invoice is Ready 9125505\n\n\u00a0\n\nExternal email. Use caution.\n\n\u00a0\nGreetings!\nThank you for choosing Aptum Technologies Inc. for your business critical hosting needs.\nYour most recent invoice is attached.\u00a0 For managed, dedicated, colocation and Mission Critical Cloud services, please log in to your account,\nwww.mypeer1.com,\n to access invoice and payment history from previous periods, or to update your account information. To help us service you better, please contact us through the\nwww.mypeer1.com\u00a0portal\n with questions or comments about your invoice. Simply submit a support ticket by clicking the SUPPORT tab, then REQUEST SUPPORT, followed by selecting the BILLING ISSUES category. You can also review our Billing FAQs inside the portal for answers to common\n questions.\nWarm regards,\nBilling Department\n\nAptum Technologies Inc.\nBilling Enquiries\n\nUS and Canada: 1.877.720.2228\n\nUK: 0800 840 7498\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office at Building\n 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments, and do not\n use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy policy outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Re: Your Aptum  Invoice is Ready 9125505"
        },
        {
          "Id": "00TOF00000jXofM2AS",
          "ActivityDate": "2026-01-30",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Re: Azure Migration - Out-of-Scope Project Work\nBody:\nMorning Neil\n\nSorry for asking again, but have you had a chance to discuss with Steve yet?\n\nAll the best\n\nDarren\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Darren Wells <Darren.Wells@aptum.com>\n\nDate: Wednesday, 21 January 2026 at 16:53\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nSubject: Re: Azure Migration - Out-of-Scope Project Work\n\nGreat, thanks for confirming Neil.\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Wednesday, 21 January 2026 at 16:50\n\nTo: Darren Wells <Darren.Wells@aptum.com>\n\nSubject: RE: Azure Migration - Out-of-Scope Project Work\n\nHi Darren,\n\nYes, received ok. I have yet to find time to discuss with Steve.\n\n\u00a0\n\nHopefully I will in the next few days.\n\n\u00a0\n\nRegards,\n\nNeil\n\n\u00a0\n\n\u00a0\n\nNeil Turner\n\nIT Director\n\n\u00a0\n\n\u00a0\n\nMobile: 07711 886890\n\nEmail:\nneil@premiasolutions.com\n\nWeb: www.premiasolutions.com\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\u00a0\u00a0\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\n\u00a0\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use\n it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are\n solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a\n result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n\u00a0\n\nFrom:\u00a0Darren Wells <Darren.Wells@aptum.com>\n\nSent:\u00a021 January 2026 16:47\n\nTo:\u00a0Neil Turner <neil@premiasolutions.com>\n\nSubject:\u00a0FW: Azure Migration - Out-of-Scope Project Work\n\n\u00a0\n\nExternal email. Use caution.\n\n\u00a0\n\nHi Neil\n\n\u00a0\n\nHope all\u2019s well.\n\n\u00a0\n\nJust wanted to check you saw my mail from earlier this week and get your thoughts\u2026\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\nFrom: Darren Wells <Darren.Wells@aptum.com>\n\nDate: Monday, 19 January 2026 at 15:04\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nCc: Steve Watts <steve.watts@premiasolutions.com>,\n Andy Petterson <Andy.Petterson@aptum.com>,\n Robert Grafton <Robert.Grafton@aptum.com>,\n Mike Julier <Mike.Julier@aptum.com>,\n Lacie Allen-Morley <Lacie.Kemp@aptum.com>\n\nSubject: Azure Migration - Out-of-Scope Project Work\n\nHi Neil\n\n\u00a0\n\nAs per our recent discussions, please find attached the 'Change Order' that captures the changes made to our original RPF proposal, the rationale behind these, and some resultant MRC savings where applicable.\n\n\u00a0\n\nI\u2019ve also attached two topology schematics outlining the \u2018before\u2019 and \u2018after\u2019 states.\n\n\u00a0\n\nPremia Azure Solution Original Topology 2 subscriptions.pdf\u00a0- This one is the original diagram we included in our RFP and Rob has marked in red the bits that were removed/changed later during the project with\n Azure Files & Entra Domain Services, and yellow that were moved into a separate Demo subscription.\n\nPremia Azure Solution Topology Live 2.4 Differences\u00a0- This is the final architecture diagram for Live. Again, Rob has marked the services that were additional to the original RFP (Entra Domain Services, Azure Files, Azure Site Recovery and the new SQL\n server live-report-db).\n\n\u00a0\n\nAs previously mentioned, we actually clocked up about 200 additional hours over and above those included in our RFP proposal, but have only billed for 100 hours as we feel that\u2019s a more reasonable\n compromise.\n\n\u00a0\n\nLet me know your thoughts and if you\u2019re happy to proceed, I can submit via AdobeSign.\n\n\u00a0\n\nAll the best\n\nDarren\u00a0\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\n\u00a0\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office\n at Building 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments,\n and do not use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy\n policy\u00a0outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Re: Azure Migration - Out-of-Scope Project Work"
        },
        {
          "Id": "00TOF00000jYsh22AC",
          "ActivityDate": "2026-01-30",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Re: Azure Migration - Out-of-Scope Project Work\nBody:\nExcellent, thanks Neil, that\u2019s great to hear.\n\nI need do two things; raise an order in your portal, and send the change order to you via AdobeSign.\n\nI\u2019ll crack on with both now.\n\nHave a great weekend.\n\nDarren\u00a0\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Friday, 30 January 2026 at 16:06\n\nTo: Darren Wells <Darren.Wells@aptum.com>\n\nSubject: RE: Azure Migration - Out-of-Scope Project Work\n\nHi Darren,\n\n\u00a0\n\nI reviewed with Steve and Gavin this morning.\n\n\u00a0\n\nHappy to say that we are happy with the out-of-scope document and the charge of \u00a317,500. You guys have done an wonderful job on the migration and we fully understand the reasons for the changes to the architecture that have taken\n place during the build and migration.\n\n\u00a0\n\nWhat do we need to do next? Do you create an order?\n\n\u00a0\n\nRegards,\n\n\u00a0\n\nNeil\n\n\u00a0\n\n\u00a0\n\nNeil Turner\n\nIT Director\n\n\u00a0\n\n\u00a0\n\nMobile: 07711 886890\n\nEmail:\nneil@premiasolutions.com\n\nWeb: www.premiasolutions.com\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\u00a0\u00a0\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\n\u00a0\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use\n it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are\n solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a\n result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n\u00a0\n\nFrom:\u00a0Darren Wells <Darren.Wells@aptum.com>\n\nSent:\u00a030 January 2026 09:48\n\nTo:\u00a0Neil Turner <neil@premiasolutions.com>\n\nSubject:\u00a0Re: Azure Migration - Out-of-Scope Project Work\n\n\u00a0\n\nExternal email. Use caution.\n\n\u00a0\n\nMorning Neil\n\n\u00a0\n\nSorry for asking again, but have you had a chance to discuss with Steve yet?\n\n\u00a0\n\nAll the best\n\nDarren\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\nFrom: Darren Wells <Darren.Wells@aptum.com>\n\nDate: Wednesday, 21 January 2026 at 16:53\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nSubject: Re: Azure Migration - Out-of-Scope Project Work\n\nGreat, thanks for confirming Neil.\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Wednesday, 21 January 2026 at 16:50\n\nTo: Darren Wells <Darren.Wells@aptum.com>\n\nSubject: RE: Azure Migration - Out-of-Scope Project Work\n\nHi Darren,\n\nYes, received ok. I have yet to find time to discuss with Steve.\n\n\u00a0\n\nHopefully I will in the next few days.\n\n\u00a0\n\nRegards,\n\nNeil\n\n\u00a0\n\n\u00a0\n\nNeil Turner\n\nIT Director\n\n\u00a0\n\n\u00a0\n\nMobile: 07711 886890\n\nEmail:\nneil@premiasolutions.com\n\nWeb: www.premiasolutions.com\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\u00a0\u00a0\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\n\u00a0\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use\n it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are\n solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a\n result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n\u00a0\n\nFrom:\u00a0Darren Wells <Darren.Wells@aptum.com>\n\nSent:\u00a021 January 2026 16:47\n\nTo:\u00a0Neil Turner <neil@premiasolutions.com>\n\nSubject:\u00a0FW: Azure Migration - Out-of-Scope Project Work\n\n\u00a0\n\nExternal email. Use caution.\n\n\u00a0\n\nHi Neil\n\n\u00a0\n\nHope all\u2019s well.\n\n\u00a0\n\nJust wanted to check you saw my mail from earlier this week and get your thoughts\u2026\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\nFrom: Darren Wells <Darren.Wells@aptum.com>\n\nDate: Monday, 19 January 2026 at 15:04\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nCc: Steve Watts <steve.watts@premiasolutions.com>,\n Andy Petterson <Andy.Petterson@aptum.com>,\n Robert Grafton <Robert.Grafton@aptum.com>,\n Mike Julier <Mike.Julier@aptum.com>,\n Lacie Allen-Morley <Lacie.Kemp@aptum.com>\n\nSubject: Azure Migration - Out-of-Scope Project Work\n\nHi Neil\n\n\u00a0\n\nAs per our recent discussions, please find attached the 'Change Order' that captures the changes made to our original RPF proposal, the rationale behind these, and some resultant MRC savings where applicable.\n\n\u00a0\n\nI\u2019ve also attached two topology schematics outlining the \u2018before\u2019 and \u2018after\u2019 states.\n\n\u00a0\n\nPremia Azure Solution Original Topology 2 subscriptions.pdf\u00a0- This one is the original diagram we included in our RFP and Rob has marked in red the bits that were removed/changed later during the project with\n Azure Files & Entra Domain Services, and yellow that were moved into a separate Demo subscription.\n\nPremia Azure Solution Topology Live 2.4 Differences\u00a0- This is the final architecture diagram for Live. Again, Rob has marked the services that were additional to the original RFP (Entra Domain Services, Azure Files, Azure Site Recovery and the new SQL\n server live-report-db).\n\n\u00a0\n\nAs previously mentioned, we actually clocked up about 200 additional hours over and above those included in our RFP proposal, but have only billed for 100 hours as we feel that\u2019s a more reasonable\n compromise.\n\n\u00a0\n\nLet me know your thoughts and if you\u2019re happy to proceed, I can submit via AdobeSign.\n\n\u00a0\n\nAll the best\n\nDarren\u00a0\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\n\u00a0\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office\n at Building 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments,\n and do not use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy\n policy\u00a0outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Re: Azure Migration - Out-of-Scope Project Work"
        },
        {
          "Id": "00TOF00000jZ01l2AC",
          "ActivityDate": "2026-01-30",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Re: Signature requested on \"Aptum CHANGE ORDER for Premia Solutions\"\nBody:\nIt certainly has, thank you !\n\nLacie will sign it now and you\u2019ll get a fully signed copy in your inbox soon.\n\nAlso, the corresponding order should be in your portal now, if you could approve please.\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Friday, 30 January 2026 at 16:57\n\nTo: Darren Wells <Darren.Wells@aptum.com>\n\nSubject: RE: Signature requested on \"Aptum CHANGE ORDER for Premia Solutions\"\n\nThat\u2019s all signed, I think.\n\n\u00a0\n\n\u00a0\n\nNeil Turner\n\nIT Director\n\n\u00a0\n\n\u00a0\n\nMobile: 07711 886890\n\nEmail:\nneil@premiasolutions.com\n\nWeb: www.premiasolutions.com\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\u00a0\u00a0\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\n\u00a0\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use\n it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are\n solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a\n result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n\u00a0\n\nFrom:\u00a0Darren Wells via Adobe Acrobat Sign <echosign@echosign.com>\n\nSent:\u00a030 January 2026 16:45\n\nTo:\u00a0Neil Turner <neil@premiasolutions.com>\n\nSubject:\u00a0Signature requested on \"Aptum CHANGE ORDER for Premia Solutions\"\n\n\u00a0\n\nExternal email. Use caution.\n\n\u00a0\n\n\u00a0\n\n\u00a0\n\nPlease review and complete this document.\n\nDarren Wells requests your signature on\n\nAptum\n CHANGE ORDER for Premia Solutions\n\n\u00a0\n\nReview\n and sign\n\n\u00a0\n\n\u00a0\n\nPlease review and complete this document.\n\nDarren Wells\nDarren.Wells@aptum.com\n\n\u00a0\n\n\u00a0\n\nAfter you sign Aptum CHANGE ORDER for Premia Solutions, the agreement will be sent to\nlacie.allen-morley@aptum.com.\n Then, all parties will receive a final PDF copy.\n\n\u00a0\n\nDon't forward this email:\u00a0if you don't want to sign, you can\ndelegate\u00a0to\n someone else.\n\nBy proceeding, you agree that this agreement may be signed using electronic or handwritten signatures.\nTo ensure that you continue receiving our emails, please add\nechosign@echosign.com\u00a0to\n your address book or safe list.\n\u00a9 2026 Adobe. All rights reserved.\n\n\u00a0\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office at Building\n 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments, and do not\n use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy policy outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Re: Signature requested on \"Aptum CHANGE ORDER for Premia Solutions\""
        },
        {
          "Id": "00TOF00000jNGX32AO",
          "ActivityDate": "2026-01-28",
          "ActivityType": "Meeting",
          "Description": null,
          "Subject": "Service Review"
        },
        {
          "Id": "00TOF00000jNK2g2AG",
          "ActivityDate": "2026-01-27",
          "ActivityType": "Meeting",
          "Description": null,
          "Subject": "Azure Migration Project Sync"
        },
        {
          "Id": "00TOF00000j8T1W2AU",
          "ActivityDate": "2026-01-21",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Re: Azure Migration - Out-of-Scope Project Work\nBody:\nGreat, thanks for confirming Neil.\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Neil Turner <neil@premiasolutions.com>\n\nDate: Wednesday, 21 January 2026 at 16:50\n\nTo: Darren Wells <Darren.Wells@aptum.com>\n\nSubject: RE: Azure Migration - Out-of-Scope Project Work\n\nHi Darren,\n\nYes, received ok. I have yet to find time to discuss with Steve.\n\n\u00a0\n\nHopefully I will in the next few days.\n\n\u00a0\n\nRegards,\n\nNeil\n\n\u00a0\n\n\u00a0\n\nNeil Turner\n\nIT Director\n\n\u00a0\n\n\u00a0\n\nMobile: 07711 886890\n\nEmail:\nneil@premiasolutions.com\n\nWeb: www.premiasolutions.com\n\nPremia Solutions Limited, 3 Corunna Court, Corunna Road, Warwick CV34 5HQ\u00a0\u00a0\n\nRegistered office: 20 Fenchurch Street, 5th Floor, London, EC3M 3BY\n\nRegistered number: 4088720\n\n\u00a0\n\nPremia Solutions Limited are authorised and regulated by the Financial Conduct Authority.\n\nThis e-mail and any files transmitted with it are confidential and intended for the addressee only. If you are not the addressee you may not copy, forward, disclose or otherwise use\n it, or any part of it, in any form whatsoever. If you have received this e-mail in error please notify the sender and ensure that all copies of this e-mail and any files transmitted with it are deleted. Any views or opinions represented in this e-mail are\n solely those of the author and do not necessarily represent those of Premia Solutions Limited. Although this e-mail and its attachments have been scanned for the presence of computer viruses, Premia Solutions Limited will not be liable for any losses as a\n result of any viruses being passed on.\n\nPlease consider the Environment before printing this email.\n\n\u00a0\n\nFrom:\u00a0Darren Wells <Darren.Wells@aptum.com>\n\nSent:\u00a021 January 2026 16:47\n\nTo:\u00a0Neil Turner <neil@premiasolutions.com>\n\nSubject:\u00a0FW: Azure Migration - Out-of-Scope Project Work\n\n\u00a0\n\nExternal email. Use caution.\n\n\u00a0\n\nHi Neil\n\n\u00a0\n\nHope all\u2019s well.\n\n\u00a0\n\nJust wanted to check you saw my mail from earlier this week and get your thoughts\u2026\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\nFrom: Darren Wells <Darren.Wells@aptum.com>\n\nDate: Monday, 19 January 2026 at 15:04\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nCc: Steve Watts <steve.watts@premiasolutions.com>,\n Andy Petterson <Andy.Petterson@aptum.com>,\n Robert Grafton <Robert.Grafton@aptum.com>,\n Mike Julier <Mike.Julier@aptum.com>,\n Lacie Allen-Morley <Lacie.Kemp@aptum.com>\n\nSubject: Azure Migration - Out-of-Scope Project Work\n\nHi Neil\n\n\u00a0\n\nAs per our recent discussions, please find attached the 'Change Order' that captures the changes made to our original RPF proposal, the rationale behind these, and some resultant MRC savings where applicable.\n\n\u00a0\n\nI\u2019ve also attached two topology schematics outlining the \u2018before\u2019 and \u2018after\u2019 states.\n\n\u00a0\n\nPremia Azure Solution Original Topology 2 subscriptions.pdf\u00a0- This one is the original diagram we included in our RFP and Rob has marked in red the bits that were removed/changed later during the project with\n Azure Files & Entra Domain Services, and yellow that were moved into a separate Demo subscription.\n\nPremia Azure Solution Topology Live 2.4 Differences\u00a0- This is the final architecture diagram for Live. Again, Rob has marked the services that were additional to the original RFP (Entra Domain Services, Azure Files, Azure Site Recovery and the new SQL\n server live-report-db).\n\n\u00a0\n\nAs previously mentioned, we actually clocked up about 200 additional hours over and above those included in our RFP proposal, but have only billed for 100 hours as we feel that\u2019s a more reasonable\n compromise.\n\n\u00a0\n\nLet me know your thoughts and if you\u2019re happy to proceed, I can submit via AdobeSign.\n\n\u00a0\n\nAll the best\n\nDarren\u00a0\n\n\u00a0\n\n\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\nLinkedIn\n\n\u00a0\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office\n at Building 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments,\n and do not use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy\n policy\u00a0outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Re: Azure Migration - Out-of-Scope Project Work"
        },
        {
          "Id": "00TOF00000j8Eci2AE",
          "ActivityDate": "2026-01-21",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: FW: Azure Migration - Out-of-Scope Project Work\nBody:\nHi Neil\n\nHope all\u2019s well.\n\nJust wanted to check you saw my mail from earlier this week and get your thoughts\u2026\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nFrom: Darren Wells <Darren.Wells@aptum.com>\n\nDate: Monday, 19 January 2026 at 15:04\n\nTo: Neil Turner <neil@premiasolutions.com>\n\nCc: Steve Watts <steve.watts@premiasolutions.com>, Andy Petterson <Andy.Petterson@aptum.com>, Robert Grafton <Robert.Grafton@aptum.com>, Mike Julier <Mike.Julier@aptum.com>, Lacie Allen-Morley <Lacie.Kemp@aptum.com>\n\nSubject: Azure Migration - Out-of-Scope Project Work\n\nHi Neil\n\nAs per our recent discussions, please find attached the 'Change Order' that captures the changes made to our original RPF proposal, the rationale behind these, and some resultant MRC savings where applicable.\n\nI\u2019ve also attached two topology schematics outlining the \u2018before\u2019 and \u2018after\u2019 states.\n\nPremia Azure Solution Original Topology 2 subscriptions.pdf\u00a0- This one is the original diagram we included in our RFP and Rob has marked in red the bits that were removed/changed later during the project with Azure Files & Entra Domain Services, and\n yellow that were moved into a separate Demo subscription.\n\nPremia Azure Solution Topology Live 2.4 Differences\u00a0- This is the final architecture diagram for Live. Again, Rob has marked the services that were additional to the original RFP (Entra Domain Services, Azure Files, Azure Site Recovery and the new SQL\n server live-report-db).\n\nAs previously mentioned, we actually clocked up about 200 additional hours over and above those included in our RFP proposal, but have only billed for 100 hours as we feel that\u2019s a more reasonable compromise.\n\nLet me know your thoughts and if you\u2019re happy to proceed, I can submit via AdobeSign.\n\nAll the best\n\nDarren\u00a0\n\nDarren Wells\n\nSenior Strategic Account Manager\n\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office at Building\n 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments, and do not\n use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy policy outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: FW: Azure Migration - Out-of-Scope Project Work"
        },
        {
          "Id": "00TOF00000j12KT2AY",
          "ActivityDate": "2026-01-19",
          "ActivityType": "Email",
          "Description": "Additional To: neil@premiasolutions.com\nCC: steve.watts@premiasolutions.com; andy.petterson@aptum.com; robert.grafton@aptum.com; mike.julier@aptum.com; lacie.kemp@aptum.com\nBCC: \nAttachment: C2_signature_aptum580x112_5c0f9e4b-2cdb-478b-b067-a306e7c6cf32.png, Premia Azure Solution Topology Live 2.4 Differences.pdf, Premia Azure Solution Original Topology 2 subscriptions.pdf, Aptum CHANGE ORDER for Premia Solutions.pdf\n\nSubject: Azure Migration - Out-of-Scope Project Work\nBody:\nHi Neil\n\nAs per our recent discussions, please find attached the 'Change Order' that captures the changes made to our original RPF proposal, the rationale behind these, and some resultant MRC savings where applicable.\n\nI\u2019ve also attached two topology schematics outlining the \u2018before\u2019 and \u2018after\u2019 states.\n\nPremia Azure Solution Original Topology 2 subscriptions.pdf - This one is the original diagram we included in our RFP and Rob has marked in red the bits that were removed/changed later during the project with Azure Files & Entra Domain Services, and yellow that were moved into a separate Demo subscription.\n\nPremia Azure Solution Topology Live 2.4 Differences - This is the final architecture diagram for Live. Again, Rob has marked the services that were additional to the original RFP (Entra Domain Services, Azure Files, Azure Site Recovery and the new SQL server live-report-db).\n\nAs previously mentioned, we actually clocked up about 200 additional hours over and above those included in our RFP proposal, but have only billed for 100 hours as we feel that\u2019s a more reasonable compromise.\n\nLet me know your thoughts and if you\u2019re happy to proceed, I can submit via AdobeSign.\n\nAll the best\nDarren\n\n\nDarren Wells\nSenior Strategic Account Manager\n\n+44 7852 926026\naptum.com<https://www.aptum.com> | LinkedIn<https://www.linkedin.com/company/aptum>\n\n[Aptum logo]<https://www.aptum.com/>\n\n\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office at Building 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments, and do not use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our privacy policy<https://aptum.com/legal/> outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Azure Migration - Out-of-Scope Project Work"
        },
        {
          "Id": "00TOF00000il76M2AQ",
          "ActivityDate": "2026-01-13",
          "ActivityType": "Meeting",
          "Description": null,
          "Subject": "Azure Migration Review"
        },
        {
          "Id": "00TOF00000iYA8d2AG",
          "ActivityDate": "2026-01-08",
          "ActivityType": "Email",
          "Description": "To: neil@premiasolutions.com\nCC: \nBCC: \nAttachment: --none--\n\nSubject: Azure Migration - Out-of-Scope Project Work\nBody:\nMorning Neil\n\nHappy New Year !\n\nJust a quick update to say that I\u2019ve got the documentation and commercials for the out-of-scope project work now, but I'm just awaiting the \u2018before\u2019 and \u2018after\u2019 diagrams.\n\nAs soon as I have those, I\u2019ll send it all over to you.\n\nSpeak soon.\n\nDarren\n\nDarren Wells\nSenior Strategic Account Manager\n+44 7852 926026\n\naptum.com\u00a0|\n\nLinkedIn\n\nThis email is sent for and on behalf of Aptum Technologies (UK) Limited, a registered company in England and Wales under number 06854675 and with its registered office at Building\n 5000, Langstone Park, Havant, PO9 1SA. This email and any attachments are confidential and intended for the recipient only. If you have received this message in error, please notify the sender immediately, destroy this email and any attachments, and do not\n use, copy, store and/or disclose to any person this email and any attachments.\n\nIf you no longer wish to receive promotional emails from Aptum Technologies our \nprivacy policy outlines how you can request that your details be removed from our mailing systems.",
          "Subject": "Email: Azure Migration - Out-of-Scope Project Work"
        }
      ]
    }
  },
  "emails": []
}

---

## LLM Output — describe-context — 2026-03-02 22:07 ET

## Context Block Summary — 2026-02-10

### What This Is
A Python script and sample output demonstrating OAuth2-authenticated extraction of Salesforce account activity history and email records. The script queries a single account's Tasks/Events (ActivityHistories) and related EmailMessage records from the past 60 days, outputting raw JSON.

### What It Contains
- **OAuth2 authentication flow** using httpx (password grant with client credentials)
- **SOQL query patterns** for fetching account details with nested ActivityHistories subquery
- **Fallback logic** for SOQL WHERE clause compatibility (some Salesforce orgs don't support WHERE in subqueries)
- **Email extraction** via EmailMessage object linked to related Contacts and Cases
- **Date filtering** in Python (ActivityDate >= last 60 days)
- **Attribute stripping** to clean Salesforce metadata from output
- **Sample JSON output** showing 14 activity records (Tasks/Events/Emails) for account "Premia Solutions Limited"

### When to Inject This
Inject when building Salesforce integration features that need to retrieve and display account activity timelines, or when troubleshooting OAuth2 token issues and SOQL query compatibility. Useful for understanding how to handle nested subqueries and pagination (nextRecordsUrl) in Salesforce API responses.