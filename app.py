import email
import imaplib
import os
import re
import webbrowser
from email.header import decode_header

from diplomacy_news.get_backstabbr import get_previous_news_season

# account credentials
username = os.environ["MAIL"]
password = os.environ["MAIL_PASS"]
# use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# or check this page: https://www.systoolsgroup.com/imap/
# for office 365, it's this:
imap_server = os.environ["MAIL_SERVER"]


def trigger_by_email():
    subjects = get_subjects()
    seasons = get_seasons(subjects)
    previous_news_season = get_previous_news_season()
    if previous_news_season != seasons[0]:
        # TODO: do stuff
        pass


def get_seasons(subjects):
    adjudications = [
        str(subject) for subject in subjects if "adjudicated" in str(subject)
    ]
    seasons_matches = [
        re.search(r"((?:fall|spring) \d\d\d\d)", subject) for subject in adjudications
    ]
    seasons = [season.group().title() for season in seasons_matches if season]
    return seasons


def get_subjects():
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    status, messages = imap.select("INBOX")
    result, data = imap.uid("search", None, "ALL")
    subjects = []
    if result == "OK":
        email_uids = data[0].split()[::-1]
        for email_uid in email_uids:
            result, email_data = imap.uid("fetch", email_uid, "(BODY.PEEK[HEADER])")
            raw_email = email_data[0][1].decode("utf-8")
            email_message = email.message_from_string(raw_email)
            subject = decode_header(email_message["Subject"])[0][0]
            subjects += [subject]
    imap.close()
    imap.logout()
    return subjects
