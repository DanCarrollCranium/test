from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd
import openai

openai.api_key = "your-api-key"

response = openai.ChatCompletion.create(
    model="gpt-4o",  # This is the new GPT-4o model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like in Paris today?"}
    ]
)


df = pd.read_json("hf://datasets/O1-OPEN/OpenO1-SFT/OpenO1-SFT.jsonl", lines=True)

model_name = "Qwen/Qwen2.5-Coder-32B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

prompt = "write a quick sort algorithm."
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)
model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

generated_ids = model.generate(
    **model_inputs,
    max_new_tokens=512
)
generated_ids = [
    output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
]

response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
