import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3
import asyncio
import threading
import logging
from aiogram import Bot
from bot.config import *
from bot.db import *
from bot.keyboards import *
from bot.main import bot as tg_bot, dp

# ------------------ Tkinter GUI ------------------
class AdminGUI:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root
        root.title("Админка - Заявки Telegram")
        root.geometry("800x500")
        root.resizable(False, False)

        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая часть - список заявок
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(left_frame, text="Список заявок:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.requests_listbox = tk.Listbox(left_frame, width=40, height=25, font=("Arial", 10))
        self.requests_listbox.pack(side=tk.LEFT, fill=tk.Y, padx=(0,5))
        self.requests_listbox.bind("<<ListboxSelect>>", self.load_request)

        scrollbar = tk.Scrollbar(left_frame, command=self.requests_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.requests_listbox.config(yscrollcommand=scrollbar.set)

        # Правая часть - текст заявки и ответ
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(right_frame, text="Текст заявки:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.comment_text = scrolledtext.ScrolledText(right_frame, height=10, font=("Arial", 10), state='disabled', wrap=tk.WORD)
        self.comment_text.pack(fill=tk.BOTH, pady=(0,10))

        tk.Label(right_frame, text="Ответ пользователю:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.answer_text = scrolledtext.ScrolledText(right_frame, height=8, font=("Arial", 10), wrap=tk.WORD)
        self.answer_text.pack(fill=tk.BOTH, pady=(0,10))

        self.send_button = tk.Button(
            right_frame, text="Отправить ответ",
            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
            command=self.send_answer
        )
        self.send_button.pack(fill=tk.X)

        self.load_requests()
        self.auto_update_requests()  # авто-обновление списка заявок

    # ------------------ Загрузка заявок ------------------
    def load_requests(self):
        self.requests_listbox.delete(0, tk.END)
        self.requests = get_requests()
        for req in self.requests:
            display_text = f"{req[0]} | @{req[2]}" if req[2] else f"{req[0]}"
            display_text += f" | {req[3][:30]}..."
            self.requests_listbox.insert(tk.END, display_text)

    def load_request(self, event):
        selection = self.requests_listbox.curselection()
        if selection:
            index = selection[0]
            req = self.requests[index]
            self.selected_request = req
            self.comment_text.config(state='normal')
            self.comment_text.delete('1.0', tk.END)
            self.comment_text.insert(tk.END, req[3])
            self.comment_text.config(state='disabled')

    # ------------------ Отправка ответа ------------------
    def send_answer(self):
        if not hasattr(self, 'selected_request'):
            messagebox.showwarning("Выберите заявку", "Сначала выберите заявку из списка")
            return
        answer = self.answer_text.get("1.0", tk.END).strip()
        if not answer:
            messagebox.showwarning("Пустой ответ", "Введите текст ответа")
            return

        request_id, user_id = self.selected_request[0], self.selected_request[1]

        # Отправка сообщения через loop бота
        asyncio.run_coroutine_threadsafe(self.send_message(user_id, answer), bot_loop)

        answer_request(request_id, answer)
        messagebox.showinfo("Успех", "Ответ отправлен и заявка помечена как отвечённая")
        self.answer_text.delete("1.0", tk.END)
        self.load_requests()

    async def send_message(self, user_id, text):
        try:
            await self.bot.send_message(user_id, f"Ответ от Администрации:\n{text}")
        except Exception as e:
            messagebox.showerror("Ошибка отправки", f"Не удалось отправить сообщение: {e}")

    # ------------------ Авто-обновление ------------------
    def auto_update_requests(self):
        self.load_requests()
        self.root.after(3000, self.auto_update_requests)  # каждые 3 секунды

# ------------------ Запуск бота в отдельном потоке ------------------
def start_bot():
    global bot_loop
    bot_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(bot_loop)
    init_db()
    bot_loop.run_until_complete(dp.start_polling(tg_bot))

if __name__ == "__main__":
    # Запуск бота
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()

    # Запуск Tkinter 
    root = tk.Tk()
    app = AdminGUI(root, tg_bot)
    root.mainloop()
