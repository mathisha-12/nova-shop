import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, g

app = Flask(__name__)
app.secret_key = "change-me-in-production"
DB = "shop.db"

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_):
    conn = g.pop("db", None)
    if conn: conn.close()

def get_cart():
    return session.setdefault("cart", {})

def cart_items():
    cart = get_cart()
    if not cart: return [], 0, 0
    ids = tuple(cart.keys())
    q = f"SELECT * FROM products WHERE id IN ({','.join('?'*len(ids))})"
    rows = db().execute(q, ids).fetchall()
    items, subtotal = [], 0
    for r in rows:
        qty = cart[str(r["id"])]
        line = r["price"] * qty
        subtotal += line
        items.append({"product": dict(r), "qty": qty, "line": line})
    count = sum(cart.values())
    return items, subtotal, count

@app.context_processor
def inject_globals():
    return {"cart_count": sum(get_cart().values())}

@app.route("/")
def index():
    products = db().execute("SELECT * FROM products LIMIT 4").fetchall()
    return render_template("index.html", products=products)

@app.route("/shop")
def shop():
    q = request.args.get("q", "").strip()
    cat = request.args.get("category", "All")
    sql = "SELECT * FROM products WHERE 1=1"; args = []
    if q:
        sql += " AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ?)"
        args += [f"%{q.lower()}%", f"%{q.lower()}%"]
    if cat and cat != "All":
        sql += " AND category = ?"; args.append(cat)
    products = db().execute(sql, args).fetchall()
    cats = [r["category"] for r in db().execute("SELECT DISTINCT category FROM products").fetchall()]
    return render_template("shop.html", products=products, categories=["All"]+cats, q=q, cat=cat)

@app.route("/product/<int:pid>")
def product(pid):
    p = db().execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if not p: return "Not found", 404
    related = db().execute("SELECT * FROM products WHERE category=? AND id<>? LIMIT 4",
                           (p["category"], pid)).fetchall()
    return render_template("product.html", p=p, related=related)

@app.route("/cart")
def cart():
    items, subtotal, _ = cart_items()
    shipping = 0 if subtotal == 0 or subtotal > 100 else 9
    return render_template("cart.html", items=items, subtotal=subtotal,
                           shipping=shipping, total=subtotal+shipping)

@app.route("/cart/add", methods=["POST"])
def cart_add():
    pid = str(request.form.get("pid"))
    qty = int(request.form.get("qty", 1))
    cart = get_cart()
    cart[pid] = cart.get(pid, 0) + qty
    session.modified = True
    if request.headers.get("X-Requested-With") == "fetch":
        return jsonify({"ok": True, "count": sum(cart.values())})
    flash("Added to cart")
    return redirect(request.referrer or url_for("shop"))

@app.route("/cart/update", methods=["POST"])
def cart_update():
    pid = str(request.form["pid"]); qty = int(request.form["qty"])
    cart = get_cart()
    if qty <= 0: cart.pop(pid, None)
    else: cart[pid] = qty
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    get_cart().pop(str(request.form["pid"]), None)
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    session["cart"] = {}; return redirect(url_for("cart"))

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        flash("Message sent — we'll be in touch!")
        return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    msg = (request.json.get("message") or "").lower()
    if "ship" in msg: r = "We ship worldwide in 2–5 business days. Free over $100."
    elif "return" in msg: r = "Free 30-day returns on all orders."
    elif "price" in msg or "cost" in msg: r = "All prices are in USD and include taxes."
    elif "contact" in msg: r = "Reach us via the Contact page anytime."
    elif "hi" in msg or "hello" in msg: r = "Hey! Looking for anything in particular?"
    else: r = "Great question! Browse the Shop page or visit Contact for help."
    return jsonify({"reply": r})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
