const express = require("express");
const app = express();
app.use(express.json());

const orders = new Map();
let balance = 1000;

app.get("/api/orders/:id", (req, res) => {
  const order = orders.get(req.params.id);
  if (!order) return res.status(404).json({ error: "not found" });
  res.json(order);
});

app.post("/api/orders", (req, res) => {
  const { qty, price } = req.body;
  const cost = qty * price;
  if (balance >= cost) {
    balance = balance - cost;
    const id = String(orders.size + 1);
    orders.set(id, { id, qty, price, owner: req.headers["x-user"] });
    return res.status(201).json({ id });
  }
  res.status(400).json({ error: "insufficient balance" });
});

app.listen(3000);
