import streamlit as st
import pandas as pd
import requests
import re
import praw
from bs4 import BeautifulSoup

# إعداد Reddit API
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit user data scraper by /u/Few_Measurement8753"
)

# استخراج بيانات Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        bio = user.subreddit.public_description if user.subreddit else "N/A"
        link = f"https://www.reddit.com/user/{username}/"
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Status": "Active",
            "Link": link
        }
    except Exception:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# استخراج بيانات Telegram
def scrape_telegram(link):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(link, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.title.text.strip() if soup.title else "N/A"
        description = soup.find("meta", {"name": "description"})
        bio = description["content"] if description else "N/A"
        return {
            "Platform": "Telegram",
            "Account Name": name,
            "Account Bio": bio,
            "Status": "Active",
            "Link": link
        }
    except Exception:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": link
        }

# الواجهة
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
user_input = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    st.write(f"جاري سحب البيانات من {platform}...")
    links = [line.strip() for line in user_input.splitlines() if line.strip()]
    results = []

    for link in links:
        if platform == "Reddit":
            match = re.search(r"reddit\.com/user/([^/]+)", link)
            if match:
                username = match.group(1)
                results.append(scrape_reddit(username))
            else:
                results.append({
                    "Platform": "Reddit",
                    "Account Name": "N/A",
                    "Account Bio": "N/A",
                    "Status": "Invalid Link",
                    "Link": link
                })
        elif platform == "Telegram":
            results.append(scrape_telegram(link))

    df = pd.DataFrame(results)
    st.subheader("📊 النتائج:")
    st.dataframe(df)
    st.download_button("📥 تحميل النتائج CSV", df.to_csv(index=False), file_name="results.csv", mime="text/csv")
