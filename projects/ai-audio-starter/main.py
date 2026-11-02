import math
import wave
def describe_wav(path):
 with wave.open(str(path),"rb") as w:
  channels=w.getnchannels()
  rate=w.getframerate()
  width=w.getsampwidth()
  frames=w.getnframes()
  if width!=2:raise ValueError("only 16-bit PCM supported")
  if w.getcomptype()!="NONE":raise ValueError("compressed WAV unsupported")
  data=w.readframes(frames)
 from array import array
 samples=array("h")
 samples.frombytes(data)
 if not samples:raise ValueError("empty audio")
 if channels<1 or rate<1:raise ValueError("invalid metadata")
 rms=math.sqrt(sum((s/32768)**2 for s in samples)/len(samples))
 return {"duration_seconds":round(frames/rate,3),"sample_rate":rate,"channels":channels,"rms":round(rms,6)}
if __name__=="__main__":
 print("Call describe_wav('recording.wav') for metadata. No speech transcription is claimed.")
