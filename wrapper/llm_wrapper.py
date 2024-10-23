from llama_cpp import Llama
from transformers import AutoTokenizer


class LLM:
    MODEL_ID = "MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M"
    MODEL_PATH = "/home/gpp/src/model/llama3-korean-bllossom-8b/llama-3-Korean-Bllossom-8B-Q4_K_M.gguf"

    model: Llama | None = None
    tokenizer: AutoTokenizer | None = None

    prompt: str = ""

    def __init__(self, verbose: bool=False, temperature: float=0.3, top_p: float=0.9, max_tokens: int=2048):
        if LLM.model is None:
            LLM.model = Llama(
                model_path=LLM.MODEL_PATH,
                n_ctx=8192,
                n_gpu_layers=-1,
                verbose=verbose
            )

        if LLM.tokenizer is None:
            LLM.tokenizer = AutoTokenizer.from_pretrained(LLM.MODEL_ID)

        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.prompt: str = ""

    def __del__(self):
        del LLM.model
        del LLM.tokenizer

        LLM.model = None
        LLM.tokenizer = None

    def set_prompt(self, prompt: str):
        self.prompt = prompt
        return

    def generate(self, instruction: str):
        if len(self.prompt) == 0:
            raise ValueError("prompt is not set.")

        if len(instruction) == 0:
            raise ValueError("instruction is not set.")

        generation_kwargs = {
            "max_tokens":self.max_tokens,
            "stop":["<|eot_id|>"],
            "top_p":self.top_p,
            "temperature":self.temperature,
        }

        messages = [
            {"role": "system", "content": f"{self.prompt}"},
            {"role": "user", "content": f"{instruction}"}
        ]

        p = LLM.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            truncation=True
        )

        response = LLM.model(p, **generation_kwargs)
        return response["choices"][0]["text"]
