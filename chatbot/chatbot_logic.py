from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ChatbotLogic:
    """Contains the logic for the chatbot."""

    def __init__(self, model_name: str = 'gpt2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # Add padding token if not already present
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': self.tokenizer.eos_token})
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.pad_token_id = self.tokenizer.pad_token_id

    def generate_response(self, user_input: str) -> str:
        """Generate a response based on the user input using the LLM."""
        prompt = f"User: {user_input}\nAssistant:"
        inputs = self.tokenizer.encode(prompt, return_tensors='pt', padding=True, truncation=True).to(self.device)
        attention_mask = torch.ones(inputs.shape, device=self.device)
        outputs = self.model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=250,
            num_return_sequences=1,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=self.pad_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self.post_process_response(response, prompt)

    def post_process_response(self, message: str, prompt: str) -> str:
        """Refine the generated response to ensure clarity and relevance."""
        response_start = message.find('Assistant:') + len('Assistant:')
        response = message[response_start:].strip()

        # Split the response into sentences
        sentences = response.split('. ')
        
        # Remove sentences that do not directly answer the question or are too short
        filtered_sentences = [s for s in sentences if 'User:' not in s and 'Assistant:' not in s and len(s) > 15]

        # Join the filtered sentences
        cleaned_message = '. '.join(filtered_sentences)

        # Limit the response length to a reasonable number of sentences
        max_sentences = 3
        if len(filtered_sentences) > max_sentences:
            cleaned_message = '. '.join(filtered_sentences[:max_sentences])

        # Ensure the response ends with a complete sentence
        if not cleaned_message.endswith('.'):
            cleaned_message += '.'

        return cleaned_message
