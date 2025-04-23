import streamlit as st
import pandas as pd
import praw
import requests
from bs4 import BeautifulSoup

# إعداد الاتصال بـ Reddit API
reddit = praw.Reddit(
    client_id="qfRizUhozPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit user data scraper by /u/Few_Measurement8753"
)

# 🔹 سكربت Reddit
def scrape_reddit(username):
    try:
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
    except Exception as e:
        return {
            "Platform": "Reddit",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": f"Error: {str(e)}",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# 🔹 سكربت Telegram
def scrape_telegram(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {
                "Platform": "Telegram",
                "Account Name": "N/A",
                "Account Bio": "N/A",
                "Status": f"Failed: {response.status_code}",
                "Link": url
            }

        soup = BeautifulSoup(response.content, "html.parser")
        name_tag = soup.find("div", class_="tgme_page_title")
        name = name_tag.text.strip() if name_tag else "N/A"
        bio_tag = soup.find("div", class_="tgme_page_description")
        bio = bio_tag.text.strip() if bio_tag else "N/A"
        status = "Active" if name != "N/A" else "Suspended"

        return {
            "Platform": "Telegram",
            "Account Name": name,
            "Account Bio": bio,
            "Status": status,
            "Link": url
        }

    except Exception as e:
        return {
            "Platform": "Telegram",
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": f"Error: {str(e)}",
            "Link": url
        }

# 🔸 واجهة Streamlit
st.title("🔍 Social Account Scraper")
platform = st.selectbox("اختر المنصة:", ["Reddit", "Telegram"])
link_input = st.text_area("أدخل رابط الحساب (أو اسم المستخدم):")

if st.button("ابدأ"):
    st.write(f"جاري استخراج البيانات من {platform}...")

    if platform == "Reddit":
        username = link_input.split("/")[-2] if "/user/" in link_input else link_input
        result = scrape_reddit(username)
    elif platform == "Telegram":
        result = scrape_telegram(link_input)
    else:
        result = {}

    df = pd.DataFrame([result])
    st.subheader("📊 النتائج:")
    st.dataframe(df)

    st.download_button("⬇️ تحميل النتائج CSV", data=df.to_csv(index=False), file_name="results.csv", mime="text/csv")
