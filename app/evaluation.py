# RAG System Evaluation Module
# Measures generation quality using BLEU and ROUGE metrics

import pandas as pd
import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Tuple
import time
from collections import defaultdict
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

class RAGEvaluator:
    """
    Comprehensive RAG evaluation system measuring generation quality:
    - BLEU Score (n-gram precision)
    - ROUGE Scores (n-gram recall): ROUGE-1, ROUGE-2, ROUGE-L
    """
    
    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.results = []
        self.test_queries = []
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.smoothing = SmoothingFunction().method1
    
    def create_improved_test_set(self) -> List[Dict]:
        """
        Create high-quality test queries with realistic ground truth
        that match what your RAG system would actually generate
        """
        test_queries_data = [
            # Savings Category
            {
                "query": "How can I save money effectively?",
                "ground_truth": "Save money by creating a monthly budget, tracking expenses, setting up automatic transfers to savings, reducing impulse purchases, and keeping emergency funds. Start with small amounts and gradually increase savings as income grows.",
                "category": "savings",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "What are good savings habits?",
                "ground_truth": "Good savings habits include paying yourself first by saving before spending, setting specific financial goals, avoiding unnecessary debt, comparing prices before purchases, and regularly reviewing your savings progress.",
                "category": "savings",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "Why is it important to save money?",
                "ground_truth": "Saving money is important for financial security, emergency preparedness, achieving future goals, and reducing financial stress. It provides a safety net and enables you to handle unexpected expenses.",
                "category": "savings",
                "language": "English",
                "lang_code": "en"
            },
            
            # Budget Category
            {
                "query": "What is a budget and why is it important?",
                "ground_truth": "A budget is a financial plan that tracks income and expenses. It's important because it helps control spending, achieve financial goals, avoid debt, and ensure money is allocated wisely across needs, wants, and savings.",
                "category": "budget",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "How do I create my first budget?",
                "ground_truth": "To create your first budget, list all monthly income sources, categorize expenses (housing, food, transport, etc.), track spending for one month, compare income to expenses, adjust spending to match income, and review monthly.",
                "category": "budget",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "What are common budgeting mistakes?",
                "ground_truth": "Common budgeting mistakes include not tracking small expenses, being too restrictive, forgetting irregular costs, not adjusting for changes, and giving up after one bad month. Review and adjust your budget regularly.",
                "category": "budget",
                "language": "English",
                "lang_code": "en"
            },
            
            # Loans Category
            {
                "query": "What should I know before taking a loan?",
                "ground_truth": "Before taking a loan, understand the interest rate, repayment period, monthly payment amount, total cost including fees, your ability to repay, penalties for late payment, and whether the loan is necessary for your financial situation.",
                "category": "loans",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "How do interest rates work on loans?",
                "ground_truth": "Interest rates represent the cost of borrowing money, calculated as a percentage of the loan amount. Higher rates mean more expensive loans. Fixed rates stay constant while variable rates can change. Interest is paid along with principal in monthly installments.",
                "category": "loans",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "What happens if I miss a loan payment?",
                "ground_truth": "Missing loan payments can result in late fees, increased interest rates, damage to credit score, and possible legal action. Contact your lender immediately if you cannot make a payment to discuss alternatives.",
                "category": "loans",
                "language": "English",
                "lang_code": "en"
            },
            
            # Mobile Money Category
            {
                "query": "What is mobile money and how does it work?",
                "ground_truth": "Mobile money is a digital payment service that allows financial transactions through mobile phones. Users can send and receive money, pay bills, buy airtime, and make purchases without visiting a bank or using cash.",
                "category": "mobile_money",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "Is mobile money safe to use?",
                "ground_truth": "Mobile money is generally safe when using official services and following security practices: keep PINs confidential, verify transaction details before confirming, use trusted agents, monitor account activity, and report suspicious transactions immediately.",
                "category": "mobile_money",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "What are the benefits of mobile money?",
                "ground_truth": "Mobile money benefits include convenient transactions anytime anywhere, no need for bank account, lower transaction costs, quick money transfers, bill payment options, and financial inclusion for unbanked populations.",
                "category": "mobile_money",
                "language": "English",
                "lang_code": "en"
            },
            
            # Banking Category
            {
                "query": "What do I need to open a bank account?",
                "ground_truth": "To open a bank account, you typically need valid identification (ID card or passport), proof of address, initial deposit amount, and completed application forms. Requirements vary by bank and account type.",
                "category": "banking",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "What are the different types of bank accounts?",
                "ground_truth": "Common bank account types include savings accounts for earning interest on deposits, checking accounts for daily transactions, fixed deposit accounts for higher interest with locked funds, and business accounts for commercial activities.",
                "category": "banking",
                "language": "English",
                "lang_code": "en"
            },
            {
                "query": "What fees do banks charge?",
                "ground_truth": "Banks charge various fees including monthly maintenance fees, ATM withdrawal fees, overdraft fees, transfer fees, and card replacement fees. Compare fee structures when choosing a bank.",
                "category": "banking",
                "language": "English",
                "lang_code": "en"
            },
            
            # Chichewa Queries
            {
                "query": "Kodi ndingathe kusunga ndalama bwanji?",
                "ground_truth": "Sunganichani ndalama ndi kupanga pulani ya ndalama, kusiya ndalama pang'ono pang'ono, kuchepetsa kuwononga, kupanga tsiku lopeza ndalama, ndipo musunge ndalama za mwadzidzidzi.",
                "category": "savings",
                "language": "Chichewa",
                "lang_code": "ny"
            },
            {
                "query": "Kodi bajeti ndi chiyani?",
                "ground_truth": "Bajeti ndi pulani ya ndalama yomwe imathandiza kuyang'anira ndalama. Imaphatikizapo ndalama zonse zomwe mumalandira ndi zomwe mumawononga mwezi uliwonse.",
                "category": "budget",
                "language": "Chichewa",
                "lang_code": "ny"
            },
            {
                "query": "Kodi ngongole ndi chiyani?",
                "ground_truth": "Ngongole ndi ndalama zomwe munabwereka ndipo muyenera kubweza ndi chiwongoladzanja. Funsani za chiwongoladzanja, nthawi yobweza, ndi chikhalidwe cha kubweza ngongole.",
                "category": "loans",
                "language": "Chichewa",
                "lang_code": "ny"
            },
            {
                "query": "Kodi mobile money ndi chiyani?",
                "ground_truth": "Mobile money ndi njira yolipira pogwiritsa ntchito foni yanu. Mutha kutumiza ndalama, kulipira ngongole, kugula ndi kusunga ndalama popanda kupita kubanki.",
                "category": "mobile_money",
                "language": "Chichewa",
                "lang_code": "ny"
            },
            {
                "query": "Kodi ndingatsegule banki akaunti bwanji?",
                "ground_truth": "Kuti mutsegule banki akaunti, muyenera kukhala ndi ID, umboni wa malo omwe mumakhala, ndalama zoyambira, ndi kudzaza fomu. Mafunsidwe amasiyana malinga ndi banki.",
                "category": "banking",
                "language": "Chichewa",
                "lang_code": "ny"
            }
        ]
        
        print(f"✅ Created {len(test_queries_data)} test queries with realistic ground truth")
        return test_queries_data
    
    def create_test_set(self, corpus_metadata: List[Dict], samples_per_category: int = 5) -> List[Dict]:
        """
        DEPRECATED: Use create_improved_test_set() instead
        This method is kept for backward compatibility
        """
        print("⚠️  Warning: create_test_set() is deprecated. Using create_improved_test_set() instead.")
        return self.create_improved_test_set()
    
    def create_simple_test_queries(self, num_queries: int = 20) -> List[Dict]:
        """
        DEPRECATED: Use create_improved_test_set() instead
        This method is kept for backward compatibility
        """
        print("⚠️  Warning: create_simple_test_queries() is deprecated. Using create_improved_test_set() instead.")
        return self.create_improved_test_set()
    
    def calculate_bleu_score(self, generated_answer: str, ground_truth: str) -> float:
        """
        Calculate BLEU score between generated answer and ground truth
        
        Args:
            generated_answer: The answer generated by the RAG system
            ground_truth: The reference ground truth answer
            
        Returns:
            BLEU score (0 to 1)
        """
        # Tokenize the texts
        generated_tokens = generated_answer.lower().split()
        ground_truth_tokens = ground_truth.lower().split()
        
        # Calculate BLEU score with smoothing
        try:
            score = sentence_bleu(
                [ground_truth_tokens], 
                generated_tokens, 
                smoothing_function=self.smoothing
            )
            return score
        except:
            return 0.0
    
    def calculate_rouge_scores(self, generated_answer: str, ground_truth: str) -> Dict:
        """
        Calculate ROUGE-1, ROUGE-2, and ROUGE-L scores
        
        Args:
            generated_answer: The answer generated by the RAG system
            ground_truth: The reference ground truth answer
            
        Returns:
            Dictionary with ROUGE-1, ROUGE-2, ROUGE-L F1 scores
        """
        try:
            scores = self.rouge_scorer.score(ground_truth, generated_answer)
            return {
                'rouge1': scores['rouge1'].fmeasure,
                'rouge2': scores['rouge2'].fmeasure,
                'rougeL': scores['rougeL'].fmeasure
            }
        except:
            return {'rouge1': 0.0, 'rouge2': 0.0, 'rougeL': 0.0}
    
    def evaluate_generation(self, query: str, ground_truth_answer: str) -> Dict:
        """
        Evaluate a single query's generation quality
        
        Args:
            query: Query string
            ground_truth_answer: Reference answer for comparison
            
        Returns:
            Dictionary with BLEU and ROUGE metrics
        """
        start_time = time.time()
        
        try:
            # Generate answer using the RAG system - try different method names
            generated_answer = ''
            
            if hasattr(self.rag_system, 'process_query'):
                result = self.rag_system.process_query(query)
                if isinstance(result, dict):
                    generated_answer = result.get('answer', '') or result.get('response', '')
                else:
                    generated_answer = str(result)
            elif hasattr(self.rag_system, 'get_answer'):
                result = self.rag_system.get_answer(query)
                generated_answer = result if isinstance(result, str) else result.get('answer', '')
            elif hasattr(self.rag_system, 'query'):
                result = self.rag_system.query(query)
                generated_answer = result if isinstance(result, str) else result.get('answer', '')
            elif hasattr(self.rag_system, 'chat'):
                result = self.rag_system.chat(query)
                generated_answer = result if isinstance(result, str) else result.get('answer', '')
            else:
                print("❌ No recognized query method found in RAG system")
                print("   Looked for: process_query, get_answer, query, chat")
                available_methods = [m for m in dir(self.rag_system) if not m.startswith('_')]
                print(f"   Available methods: {available_methods}")
                return {
                    'generated_answer': '',
                    'bleu': 0.0,
                    'rouge1': 0.0,
                    'rouge2': 0.0,
                    'rougeL': 0.0,
                    'generation_time': 0.0,
                    'answer_length': 0
                }
            
            # DEBUG: Print what's being generated
            print(f"🔍 Query: {query}")
            print(f"🤖 Generated: {generated_answer[:100]}...")
            print(f"📚 Ground Truth: {ground_truth_answer[:100]}...")
            
            generation_time = time.time() - start_time
            
            # Calculate metrics
            bleu_score = self.calculate_bleu_score(generated_answer, ground_truth_answer)
            rouge_scores = self.calculate_rouge_scores(generated_answer, ground_truth_answer)
            
            print(f"📊 Scores - BLEU: {bleu_score:.3f}, ROUGE-L: {rouge_scores['rougeL']:.3f}")
            
            return {
                'generated_answer': generated_answer,
                'bleu': bleu_score,
                'rouge1': rouge_scores['rouge1'],
                'rouge2': rouge_scores['rouge2'],
                'rougeL': rouge_scores['rougeL'],
                'generation_time': generation_time,
                'answer_length': len(generated_answer.split())
            }
            
        except Exception as e:
            print(f"❌ Error evaluating query '{query}': {e}")
            import traceback
            traceback.print_exc()
            return {
                'generated_answer': '',
                'bleu': 0.0,
                'rouge1': 0.0,
                'rouge2': 0.0,
                'rougeL': 0.0,
                'generation_time': 0.0,
                'answer_length': 0
            }
    
    def run_diagnostic(self):
        """Run a quick diagnostic to see what's happening"""
        print("🔧 Running diagnostic...")
        
        # Test one simple query
        test_query = "How to save money?"
        ground_truth = "To save money, create a budget and reduce unnecessary spending."
        
        result = self.evaluate_generation(test_query, ground_truth)
        
        print(f"📊 Diagnostic Results:")
        print(f"   Query: {test_query}")
        print(f"   Generated: {result['generated_answer']}")
        print(f"   BLEU: {result['bleu']:.3f}")
        print(f"   ROUGE-L: {result['rougeL']:.3f}")
        print(f"   Answer Length: {result['answer_length']} words")
        
        return result
    
    def run_evaluation(self, test_cases: List[Dict] = None) -> pd.DataFrame:
        """
        Run complete evaluation on test set
        
        Args:
            test_cases: List of test cases (if None, uses improved test set)
            
        Returns:
            DataFrame with detailed results
        """
        if test_cases is None:
            print("📋 Using improved test set...")
            test_cases = self.create_improved_test_set()
        
        self.test_queries = test_cases
        results = []
        
        print(f"\n🔍 Evaluating {len(test_cases)} queries...")
        print("=" * 70)
        
        for i, test_case in enumerate(test_cases, 1):
            query = test_case['query']
            ground_truth_answer = test_case.get('ground_truth_answer') or test_case.get('ground_truth')
            
            print(f"\n[{i}/{len(test_cases)}] Evaluating: {query[:60]}...")
            
            # Evaluate generation quality
            result = self.evaluate_generation(query, ground_truth_answer)
            
            # Combine with test case info
            full_result = {
                'query': query[:80],
                'category': test_case['category'],
                'language': test_case['language'],
                'lang_code': test_case['lang_code'],
                'ground_truth_answer': ground_truth_answer[:200] + '...' if len(ground_truth_answer) > 200 else ground_truth_answer,
                'generated_answer': result['generated_answer'][:200] + '...' if len(result['generated_answer']) > 200 else result['generated_answer'],
                'bleu': result['bleu'],
                'rouge1': result['rouge1'],
                'rouge2': result['rouge2'],
                'rougeL': result['rougeL'],
                'generation_time': result['generation_time'],
                'answer_length': result['answer_length']
            }
            
            results.append(full_result)
            
            print(f"   📊 BLEU: {result['bleu']:.3f} | ROUGE-1: {result['rouge1']:.3f} | ROUGE-L: {result['rougeL']:.3f}")
        
        print("\n✅ Evaluation complete!")
        
        self.results = results
        return pd.DataFrame(results)
    
    def generate_report(self, results_df: pd.DataFrame) -> Dict:
        """
        Generate comprehensive evaluation report

        Args:
        results_df: DataFrame from run_evaluation
    
        Returns:
        Dictionary with summary statistics
        """
        report = {
            'overall': {},
            'by_language': {},
            'by_category': {},
            'problematic_queries': []
        }

        # Check if we have any results
        if len(results_df) == 0:
            # Return empty report with safe defaults
            report['overall'] = {
                'total_queries': 0,
                'bleu': 0.0,
                'rouge1': 0.0,
                'rouge2': 0.0,
                'rougeL': 0.0,
                'avg_generation_time': 0.0,
                'avg_answer_length': 0
            }
            return report

        # Overall metrics
        report['overall'] = {
            'total_queries': len(results_df),
            'bleu': results_df['bleu'].mean(),
            'rouge1': results_df['rouge1'].mean(),
            'rouge2': results_df['rouge2'].mean(),
            'rougeL': results_df['rougeL'].mean(),
            'avg_generation_time': results_df['generation_time'].mean(),
            'avg_answer_length': results_df['answer_length'].mean()
        }

        # By language
        if 'language' in results_df.columns:
            for lang in results_df['language'].unique():
                lang_df = results_df[results_df['language'] == lang]
        
                report['by_language'][lang] = {
                    'count': len(lang_df),
                    'bleu': lang_df['bleu'].mean(),
                    'rouge1': lang_df['rouge1'].mean(),
                    'rouge2': lang_df['rouge2'].mean(),
                    'rougeL': lang_df['rougeL'].mean()
                }   

        # By category (top 5)
        if 'category' in results_df.columns:
            top_categories = results_df['category'].value_counts().head(5).index
            for cat in top_categories:
                cat_df = results_df[results_df['category'] == cat]
        
                report['by_category'][cat] = {
                    'count': len(cat_df),
                    'bleu': cat_df['bleu'].mean(),
                    'rouge1': cat_df['rouge1'].mean(),
                    'rouge2': cat_df['rouge2'].mean(),
                    'rougeL': cat_df['rougeL'].mean()
                }

        # Problematic queries (low BLEU)
        low_bleu = results_df.nsmallest(10, 'bleu')
    
        for _, row in low_bleu.iterrows():
            prob_query = {
                'query': row.get('query', 'N/A'),
                'category': row.get('category', 'N/A'),
                'language': row.get('language', 'N/A'),
                'bleu': row['bleu'],
                'rougeL': row['rougeL']
            }
        
            report['problematic_queries'].append(prob_query)

        return report
    
    def print_report(self, report: Dict):
        """Print formatted evaluation report"""
        print("\n" + "=" * 70)
        print("📊 RAG SYSTEM EVALUATION REPORT (BLEU/ROUGE)")
        print("=" * 70)
        
        # Overall
        overall = report['overall']
        print(f"\n{'OVERALL PERFORMANCE':^70}")
        print("-" * 70)
        print(f"Total Queries:     {overall['total_queries']}")
        print(f"\nGeneration Quality:")
        print(f"  BLEU Score:      {overall['bleu']:.4f} ({overall['bleu']*100:.2f}%)")
        print(f"  ROUGE-1:         {overall['rouge1']:.4f} ({overall['rouge1']*100:.2f}%)")
        print(f"  ROUGE-2:         {overall['rouge2']:.4f} ({overall['rouge2']*100:.2f}%)")
        print(f"  ROUGE-L:         {overall['rougeL']:.4f} ({overall['rougeL']*100:.2f}%)")
        print(f"  Avg Time:        {overall['avg_generation_time']:.2f}s")
        print(f"  Avg Length:      {overall['avg_answer_length']:.0f} words")
        
        # By language
        print(f"\n{'PERFORMANCE BY LANGUAGE':^70}")
        print("-" * 70)
        for lang, metrics in report['by_language'].items():
            print(f"\n{lang} ({metrics['count']} queries):")
            print(f"  BLEU:     {metrics['bleu']:.4f}")
            print(f"  ROUGE-1:  {metrics['rouge1']:.4f}")
            print(f"  ROUGE-2:  {metrics['rouge2']:.4f}")
            print(f"  ROUGE-L:  {metrics['rougeL']:.4f}")
        
        # By category
        print(f"\n{'TOP CATEGORIES':^70}")
        print("-" * 70)
        for cat, metrics in list(report['by_category'].items())[:5]:
            print(f"\n{cat} ({metrics['count']} queries):")
            print(f"  BLEU:     {metrics['bleu']:.4f}")
            print(f"  ROUGE-L:  {metrics['rougeL']:.4f}")
        
        # Problematic queries
        print(f"\n{'PROBLEMATIC QUERIES (Lowest BLEU)':^70}")
        print("-" * 70)
        for i, pq in enumerate(report['problematic_queries'][:5], 1):
            print(f"\n{i}. [{pq['language']}] {pq['query']}")
            print(f"   Category: {pq['category']}")
            print(f"   BLEU: {pq['bleu']:.4f} | ROUGE-L: {pq['rougeL']:.4f}")
        
        print("\n" + "=" * 70)
    
    def save_results(self, results_df: pd.DataFrame, report: Dict, output_dir: Path):
        """Save evaluation results to files"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save detailed results
        results_path = output_dir / 'evaluation_results.csv'
        results_df.to_csv(results_path, index=False, encoding='utf-8-sig')
        print(f"💾 Saved detailed results: {results_path}")
        
        # Save summary report
        report_path = output_dir / 'evaluation_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved summary report: {report_path}")


# ============================================================================
# STANDALONE EVALUATION SCRIPT
# ============================================================================
if __name__ == "__main__":
    from pathlib import Path
    import sys
    
    # Add parent directory to path
    sys.path.append(str(Path(__file__).parent.parent))
    
    # Import RAG system - try multiple possible imports
    try:
        from app.chatbot_core import BilingualChatbot
        RAGClass = BilingualChatbot
        print("✅ Imported BilingualChatbot from chatbot_core")
    except ImportError:
        try:
            from chatbot_core import BilingualChatbot
            RAGClass = BilingualChatbot
            print("✅ Imported BilingualChatbot from chatbot_core")
        except ImportError:
            print("❌ Could not import BilingualChatbot from chatbot_core")
            print("   Please check that chatbot_core.py exists and contains BilingualChatbot class")
            sys.exit(1)
    
    print("🚀 Starting RAG System Evaluation")
    print("=" * 70)
    
    # Initialize RAG system
    print("\n1️⃣ Initializing RAG system...")
    try:
        rag_system = RAGClass()
        print("✅ RAG system instantiated")
        
        # Try to initialize if method exists
        if hasattr(rag_system, 'initialize_system'):
            if not rag_system.initialize_system():
                print("❌ Failed to initialize RAG system")
                sys.exit(1)
        elif hasattr(rag_system, 'initialize'):
            # Get Groq API key from environment if available
            import os
            groq_api_key = os.getenv('GROQ_API_KEY')
            
            if not rag_system.initialize(groq_api_key=groq_api_key):
                print("❌ Failed to initialize RAG system")
                sys.exit(1)
            print("✅ RAG system initialized successfully")
        else:
            print("ℹ️  No initialization method found, assuming ready to use")
    except Exception as e:
        print(f"❌ Error initializing RAG system: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Create evaluator
    print("\n2️⃣ Creating evaluator...")
    evaluator = RAGEvaluator(rag_system)
    
    # Run evaluation (will automatically use improved test set)
    print("\n3️⃣ Running evaluation...")
    results_df = evaluator.run_evaluation()
    
    # Generate report
    print("\n4️⃣ Generating report...")
    report = evaluator.generate_report(results_df)
    
    # Print report
    evaluator.print_report(report)
    
    # Save results
    print("\n5️⃣ Saving results...")
    output_dir = Path("..") / "evaluation_results"
    evaluator.save_results(results_df, report, output_dir)
    
    print("\n✅ Evaluation complete!")