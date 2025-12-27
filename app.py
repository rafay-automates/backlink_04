# import streamlit as st
# import requests
# from typing import Dict, Any
#
# API_URL = "https://app.backlinkscan.com/api/backlink-checker"
#
# HEADERS = {
#     "accept": "*/*",
#     "accept-language": "en-US,en;q=0.9",
#     "origin": "https://backlinkscan.com",
#     "referer": "https://backlinkscan.com/",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site",
#     "user-agent": (
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#         "AppleWebKit/537.36 (KHTML, like Gecko) "
#         "Chrome/142.0.0.0 Safari/537.36"
#     )
# }
#
#
# def fetch_backlink_data(domain: str) -> Dict[str, Any]:
#     response = requests.get(
#         API_URL,
#         params={"domain": domain},
#         headers=HEADERS,
#         timeout=30
#     )
#     response.raise_for_status()
#     return response.json()
#
# def add_country_percentages(top_countries):
#     total = sum(item["count"] for item in top_countries)
#
#     if total == 0:
#         return top_countries
#
#     result = []
#     for item in top_countries:
#         result.append({
#             "country": item["country"],
#             "count": item["count"],
#             "percentage": round((item["count"] / total) * 100, 2)
#         })
#
#     return result
#
# def extract_general_overview(api_response: Dict[str, Any]) -> Dict[str, Any]:
#     summary = api_response.get("summary", {})
#
#     return {
#         "domain": summary.get("target"),
#         "rank": summary.get("rank"),
#         "backlinks": summary.get("backlinks"),
#         "backlinks_spam_score": summary.get("backlinks_spam_score"),
#         "broken_backlinks": summary.get("broken_backlinks"),
#         "broken_pages": summary.get("broken_pages"),
#         "crawled_pages": summary.get("crawled_pages"),
#         "external_links_count": summary.get("external_links_count"),
#         "top_countries": api_response.get("top_countries", [])
#     }
#
#
# # ===================== UI =====================
#
# st.set_page_config(
#     page_title="Backlink Overview Tool",
#     page_icon="🔗",
#     layout="wide"
# )
#
# st.title("🔗 Backlink Overview Checker")
# st.write("Get a quick backlink health overview for any domain.")
#
# domain = st.text_input(
#     "Enter domain",
#     placeholder="example.com"
# )
#
# if st.button("Check Backlinks", type="primary"):
#     if not domain:
#         st.warning("Please enter a domain.")
#     else:
#         with st.spinner("Fetching backlink data..."):
#             try:
#                 data = fetch_backlink_data(domain)
#                 overview = extract_general_overview(data)
#
#                 st.success("Data fetched successfully!")
#
#                 # ===== METRICS =====
#                 col1, col2, col3, col4 = st.columns(4)
#
#                 col1.metric("Domain Rank", overview["rank"])
#                 col2.metric("Total Backlinks", overview["backlinks"])
#                 col3.metric("Spam Score", overview["backlinks_spam_score"])
#                 col4.metric("Broken Backlinks", overview["broken_backlinks"])
#
#                 col5, col6, col7 = st.columns(3)
#
#                 col5.metric("Broken Pages", overview["broken_pages"])
#                 col6.metric("Crawled Pages", overview["crawled_pages"])
#                 col7.metric("External Links", overview["external_links_count"])
#
#                 # ===== TOP COUNTRIES =====
#                 st.subheader("🌍 Top Referring Countries")
#
#                 if overview["top_countries"]:
#                     countries_with_percent = add_country_percentages(
#                         overview["top_countries"]
#                     )
#
#                     st.table(countries_with_percent)
#
#
#                 else:
#                     st.info("No country data available.")
#
#             except Exception as e:
#                 st.error(f"Failed to fetch data: {e}")

import streamlit as st
import requests
from typing import Dict, Any


# ===================== CONFIG =====================
st.set_page_config(
    page_title="Backlink Overview",
    page_icon="🔗",
    layout="wide"
)

API_URL = "https://app.backlinkscan.com/api/backlink-checker"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://backlinkscan.com",
    "referer": "https://backlinkscan.com/",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0.0.0 Safari/537.36"
    )
}


# ===================== FUNCTIONS =====================
def fetch_backlink_data(domain: str) -> Dict[str, Any]:
    response = requests.get(
        API_URL,
        params={"domain": domain},
        headers=HEADERS,
        timeout=30
    )
    response.raise_for_status()
    return response.json()


def extract_general_overview(api_response: Dict[str, Any]) -> Dict[str, Any]:
    summary = api_response.get("summary", {})

    return {
        "domain": summary.get("target"),
        "rank": summary.get("rank"),
        "backlinks": summary.get("backlinks"),
        "backlinks_spam_score": summary.get("backlinks_spam_score"),
        "broken_backlinks": summary.get("broken_backlinks"),
        "broken_pages": summary.get("broken_pages"),
        "crawled_pages": summary.get("crawled_pages"),
        "external_links_count": summary.get("external_links_count"),
        "top_countries": api_response.get("top_countries", [])
    }


def add_country_percentages(top_countries):
    total = sum(item["count"] for item in top_countries)
    if total == 0:
        return []

    return [
        {
            "Country": item["country"],
            "Percentage (%)": round((item["count"] / total) * 100, 2)
        }
        for item in top_countries
    ]


# ===================== HEADER =====================
st.markdown(
    """
    <h1 style='text-align:center;'>🔗 Backlink Overview Checker</h1>
    <p style='text-align:center;color:gray;'>
    Analyze backlink health, authority & geographic distribution
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ===================== INPUT SECTION =====================
col_left, col_center, col_right = st.columns([1, 2, 1])

with col_center:
    domain = st.text_input(
        "Enter domain",
        placeholder="example.com",
        label_visibility="collapsed"
    )

    run_check = st.button("🚀 Analyze Domain", use_container_width=True)

# ===================== MAIN LOGIC =====================
if run_check:
    if not domain:
        st.warning("Please enter a valid domain.")
    else:
        with st.spinner("Analyzing backlink profile..."):
            try:
                data = fetch_backlink_data(domain)
                overview = extract_general_overview(data)

                st.success(f"Analysis completed for **{overview['domain']}**")

                st.divider()

                # ===================== KPI CARDS =====================
                k1, k2, k3, k4 = st.columns(4)

                k1.metric("Domain Rank", overview["rank"])
                k2.metric("Total Backlinks", f"{overview['backlinks']:,}")
                k3.metric("Spam Score", overview["backlinks_spam_score"])
                k4.metric("Broken Backlinks", f"{overview['broken_backlinks']:,}")

                k5, k6, k7 = st.columns(3)

                k5.metric("Broken Pages", f"{overview['broken_pages']:,}")
                k6.metric("Crawled Pages", f"{overview['crawled_pages']:,}")
                k7.metric("External Links", f"{overview['external_links_count']:,}")

                st.divider()

                # ===================== COUNTRIES SECTION =====================
                st.subheader("🌍 Top Referring Countries")

                countries_data = add_country_percentages(
                    overview["top_countries"]
                )

                if countries_data:
                    st.dataframe(
                        countries_data,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown("#### Distribution")
                    for item in countries_data:
                        st.write(
                            f"**{item['Country']}** — {item['Percentage (%)']}%"
                        )
                        st.progress(item["Percentage (%)"] / 100)

                else:
                    st.info("No country distribution data available.")

            except Exception as e:
                st.error(f"Failed to fetch data: {e}")

# ===================== FOOTER =====================
st.divider()
st.caption(
    "⚠️ Metrics are estimates based on available backlink data and may vary over time."
)
