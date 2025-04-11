from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ctransformers import AutoModelForCausalLM

# Request model
class MessageRequest(BaseModel):
    message: str

# Initialize app
app = FastAPI()

# Allow CORS for frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once when FastAPI starts
print("🔄 Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/zephyr-7B-alpha-GGUF",
    model_file="zephyr-7b-alpha.Q4_K_M.gguf",
    model_type="mistral",
    gpu_layers=0,
    context_length=1024
)
print("✅ Model loaded!")

# Health check
@app.get("/")
async def root():
    return {"message": "Zephyr-7B-Alpha backend is live!"}

# Chat endpoint
@app.post("/chat")
async def chat(req: MessageRequest):
    print(f"📨 Received message: {req.message}")
    user_message = req.message.strip()

    prompt = f"""<|system|>You are AURA, an intelligent AI assistant.<|end|>
<|user|>{user_message}<|end|>
<|assistant|>"""

    try:
        output = model(prompt, max_new_tokens=256, temperature=0.7)
        return {"response": output}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
