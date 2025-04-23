import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw

# إعداد الاتصال بـ Reddit API
reddit = praw.Reddit(
    client_id="qfRizUHoZPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit user data scraper by /u/Few_Measurement8753"
)

# ---------------------- دالة Telegram ----------------------
def scrape_telegram(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        name_tag = soup.find("meta", property="og:title")
        bio_tag = soup.find("meta", property="og:description")

        name = name_tag["content"] if name_tag else "N/A"
        bio = bio_tag["content"] if bio_tag else "N/A"

        return {
            "Platform": "Telegram",
            "Account Name": name,
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

# ---------------------- دالة Reddit ----------------------
def scrape_reddit(link):
    try:
        username = link.strip("/").split("/")[-1]
        user = reddit.redditor(username)
        name = user.name
        bio = user.subreddit.public_description if user.subreddit else "N/A"
        return {
            "Platform": "Reddit",
            "Account Name": name,
            "Account Bio": bio,
            "Status": "Active",
            "Link": link
        }
    except:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": link
        }

# ---------------------- واجهة Streamlit ----------------------
st.set_page_config(page_title="Social Account Scraper", layout="centered")
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
links_input = st.text_area("📥 أدخل روابط الحسابات (كل رابط في سطر):")

if st.button("ابدأ"):
    links = [link.strip() for link in links_input.splitlines() if link.strip()]
    results = []
    for link in links:
        if platform == "Telegram":
            results.append(scrape_telegram(link))
        elif platform == "Reddit":
            results.append(scrape_reddit(link))

    df = pd.DataFrame(results)
    st.subheader("📊 النتائج:")
    st.dataframe(df)
    st.download_button("📥 تحميل النتائج CSV", data=df.to_csv(index=False), file_name="account_data.csv", mime="text/csv")
