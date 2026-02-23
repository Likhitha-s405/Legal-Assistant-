import httpx
import asyncio

class InferenceEngine:
    def __init__(self):
        # 🟢 Use your live URL from the Colab output
        self.api_url = "https://hammocklike-apogamically-alayna.ngrok-free.dev/summarize"

    async def generate_async(self, prompt: str, system_msg: str = ""):
        """Sends data to your fine-tuned model in Colab."""
        # Use a long timeout (300s) because legal text is heavy
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(
                    self.api_url, 
                    json={"text": prompt},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    return response.json().get("summary")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    return None
            except Exception as e:
                print(f"❌ Connection Error: {e}")
                return None