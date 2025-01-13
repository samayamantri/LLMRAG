from typing import Dict, Any, Optional
from .ethical_framework import EthicalFramework
from .metadata_enricher import MetadataEnricher
from .rag_engine import RAGEngine

class LLMRAGClient:
    def __init__(
        self,
        ethical_framework: str = "default",
        metadata_schema: str = "standard",
        rag_config: Optional[Dict[str, Any]] = None
    ):
        self.ethical_framework = EthicalFramework(framework_type=ethical_framework)
        self.metadata_enricher = MetadataEnricher(schema=metadata_schema)
        self.rag_engine = RAGEngine(config=rag_config or {})
        
    def process_query(
        self,
        query: str,
        context_type: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a query through the RAG system with ethical considerations
        
        Args:
            query: The input query
            context_type: Type of context (e.g., 'healthcare', 'finance')
            additional_context: Additional context information
            
        Returns:
            Dict containing processed response and metadata
        """
        # Step 1: Enrich with metadata
        enriched_query = self.metadata_enricher.enrich(
            query,
            context_type,
            additional_context
        )
        
        # Step 2: Apply ethical framework
        ethical_context = self.ethical_framework.evaluate(
            enriched_query,
            context_type
        )
        
        # Step 3: Process through RAG
        rag_response = self.rag_engine.process(
            enriched_query,
            ethical_context
        )
        
        # Step 4: Validate response
        validated_response = self.ethical_framework.validate_response(
            rag_response,
            ethical_context
        )
        
        return {
            "response": validated_response,
            "metadata": enriched_query["metadata"],
            "ethical_context": ethical_context,
            "safety_metrics": validated_response["safety_metrics"] if isinstance(validated_response, dict) else {}
        } 