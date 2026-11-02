import json
from pathlib import Path
def evaluate(metrics,minimums):
 if not isinstance(metrics,dict) or not isinstance(minimums,dict):raise ValueError("expected metric dictionaries")
 status={}
 for key,threshold in minimums.items():
  value=metrics.get(key)
  if isinstance(value,bool) or not isinstance(value,(int,float)) or not isinstance(threshold,(int,float)):raise ValueError("invalid metric")
  if not (0<=value<=1 and 0<=threshold<=1):raise ValueError("expected metrics between 0 and 1")
  status[key]={"value":value,"minimum":threshold,"pass":value>=threshold}
 return {"pass":all(x["pass"] for x in status.values()),"metrics":status}
if __name__=="__main__":
 print(json.dumps(evaluate({"accuracy":0.83,"f1":0.77},{"accuracy":0.8,"f1":0.75}),indent=2))
