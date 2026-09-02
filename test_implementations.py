#!/usr/bin/env python3
"""
Quick test script to validate all implementations
"""
import sys
from pathlib import Path

# Test imports
print("Testing imports...")
try:
    from llm_client import generate_response
    print("✓ llm_client imported successfully")
except Exception as e:
    print(f"✗ Error importing llm_client: {e}")
    sys.exit(1)

try:
    from rag_client import (discover_chroma_backends, initialize_rag_system, 
                           retrieve_documents, format_context)
    print("✓ rag_client imported successfully")
except Exception as e:
    print(f"✗ Error importing rag_client: {e}")
    sys.exit(1)

try:
    from embedding_pipeline import ChromaEmbeddingPipelineTextOnly
    print("✓ embedding_pipeline imported successfully")
except Exception as e:
    print(f"✗ Error importing embedding_pipeline: {e}")
    sys.exit(1)

try:
    from ragas_evaluator import evaluate_response_quality
    print("✓ ragas_evaluator imported successfully")
except Exception as e:
    print(f"✗ Error importing ragas_evaluator: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("IMPORT TEST PASSED!")
print("="*60)

# Test function signatures
print("\nTesting function signatures...")

# Test llm_client
print("\n1. Testing llm_client.generate_response...")
try:
    import inspect
    sig = inspect.signature(generate_response)
    params = list(sig.parameters.keys())
    expected = ['openai_key', 'user_message', 'context', 'conversation_history', 'model']
    assert params == expected, f"Expected {expected}, got {params}"
    print(f"   ✓ Function signature correct: {sig}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test rag_client
print("\n2. Testing rag_client functions...")
try:
    sig = inspect.signature(discover_chroma_backends)
    print(f"   ✓ discover_chroma_backends: {sig}")
    
    sig = inspect.signature(initialize_rag_system)
    print(f"   ✓ initialize_rag_system: {sig}")
    
    sig = inspect.signature(retrieve_documents)
    print(f"   ✓ retrieve_documents: {sig}")
    
    sig = inspect.signature(format_context)
    print(f"   ✓ format_context: {sig}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test embedding_pipeline
print("\n3. Testing embedding_pipeline.ChromaEmbeddingPipelineTextOnly...")
try:
    sig = inspect.signature(ChromaEmbeddingPipelineTextOnly.__init__)
    print(f"   ✓ __init__: {sig}")
    
    methods = [
        'chunk_text', 'check_document_exists', 'update_document',
        'get_embedding', 'generate_document_id', 'process_text_file',
        'add_documents_to_collection', 'process_all_text_data',
        'get_collection_info', 'query_collection', 'get_collection_stats'
    ]
    
    for method_name in methods:
        if hasattr(ChromaEmbeddingPipelineTextOnly, method_name):
            print(f"   ✓ {method_name} exists")
        else:
            print(f"   ✗ {method_name} missing")
            sys.exit(1)
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

# Test ragas_evaluator
print("\n4. Testing ragas_evaluator.evaluate_response_quality...")
try:
    sig = inspect.signature(evaluate_response_quality)
    params = list(sig.parameters.keys())
    expected = ['question', 'answer', 'contexts']
    assert params == expected, f"Expected {expected}, got {params}"
    print(f"   ✓ Function signature correct: {sig}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print("\nNext steps:")
print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
print("2. Run embedding pipeline: python embedding_pipeline.py --help")
print("3. Launch chat app: streamlit run chat.py")
