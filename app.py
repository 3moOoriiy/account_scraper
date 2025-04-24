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
    password="4248قةشةق",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# إعداد Instagram (باستخدام ملف الجلسة)
SESSION_FILE = "session-frfrre45"
loader = instaloader.Instaloader()

# دالة سحب بيانات من Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        try:
            bio = user.subreddit.public_description
        except:
            bio = "N/A"
        karma = user.link_karma + user.comment_karma
        created = str(user.created_utc)
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Karma": karma,
            "Created At": created,
            "Status": "Active",
            "Link": f"https://www.reddit.com/user/{username}/"
        }
    except:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created At": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# دالة سحب بيانات من Instagram
def scrape_instagram(username):
    try:
        loader.load_session_from_file("frfrre45", SESSION_FILE)
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
    except:
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

# دالة سحب بيانات من TikTok
def scrape_tiktok(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {
                "Platform": "TikTok",
                "Account Name": username,
                "Account Bio": "N/A",
                "Followers": "جارٍ التحديث",
                "Following": "جارٍ التحديث",
                "Posts": "جارٍ التحديث",
                "Created": "N/A",
                "Status": "Active",
                "Link": url
            }
        else:
            raise Exception("Not found")
    except:
        return {
            "Platform": "TikTok",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# واجهة Streamlit
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Instagram", "Reddit", "TikTok"])
input_text = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    st.info(f"جاري سحب البيانات من {platform}...")
    results = []
    links = [line.strip() for line in input_text.split("\n") if line.strip()]

    for link in links:
        if platform == "Reddit":
            username = link.rstrip("/").split("/")[-1]
            results.append(scrape_reddit(username))
        elif platform == "Instagram":
            username = link.rstrip("/").split("/")[-1]
            results.append(scrape_instagram(username))
        elif platform == "TikTok":
            username = link.rstrip("/").split("@")[1] if "@" in link else link.rstrip("/").split("/")[-1]
            results.append(scrape_tiktok(username))

    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 النتائج:")
        st.dataframe(df)
        st.download_button("📥 تحميل النتائج CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
