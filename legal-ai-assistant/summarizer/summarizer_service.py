import asyncio
from langchain_text_splitters import RecursiveCharacterTextSplitter
from inference.groq_client import InferenceEngine

class LongDocSummarizer:
    def __init__(self):
        self.engine = InferenceEngine()
        # Use a single large chunking strategy to keep context intact
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=5000, 
            chunk_overlap=500,
            separators=["\n\n", "\n", ". ", " "]
        )

    async def _safe_generate(self, prompt):
        return await self.engine.generate_async(prompt)

    async def summarize_bail(self, text: str):
    # This must match your training "prompt_style" 100%
        prompt = f"""Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
Extract legal parameters into JSON format from this bail order.

### Input:
{text[:5000]}

### Response:
"""
        return await self._safe_generate(prompt)

    async def summarize_judgement(self, text: str):
        """EXACT PROMPT FROM YOUR JUDGEMENT FINETUNING"""
        # Split into chunks if document is very long
        chunks = self.text_splitter.split_text(text)
        
        if len(chunks) == 1:
            prompt = f"""### Instruction:
Below is a legal judgement.Write a concise and accurate English summary that captures the key facts,issues, and the final decision.

### Judgement : 
{chunks[0]}

### Summary :
"""
            return await self._safe_generate(prompt)

        # For long judgements: summarize parts and combine
        print(f"[Summarizer] Processing {len(chunks)} judgment chunks...")
        summaries = []
        for chunk in chunks:
            p = f"Summarize this legal section:\n\n{chunk}\n\nSummary:"
            res = await self._safe_generate(p)
            if res: summaries.append(res)
            
        combined_text = "\n".join(summaries)
        final_prompt = f"""### Instruction:
Below is a legal judgement.Write a concise and accurate English summary that captures the key facts,issues, and the final decision.

### Judgement : 
{combined_text[:5000]}

### Summary :
"""
        return await self._safe_generate(final_prompt)

    async def summarize(self, full_text: str, doc_type: str = "judgement"):
        """Main entry point"""
        if doc_type == "bail":
            return await self.summarize_bail(full_text)
        else:
            return await self.summarize_judgement(full_text)