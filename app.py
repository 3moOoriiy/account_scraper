import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw
import instaloader
import os

# إعداد Reddit
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    username="Few_Measurement8753",
    password="4248قشةق",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# إعداد Instagram
SESSION_FILE = "session-frfrre45"
loader = instaloader.Instaloader()
loader.load_session_from_file("frfrre45", SESSION_FILE)

# دالة سحب بيانات Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        try:
            bio = user.subreddit.public_description
        except:
            bio = "N/A"
        created = str(user.created_utc)
        karma = user.link_karma + user.comment_karma
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Karma": karma,
            "Created At": created,
            "Status": "Active",
            "Link": f"https://www.reddit.com/user/{username}/"
        }
    except Exception as e:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created At": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# دالة سحب بيانات Instagram
def scrape_instagram(username):
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        return {
            "Platform": "Instagram",
            "Account Name": profile.username,
            "Account Bio": profile.biography,
            "Followers": profile.followers,
            "Following": profile.followees,
            "Posts": profile.mediacount,
            "Created": profile.date_joined.strftime('%Y-%m-%d') if profile.date_joined else "N/A",
            "Status": "Active",
            "Link": f"https://www.instagram.com/{username}/"
        }
    except Exception as e:
        return {
            "Platform": "Instagram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.instagram.com/{username}/"
        }

# دالة سحب بيانات TikTok
def scrape_tiktok(username):
    try:
        url = f"https://www.tiktok.com/@{username}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        name_tag = soup.find("h1")
        bio_tag = soup.find("h2")
        return {
            "Platform": "TikTok",
            "Account Name": name_tag.text.strip() if name_tag else "N/A",
            "Account Bio": bio_tag.text.strip() if bio_tag else "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Active" if name_tag else "Failed or Not Found",
            "Link": url
        }
    except Exception as e:
        return {
            "Platform": "TikTok",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.tiktok.com/@{username}"
        }

# دالة سحب بيانات Telegram
def scrape_telegram(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        name = soup.find("meta", property="og:title")
        bio = soup.find("meta", property="og:description")
        return {
            "Platform": "Telegram",
            "Account Name": name["content"] if name else "N/A",
            "Account Bio": bio["content"] if bio else "N/A",
            "Status": "Active",
            "Link": url
        }
    except Exception as e:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# واجهة Streamlit
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Instagram", "Reddit", "Telegram", "TikTok"])
input_text = st.text_area("أدخل روابط الحسابات (كل رابط في سطر منفصل):")

if st.button("ابدأ"):
    st.info(f"جاري سحب البيانات من {platform}...")
    results = []
    links = [line.strip() for line in input_text.split("\n") if line.strip()]

    for link in links:
        if platform == "Reddit":
            username = link.split("/")[-2] if link.endswith("/") else link.split("/")[-1]
            results.append(scrape_reddit(username))
        elif platform == "Instagram":
            username = link.split("/")[-2] if link.endswith("/") else link.split("/")[-1]
            results.append(scrape_instagram(username))
        elif platform == "TikTok":
            username = link.split("@")[-1].strip("/")
            results.append(scrape_tiktok(username))
        elif platform == "Telegram":
            results.append(scrape_telegram(link))

    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 النتائج:")
        st.dataframe(df)
        st.download_button("تحميل النتائج CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
