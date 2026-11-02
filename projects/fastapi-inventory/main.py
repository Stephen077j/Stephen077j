from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field

app=FastAPI(title="Stock Tracker",version="0.1.0")
class Item(BaseModel):
    name:str=Field(min_length=1,max_length=80)
    quantity:int=Field(ge=0,le=100000)

items={1:Item(name="Keyboard",quantity=12)}
@app.get("/health")
def health(): return {"status":"ok"}
@app.get("/items")
def list_items(): return [{"id":key,**value.model_dump()} for key,value in items.items()]
@app.post("/items/{item_id}")
def put_item(item_id:int,item:Item):
    if item_id<1: raise HTTPException(status_code=422,detail="Invalid item ID")
    items[item_id]=item
    return {"id":item_id,**item.model_dump()}
