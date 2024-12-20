from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-fe07afd3b5f04e61b1d0f8fc884d9fe7"  # 请替换为你的真实 API key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"


class DeepSeekChatView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # 从前端请求中获取用户发送的消息和历史记录
            user_message = request.data.get("message")
            chat_history = request.data.get("history", [])
            
            if not user_message:
                return Response({"error": "Message content is required"}, status=status.HTTP_400_BAD_REQUEST)

            # 构建消息历史
            messages = [{"role": "system", "content": "You are a helpful assistant"}]
            
            # 添加历史消息
            for msg in chat_history:
                role = "assistant" if msg["sender"] == "bot" else "user"
                messages.append({"role": role, "content": msg["text"]})
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": user_message})

            # 初始化 DeepSeek API 客户端
            client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

            # 调用 DeepSeek API
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
                stream=False,
            )

            # 提取 DeepSeek 的回复内容
            assistant_reply = response.choices[0].message.content

            # 返回 JSON 格式的响应
            return Response({"reply": assistant_reply}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)