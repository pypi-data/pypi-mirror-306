from _context import sm

# Defaults to the default provider (openai)
r = sm.generate_text("Write a poem about the moon", llm_provider="groq", stream=True)

for chunk in r:
    print(chunk, end="", flush=True)
