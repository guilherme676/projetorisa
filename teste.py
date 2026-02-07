import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzcxMDQ0ODU1fQ.LBIf8-_3sHTdW0TYEDP-594_gJkajZV8OGNTnSYTzmY"
}

requisicao = requests.get("http://localhost:8000/auth/refresh", headers=headers)
print(requisicao)
