import asyncio
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from inference.inference import InferenceEngine


class LongDocSummarizer:
    def __init__(self):
        self.engine = InferenceEngine()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=800,
            separators=["\n\n", "\n", ". ", " "]
        )

    async def _safe_generate(self, prompt):
        return await self.engine.generate_async(prompt)

    def _clean_output(self, raw: str) -> str:
        """Clean judgement output — strips echoed prompt before ### Summary :"""
        if not raw:
            return ""
        markers = [
            "### Summary :\n", "### Summary:\n",
            "### Summary : \n", "### Summary :  \n",
            "### Summary :", "### Summary:",
            "### summary :", "### summary:",
        ]
        for marker in markers:
            idx = raw.rfind(marker)
            if idx != -1:
                cleaned = raw[idx + len(marker):].strip()
                if cleaned:
                    return cleaned
        return raw.strip()

    def _clean_bail_output(self, raw: str) -> str:
        """Clean bail output — extracts JSON block after ### Response:"""
        if not raw:
            return ""
        # Strip echoed prompt — extract after last ### Response:
        for marker in ["### Response:", "### response:"]:
            idx = raw.rfind(marker)
            if idx != -1:
                cleaned = raw[idx + len(marker):].strip()
                if cleaned:
                    return cleaned
        # Fallback: extract raw JSON block if present
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return match.group(0).strip()
        return raw.strip()

    # ── BAIL ──────────────────────────────────────────────────────────────────
    async def summarize_bail(self, text: str):
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
        raw = await self._safe_generate(prompt)
        return self._clean_bail_output(raw)

    # ── JUDGEMENT ─────────────────────────────────────────────────────────────
    async def summarize_judgement(self, text: str):
        chunks = self.text_splitter.split_text(text)

        # Single chunk — send directly
        if len(chunks) == 1:
            prompt = f"""### Instruction:
Below is a legal judgement. Write a concise and accurate English summary that captures the key facts, issues, and the final decision.

### Judgement :
{chunks[0]}

### Summary :
"""
            raw = await self._safe_generate(prompt)
            return self._clean_output(raw)

        # Multiple chunks — summarise each, then merge
        case_header = self._extract_case_header(text)
        print(f"[Summarizer] Processing {len(chunks)} chunks...")

        summaries = []
        for i, chunk in enumerate(chunks):
            print(f"[Summarizer] Chunk {i+1}/{len(chunks)}...")
            chunk_with_context = chunk if i == 0 else f"{case_header}\n\n[...continued...]\n\n{chunk}"

            prompt = f"""### Instruction:
You are an expert legal annotator. Summarize this chunk of a judicial judgment accurately. Do not assume it represents the final outcome of the entire case.

Rules:
1. Identify whether this chunk covers: facts, lawyer arguments, cited precedents, or the final ruling.
2. Do not treat cited older cases as the current court's decision.
3. Do not write a definitive HELD unless this chunk explicitly states the final order.
4. Be concise.

### Judgement :
{chunk_with_context}

### Summary :
"""
            raw = await self._safe_generate(prompt)
            if raw:
                clean = self._clean_output(raw)
                print(f"[Summarizer] Chunk {i+1} done: {len(clean)} chars")
                summaries.append(clean)
            else:
                print(f"[Summarizer] Chunk {i+1} returned empty, skipping.")

        if not summaries:
            return None

        return self._deduplicate_and_merge(summaries)

    # ── HELPERS ───────────────────────────────────────────────────────────────
    def _extract_case_header(self, text: str) -> str:
        header = text[:500].strip()
        header = re.sub(r'\n{3,}', '\n\n', header)
        return header

    def _deduplicate_and_merge(self, summaries: list) -> str:
        seen = []
        result_sentences = []

        for summary in summaries:
            sentences = [s.strip() for s in summary.replace('\n', ' ').split('. ') if s.strip()]
            for sentence in sentences:
                if not sentence:
                    continue
                is_dup = any(self._overlap(sentence, s) > 0.70 for s in seen)
                if not is_dup:
                    result_sentences.append(sentence)
                    seen.append(sentence)

        paragraphs = []
        for i in range(0, len(result_sentences), 4):
            para = '. '.join(result_sentences[i:i+4])
            if not para.endswith('.'):
                para += '.'
            paragraphs.append(para)

        return '\n\n'.join(paragraphs)

    def _overlap(self, a: str, b: str) -> float:
        a_words = set(a.lower().split())
        b_words = set(b.lower().split())
        if not a_words or not b_words:
            return 0.0
        return len(a_words & b_words) / max(len(a_words), len(b_words))

    # ── ENTRY POINT ───────────────────────────────────────────────────────────
    async def summarize(self, full_text: str, doc_type: str = "judgement"):
        if doc_type == "bail":
            return await self.summarize_bail(full_text)
        else:
            return await self.summarize_judgement(full_text)