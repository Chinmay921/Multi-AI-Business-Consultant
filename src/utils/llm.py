"""LLM utility for interacting with Qwen3:8b model."""

import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import json

load_dotenv()


class QwenLLM:
    """Wrapper for Qwen3:8b model interactions."""
    
    def __init__(self):
        self.api_key = os.getenv("QWEN_API_KEY")
        self.api_base = os.getenv("QWEN_API_BASE", "https://api.example.com/v1")
        self.model_path = os.getenv("QWEN_MODEL_PATH")
        self.model_name = os.getenv("MODEL_NAME", "qwen3:8b")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
        self.use_ollama = False
        
        # Try to use OpenAI-compatible API or local model
        self._setup_client()
    
    def _setup_client(self):
        """Setup the LLM client."""
        try:
            from openai import OpenAI
            
            # Check for Ollama first (local model)
            ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            use_ollama = os.getenv("USE_OLLAMA", "true").lower() == "true"
            
            if use_ollama:
                # Use Ollama with OpenAI-compatible API
                try:
                    self.client = OpenAI(
                        api_key="ollama",  # Ollama doesn't require a real API key
                        base_url=ollama_base
                    )
                    self.use_api = True
                    self.use_ollama = True
                    print(f"[LLM] Using Ollama at {ollama_base} with model {self.model_name}")
                    return
                except Exception as e:
                    print(f"[LLM] Warning: Could not connect to Ollama: {e}")
                    print(f"[LLM] Falling back to other methods...")
            
            # Try external API if configured
            if self.api_key:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.api_base
                )
                self.use_api = True
                self.use_ollama = False
            else:
                # Fallback to local model if available
                self.use_api = False
                self.use_ollama = False
                self.client = None
        except ImportError:
            self.client = None
            self.use_api = False
            self.use_ollama = False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False
    ) -> str:
        """
        Generate a response from the model.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt/instructions
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            json_mode: Whether to force JSON output
            
        Returns:
            Generated text response
        """
        temp = temperature if temperature is not None else self.temperature
        max_t = max_tokens if max_tokens is not None else self.max_tokens
        
        if self.use_ollama:
            # Always use direct Ollama API (more reliable)
            return self._generate_local(prompt, system_prompt, temp, max_t, json_mode)
        elif self.use_api and self.client:
            # Use OpenAI-compatible API
            return self._generate_api(prompt, system_prompt, temp, max_t, json_mode)
        else:
            # Fallback to direct Ollama API
            return self._generate_local(prompt, system_prompt, temp, max_t, json_mode)
    
    def _generate_api(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        json_mode: bool
    ) -> str:
        """Generate using API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response_format = {"type": "json_object"} if json_mode else None
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                response_format=response_format
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"API error: {e}")
            return self._generate_local(prompt, system_prompt, temperature, max_tokens, json_mode)
    
    def _generate_local(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int,
        json_mode: bool
    ) -> str:
        """Generate using local Ollama model."""
        try:
            import requests
            
            ollama_base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model_name = self.model_name
            
            # Build the prompt - Ollama's generate endpoint uses simple prompt format
            # For system prompts, we can include them in the prompt text
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            else:
                full_prompt = prompt
            
            if json_mode:
                # Add JSON format instruction
                full_prompt = f"{full_prompt}\n\nPlease respond with valid JSON only, no additional text or markdown."
            
            # Use Ollama's API directly
            url = f"{ollama_base}/api/generate"
            # Increase num_predict to ensure we get a response (Ollama uses this for max tokens)
            num_predict = max(max_tokens, 500)  # Ensure minimum of 500 tokens
            payload = {
                "model": model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": num_predict
                }
            }
            
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            result = response.json()
            response_text = result.get("response", "")
            
            if not response_text:
                print(f"[LLM] Warning: Empty response from Ollama. Full result: {result}")
            
            return response_text
            
        except ImportError:
            print("[LLM] Error: 'requests' library not found. Install it with: pip install requests")
            raise
        except requests.exceptions.ConnectionError:
            print(f"[LLM] Error: Could not connect to Ollama at {ollama_base}")
            print("[LLM] Make sure Ollama is running: ollama serve")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[LLM] Request error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"[LLM] Response status: {e.response.status_code}")
                print(f"[LLM] Response body: {e.response.text[:500]}")
            raise
        except Exception as e:
            print(f"[LLM] Error generating response: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a JSON response.
        
        Args:
            prompt: User prompt
            system_prompt: System instructions
            schema: Optional JSON schema to guide output
            
        Returns:
            Parsed JSON dictionary
        """
        if schema:
            schema_prompt = f"\n\nPlease respond in JSON format matching this schema:\n{json.dumps(schema, indent=2)}"
            prompt = prompt + schema_prompt
        
        response = self.generate(prompt, system_prompt, json_mode=True)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Could not parse JSON from response: {response[:200]}")


# Global instance
_llm_instance: Optional[QwenLLM] = None


def get_llm() -> QwenLLM:
    """Get or create the global LLM instance."""
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = QwenLLM()
    return _llm_instance

