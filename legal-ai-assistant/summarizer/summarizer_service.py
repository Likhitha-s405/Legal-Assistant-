import asyncio
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from inference.inference import InferenceEngine

class LongDocSummarizer:
    def __init__(self):
        self.engine = InferenceEngine()
        # Use a single large chunking strategy to keep context intact
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000, 
            chunk_overlap=800,
            separators=["\n\n", "\n", ". ", " "]
        )

    
    async def _safe_generate(self, prompt):
        return await self.engine.generate_async(prompt)

    async def summarize_bail(self, text: str):
    # This must match your training "prompt_style" 100%
        prompt = f"""### Instruction:
Extract legal parameters into JSON format from this bail order.

Required JSON fields:
- case_title
- court_name
- judge_name
- case_number
- applicant_name
- opposite_party
- sections_invoked
- police_station
- district
- order_date
- bail_granted
- bail_conditions

### Input:
{text[:5000]}

### Response:
"""
        return await self._safe_generate(prompt)

    async def summarize_judgement(self, text: str):
        """EXACT PROMPT FROM YOUR JUDGEMENT FINETUNING"""
        chunks = self.text_splitter.split_text(text)
        
        if len(chunks) == 1:
            prompt = f"""### Instruction:
Below is a legal judgement.Write a concise and accurate English summary that captures the key facts,issues, and the final decision.

### Judgement : 
{chunks[0]}

### Summary :
"""
            return await self._safe_generate(prompt)

        # For long judgements: summarize each chunk using the EXACT trained prompt format

        case_header = self._extract_case_header(text)
        print(f"[Summarizer] Case header: {case_header[:100]}...")

        print(f"[Summarizer] Processing {len(chunks)} judgment chunks...")
        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"[Summarizer] Sending chunk {i+1}/{len(chunks)}...")
            if i == 0:
                chunk_with_context = chunk
            else:
                chunk_with_context = f"{case_header}\n\n[...continued...]\n\n{chunk}"
            p = f"""### Instruction:
You are an expert legal annotator. You will be given a CHUNK of a larger judicial judgment. Your task is to summarize this specific chunk accurately without assuming it represents the final outcome of the entire case.

Follow these strict rules:
1. **Identify the Role of the Text:** Determine if the chunk is describing (A) The facts of the case, (B) Arguments by lawyers, (C) Historical case law/precedents cited by the judges, or (D) The final ruling of the court.
2. **Do Not Conflate Precedents with the Current Case:** If the text mentions the "Privy Council," "House of Lords," or older cases, summarize them as *citations used for reasoning*, not as the court deciding this current appeal.
3. **Avoid Premature Conclusions:** Do not write a definitive "HELD" or "Dismissed/Allowed" unless the text explicitly states the final order of the bench (usually found in the final chunk).
4. **Be Concise:** Do not repeat statutory definitions if they were explained in previous paragraphs.

### Judgement : 
{chunk}

### Summary :
"""
            res = await self._safe_generate(p)
            if res:
                clean = res.strip()
                
                print(f"[Summarizer] Chunk {i+1} done: {len(clean)} chars\n{clean}")
                summaries.append(clean)
            else:
                print(f"[Summarizer] Chunk {i+1} returned no response, skipping.")

        if not summaries:
            return None

        # Deduplicate and merge — NO second model call, just clean text joining
        merged = self._deduplicate_and_merge(summaries)
        return merged

    def _extract_case_header(self, text: str) -> str:
        """
    Extract the opening section of the judgement — typically contains
    court name, case number, parties, and judge. Used as context anchor
    for subsequent chunks so the model doesn't hallucinate case details.
        """
    # Take the first 500 chars — nearly always contains the case header
        header = text[:500].strip()
    
    # Clean up excessive whitespace
        header = re.sub(r'\n{3,}', '\n\n', header)
    
        return header

    def _deduplicate_and_merge(self, summaries: list) -> str:
        """
        Merge chunk summaries by removing repeated sentences.
        No model call — pure text dedup to avoid hallucination on foreign prompts.
        """
        seen = []
        result_sentences = []

        for summary in summaries:
            # Split on sentence boundaries
            sentences = [s.strip() for s in summary.replace('\n', ' ').split('. ') if s.strip()]
            for sentence in sentences:
                if not sentence:
                    continue
                # Skip if too similar to an already-seen sentence
                is_dup = any(self._overlap(sentence, seen_s) > 0.70 for seen_s in seen)
                if not is_dup:
                    result_sentences.append(sentence)
                    seen.append(sentence)

        # Re-join into clean paragraphs (group every ~4 sentences)
        paragraphs = []
        for i in range(0, len(result_sentences), 4):
            para = '. '.join(result_sentences[i:i+4])
            if not para.endswith('.'):
                para += '.'
            paragraphs.append(para)

        return '\n\n'.join(paragraphs)

    def _overlap(self, a: str, b: str) -> float:
        """Word-overlap ratio between two sentences."""
        a_words = set(a.lower().split())
        b_words = set(b.lower().split())
        if not a_words or not b_words:
            return 0.0
        return len(a_words & b_words) / max(len(a_words), len(b_words))

    async def summarize(self, full_text: str, doc_type: str = "judgement"):
        """Main entry point"""
        if doc_type == "bail":
            return await self.summarize_bail(full_text)
        else:
            return await self.summarize_judgement(full_text)