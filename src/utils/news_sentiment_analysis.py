import os
from cozepy import COZE_CN_BASE_URL
import json

coze_api_token = '{token}'
coze_api_base = COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType  # noqa

coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# Create a workflow instance in Coze, copy the last number from the web link as the workflow's ID.
workflow_id = '7516058828006539299'

# Call the coze.workflows.runs.create method to create a workflow run. The create method
# is a non-streaming chat and will return a WorkflowRunResult class.


def analysis_news_sentiment(news_url, ticker, ticker_name):
    workflow = coze.workflows.runs.create(
        workflow_id=workflow_id,
        parameters={
            "news_url": news_url,
            "ticker": ticker,
            "ticker_name": ticker_name,
        }
    )
    try:
        response_data = json.loads(workflow.data)
        output_str = response_data.get("output", "")
        # 去除 markdown 代码块标记
        if output_str.startswith("```json\n"):
            output_str = output_str[8:]  # 去除 "```json\n"
        if output_str.endswith("\n```"):
            output_str = output_str[:-4]  # 去除 "\n```"
        # 解析内层 JSON
        data = json.loads(output_str)
        
        # 提取所需字段
        sentiment_analysis = data.get("sentiment_analysis", {})
        analysis_details = data.get("analysis_details", {})
        
        # 返回结果
        result = {
            "sentiment_analysis": sentiment_analysis,
            "analysis_details": analysis_details
        }
        return result
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")
        return None
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
        return None
