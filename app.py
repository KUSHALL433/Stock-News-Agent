from langgraph.graph import START,END,StateGraph
from dotenv import load_dotenv
from typing import TypedDict,List,Dict
from langchain_core.messages import HumanMessage
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
import os
load_dotenv()

class AgentState(TypedDict):
    business_articles:List[Dict]
    economy_articles:List[Dict]
    company_articles:List[Dict]
    ipo_articles:List[Dict]
    startup_articles:List[Dict]
    stocks_articles:List[Dict]

    ai_summary:str

def business_scraper(state:AgentState):
    from moneycontrol import get_article_links,scrape_article
    business_url="https://www.moneycontrol.com/news/business/"
    links=get_article_links(business_url)
    articles=[scrape_article(link,"business") for link in links]
    state["business_articles"]=[a for a in articles if a]
    return {"business_articles": state["business_articles"]}
def economy_scraper(state:AgentState):
    from moneycontrol import get_article_links,scrape_article
    business_url="https://www.moneycontrol.com/news/business/economy/"
    links=get_article_links(business_url)
    articles=[scrape_article(link,"economy") for link in links]
    state["economy_articles"]=[a for a in articles if a]
    return {"economy_articles":state['economy_articles']}
def companies_scraper(state:AgentState):
    from moneycontrol import get_article_links,scrape_article
    business_url="https://www.moneycontrol.com/news/business/companies/"
    links=get_article_links(business_url)
    articles=[scrape_article(link,"companies") for link in links]
    state["company_articles"]=[a for a in articles if a]
    return {"company_articles":state["company_articles"]}
def ipo_scraper(state:AgentState):
    from moneycontrol import get_article_links,scrape_article
    business_url="https://www.moneycontrol.com/news/business/ipo/"
    links=get_article_links(business_url)
    articles=[scrape_article(link,"ipo") for link in links]
    state["ipo_articles"]=[a for a in articles if a]
    return {"ipo_articles":state['ipo_articles']}
def startup_scraper(state:AgentState):
    from moneycontrol import get_article_links,scrape_article
    business_url="https://www.moneycontrol.com/news/business/startup/"
    links=get_article_links(business_url)
    articles=[scrape_article(link,"startup") for link in links]
    state["startup_articles"]=[a for a in articles if a]
    return {"startup_articles":state['startup_articles']}
def stock_scraper(state:AgentState):
    from moneycontrol import get_article_links,scrape_article
    business_url="https://www.moneycontrol.com/news/business/stocks/"
    links=get_article_links(business_url)
    articles=[scrape_article(link,"stocks") for link in links]
    state["stocks_articles"]=[a for a in articles if a]
    return {"stocks_articles":state['stocks_articles']}


HUGGING_FACE_API_KEY=os.getenv("HUGGINGFACE_API_KEY")

model=HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.1-8B-Instruct",huggingfacehub_api_token=HUGGING_FACE_API_KEY,task='text-generation')
llm=ChatHuggingFace(llm=model)

def ai_summary(state:AgentState):
    combined_text = ""

    for section in ["business_articles", "economy_articles", "ipo_articles", 
                "company_articles", "startup_articles", "stocks_articles"]:
        for article in state.get(section, []):
            combined_text += f"\n\n[{article['section'].upper()}] {article['title']}\n{article['content'][:800]}"

    prompt = f"""
    You are a financial AI assistant.
    Analyze the following recent Indian news articles and identify:
    1. Stocks or sectors likely to rise or fall.
    2. Summarize different companies news.
    3. IPOs to watch
    4. Reasons for the suggested stock moves.


    Articles:
    {combined_text[:10000]}
    """

    result = llm.invoke([HumanMessage(content=prompt)])
    state["ai_summary"] = result.content
    return state
graph = StateGraph(AgentState)

graph.add_node("business_scraper",business_scraper)
graph.add_node("economy_scraper",economy_scraper)
graph.add_node("stock_scraper",stock_scraper)
graph.add_node("ipo_scraper",ipo_scraper)
graph.add_node("companies_scraper",companies_scraper)
graph.add_node("startup_scraper",startup_scraper)
graph.add_node("ai_summary",ai_summary)


graph.add_edge(START,"business_scraper")
graph.add_edge(START,"economy_scraper")
graph.add_edge(START,"stock_scraper")
graph.add_edge(START,"ipo_scraper")
graph.add_edge(START,"companies_scraper")
graph.add_edge(START,"startup_scraper")

graph.add_edge("business_scraper","ai_summary")
graph.add_edge("economy_scraper","ai_summary")
graph.add_edge("stock_scraper","ai_summary")
graph.add_edge("ipo_scraper","ai_summary")
graph.add_edge("companies_scraper","ai_summary")
graph.add_edge("startup_scraper","ai_summary")


graph.add_edge("ai_summary",END)

app=graph.compile()


output=app.invoke({'business_articles':[],
    'economy_articles':[],
    'company_articles':[],
    'ipo_articles':[],
    'startup_articles':[],
    'stocks_articles':[],
    'ai_summary':''})


print(output['ai_summary'])
