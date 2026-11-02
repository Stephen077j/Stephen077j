from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def amount(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise ValueError("Expected a numeric amount")
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("Expected a numeric amount") from exc
    if not result.is_finite():
        raise ValueError("Amount must be finite")
    return result


def calculate_quote(payload):
    if not isinstance(payload, dict):
        raise ValueError("Expected a JSON object")
    items = payload.get("items")
    if not isinstance(items, list) or not 1 <= len(items) <= 100:
        raise ValueError("items must contain between 1 and 100 lines")
    tax_rate = amount(payload.get("tax_percent", 0))
    if not 0 <= tax_rate <= 100:
        raise ValueError("tax_percent must be between 0 and 100")
    lines = []
    subtotal = Decimal("0.00")
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each item must be an object")
        description = item.get("description")
        quantity = item.get("quantity")
        if not isinstance(description, str) or not 1 <= len(description.strip()) <= 120:
            raise ValueError("description must contain 1 to 120 characters")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= 10000:
            raise ValueError("quantity must be an integer from 1 to 10000")
        price = amount(item.get("unit_price"))
        if not 0 <= price <= 100000000:
            raise ValueError("unit_price must be between 0 and 100000000")
        line_total = (price * quantity).quantize(CENT, rounding=ROUND_HALF_UP)
        subtotal += line_total
        lines.append({"description": description.strip(), "quantity": quantity,
                      "unit_price": str(price), "line_total": str(line_total)})
    tax = (subtotal * tax_rate / 100).quantize(CENT, rounding=ROUND_HALF_UP)
    return {"items": lines, "subtotal": str(subtotal), "tax": str(tax),
            "total": str(subtotal + tax), "tax_percent": str(tax_rate)}
