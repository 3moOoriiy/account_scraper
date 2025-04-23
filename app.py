import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw

# إعداد API لـ Reddit
reddit = praw.Reddit(
    client_id="qfRizUHOzPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit user data scraper by /u/Few_Measurement8753"
)

# ==============================
# دالة Telegram
# ==============================
def scrape_telegram(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        name = soup.find("meta", property="og:title")["content"] if soup.find("meta", property="og:title") else "N/A"
        bio = soup.find("meta", property="og:description")["content"] if soup.find("meta", property="og:description") else "N/A"
        return {
            "Platform": "Telegram",
            "Account Name": name,
            "Account Bio": bio,
            "Status": "Active",
            "Link": link
        }
    except:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Failed or Not Found",
            "Link": link
        }

# ==============================
# دالة Reddit
# ==============================
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

# ==============================
# Streamlit UI
# ==============================
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
links_input = st.text_area("📥 أدخل روابط الحسابات (كل رابط في سطر)")

if st.button("ابدأ"):
    st.write(f"جاري سحب البيانات من {platform}...")
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
