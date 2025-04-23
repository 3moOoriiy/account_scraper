import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import praw

# ---------------------- دالة Telegram ----------------------
def scrape_telegram(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        name = soup.find("meta", property="og:title")
        bio = soup.find("meta", property="og:description")

        return {
            "Platform": "Telegram",
            "Account Name": name["content"] if name else "N/A",
            "Account Bio": bio["content"] if bio else "N/A",
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
def scrape_reddit(username):
    try:
        reddit = praw.Reddit(
            client_id="qfRizUHozPM5DXtO8a3UoQ",
            client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
            user_agent="Reddit user data scraper by /u/Few_Measurement8753"
        )
        user = reddit.redditor(username)
        bio = user.subreddit.public_description if user.subreddit else "N/A"
        name = user.name
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

# ---------------------- واجهة Streamlit ----------------------
st.set_page_config(page_title="Social Account Scraper", layout="centered")
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
input_text = st.text_area("أدخل رابط الحساب:", placeholder="مثال: https://t.me/username أو https://www.reddit.com/user/username")

if st.button("ابدأ"):
    st.write("🔄 جاري سحب البيانات من", platform, "...")
    if platform == "Telegram":
        result = scrape_telegram(input_text)
    elif platform == "Reddit":
        username = input_text.strip().split("/")[-1]
        result = scrape_reddit(username)

    df = pd.DataFrame([result])
    st.subheader("📊 النتائج:")
    st.table(df)

    st.download_button(
        label="📥 تحميل النتائج CSV",
        data=df.to_csv(index=False),
        file_name="scraped_results.csv",
        mime="text/csv"
    )
