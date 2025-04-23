import requests
from bs4 import BeautifulSoup
import praw
import pandas as pd
import streamlit as st

# إعداد Reddit API
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit scraper by u/Few_Measurement8753",
    username="Few_Measurement8753",
    password="شةقشةق4248"
)

# دالة لجلب معلومات حساب Reddit
def scrape_reddit(username):
    try:
        user = reddit.redditor(username)
        name = user.name
        created = pd.to_datetime(user.created_utc, unit='s').strftime('%Y-%m-%d')
        try:
            bio = user.subreddit.public_description
        except:
            bio = "N/A"
        try:
            post_karma = user.link_karma
            comment_karma = user.comment_karma
            karma = f"{post_karma + comment_karma} (Post: {post_karma}, Comment: {comment_karma})"
        except:
            karma = "N/A"
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

# دالة لجلب معلومات حساب Telegram
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
            "Created At": "N/A",
            "Status": "Active",
            "Link": url
        }
    except Exception as e:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Karma": "N/A",
            "Created At": "N/A",
            "Status": "Failed or Not Found",
            "Link": url
        }

# بناء واجهة Streamlit
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
        st.dataframe(df)
        st.download_button("تحميل النتائج CSV", df.to_csv(index=False).encode('utf-8'), "results.csv", "text/csv")
