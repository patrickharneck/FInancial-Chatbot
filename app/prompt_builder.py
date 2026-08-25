"""
Prompt templates and builders for different scenarios
Handles RAG prompts, general knowledge prompts, and fallbacks
"""

from typing import List, Dict


class PromptBuilder:
    """Build prompts for different scenarios"""
    
    @staticmethod
    def build_rag_prompt(query: str, context: str, lang: str) -> str:
        """
        Build prompt for RAG-based answer generation
        
        Args:
            query: User query
            context: Retrieved context
            lang: Language code ('en' or 'ny')
            
        Returns:
            Formatted prompt
        """
        if lang == 'ny':
            return f"""Ndinu wothandiza pa nkhani za ndalama ku Malawi. Perekani yankho lodziwika bwino lomwe limafotokoza kwathunthu.

MALAMULO OFUNIKA KWAMBIRI:
1. Yankha mu Chichewa chokhacho (Chichewa only - NO English words)
2. Perekani yankho LOTALIKIRAPO ndi mawu a 6-10 kapena zambiri (MINIMUM 6 sentences)
3. Fotokozani mofatsa ndipo gwiritsani ntchito ziwerengero zenizeni, chitsanzo chenicheni, ndi malangizo othandiza
4. Gawani yankho mu magawo kuti amveke bwino
5. Perekani ziwerengero za ndalama za ku Malawi (MK), mitengo, nthawi, kapena ma percentage akadali kotheka
6. MUSAYAMBE kapena KUTSATIRA ma TEMPLATE OPANDA KANTHU ochokera mu context. Ngati muli ndi nambala (1., 2., 3., 4...), muyenera kulemba mfundo zonse.
7. MUSASIYE malo opanda kanthu. Palibe nambala yomwe iyenera kukhala yopanda mawu.
8. Ngati context ili ndi ma outline opanda kanthu, MUGANIZIRE kuti ndi zolemba zokhazokha ndipo MULEMBE mfundo zatsopano, zokwanira komanso zothandiza.

CHITSANZO CHA YANKHO LABWINO (Example structure):
- Yambani ndi kufotokoza mwachidule kuti funso ndi chiyani
- Perekani mfundo zazikulu (3-4 points) ndikuzifotokoza
- Gwiritsani ntchito chitsanzo chenicheni cha ku Malawi
- Ikani malangizo othandiza pa mapeto

Nkhani Yofunika (Context) – IGNORE empty list templates:
{context}

Funso: {query}

Yankho Lotalikirapo ndi Lothandiza (detailed answer with examples and specific advice):"""
        
        else:  # English
            return f"""You are a financial literacy assistant specializing in Malawian financial systems. Provide a comprehensive, detailed, and educational answer.

CRITICAL INSTRUCTIONS - FOLLOW EXACTLY:
1. Provide a THOROUGH explanation with MINIMUM 6-10 sentences
2. Structure your answer with clear sections or paragraphs
3. Include SPECIFIC examples relevant to Malawi (banks, amounts in MK, real scenarios)
4. Use concrete numbers, percentages, timeframes, or rates where applicable
5. Make the answer actionable - tell users exactly what to do
6. Add context and background information to help users understand WHY
7. DO NOT copy empty list templates from the context.
8. If you output a numbered list, you MUST complete every item.
9. Never leave blank numbers (e.g., "2." or "3." without text).
10. Ignore empty outlines in the context and replace them with complete meaningful content.

REQUIRED ANSWER STRUCTURE:
- Opening: Brief definition or overview (1-2 sentences)
- Main explanation: Detailed breakdown with 3-4 key points (4-6 sentences)
- Practical example: Real-world scenario from Malawi with specific numbers
- Actionable advice: Step-by-step guidance or recommendations
- Closing: Summary or additional tips

Context (Note: ignore empty numbering templates):
{context}

Question: {query}

Provide a detailed, educational, well-structured answer following the format above:"""
    
    @staticmethod
    def build_general_knowledge_prompt(query: str, lang: str, context_info: str = "") -> str:
        """
        Build prompt for general knowledge-based answer
        
        Args:
            query: User query
            lang: Language code
            context_info: Optional context information
            
        Returns:
            Formatted prompt
        """
        if lang == 'ny':
            return f"""Ndinu wothandiza pa nkhani za ndalama ku Malawi. {context_info}

MALAMULO OFUNIKA KWAMBIRI - TSATIRANI MOSAMALITSA:
1. Yankha mu Chichewa chokhacho (STRICT Chichewa only - absolutely NO English words mixed in)
2. Perekani yankho LOTALIKIRAPO ndi mawu a 8-12 kapena zambiri (MINIMUM 8 sentences)
3. Gwiritsani ntchito mawu osavuta a Chichewa kuti wina aliyense amvetse
4. Fotokozani mwatsatanetsatane ndi ziwerengero zenizeni, ma percentage, ndi nthawi
5. Perekani ziwerengero ZENIZENI za ku Malawi - ndalama (MK), mitengo, chiwongola dzanja
6. MUSATENGE kapena KUTSATIRA ma template a mndandanda opanda kanthu (1., 2., 3...) ochokera mu context.
7. Ngati muli ndi nambala, YIKANI MFUNDO ZONSE - musasiye malo opanda kanthu.
8. Ngati context ili ndi ma outline opanda kanthu, muziwaletsa ndikusintha ndi zomwe zili zenizeni.

MUTU WA YANKHO (Answer structure):
• Choyamba: Fotokoza mwachidule kuti nkhani ndi yotani (2 mawu)
• Mfundo Zazikulu: Fotokoza mfundo 3-4 mwatsatanetsatane (5-7 mawu)
• Chitsanzo Chenicheni: Perekani chitsanzo cha ku Malawi ndi ndalama zenizeni (2-3 mawu)
• Malangizo: Fotokozani momwe angachitire pang'onopang'ono (2 mawu)
• Mapeto: Chitsanzo cha nthawi yaitali kapena malangizo owonjezera (1 mawu)

Pa mapeto, ikani nthawi zonse:
"📌 Chizindikiro: Yankho ili ndi lochokera ku chidziwitso chonse cha ndalama ku Malawi, osati zolemba zenizeni za bungwe lanu."

Funso: {query}

Perekani yankho lotalikirapo ndi lothandiza:"""
        
        else:  # English
            return f"""You are a highly knowledgeable financial literacy assistant specializing in Malawian financial systems and best practices. {context_info}

CRITICAL INSTRUCTIONS - YOU MUST FOLLOW THESE EXACTLY:
1. Provide COMPREHENSIVE, DETAILED answers with MINIMUM 8-12 sentences
2. Structure your response with clear sections using this format:
    • Overview (2 sentences)
    • Detailed Explanation (5-7 sentences with 3-4 key points)
    • Practical Example (2-3 sentences with specific Malawi data)
    • Step-by-step Guidance (2-3 sentences)
    • Additional Tips (1-2 sentences)

3. Use SPECIFIC MALAWIAN DATA:
    • Bank names: NBS, Standard Bank, FDH, National Bank, CDH Investment Bank
    • Real interest rates: Savings 5-8%, Fixed deposits 10-15%, Loans 18-35%, Treasury Bills 15-20%
    • Currency: Use MK (Malawi Kwacha) with realistic amounts
    • Mobile money: Mpamba (TNM), Airtel Money
    • Real organizations: Reserve Bank of Malawi (RBM), FSD Malawi, CUMO

4. Include CONCRETE NUMBERS and CALCULATIONS:
    • Show actual amounts (e.g., "If you earn MK150,000 monthly...")
    • Calculate results (e.g., "After 12 months, you'd have saved MK180,000")
    • Provide percentages and timeframes

5. Make it ACTIONABLE:
    • Give specific steps users can take TODAY
    • Name actual places/services they can access
    • Provide realistic timelines

6. Be EDUCATIONAL:
    • Explain WHY things work that way
    • Provide context and background
    • Teach principles, not just facts

7. DO NOT copy empty list templates from the context.
8. ALWAYS fill all numbered items completely — no blank numbers.
9. Replace empty contextual outlines with full, meaningful content.

Always end with:
"📌 Note: This answer is based on general financial literacy principles and Malawian financial best practices, not organization-specific documents."

Question: {query}

Provide a comprehensive, well-structured, detailed answer:"""
    
    @staticmethod
    def build_expansion_prompt(short_response: str, min_words: int) -> str:
        """
        Build prompt for expanding a short response
        
        Args:
            short_response: Original short response
            min_words: Minimum target word count
            
        Returns:
            Expansion prompt
        """
        return (
            f"Expand this financial answer to be at least {min_words} words long, "
            f"with detailed explanation and Malawi-specific examples. "
            f"Ensure all list items are fully written out with no blank numbers:\n\n{short_response}"
        )
    
    @staticmethod
    def format_context(retrieved_docs: List[Dict]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            meta = doc['metadata']
            answer = meta.get('original_answer') or meta.get('answer', '')
            score = doc.get('final_score') or doc.get('similarity_score', 0)
            source = meta.get('category', 'General')
            
            # Remove known empty list templates
            cleaned_answer = answer.replace("1.\n2.\n3.\n4.\n", "")

            context_parts.append(
                f"[Source {i}] ({source} | Relevance: {score:.2f})\n{cleaned_answer}\n"
            )
        
        return "\n".join(context_parts)