import csv
import io
import streamlit as st
from statistics import mean

def summarize(csv_text):
    rows=list(csv.DictReader(io.StringIO(csv_text)))
    amounts=[]
    for row in rows:
        value=float(row["amount"])
        if not -1e9 < value < 1e9:
            raise ValueError("Invalid amount")
        amounts.append(value)
    if not amounts: return {"count":0,"total":0,"average":0}
    return {"count":len(amounts),"total":round(sum(amounts),2),"average":round(mean(amounts),2)}

def main():
    st.set_page_config(page_title="Sales Dashboard",layout="wide")
    st.title("Sales Dashboard")
    st.caption("Local demo — use sample data only")
    upload=st.file_uploader("CSV containing an amount column",type=["csv"])
    text=upload.getvalue().decode("utf-8") if upload else "amount\n120\n80\n150\n"
    try:
        result=summarize(text)
        a,b,c=st.columns(3)
        a.metric("Records",result["count"])
        b.metric("Total",result["total"])
        c.metric("Average",result["average"])
    except (ValueError,KeyError,UnicodeDecodeError) as exc:
        st.error("Invalid CSV: "+str(exc))
if __name__=="__main__": main()
