from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db, add_expense, get_expenses, delete_expense, get_total

app = Flask(__name__)
init_db()


@app.route("/")
def index():
    expenses = get_expenses()
    total = get_total()
    return render_template("index.html", expenses=expenses, total=total)


@app.route("/add", methods=["POST"])
def add():
    try:
        amount = float(request.form.get("amount", "0").replace(",", "."))
        category = request.form.get("category", "").strip()
        date = request.form.get("date", "").strip()
        comment = request.form.get("comment", "").strip()

        if amount <= 0:
            return render_template(
                "index.html", expenses=get_expenses(), total=get_total(),
                error="Сумма должна быть больше нуля."
            )
        if not category or not date:
            return render_template(
                "index.html", expenses=get_expenses(), total=get_total(),
                error="Заполните категорию и дату."
            )

        add_expense(amount, category, date, comment)
        return redirect(url_for("index"))
    except ValueError:
        return render_template(
            "index.html", expenses=get_expenses(), total=get_total(),
            error="Введите корректную сумму."
        )


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    delete_expense(expense_id)
    return redirect(url_for("index"))


# REST API: получить список расходов
@app.route("/api/expenses", methods=["GET"])
def api_get_expenses():
    return jsonify(get_expenses())


# REST API: добавить расход
@app.route("/api/expenses", methods=["POST"])
def api_add_expense():
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "Сумма должна быть числом."}), 400

    category = str(data.get("category", "")).strip()
    date = str(data.get("date", "")).strip()
    comment = str(data.get("comment", "")).strip()

    if amount <= 0:
        return jsonify({"error": "Сумма должна быть больше нуля."}), 400
    if not category or not date:
        return jsonify({"error": "Укажите category и date."}), 400

    expense_id = add_expense(amount, category, date, comment)
    return jsonify({
        "id": expense_id, "amount": amount, "category": category,
        "date": date, "comment": comment
    }), 201


# REST API: удалить расход
@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
def api_delete_expense(expense_id):
    deleted = delete_expense(expense_id)
    if not deleted:
        return jsonify({"error": "Расход не найден."}), 404
    return jsonify({"message": "Расход удалён."})


@app.route("/api/total", methods=["GET"])
def api_total():
    return jsonify({"total": get_total()})


if __name__ == "__main__":
    app.run(debug=True)
