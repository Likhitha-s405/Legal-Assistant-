import httpx

class InferenceEngine:
    def __init__(self):
        # 🔁 Make sure this matches your CURRENT ngrok URL
        self.api_url = "https://unhealed-unosmotic-tova.ngrok-free.dev/generate"

    async def generate_async(self, prompt: str, system_msg: str = ""):
        """Sends data to your fine-tuned model in Colab."""

        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    json={
                        "prompt": prompt,
                        "max_new_tokens": 300
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get("response")   # ✅ correct key

                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    return None

            except Exception as e:
                print(f"❌ Connection Error: {e}")
                return None