import os
import sys
import time
import threading
import uvicorn
import webview
from app.main import app

def start_server():
    """Запускает FastAPI сервер в фоне"""
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

if __name__ == '__main__':
    # Запускаем FastAPI сервер в отдельном daemon-потоке
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Даем серверу немного времени на старт
    time.sleep(1)

    # URL фронтенда (на этапе разработки Vite работает на порту 5173)
    # В проде (Этап 3) здесь будет локальный путь к собранному HTML
    frontend_url = "http://localhost:5173"

    # Создаем и запускаем окно WebView
    window = webview.create_window('LocalTest Admin Panel', frontend_url, width=1280, height=800)
    
    # Запускаем цикл обработки событий. Когда окно закроется, скрипт завершится
    webview.start()
