from fastapi import FastAPI, Request, Query
from fastapi.params import Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

from auth import check_credentials, login_user, get_current_user, logout_user
from build_hash_index import build_hash_index
from get_dataframe import get_dataframe
from columns_count_validation import check_error_return_html_table
from check_id import check_id


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name = "static")

templates = Jinja2Templates(directory = "templates")

path = "data/supermarket_large_dataset.csv"
df = get_dataframe(path)

size = df.shape

unique_field = "transaction_id"
series = df[unique_field]
keys = series.tolist()

hash_index = build_hash_index(keys)

@app.get("/")
def require_user(request: Request):

    user = get_current_user(request)

    if user is None:
        return RedirectResponse(url = "/login", status_code = 302)

    return user

@app.get("/homepage", response_class=HTMLResponse)
def read_root(request: Request):

    user = require_user(request)

    if isinstance(user, RedirectResponse):
        return user 

    return templates.TemplateResponse(
        request=request,
        name = "homepage.html",
        context = {},
    )

@app.get("/selectcolumns", response_class=HTMLResponse)
def choose_columns(request: Request):

    user = require_user(request)

    if isinstance(user, RedirectResponse):
        return user 

    return templates.TemplateResponse(
        request = request, 
        name = "show_dataframe.html",
        context = {
            "columns": df.columns.tolist(),
        }
    )

@app.get("/table", response_class=HTMLResponse)
def show_table(request: Request, cols: List[str] = Query(default = [])):

    user = require_user(request)

    if isinstance(user, RedirectResponse):
        return user 

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

@app.get("/search_by_id", response_class=HTMLResponse)
def search(request: Request, transaction_id: str = None):
    
    user = require_user(request)

    if isinstance(user, RedirectResponse):
        return user 

    row = None
    error = None

    if transaction_id is not None:

        transaction_id = transaction_id.strip()
        error = check_id(transaction_id, keys)  

        if error is None:
            row_id = hash_index.get(transaction_id)
            row = df.iloc[row_id].to_dict()
            
    return templates.TemplateResponse(
        request = request,
        name = "search.html",
        context = {
            "selected_transaction_id": transaction_id,
            "selected_row": row,
            "error": error,
        }
    )

@app.get("/login", response_class=HTMLResponse)
def st_login(request: Request, error: str = None):

    return templates.TemplateResponse(
        request = request,
        name = "login.html",
        context = {"error": error},
    )

@app.post("/api/login")
def login(request: Request, username: str = Form(), password: str = Form()):

    if not check_credentials(username, password):
        
        return RedirectResponse(url = "/login?error=wrong", status_code = 302)
        
    response = RedirectResponse(url = "/homepage", status_code = 302)
    login_user(response, username)

    return response 

@app.post("/api/logout", response_class = RedirectResponse)
def logout(request: Request):
    
    response = RedirectResponse(url = "/login", status_code = 302)
    logout_user(request, response)

    return response 
