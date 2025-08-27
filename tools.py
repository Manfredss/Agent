import json, os, requests
from datetime import datetime
from typing import Dict, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool

WEATHER_API_HOST = 'YOUR-API-HOST'
WEATHER_API_KEY = 'YOUR-API-KEY'
DATE = datetime.now().strftime("%Y-%m-%d")

def weather_tool(city_name: str) -> Dict | None:
    """
    使用JSON格式请求查询中国城市天气的函数
    
    参数:
    city_name (str): 城市名称，如"北京"、"上海"
    api_host (str): 和风天气API主机地址（需注册获取）
    api_key (str): 和风天气API密钥（需注册获取）
    
    返回:
    dict: 包含天气信息的字典，如果查询失败则返回None
    """
    # 获取城市位置信息
    location_url = f"https://{WEATHER_API_HOST}/geo/v2/city/lookup?location={city_name}&key={WEATHER_API_KEY}"
    
    # 准备请求参数（使用JSON格式）
    
    try:
        # 发送请求
        location_response = requests.get(location_url)
        location_data = location_response.json()
        if location_data['code'] != '200':
            print(f"错误: {location_data['message']}")
            return None
        # 获得城市ID
        city_id = location_data['location'][0]['id']
        
        # 根据城市ID获取当地未来一周（包含今天）的天气预报
        weather_url = f"https://{WEATHER_API_HOST}/v7/weather/7d?location={city_id}&key={WEATHER_API_KEY}"
        # 发送请求
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        if weather_data['code'] != '200':
            print(f"错误: {weather_data['message']}")
            return None
        
        # 提取并返回所需天气信息
        # weather_info = {
        #     'city': city_name,
        #     'temp': weather_data['now']['temp'],  # 温度
        #     'feels_like': weather_data['now']['feelsLike'],  # 体感温度
        #     'weather': weather_data['now']['text'],  # 天气状况
        #     'wind_dir': weather_data['now']['windDir'],  # 风向
        #     'wind_scale': weather_data['now']['windScale'],  # 风力等级
        #     'humidity': weather_data['now']['humidity'],  # 湿度
        #     'update_time': weather_data['updateTime']  # 更新时间
        # }
        
        return weather_data
        
    except requests.exceptions.RequestException as e:
        print(f"网络请求错误: {e}")
        return None
    except KeyError as e:
        print(f"数据解析错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        return None

# 异步调用版
async def weather_tool_async(self, city: str) -> str:
    raise NotImplementedError("This tool does not support async")
