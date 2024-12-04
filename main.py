from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_react_agent,
    create_openai_functions_agent,
    create_tool_calling_agent
)
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
import requests
import json
import os
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools.tavily_search.tool import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
import uuid


api_base = "https://api.staging.langdb.ai"  # LangDB API base URL
pre_defined_run_id =  uuid.uuid4()
default_headers = {"x-project-id": "xxxx", ## Enter LangDB Project ID
                  "x-run-id": pre_defined_run_id} 
os.environ['OPENAI_API_KEY'] = 'xxxxx' ## Enter LangDB API Key
os.environ['TAVILY_API_KEY'] = 'xxxxx' ## Enter Tavily API Key



def get_function_tools():
  search = TavilySearchAPIWrapper()
  tavily_tool = TavilySearchResults(api_wrapper=search)

  tools = [
      tavily_tool
  ]

  tools.extend(load_tools(['wikipedia']))

  return tools



def init_action():
  llm = ChatOpenAI(model_name='gpt-4o-mini' , temperature=0.3, openai_api_base=api_base, default_headers=default_headers )
  prompt = hub.pull("hwchase17/openai-functions-agent")
  tools = get_function_tools()
  agent = create_tool_calling_agent(llm, tools, prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
  pre_defined_run_id = uuid.uuid4()
  config = {"run_id": pre_defined_run_id}
  response = agent_executor.invoke({"input": "Who is the owner of Tesla company? Let me know details about owner."}, config=config, include_run_info=True)



init_action()
