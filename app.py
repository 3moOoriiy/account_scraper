import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw
import datetime
from instagramy import InstagramUser

# إعداد Reddit API
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit scraper by u/Few_Measurement8753",
    username="Few_Measurement8753",
    password="شةقشةق4248"
)

# دالة Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        bio = getattr(user.subreddit, "public_description", "N/A") if hasattr(user, "subreddit") else "N/A"
        karma = user.link_karma + user.comment_karma
        created = datetime.datetime.fromtimestamp(user.created_utc).strftime("%Y-%m-%d")
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Followers": karma,
            "Following": "N/A",
            "Posts": "N/A",
            "Created": created,
            "Status": "Active",
            "Link": f"https://www.reddit.com/user/{username}/"
        }
    except:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# دالة Telegram
def scrape_telegram(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        name = soup.find("meta", property="og:title")
        bio = soup.find("meta", property="og:description")
        return {
            "Platform": "Telegram",
            "Account Name": name["content"] if name else "N/A",
            "Account Bio": bio["content"] if bio else "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Active",
            "Link": url
        }
    except:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Followers": "N/A",
            "Following": "N/A",
            "Posts": "N/A",
            "Created": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# دالة Instagram
def scrape_instagram(username):
    try:
        user = InstagramUser(username)
        return {
            "Platform": "Instagram",
            "Account Name": user.fullname,
            "Account Bio": user.biography,
            "Followers": user.followers,
            "Following": user.following,
            "Posts": user.number_of_posts,
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

# Streamlit واجهة المستخدم
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit", "Instagram"])
input_text = st.text_area("📥 أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    links = [line.strip() for line in input_text.split("\n") if line.strip()]
    results = []

    for link in links:
        if platform == "Reddit":
            username = link.split("/")[-2] if link.endswith("/") else link.split("/")[-1]
            results.append(scrape_reddit(username))
        elif platform == "Telegram":
            results.append(scrape_telegram(link))
        elif platform == "Instagram":
            username = link.split("/")[-2] if link.endswith("/") else link.split("/")[-1]
            results.append(scrape_instagram(username))

    df = pd.DataFrame(results)
    st.markdown("### 📊 النتائج:")
    st.dataframe(df)
    st.download_button("📥 تحميل النتائج CSV", df.to_csv(index=False), file_name="results.csv", mime="text/csv")
