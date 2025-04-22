import streamlit as st
import pandas as pd

def scrape_account(platform, url):
    if "twitter.com" in url:
        return {
            "Platform": "Twitter",
            "Account Name": "@test_user",
            "Account Bio": "This is a sample Twitter bio.",
            "Status": "Active",
            "Link": url
        }
    elif "t.me" in url:
        return {
            "Platform": "Telegram",
            "Account Name": "@telegram_user",
            "Account Bio": "قناة مهتمة بالتقنية",
            "Status": "Active",
            "Link": url
        }
    else:
        return {
            "Platform": platform,
            "Account Name": "N/A",
            "Account Bio": "N/A",
            "Status": "Suspended",
            "Link": url
        }

st.set_page_config(page_title="Account Scraper", layout="centered")
st.title("🔍 Social Account Scraper")

platform = st.selectbox("اختر المنصة:", ["Twitter", "Telegram", "Reddit", "TikTok"])
urls_input = st.text_area("أدخل روابط الحسابات (كل رابط في سطر):")

if "results" not in st.session_state:
    st.session_state.results = []

if st.button("ابدأ"):
    urls = [u.strip() for u in urls_input.split("\\n") if u.strip()]
    if urls:
        for url in urls:
            result = scrape_account(platform, url)
            st.session_state.results.append(result)
    else:
        st.warning("يرجى إدخال رابط أو أكثر")

if st.session_state.results:
    st.markdown("---")
    st.subheader("📊 النتائج:")
    df = pd.DataFrame(st.session_state.results)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("💾 تحميل النتائج CSV", csv, "accounts.csv", "text/csv")
