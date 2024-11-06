import requests
from typing import Optional


class EconometricAI:
    def __init__(self):
        """Инициализация AI интерпретатора

        Args:
            api_token: токен для доступа к API
        """
        self.API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.API_TOKEN = 'g4Qd1qksVb7oq4Jwzz7EKYByx63pmFe8'

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
Вы - опытный эконометрист, которому поручено ответить на вопросы по пунктам в задании связанным с регрессией МНК.  
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
