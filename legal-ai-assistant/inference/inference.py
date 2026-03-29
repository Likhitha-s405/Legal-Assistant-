import httpx
import asyncio
import time

class InferenceEngine:
    def __init__(self):
        # 🔁 Replace with your CURRENT ngrok URL
        self.api_url = "https://unhealed-unosmotic-tova.ngrok-free.dev/generate"
        self.max_retries = 3
        self.retry_delay = 2  # seconds, will be doubled each retry

    async def generate_async(self, prompt: str, max_new_tokens: int = 300):
        """Send prompt to Colab API with retries and shorter timeout."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            for attempt in range(self.max_retries):
                try:
                    response = await client.post(
                        self.api_url,
                        json={
                            "prompt": prompt,
                            "max_new_tokens": max_new_tokens
                        }
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return result.get("response")   # expected key
                    else:
                        print(f"❌ HTTP {response.status_code}: {response.text}")
                        if attempt < self.max_retries - 1:
                            wait = self.retry_delay * (2 ** attempt)
                            print(f"Retrying in {wait}s...")
                            await asyncio.sleep(wait)
                        else:
                            return None
                except httpx.TimeoutException:
                    print(f"❌ Timeout on attempt {attempt+1}")
                    if attempt < self.max_retries - 1:
                        wait = self.retry_delay * (2 ** attempt)
                        print(f"Retrying in {wait}s...")
                        await asyncio.sleep(wait)
                    else:
                        return None
                except Exception as e:
                    print(f"❌ Connection error: {e}")
                    if attempt < self.max_retries - 1:
                        wait = self.retry_delay * (2 ** attempt)
                        print(f"Retrying in {wait}s...")
                        await asyncio.sleep(wait)
                    else:
                        return None
        return None