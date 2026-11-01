export function calculateQuote(items, taxPercent = 0) {
  if (!Array.isArray(items) || !Number.isFinite(taxPercent) || taxPercent < 0 || taxPercent > 100) throw new Error('Invalid quote input');
  const normalized = items.map(item => {
    const description = String(item.description || '').trim();
    const quantity = Number(item.quantity), unitPrice = Number(item.unitPrice);
    if (!description || !Number.isInteger(quantity) || quantity < 1 || quantity > 10000 || !Number.isFinite(unitPrice) || unitPrice < 0 || unitPrice > 100000000) throw new Error('Invalid line item');
    const lineTotal = Math.round(quantity * unitPrice * 100) / 100;
    return {description, quantity, unitPrice, lineTotal};
  });
  const subtotal = Math.round(normalized.reduce((sum, line) => sum + line.lineTotal, 0) * 100) / 100;
  const tax = Math.round(subtotal * taxPercent) / 100;
  return {items:normalized,subtotal,tax,total:Math.round((subtotal+tax)*100)/100,taxPercent};
}