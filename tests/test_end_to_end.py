from llmrag import LLMRAGClient
from pprint import pprint

def test_healthcare_query():
    # Initialize the client
    client = LLMRAGClient(
        ethical_framework="default",
        metadata_schema="standard",
        rag_config={"model": "test"}
    )

    # Example healthcare-related query
    query = "What are the privacy implications of sharing patient health records with AI systems?"
    
    # Process the query
    result = client.process_query(
        query=query,
        context_type="healthcare",
        additional_context={
            "user_role": "healthcare_professional",
            "purpose": "research"
        }
    )

    # Print the results
    print("\n=== Healthcare Query Test ===")
    print("\nInput Query:", query)
    print("\nProcessed Result:")
    pprint(result)
    
    return result

def test_financial_query():
    # Initialize the client
    client = LLMRAGClient(
        ethical_framework="default",
        metadata_schema="standard"
    )

    # Example financial query
    query = "How can AI be used to analyze customer banking patterns?"
    
    # Process the query
    result = client.process_query(
        query=query,
        context_type="finance",
        additional_context={
            "user_role": "financial_analyst",
            "purpose": "fraud_detection"
        }
    )

    # Print the results
    print("\n=== Financial Query Test ===")
    print("\nInput Query:", query)
    print("\nProcessed Result:")
    pprint(result)
    
    return result

def test_mlm_query():
    # Initialize the client
    client = LLMRAGClient(
        ethical_framework="default",
        metadata_schema="standard",
        rag_config={"model": "test"}
    )

    # Example MLM-related queries
    queries = [
        {
            "query": "Our skincare product guarantees permanent wrinkle removal and medical-grade results!",
            "context_type": "mlm_beauty_wellness",
            "additional_context": {
                "user_role": "distributor",
                "purpose": "product_marketing"
            }
        },
        {
            "query": "Join our team and earn $10,000 in your first month guaranteed!",
            "context_type": "mlm_beauty_wellness",
            "additional_context": {
                "user_role": "recruiter",
                "purpose": "recruitment"
            }
        }
    ]
    
    results = []
    for test_case in queries:
        # Process the query
        result = client.process_query(
            query=test_case["query"],
            context_type=test_case["context_type"],
            additional_context=test_case["additional_context"]
        )

        # Print the results
        print(f"\n=== MLM Query Test: {test_case['additional_context']['purpose']} ===")
        print("\nInput Query:", test_case["query"])
        print("\nProcessed Result:")
        pprint(result)
        results.append(result)
    
    return results

if __name__ == "__main__":
    # Run all tests
    print("\n=== Running Healthcare Test ===")
    healthcare_result = test_healthcare_query()
    
    print("\n=== Running Financial Test ===")
    financial_result = test_financial_query()
    
    print("\n=== Running MLM Tests ===")
    mlm_results = test_mlm_query()