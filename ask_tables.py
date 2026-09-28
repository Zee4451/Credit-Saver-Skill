import sys
from runner import ask_openrouter

prompt = """
You are an expert React and CSS designer.
In a POS restaurant app (React 19 + CSS Modules), we need to create a dedicated, modern Table Management component:
Currently, it only shows:
- Button: "Add New Table"
- A basic grid of cards:
  <h3>Table {tableId}</h3>
  <p>Orders: {tableData.orders?.length || 0}</p>
  <p>Total: ₹{tableData.total || 0}</p>
  <button onClick={() => deleteTable(tableId)}>Delete Table</button>

Design an ultra modern, premium Table Management component with:
1. Summary Stats Bar at the top:
   - Total Tables count
   - Occupied / Active Tables (where (tableData.orders && tableData.orders.length > 0) || tableData.total > 0)
   - Available / Vacant Tables
   - Current Live Dine-In Revenue (sum of all tableData.total)
2. Filter & Action Toolbar:
   - Search table by ID / number
   - Filter pills: All, Occupied, Available
   - "Add New Table" button with clean modern styling and plus icon (+ Add Table)
3. Modern Table Cards Grid:
   - Status badge: "Occupied" (amber/emerald glowing badge) vs "Available" (subtle teal/green or slate badge)
   - Table ID header with modern table icon
   - Order count badge/metric
   - Live Bill amount formatted in INR (₹)
   - "Delete Table" button with confirmation state or clean inline confirm
4. CSS module styles with clean variables, responsive grid (auto-fill, minmax 240px, 1fr), sleek card borders, smooth hover animations.

Provide:
1. Complete React component code for `TableManagement.jsx` (props: `tables`, `addNewTable`, `deleteTable`)
2. Complete CSS module code for `TableManagement.module.css`
"""

res = ask_openrouter(prompt, model="cohere")
if res.get("success"):
    print("\n\nSUCCESS FROM MODEL:", res.get("model_used"))
else:
    print("FAILED:", res.get("error"))
