import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw

# إعداد Reddit API
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    username="Few_Measurement8753",
    password="شةقشةق4248",  # تأكد إنك تحافظ على الخصوصية
    user_agent="Reddit scraper by u/Few_Measurement8753"
)

# دالة سحب بيانات Reddit
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
    except Exception as e:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# دالة سحب بيانات Telegram
def scrape_telegram(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            raise Exception("Page not reachable")

        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find("title").text.strip()
        bio_tag = soup.find("meta", attrs={"name": "description"})
        bio = bio_tag["content"].strip() if bio_tag else "N/A"

        return {
            "Platform": "Telegram",
            "Account Name": title,
            "Account Bio": bio,
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

# واجهة Streamlit
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
links_input = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")
submit = st.button("ابدأ")

if submit and links_input:
    links = [l.strip() for l in links_input.splitlines() if l.strip()]
    results = []

    for link in links:
        if platform == "Telegram":
            results.append(scrape_telegram(link))
        elif platform == "Reddit":
            username = link.strip('/').split('/')[-1]
            results.append(scrape_reddit(username))

    df = pd.DataFrame(results)
    st.markdown("### 📊 النتائج:")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل النتائج CSV", data=csv, file_name="results.csv", mime="text/csv")
