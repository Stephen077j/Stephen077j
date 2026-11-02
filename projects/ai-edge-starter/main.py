import hashlib
from pathlib import Path
def model_manifest(path,expected_sha256=None,max_bytes=100_000_000):
 p=Path(path)
 if p.suffix.lower()!=".onnx":raise ValueError("expected .onnx file")
 size=p.stat().st_size
 if not 0<size<=max_bytes:raise ValueError("model size not permitted")
 digest=hashlib.sha256(p.read_bytes()).hexdigest()
 if expected_sha256 and digest!=expected_sha256:raise ValueError("model hash mismatch")
 return {"name":p.name,"size_bytes":size,"sha256":digest,"format":"onnx"}
if __name__=="__main__":
 print("Validate a local .onnx file with model_manifest. Does not execute ONNX inference.")
