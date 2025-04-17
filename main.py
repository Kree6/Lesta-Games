from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import math
from typing import Optional
from fastapi import Query
from collections import Counter
import re
import copy


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    page: int = 1,
    sort: str = "idf",
    search: str = "",
    min_tf: Optional[str] = Query(default=None),
    min_idf: Optional[str] = Query(default=None)
):
    result = copy.deepcopy(getattr(app.state, "result", []))

    try:
        min_tf_val = int(min_tf) if min_tf not in [None, ""] else None
    except ValueError:
        min_tf_val = None

    try:
        min_idf_val = float(min_idf) if min_idf not in [None, ""] else None
    except ValueError:
        min_idf_val = None

    if search:
        result = [r for r in result if search.lower() in r["word"]]
    if min_tf_val is not None:
        result = [r for r in result if r["tf"] >= min_tf_val]
    if min_idf_val is not None:
        result = [r for r in result if r["idf"] >= min_idf_val]

    if sort in ["word", "tf", "idf"]:
        result = sorted(result, key=lambda x: x[sort], reverse=(sort != "word"))

    per_page = 50
    total_pages = max(1, (len(result) + per_page - 1) // per_page)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = result[start:end]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": paginated,
        "current_page": page,
        "total_pages": total_pages
    })


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(...)):
    if not file:
        return HTMLResponse(content="Файл не выбран", status_code=400)

    content = await file.read()
    text = content.decode("utf-8").lower()
    words = re.findall(r"\b\w+\b", text, flags=re.UNICODE)
    tf_counter = Counter(words)
    total_words = len(words)

    def compute_idf(word):
        return math.log((1 + total_words) / (1 + tf_counter[word])) + 1

    result = []
    for word, tf in tf_counter.items():
        idf = compute_idf(word)
        result.append({"word": word, "tf": tf, "idf": round(idf, 4)})

    app.state.result = result
    return RedirectResponse(url="/", status_code=303)
