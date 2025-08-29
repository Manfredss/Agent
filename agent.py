import langchain
from langchain.agents import create_react_agent, AgentExecutor, AgentType
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
)
from langchain_core.prompts import ChatPromptTemplate

import sys
from tools import *
from model import DeepSeek_R1
from typing import Any, Dict, Iterator, List, Optional


# YOUR-API-KEY 均为你选用的模型的密钥。这里用 DeepSeek
llm = DeepSeek_R1().getLLM()
tools = [Tool(func=weather_tool,
              name="weather_tool",
              description='用于查询城市天气。输入是一个城市名称'),
         Tool(func=readFile,
              name="readFile_rool",
              description='用于读取文件。输入是一个文件路径。用json格式\{"filepath": ""\}返回答案'),
         Tool(func=writeFile,
              name="writeFile_tool",
              description='用于写入文件，输入是一个文件路径和内容。用json格式\{"filepath": "", "content": ""\}返回答案'),
         Tool(func=webSearch,
              name="webSearch_tool",
              description='用于搜索网页，输入是一段话')]
PREFIX = '''
You are a helpful assistant. Answer the user's questions in a friendly and informative manner. You are not allowed to use any other language except Chinese and English(UK). You are given a series of tools to assist you in answering the user's questions. The tools are as follows:
{tools}

Before answering the user's question, you need to check if the question is related to the tools. If it is, you need to use the corresponding tool to answer the question(You may repeat this 'Thought/Action/Action Input/Observation' process several times until you have an answer to the input question). If not, you can answer the question directly.

Using the following format:

Question: the question from the user you need to answer
Thought: you should always think about what to do
Action: the action to take to answer the question, using the tools if needed [{tool_names}]
Action Input: the input of the action
Observation: the result of executing the action
Thought: I now know the final answer to the question
Final Answer: the final answer to the question

Note:
- Each time you reply, the content must contain two parts: Thoughts and Actions or Thoughts and Final Answer.
- Stop generate right after generating Action Input. You must wait until the action returns.
- You must output the final answer in the language the same as the input language. You may need to translate the final answer to THE input language.
- You are running on a computer that runs Windows 11 Pro (24H2)
'''

SUFFIX ='''Begin!

Q: {input}
Thought: {agent_scratchpad}
'''
agent = create_react_agent(
                         tools=tools,
                         llm=llm,
                         prompt=ChatPromptTemplate.from_template(PROMPT))
agent = AgentExecutor(agent=agent, 
                      tools=tools,
                      verbose=True)

print('>> Assistant: 你好😊，我是一个智能助手🤖，你可以向我提问任何问题~: ', end='', flush=True)
for line in sys.stdin:
    userPrompt = line.strip()
    response = agent.invoke({"input": userPrompt})
    response_ = response['output']
    if 'bye' in userPrompt or '再见' in userPrompt:        
        print(f'>> Assistant: {response_}\n')
        break
    else:
        print(f'>> Assistant: {response_}\n')
        print('>> Assistant: 还有其他想问的嘛~: ', end='', flush=True)