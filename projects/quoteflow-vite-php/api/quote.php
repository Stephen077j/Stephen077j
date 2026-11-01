<?php
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {http_response_code(405); header('Allow: POST'); echo json_encode(['error'=>'Use POST']); exit;}
if (strlen(file_get_contents('php://input', false, null, 0, 65537)) > 65536) {http_response_code(413); echo json_encode(['error'=>'Request too large']); exit;}
try {
  $body = json_decode(file_get_contents('php://input'), true, 512, JSON_THROW_ON_ERROR);
  if (!is_array($body) || !isset($body['items']) || !is_array($body['items']) || count($body['items']) > 100) throw new InvalidArgumentException('Invalid items');
  $taxRate = $body['taxPercent'] ?? 0;
  if (!is_numeric($taxRate) || (float)$taxRate < 0 || (float)$taxRate > 100) throw new InvalidArgumentException('Invalid tax');
  $subtotal = 0.0;
  foreach ($body['items'] as $line) {
    if (!is_array($line)) throw new InvalidArgumentException('Invalid line');
    $description = trim((string)($line['description'] ?? ''));
    $qty = $line['quantity'] ?? null;
    $price = $line['unitPrice'] ?? null;
    if ($description === '' || strlen($description) > 120 || filter_var($qty, FILTER_VALIDATE_INT) === false || (int)$qty < 1 || (int)$qty > 10000 || !is_numeric($price) || !is_finite((float)$price) || (float)$price < 0 || (float)$price > 100000000) throw new InvalidArgumentException('Invalid line values');
    $subtotal += round((int)$qty * (float)$price, 2);
  }
  $subtotal = round($subtotal, 2); $tax = round($subtotal * (float)$taxRate / 100, 2);
  echo json_encode(['subtotal'=>$subtotal,'tax'=>$tax,'total'=>round($subtotal+$tax,2)],JSON_THROW_ON_ERROR);
} catch (Throwable $e) {http_response_code(422);echo json_encode(['error'=>'Invalid quote data']);}
