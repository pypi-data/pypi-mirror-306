import requests
from typing import Optional


class EconometricAI:
    def __init__(self, api_token: str):
        """Инициализация AI интерпретатора

        Args:
            api_token: токен для доступа к API
        """
        self.API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.API_TOKEN = api_token

    def interpret_results(self, stats_data: str) -> str:
        """Интерпретация результатов с помощью AI

        Args:
            stats_data: строка с статистическими данными

        Returns:
            str: интерпретация результатов
        """
        headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Content-Type": "application/json"
        }

        messages = [
            {"role": "system", "content": '''
            Вы - эксперт-эконометрист, анализирующий результаты регрессии...
            [ваш system prompt]
            '''},
            {"role": "user", "content": stats_data}
        ]

        data = {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": messages
        }

        try:
            response = requests.post(self.API_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"