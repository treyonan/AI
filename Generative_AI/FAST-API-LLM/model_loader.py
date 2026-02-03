from transformers import pipeline

# Load the GPT-2 model once during startup
generator = pipeline("text-generation", model="gpt2")