import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw
import instaloader

# إعداد Reddit
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    username="Few_Measurement8753",
    password="4248قشةق",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# إعداد Instagram باستخدام session محفوظة
SESSION_FILE = "session-frfrre45"
loader = instaloader.Instaloader()
loader.load_session_from_file("frfrre45", SESSION_FILE)

# دالة سحب بيانات Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        bio = user.subreddit.public_description if user.subreddit else "N/A"
        karma = user.link_karma + user.comment_karma
        created = pd.to_datetime(user.created_utc, unit='s').strftime('%Y-%m-%d')
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
    except:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
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

# واجهة Streamlit
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Instagram", "Reddit", "Telegram"])
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

        elif platform == "Telegram":
            results.append(scrape_telegram(link))

    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 النتائج:")
        st.dataframe(df)
        st.download_button("تحميل النتائج CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
