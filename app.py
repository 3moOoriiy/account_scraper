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
    password="شةقشةق4248",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# إعداد Instagram (باستخدام ملف الجلسة)
loader = instaloader.Instaloader()
SESSION_FILE = "session-frfrre45"
if os.path.exists(SESSION_FILE):
    try:
        loader.load_session_from_file("frfrre45", SESSION_FILE)
    except Exception as e:
        st.error(f"خطأ في تحميل جلسة Instagram: {e}")
else:
    st.warning("⚠️ ملف الجلسة غير موجود. لن تعمل خاصية Instagram.")

# دالة استخراج بيانات Instagram
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
            "Created": profile.date_joined.strftime("%Y-%m-%d") if profile.date_joined else "N/A",
            "Status": "Active"
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
            "Status": "Failed or Not Found"
        }

# دالة Telegram
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
    except Exception:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# دالة Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        bio = user.subreddit.public_description if user.subreddit else "N/A"
        karma = user.link_karma + user.comment_karma
        cake_day = user.created_utc
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Karma": karma,
            "Created At": pd.to_datetime(cake_day, unit="s").strftime("%Y-%m-%d"),
            "Status": "Active",
            "Link": f"https://www.reddit.com/user/{username}/"
        }
    except Exception:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created At": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# واجهة Streamlit
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Instagram", "Telegram", "Reddit"])
input_text = st.text_area("أدخل روابط أو أسماء الحسابات (كل سطر يمثل حساب):")

if st.button("ابدأ"):
    st.info(f"جاري سحب البيانات من {platform}...")
    results = []
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    
    for item in lines:
        if platform == "Instagram":
            username = item.split("/")[-2] if item.endswith("/") else item.split("/")[-1]
            results.append(scrape_instagram(username))
        elif platform == "Telegram":
            results.append(scrape_telegram(item))
        elif platform == "Reddit":
            username = item.split("/")[-2] if item.endswith("/") else item.split("/")[-1]
            results.append(scrape_reddit(username))
    
    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 النتائج:")
        st.dataframe(df)
        st.download_button("تحميل النتائج CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
