import frappe

# Map of DocType -> list of fieldnames to include in Global Search
TARGETS = {
    "Sales Invoice": ["grand_total", "outstanding_amount", "rounded_total"],
    "Purchase Invoice": ["grand_total", "outstanding_amount", "rounded_total"],
    "Sales Order": ["grand_total", "rounded_total"],
    "Purchase Order": ["grand_total", "rounded_total"],
    "Payment Entry": ["paid_amount", "received_amount"],
    "Journal Entry": ["total_debit", "total_credit"],
    "GL Entry": ["debit", "credit"],
}

def make_property_setter(dt, fieldname):
    """Ensure DocField is included in Global Search via Property Setter."""
    if not frappe.db.exists(
        "Property Setter",
        {"doc_type": dt, "field_name": fieldname, "property": "in_global_search"},
    ):
        frappe.get_doc({
            "doctype": "Property Setter",
            "doc_type": dt,
            "doctype_or_field": "DocField",
            "field_name": fieldname,
            "property": "in_global_search",
            "value": "1",
            "property_type": "Check",
        }).insert(ignore_permissions=True)
    else:
        frappe.db.set_value(
            "Property Setter",
            {"doc_type": dt, "field_name": fieldname, "property": "in_global_search"},
            "value",
            "1",
        )

def execute():
    """Create/Update property setters only; defer indexing to a post-migrate step."""
    for dt, fields in TARGETS.items():
        for fn in fields:
            try:
                make_property_setter(dt, fn)
            except Exception:
                frappe.log_error(f"Could not set in_global_search for {dt}.{fn}")

    # Clear caches so metadata reflects new property setters
    frappe.clear_cache()

    # IMPORTANT: Do NOT rebuild the global search index here.
    # Run `bench --site <yoursite> reindex` after migrate.
    #
    # If you ever want to enqueue per-doctype rebuilds instead, do it outside migrate:
    # from frappe import enqueue
    # for dt in TARGETS.keys():
    #     enqueue("frappe.utils.global_search.rebuild_for_doctype", doctype=dt)
