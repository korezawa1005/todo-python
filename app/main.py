from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

CONVERSATIONS = [
    {"text": "買い物リストを更新した", "status": "active"},
    {"text": "会議のメモを共有した", "status": "completed"},
    {"text": "FastAPIの調査を進めた", "status": "active"},
    {"text": "デザインの確認が完了", "status": "completed"},
]

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/api/conversations")
async def get_conversations(request: Request):
    conversations = [
        "こんにちは",
        "FastAPI便利ですね",
        "htmxいい感じ",
        f"更新時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    return templates.TemplateResponse(
        "conversations.html",
        {
            "request": request,
            "conversations": conversations
        }
    )


@app.get("/api/search")
async def search(request: Request, query: str = "", status: str = "active"):
    normalized_query = query.strip()
    results = []
    for item in CONVERSATIONS:
        if status and item["status"] != status:
            continue
        if normalized_query and normalized_query not in item["text"]:
            continue
        results.append(f'{item["text"]} ({item["status"]})')
    return templates.TemplateResponse(
        "results.html",
        {"request": request, "results": results}
    )
