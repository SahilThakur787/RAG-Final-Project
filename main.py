from dotenv import load_dotenv
import os

load_dotenv()

print("Loaded Key:", os.getenv("GROQ_API_KEY"))

import argparse
from app.ingest import ingest_pdf
from app.chat import chat_loop

p = argparse.ArgumentParser()
p.add_argument("--ingest")
p.add_argument("--chat", action="store_true")
a = p.parse_args()

if a.ingest:
    ingest_pdf(a.ingest)
elif a.chat:
    chat_loop()
else:
    print("Use --ingest <pdf> or --chat")