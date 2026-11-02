import re
def words(text): return set(re.findall(r"\w+",text.casefold()))
def retrieve(query,documents,limit=3):
    if not isinstance(query,str) or not query.strip(): raise ValueError("query required")
    if not 1<=limit<=20: raise ValueError("invalid limit")
    q=words(query)
    ranked=[]
    for doc in documents:
        if not isinstance(doc,dict) or not isinstance(doc.get("id"),str) or not isinstance(doc.get("text"),str): raise ValueError("invalid document")
        score=len(words(doc["text"]) & q)
        if score: ranked.append((score,doc["id"],doc["text"]))
    ranked.sort(key=lambda x:(-x[0],x[1]))
    return [{"source":source,"excerpt":text[:300],"score":score} for score,source,text in ranked[:limit]]
if __name__=="__main__":
    print(retrieve("school fees",[{"id":"school-policy","text":"School fees are paid each semester"},{"id":"holidays","text":"Summer holidays are in July"}]))
