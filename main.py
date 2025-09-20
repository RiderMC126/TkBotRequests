import tkinter as tk
from tkinter import messagebox, scrolledtext
import sqlite3
import asyncio
from aiogram import Bot
from .bot.config import *
from .bot.db import *


class AdminGUI:
    def __init__(self, root, bot):
        self.bot = bot
        self.root = root
        root.title("Админка - Заявки Telegram")
        root.geometry("600x400")

        # Список заявок
        self.requests_listbox = tk.Listbox(root, width=80)
        self.requests_listbox.pack(pady=10)
        self.requests_listbox.bind("<<ListboxSelect>>", self.load_request)

        # Поле для текста заявки
        tk.Label(root, text="Текст заявки:").pack()
        self.comment_text = scrolledtext.ScrolledText(root, height=5, width=70, state='disabled')
        self.comment_text.pack()

        # Поле для ответа
        tk.Label(root, text="Ответ пользователю:").pack()
        self.answer_text = scrolledtext.ScrolledText(root, height=5, width=70)
        self.answer_text.pack()

        # Кнопка отправки
        self.send_button = tk.Button(root, text="Отправить ответ", command=self.send_answer)
        self.send_button.pack(pady=10)

        self.load_requests()

    def load_requests(self):
        self.requests_listbox.delete(0, tk.END)
        self.requests = get_requests()
        for req in self.requests:
            display_text = f"{req[0]} | @{req[2]} | {req[3][:30]}..." if req[2] else f"{req[0]} | {req[3][:30]}..."
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

    def send_answer(self):
        if not hasattr(self, 'selected_request'):
            messagebox.showwarning("Выберите заявку", "Сначала выберите заявку из списка")
            return
        answer = self.answer_text.get("1.0", tk.END).strip()
        if not answer:
            messagebox.showwarning("Пустой ответ", "Введите текст ответа")
            return

        request_id, user_id = self.selected_request[0], self.selected_request[1]
        asyncio.run(self.send_message(user_id, answer))
        answer_request(request_id, answer)
        messagebox.showinfo("Успех", "Ответ отправлен и заявка помечена как отвечённая")
        self.answer_text.delete("1.0", tk.END)
        self.load_requests()

    async def send_message(self, user_id, text):
        try:
            await self.bot.send_message(user_id, text)
        except Exception as e:
            messagebox.showerror("Ошибка отправки", f"Не удалось отправить сообщение: {e}")


# ------------------ Запуск ------------------
if __name__ == "__main__":
    bot = Bot(token=TOKEN)
    root = tk.Tk()
    app = AdminGUI(root, bot)
    root.mainloop()
