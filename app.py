import streamlit as st
import pandas as pd
from telegram_scraper import scrape_telegram  # تأكد أن الملف موجود بنفس المجلد
import praw

# إعداد التوصيل لريديت
reddit = praw.Reddit(
    client_id="qfRizUhozPM5DXtO8a3UoQ",
    client_secret="nrklg9cnDPaqu0Vzfa_RdOk2lETt3A",
    user_agent="Reddit user data scraper by /u/Few_Measurement8753"
)

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
            "Status": "Suspended or Not Found",
            "Link": f"https://www.reddit.com/user/{username}/"
        }

# Streamlit UI
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Telegram", "Reddit"])
link_input = st.text_area("أدخل رابط الحساب (لارتباط في سطر):")

if st.button("ابدأ"):
    data = []
    links = [l.strip() for l in link_input.splitlines() if l.strip()]

    for url in links:
        if platform == "Telegram" and "t.me/" in url:
            result = scrape_telegram(url)
            data.append(result)
        elif platform == "Reddit" and "/user/" in url:
            username = url.rstrip("/").split("/")[-1]
            result = scrape_reddit(username)
            data.append(result)

    if data:
        df = pd.DataFrame(data)
        st.subheader(":bar_chart: النتائج:")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("تحميل النتائج CSV", csv, "results.csv", "text/csv")
    else:
        st.warning("لم يتم استرجاع أي نتائج.")
