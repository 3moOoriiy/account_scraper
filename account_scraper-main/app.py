import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import instaloader
import praw

# إعداد Reddit API
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    username="Few_Measurement8753",
    password="شةقشةق4248",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# دالة استخراج بيانات Reddit
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
            "Created": created,
            "Status": "Active",
            "Link": f"https://www.reddit.com/user/{username}/"
        }
    except:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# دالة استخراج بيانات Telegram
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
            "Karma": "N/A",
            "Created": "N/A",
            "Status": "Active",
            "Link": url
        }
    except:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# دالة استخراج بيانات Instagram
def scrape_instagram(username):
    try:
        L = instaloader.Instaloader()
        L.load_session_from_file("frfrre45")  # اسم المستخدم اللي سجلت منه
        profile = instaloader.Profile.from_username(L.context, username)
        return {
            "Platform": "Instagram",
            "Account Name": profile.username,
            "Account Bio": profile.biography,
            "Followers": profile.followers,
            "Following": profile.followees,
            "Posts": profile.mediacount,
            "Created": "N/A",
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

# واجهة المستخدم
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Reddit", "Telegram", "Instagram"])
input_text = st.text_area("أدخل روابط أو يوزرات الحسابات (كل واحد في سطر):")

if st.button("ابدأ"):
    results = []
    entries = [line.strip() for line in input_text.splitlines() if line.strip()]
    
    with st.spinner(f"جاري سحب البيانات من {platform}..."):
        for entry in entries:
            if platform == "Reddit":
                username = entry.split("/")[-2] if entry.endswith("/") else entry.split("/")[-1]
                results.append(scrape_reddit(username))
            elif platform == "Telegram":
                results.append(scrape_telegram(entry))
            elif platform == "Instagram":
                username = entry.split("/")[-2] if entry.endswith("/") else entry.split("/")[-1]
                results.append(scrape_instagram(username))

    if results:
        df = pd.DataFrame(results)
        st.markdown("### النتائج:")
        st.dataframe(df)
        st.download_button("تحميل النتائج CSV", df.to_csv(index=False).encode("utf-8"), "results.csv", "text/csv")
