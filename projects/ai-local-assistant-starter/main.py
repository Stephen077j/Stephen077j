import json
from urllib.request import Request,urlopen
from urllib.parse import urlparse
def ask(prompt,model="gemma3:1b",base_url="http://127.0.0.1:11434",transport=None):
 if not isinstance(prompt,str) or not prompt.strip() or len(prompt)>4000:raise ValueError("invalid prompt")
 parsed=urlparse(base_url)
 if parsed.scheme!="http" or parsed.hostname not in ("127.0.0.1","localhost") or parsed.username or parsed.password:raise ValueError("only local HTTP is supported")
 payload=json.dumps({"model":model,"prompt":prompt,"stream":False}).encode()
 request=Request(base_url.rstrip("/")+"/api/generate",data=payload,headers={"Content-Type":"application/json"})
 if transport:
  result=transport(request)
 else:
  with urlopen(request,timeout=60) as response:result=json.load(response)
 return result["response"]
if __name__=="__main__":
 print("Start Ollama locally and then call ask('Hello') from Python. No model is downloaded automatically.")
