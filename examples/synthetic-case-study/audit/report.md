# Audit report

- **target**: examples/synthetic-case-study/audit/fixture
- **in scope**: server.js, index.html
- **out of scope**: app.js (not present), deployment
- **method**: static review, no server started
- **authorization**: fictional fixture written for this example

## Executive summary

Findings: critical 0, high 4, medium 1, low 0, info 0.
Citations verified: 5 of 5 file citations.
Fix first: A11Y-001 Buy control is a div with a click handler; COR-001 Order quantity and price are not validated; SEC-001 Any caller can read any order (no ownership check).

## Coverage

| class | method | covered | checked | result |
|---|---|---|---|---|
| security | read handlers | server.js | yes | 2 findings |
| accessibility | read markup | index.html | yes | 2 findings |
| correctness | read handlers | server.js | yes | 1 finding |
| performance | none |  | no | no build output or runtime in scope |
| dependencies | none |  | no | no lockfile in the fixture |

## Findings

### A11Y-001 Buy control is a div with a click handler (high, accessibility, confidence INFERRED)

- Location: `index.html:5` (citation: verified)
- Evidence:

```
<div class="btn" onclick="placeOrder()">Buy</div>
```

- Reproduction: Tab through the page: the Buy control never receives focus; screen readers do not announce a button.
- Impact: Keyboard and screen-reader users cannot place an order.
- Fix: Use <button type="button">Buy</button>.

### COR-001 Order quantity and price are not validated (high, correctness, confidence INFERRED)

- Location: `server.js:15` (citation: verified)
- Evidence:

```
const { qty, price } = req.body;
  const cost = qty * price;
```

- Reproduction: POST {"qty": -10, "price": 100} increases the balance by 1000.
- Impact: Negative or non-numeric quantities mint balance; strings produce NaN costs that pass the balance check.
- Fix: Validate qty as a positive integer and price as a positive number on a tick grid; reject otherwise with 400.
- False-positive notes: Would be lower if a validating proxy sits in front; none is in scope.

### SEC-001 Any caller can read any order (no ownership check) (high, security, confidence INFERRED)

- Location: `server.js:9` (citation: verified)
- Evidence:

```
const order = orders.get(req.params.id);
```

- Reproduction: GET /api/orders/1 with any or no x-user header returns another user's order.
- Impact: Order details of every user are exposed by enumerating ids.
- Fix: Look up the order, then return 404 unless order.owner equals the authenticated user id from the session (not a client header).

### SEC-002 Identity taken from a client-supplied header (high, security, confidence INFERRED)

- Location: `server.js:20` (citation: verified)
- Evidence:

```
orders.set(id, { id, qty, price, owner: req.headers["x-user"] });
```

- Reproduction: POST /api/orders with x-user: someone-else creates an order owned by that user.
- Impact: Anyone can act as anyone.
- Fix: Derive the owner from a verified session or token on the server.

### A11Y-002 Zoom disabled and field labeled only by a placeholder (medium, accessibility, confidence INFERRED)

- Location: `index.html:3` (citation: verified)
- Evidence:

```
<head><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"><title>Orders</title></head>
```

- Reproduction: Pinch-zoom on a phone does not enlarge text; the quantity field has no label once typing starts.
- Impact: Low-vision users cannot zoom; the field loses its name.
- Fix: Remove maximum-scale; add <label for="qty">Quantity</label>; add lang on html.

## Not checked

- performance: no build output or runtime in scope
- dependencies: no lockfile in the fixture
