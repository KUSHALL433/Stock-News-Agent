import streamlit as st
import asyncio
from app import app

st.set_page_config(
    page_title="Stock News Summary | Moneycontrol",
    page_icon='📈'
)

st.header("AI Stock News Summary", anchor=False)

async def run_summary():
    placeholder = st.empty()
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

    # async generator
    events = app.astream_events(input=initial_state, version="v2")

    async for event in events:
        if event["event"] == "on_chat_model_stream":
            chunk = event["data"]["chunk"].content
            streamed_text += chunk
            placeholder.markdown(streamed_text)


if st.button("Run Summary"):
    asyncio.run(run_summary())

