from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional

# RAGAS imports
try:
    from ragas import SingleTurnSample
    from ragas.metrics import BleuScore, NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness, RougeScore
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    # Create evaluator LLM with model gpt-3.5-turbo
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-3.5-turbo", temperature=0))
    
    # Create evaluator_embeddings with model text-embedding-3-small
    evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))
    
    # Define an instance for each metric to evaluate
    metrics = [
        ResponseRelevancy(llm=evaluator_llm, embeddings=evaluator_embeddings),
        Faithfulness(llm=evaluator_llm),
    ]
    
    # Create a single turn sample
    sample = SingleTurnSample(
        user_input=question,
        retrieved_contexts=contexts,
        response=answer
    )
    
    # Evaluate the response using the metrics
    results = {}
    try:
        for metric in metrics:
            try:
                score = metric.score_single(sample)
                metric_name = metric.__class__.__name__
                results[metric_name] = score
            except Exception as e:
                results[f"{metric.__class__.__name__}_error"] = str(e)
    except Exception as e:
        results["evaluation_error"] = str(e)
    
    # Return the evaluation results
    return results
