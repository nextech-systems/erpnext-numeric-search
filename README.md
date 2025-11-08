# ERPNext Numeric Search

Make **numeric and currency fields** searchable via the **Global Search** in ERPNext/Frappe v14.  
This tiny app toggles `in_global_search` for key accounting fields (e.g., **grand_total**, **outstanding_amount**, **debit/credit**) using **Property Setters**—so it’s upgrade-safe and doesn’t modify core files.

---

## ✨ Features

- Enables Global Search for commonly used **money/number fields** across accounting doctypes:
  - **Sales Invoice**: `grand_total`, `outstanding_amount`, `rounded_total`
  - **Purchase Invoice**: `grand_total`, `outstanding_amount`, `rounded_total`
  - **Sales Order** / **Purchase Order**: `grand_total`, `rounded_total`
  - **Payment Entry**: `paid_amount`, `received_amount`
  - **Journal Entry**: `total_debit`, `total_credit`
  - **GL Entry**: `debit`, `credit`
- No server restarts required beyond migrate.
- Easy to extend: add your own doctypes/fields in one dictionary.

> After install, you can type numbers like `5000` or `12500.00` in the **Global Search** (top-right, Ctrl+G) and see matching entries.

---

## ✅ Compatibility

- **ERPNext / Frappe v14**
- Tested on Linux. Works fine on Windows WSL; commands below include Windows-friendly variants.

---

## 📦 Installation

> Replace `<your-site>` with your site name.

### Option A: Install via Git (recommended)

```bash
# From your bench folder
bench get-app https://github.com/nextech-systems/erpnext-numeric-search.git
bench --site <your-site> install-app erpnext_numeric_search
bench --site <your-site> migrate


Now rebuild the Global Search index (one-time):

# Rebuild only the affected doctypes (faster)
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Sales Invoice'}"
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Purchase Invoice'}"
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Payment Entry'}"
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Journal Entry'}"
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'GL Entry'}"
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Sales Order'}"
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Purchase Order'}"

Option B: Install from local folder
# If you cloned the app directly into apps/
bench --site <your-site> install-app erpnext_numeric_search
bench --site <your-site> migrate

🧪 Usage

Open ERPNext and use the Global Search (top-right or Ctrl+G / Cmd+G).
Search for numbers like 5000 and you’ll see results grouped by doctype (e.g., Sales Invoice, Payment Entry, etc.).

If you don’t see results the first time, make sure you ran the rebuild commands above.

🛠 Configuration (extend to more fields)

You can add more doctypes/fields by editing:

erpnext_numeric_search/erpnext_numeric_search/patches/v14_001_enable_numeric_global_search.py


Modify the TARGETS dict to include your additional fields. Then run:

bench --site <your-site> migrate
# and rebuild for the new doctypes:
bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'<Your DocType>'}"

🧹 Uninstall
bench --site <your-site> uninstall-app erpnext_numeric_search
bench --site <your-site> migrate


Uninstalling does not automatically revert Property Setters.
If you want to remove them, delete the relevant Property Setter rows (filter by property = in_global_search and the doctypes above) and rebuild Global Search again for those doctypes.

🔍 Troubleshooting

Migrate seems slow / hangs
Don’t run heavy reindexing inside a patch. This app’s patch only creates Property Setters. Rebuild after migrate using the commands above.

No such command reindex
In Frappe v14 there’s no bench reindex command. Use the per-doctype rebuild:

bench --site <your-site> execute frappe.utils.global_search.rebuild_for_doctype --kwargs "{'doctype':'Sales Invoice'}"


Nothing shows up for numbers
Ensure you rebuilt for the doctypes you care about, and try exact numeric strings (e.g., 5000 vs 5000.00).
Consider indexing both rounded and exact fields if needed.

🤝 Contributing

PRs welcome! Ideas:

Add a small settings page to toggle doctypes/fields.

Include more accounting doctypes (POS Invoice, Expense Claim).

Optional rounding/index variants for numeric fields.

📜 License

MIT


---
