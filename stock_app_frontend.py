import streamlit as st
from stock_app_final import app

st.set_page_config(
    page_title="Stock News Summary | AI Agent",
    page_icon="📈",
    layout="centered"
)

st.markdown("""
<div style='text-align:center; margin-top: 10px;'>
    <h1 style='font-size: 40px;'>📈 AI Stock News Summary</h1>
    <p style='font-size:18px; color:gray;'>
        Get real-time summaries of the latest Stock & Business News.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

start_summary = st.button("🚀 Get Summary", use_container_width=True)



if start_summary:
    loader_container = st.container()

    with loader_container:

        loader_text = st.markdown(
            "<p style='text-align:center; color:#ccc; font-size:18px;'>⏳ Starting...</p>",
            unsafe_allow_html=True
        )

    summary_box = st.container()
    summary_placeholder = summary_box.empty()
    streamed_text = ""

    initial_state = {
        "business_articles": [],
        "economy_articles": [],
        "company_articles": [],
        "ipo_articles": [],
        "startup_articles": [],
        "stocks_articles": [],
        "ai_summary": ""
    }

    for mode, data in app.stream(
        initial_state,
        stream_mode=["messages", "custom"],
    ):

        if mode == "custom":
            loader_text.markdown(
            f"<p style='text-align:center; color:#ccc; font-size:18px;'>🔄 {data['custom_key']}</p>",
            unsafe_allow_html=True
            )

        else:
            loader_container.empty()
            chunk, meta = data
            streamed_text += chunk.content

            summary_placeholder.markdown(
                f"""
                <div style="
                    padding:18px;
                    background:#1e1e1e;
                    border-radius:12px;
                    border:1px solid #333;
                    color:#e6e6e6;
                    font-size:17px;
                    line-height:1.6;
                    white-space:pre-wrap;
                ">
                    {streamed_text}
                </div>
                """,
                unsafe_allow_html=True,
            )
# ************************** OLD CODE **************************************

# import streamlit as st
# import asyncio
# from app import app

# st.set_page_config(
#     page_title="Stock News Summary | Moneycontrol",
#     page_icon='📈'
# )

# st.header("AI Stock News Summary", anchor=False)

# async def run_summary():
#     placeholder = st.empty()
#     streamed_text = ""

#     initial_state = {
#         "business_articles": [],
#         "economy_articles": [],
#         "company_articles": [],
#         "ipo_articles": [],
#         "startup_articles": [],
#         "stocks_articles": [],
#         "ai_summary": ""
#     }

#     # async generator
#     events = app.astream_events(input=initial_state, version="v2")

#     async for event in events:
#         if event["event"] == "on_chat_model_stream":
#             chunk = event["data"]["chunk"].content
#             streamed_text += chunk
#             placeholder.markdown(streamed_text)


# if st.button("Run Summary"):
#     asyncio.run(run_summary())


