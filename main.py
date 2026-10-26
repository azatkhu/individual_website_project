from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from get_dataframe import get_dataframe
from columns_count_validation import check_error_return_html_table
from typing import List


app = FastAPI()
templates = Jinja2Templates(directory = "templates")

path = "data/supermarket_large_dataset.csv"
df = get_dataframe(path)

size = df.shape

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name = "homepage.html",
        context = {},
    )

@app.get("/selectcolumns", response_class=HTMLResponse)
def choose_columns(request: Request):

    return templates.TemplateResponse(
        request = request, 
        name = "show_dataframe.html",
        context = {
            "columns": df.columns.tolist(),
        }
    )

@app.get("/table", response_class=HTMLResponse)
def show_table(request: Request, cols: List[str] = Query(default = [])):

    table_html, error = check_error_return_html_table(df = df, list_cols = cols)

    return templates.TemplateResponse(
        request = request,
        name = "table.html",
        context = {
            "selected_columns": cols,
            "error": error,
            "table": table_html,
        }
    )
