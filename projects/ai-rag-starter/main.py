"""Local evidence retrieval using TF-IDF; no LLM or fabricated answers."""
import math
import re
from collections import Counter

def tokens(text):
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    return re.findall(r"[^\W_]+", text.casefold())

def retrieve(query, documents, limit=3):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query required")
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 20:
        raise ValueError("invalid limit")
    if not isinstance(documents, list) or len(documents) > 1000:
        raise ValueError("documents must be a list of at most 1000 items")
    clean = []
    seen = set()
    for doc in documents:
        if not isinstance(doc, dict) or not isinstance(doc.get("id"), str) or not isinstance(doc.get("text"), str):
            raise ValueError("invalid document")
        if not doc["id"].strip() or doc["id"] in seen or len(doc["text"]) > 100000:
            raise ValueError("duplicate id, blank id, or oversized document")
        seen.add(doc["id"])
        clean.append((doc["id"], doc["text"], Counter(tokens(doc["text"]))))
    query_counts = Counter(tokens(query))
    if not query_counts:
        return []
    document_frequency = Counter()
    for _, _, frequencies in clean:
        document_frequency.update(frequencies.keys())
    results = []
    n = len(clean)
    for source, text, frequencies in clean:
        score = 0.0
        for word, query_frequency in query_counts.items():
            if frequencies[word]:
                idf = math.log(1 + (n + 1) / (document_frequency[word] + 1))
                score += (1 + math.log(frequencies[word])) * idf * (1 + math.log(query_frequency))
        if score > 0:
            results.append((score, source, text))
    results.sort(key=lambda row: (-row[0], row[1]))
    return [{"source": source, "excerpt": text[:300], "score": round(score, 6)}
            for score, source, text in results[:limit]]

if __name__ == "__main__":
    print(retrieve("school fees", [
        {"id": "school-policy", "text": "School fees are paid each semester"},
        {"id": "holidays", "text": "Summer holidays are in July"}]))
