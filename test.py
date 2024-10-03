import requests

a, b = 30, 5
r = requests.get(f'http://127.0.0.1:8000/add?a={a}&b={b}')
res = r.json()

print(f"{a} + {b} = {res['sum']}")