import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw
import instaloader

# إعداد الاتصال بـ Reddit
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    username="Few_Measurement8753",
    password="شةقشةق4248",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# دالة سحب بيانات من Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        karma = user.link_karma + user.comment_karma
        created_at = pd.to_datetime(user.created_utc, unit='s').date()
        try:
            bio = user.subreddit.public_description
        except:
            bio = "N/A"
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Karma": karma,
            "Created": created_at,
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

# دالة سحب بيانات من Telegram
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

# دالة سحب بيانات من Instagram
def scrape_instagram(username):
    try:
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, username)
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

# واجهة Streamlit
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit", "Instagram"])
input_text = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    st.info(f"جاري سحب البيانات من {platform}...")
    results = []
    links = [line.strip() for line in input_text.split("\n") if line.strip()]

    for link in links:
        if platform == "Reddit":
            username = link.rstrip("/").split("/")[-1]
            results.append(scrape_reddit(username))
        elif platform == "Telegram":
            results.append(scrape_telegram(link))
        elif platform == "Instagram":
            username = link.rstrip("/").split("/")[-1]
            results.append(scrape_instagram(username))

    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 النتائج:")
        st.dataframe(df)
        st.download_button("📁 تحميل النتائج CSV", df.to_csv(index=False).encode("utf-8"), "results.csv", "text/csv")
