import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw

# إعداد ريديت
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    username="Few_Measurement8753",
    password="شةقشةق4248",
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# دالة سحب بيانات Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        try:
            bio = user.subreddit.public_description if user.subreddit else "N/A"
        except:
            bio = "N/A"
        try:
            karma = user.link_karma + user.comment_karma
        except:
            karma = "N/A"
        try:
            created = pd.to_datetime(user.created_utc, unit='s').strftime('%Y-%m-%d')
        except:
            created = "N/A"
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
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        name = soup.find("meta", property="og:title")
        bio = soup.find("meta", property="og:description")
        return {
            "Platform": "Telegram",
            "Account Name": name["content"] if name else "N/A",
            "Account Bio": bio["content"] if bio else "N/A",
            "Karma": "N/A",
            "Created At": "N/A",
            "Status": "Active",
            "Link": url
        }
    except:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created At": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# واجهة Streamlit
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
input_text = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    st.info(f"جاري سحب البيانات من {platform}...")
    results = []
    links = [line.strip() for line in input_text.split("\n") if line.strip()]
    
    for link in links:
        if platform == "Reddit":
            username = link.split("/")[-2] if link.endswith("/") else link.split("/")[-1]
            results.append(scrape_reddit(username))
        elif platform == "Telegram":
            results.append(scrape_telegram(link))

    if results:
        df = pd.DataFrame(results)
        st.markdown("### 📊 النتائج:")
        st.dataframe(df, use_container_width=True)
        st.download_button("تحميل النتائج CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
