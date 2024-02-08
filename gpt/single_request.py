from openai import OpenAI
import json

OPENAI_API_KEY = "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"
ORGANIZATION = "org-SqAqKbRAlkpTd28SbobD0Prf"

MODEL = "gpt-3.5-turbo"
SEED = 42
TEMPERATURE = 0
TOP_P = 1
MAX_TOKENS = 1
LOGPROBS = True
TOP_LOGPROBS = 5

client = OpenAI(api_key=OPENAI_API_KEY, organization=ORGANIZATION)

class GPTLabeler:
    def __init__(self, openai_client, texts_per_batch, output_jsonl_path,
                 temperature=TEMPERATURE, top_p=TOP_P, model=MODEL,
                 seed=SEED, max_tokens=MAX_TOKENS,
                 logprobs=LOGPROBS, top_logprobs=TOP_LOGPROBS):
        
        self.openai_client = openai_client
        self.model = model
        self.seed = seed
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.logprobs = logprobs
        self.top_logprobs = top_logprobs
        self.texts_per_batch = texts_per_batch
        self.output_jsonl_path = output_jsonl_path

    def label_texts(self, texts):
        labels = []
        num_batches = len(texts) // self.texts_per_batch + (1 if len(texts) % self.texts_per_batch != 0 else 0)
        for batch_idx in range(num_batches):
            batch_texts = texts[batch_idx * self.texts_per_batch : (batch_idx + 1) * self.texts_per_batch]
            batch_input = [{"prompt": text, "completion": "<|endoftext|>", "max_tokens": 1} for text in batch_texts]
            batch_output = self._get_batch_completion(batch_input)
            batch_labels = self._process_batch_output(batch_output)
            labels.extend(batch_labels)
            self._write_to_jsonl(batch_texts, batch_labels)
        return labels
    
    def _get_mesage(self, batch_input):
        
        for _input in batch_input:
            
        pass

    def _get_batch_completion(self, batch_input):
        completion = self.openai_client.chat.completions.create(
            model=self.model,
            seed=self.seed,
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
            logprobs=self.logprobs,
            top_logprobs=self.top_logprobs,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
        )
        return completion

    def _process_batch_output(self, batch_output):
        labels = []
        for result in batch_output["choices"]:
            if result["finish_reason"] == "completed" and result["error"] is None:
                label = "Relevant" if result["text"].strip().lower() == "yes" else "Irrelevant"
                labels.append(label)
            else:
                labels.append("Error")
        return labels

    def _write_to_jsonl(self, texts, labels):
        with open(self.output_jsonl_path, "a") as f:
            for text, label in zip(texts, labels):
                data = {"text": text, "label": label}
                json.dump(data, f)
                f.write("\n")

# Example usage
api_key = "YOUR_OPENAI_API_KEY"
texts_to_label = [
    "This is a relevant text.",
    "This is an irrelevant text.",
    "Another relevant example.",
    "Another irrelevant example."
]
texts_per_batch = 2
output_jsonl_path = "labeled_data.jsonl"

labeler = GPTLabeler(api_key, texts_per_batch, output_jsonl_path)
labels = labeler.label_texts(texts_to_label)

print("Labels:", labels)
