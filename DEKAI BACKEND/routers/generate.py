from fastapi import APIRouter, Depends,requests,HTTPException
from sqlalchemy.orm import Session
from schemas import Message
from oath2 import get_current_user
import schemas
import models
from database import sessionmk
from vector_store import chroma_db 
from langchain_core.documents import Document  

#models
from model import dekainlp01,openrouter,dekainlp15


router = APIRouter(
    tags=["generation"]
)


def get_db():
    db=sessionmk()
    try:
        yield db
    finally:
        db.close()
"""
def serialize_history(db_messages):
    formatted = []

    for m in db_messages:
        role = "assistant" if m.sender == "assistant" else "user"
        formatted.append({
            "role": role,
            "content": m.content
        })

    return formatted
"""
def serialize_history(db_messages):
    formatted = []
    for m in db_messages:
        # 1. Ensure we only send 'user' or 'assistant' roles
        # 2. Ensure content is a string and not empty
        role = "assistant" if getattr(m, 'sender', None) == "assistant" else "user"
        content = getattr(m, 'content', "")
        
        if content and content.strip():
            formatted.append({"role": role, "content": content.strip()})
    
    return formatted

@router.post("/conversation/{conversation_id}/generate")
def generate_reply(
    conversation_id: int,
    request: schemas.GenerateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1️⃣ Verify conversation ownership
    conversation = db.query(models.Conversation).filter(
        models.Conversation.conversation_id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2️⃣ Fetch last N messages
    messages = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.created_at.asc())
        .limit(6)
        .all()
    )
    messages = list(reversed(messages))

    # 3️⃣ Build history
    history = []
    for m in messages:
        history.append(m.content)

    # 4️⃣ Generate
    reply = dekainlp01.generate_reply_from_history(history)

    if not reply:
     reply = "🙂 Tell me a bit more."

    return {"text": reply}




@router.post("/conversation/{conversation_id}/generater")
def generate_open_reply(
    conversation_id: int,
    request_data: schemas.GenerateRequest, # <--- THIS IS REQUIRED to process the POST body
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    
    # 1. Verify ownership (standard check)
    conversation = db.query(models.Conversation).filter(
        models.Conversation.conversation_id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # 1. Fetch messages from DB
   
    db_messages = (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.created_at)
        .all()
    )

    query = request_data.prompt
    docs = chroma_db.max_marginal_relevance_search(query, k=10, fetch_k=20)
    
    """
    print("RETRIEVED DOCS:")
    for i, doc in enumerate(docs):
      print(f"Doc {i+1}:")
      print(doc.page_content[:500])  # print first few hundred characters
    """

    # Format the retrieved docs as a single context block
    context_text = "\n\n".join([doc.page_content for doc in docs])

    # 2. Combine context + prompt
    full_prompt = f"""Use the following context from Dedan Kimathi University documents to answer the questions specifically involving dedan kimathi university.Dont use context if the query does not involve dedan kimathi.
If the context does not contain an answer, use your own knowledge then if you still dont know say you dont know.Ensure the user does
not suspect you are using context,make it seem like you know this info although its from context.

Context:
{context_text}

Question: {query}
Answer:"""

    # 3. Convert to OpenRouter format
    history = serialize_history(db_messages)
    
    # 3. Add system prompt and the NEW prompt from the request
    messages = [
        {"role": "system", "content": "You are DEKAI, a kind,chearful and helpful AI assistant.You do not have to refer to yourself as a computer everytime user asks personal question find some corny funny way to reply "},*history,
        {"role": "user", "content": full_prompt}
    ]

    # 4. Call OpenRouter
    reply = openrouter.generate_openrouter_reply(messages)

    return {"text": reply}


@router.post("/conversation/{conversation_id}/generate-v1.5")
def generate_v15(
    conversation_id: int,
    request: schemas.GenerateRequest, # Use your request schema for user_input
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Verify ownership (standard check)
    conversation = db.query(models.Conversation).filter(
        models.Conversation.conversation_id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2. Call the new advanced model
    # We pass the user's latest input from the request
    reply = dekainlp15.generate_advanced_reply(request.prompt)

    return {"text": reply }