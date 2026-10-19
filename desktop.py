import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, add_expense, get_expenses, delete_expense, get_total

init_db()


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Трекер личных расходов")
        self.root.geometry("850x600")
        self.root.minsize(700, 500)

        title = ttk.Label(root, text="Трекер личных расходов", font=("Arial", 18, "bold"))
        title.pack(pady=(16, 4))
        self.total_label = ttk.Label(root, text="Всего расходов: 0.00 ₽", font=("Arial", 12))
        self.total_label.pack(pady=(0, 12))

        form = ttk.LabelFrame(root, text="Добавить расход", padding=12)
        form.pack(fill="x", padx=16, pady=8)

        ttk.Label(form, text="Сумма, ₽").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.amount = ttk.Entry(form, width=18)
        self.amount.grid(row=1, column=0, padx=5, pady=4)

        ttk.Label(form, text="Категория").grid(row=0, column=1, sticky="w", padx=5, pady=4)
        self.category = ttk.Combobox(
            form, values=["Продукты", "Транспорт", "Кафе", "Покупки", "Учёба", "Другое"],
            state="readonly", width=18
        )
        self.category.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(form, text="Дата (ГГГГ-ММ-ДД)").grid(row=0, column=2, sticky="w", padx=5, pady=4)
        self.date = ttk.Entry(form, width=18)
        self.date.grid(row=1, column=2, padx=5, pady=4)

        ttk.Label(form, text="Комментарий").grid(row=0, column=3, sticky="w", padx=5, pady=4)
        self.comment = ttk.Entry(form, width=20)
        self.comment.grid(row=1, column=3, padx=5, pady=4)

        ttk.Button(form, text="Добавить", command=self.add).grid(row=1, column=4, padx=8, pady=4)

        columns = ("date", "category", "comment", "amount", "id")
        self.table = ttk.Treeview(root, columns=columns, show="headings", height=14)
        self.table.heading("date", text="Дата")
        self.table.heading("category", text="Категория")
        self.table.heading("comment", text="Комментарий")
        self.table.heading("amount", text="Сумма")
        self.table.heading("id", text="ID")
        self.table.column("date", width=120)
        self.table.column("category", width=150)
        self.table.column("comment", width=300)
        self.table.column("amount", width=120)
        self.table.column("id", width=0, stretch=False)
        self.table.pack(fill="both", expand=True, padx=16, pady=8)

        buttons = ttk.Frame(root)
        buttons.pack(fill="x", padx=16, pady=(0, 14))
        ttk.Button(buttons, text="Удалить выбранный расход", command=self.delete).pack(side="left")
        ttk.Button(buttons, text="Обновить список", command=self.refresh).pack(side="left", padx=8)

        self.refresh()

    def add(self):
        try:
            amount = float(self.amount.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Ошибка", "Введите сумму числом.")
            return
        category = self.category.get().strip()
        date = self.date.get().strip()
        comment = self.comment.get().strip()

        if amount <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть больше нуля.")
            return
        if not category or not date:
            messagebox.showerror("Ошибка", "Выберите категорию и укажите дату.")
            return

        add_expense(amount, category, date, comment)
        self.amount.delete(0, tk.END)
        self.category.set("")
        self.date.delete(0, tk.END)
        self.comment.delete(0, tk.END)
        self.refresh()

    def delete(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("Удаление", "Сначала выберите расход в таблице.")
            return
        expense_id = int(self.table.item(selected[0], "values")[-1])
        if messagebox.askyesno("Подтверждение", "Удалить выбранный расход?"):
            delete_expense(expense_id)
            self.refresh()

    def refresh(self):
        for item in self.table.get_children():
            self.table.delete(item)
        for expense in get_expenses():
            self.table.insert(
                "", tk.END,
                values=(expense["date"], expense["category"], expense["comment"],
                        f'{expense["amount"]:.2f} ₽', expense["id"])
            )
        self.total_label.config(text=f"Всего расходов: {get_total():.2f} ₽")


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
