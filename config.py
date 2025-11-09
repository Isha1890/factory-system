# config.py
import os

# --- SUPABASE CONFIG ---
# Replace with your actual Supabase URL and Key
SUPABASE_URL = "https://qabkagbyvvbghkyigmmf.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhYmthZ2J5dnZiZ2hreWlnbW1mIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI2NTg4MTEsImV4cCI6MjA3ODIzNDgxMX0.ISAbVyQKeU39JUsFmKJkxl__bPr4eL0nbeudwjKAQtk"

# --- RAG & EMBEDDING CONFIG ---
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
LLM_MODEL = 'llama3'

# --- ANOMALY THRESHOLDS ---
ANOMALY_THRESHOLDS = {
    "PUMP-101": {"vibration_mm_s": 5.0}
}

# --- KNOWLEDGE BASE ---
MANUALS_DIR = 'manuals/'