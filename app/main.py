from datetime import datetime
from itertools import count, cycle
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

CONVERSATIONS = [
    {"text": "A", "status": "active"},
    {"text": "B", "status": "completed"},
    {"text": "C", "status": "active"},
    {"text": "D", "status": "completed"},
]
BASE_CONVERSATIONS = [
    "こんにちは",
    "FastAPI便利ですね",
    "htmxいい感じ",
]
CONVERSATION_STREAM = cycle(BASE_CONVERSATIONS)
CONVERSATION_LOG = []
CONVERSATION_ID = count(1)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/api/conversations")
async def get_conversations(request: Request):
    CONVERSATION_LOG.append(
        {
            "id": next(CONVERSATION_ID),
            "text": next(CONVERSATION_STREAM),
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
    )
    return templates.TemplateResponse(
        "conversations.html",
        {
            "request": request,
            "conversations": CONVERSATION_LOG
        }
    )

@app.post("/api/conversations/{message_id}/delete")
async def delete_conversation(request: Request, message_id: int):
    for index, item in enumerate(CONVERSATION_LOG):
        if item["id"] == message_id:
            del CONVERSATION_LOG[index]
            break
    return templates.TemplateResponse(
        "conversations.html",
        {
            "request": request,
            "conversations": CONVERSATION_LOG,
        },
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
