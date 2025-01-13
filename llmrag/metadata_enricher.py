from typing import Dict, Any, Optional
from datetime import datetime

class MetadataEnricher:
    def __init__(self, schema: str = "standard"):
        self.schema = schema
        
    def enrich(
        self,
        query: str,
        context_type: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enrich query with metadata
        
        Returns:
            Dictionary containing enriched query and metadata
        """
        metadata = {
            "timestamp": datetime.utcnow().isoformat(),
            "context_type": context_type,
            "query_type": self._classify_query(query),
            "sensitivity_level": self._assess_sensitivity(query),
            "domain_context": self._extract_domain_context(query),
        }
        
        if additional_context:
            metadata.update(additional_context)
            
        return {
            "query": query,
            "metadata": metadata
        } 

    def _classify_query(self, query: str) -> str:
        """Classify the type of query"""
        query = query.lower()
        if '?' in query:
            return "question"
        elif any(cmd in query for cmd in ['show', 'list', 'display']):
            return "retrieval"
        elif any(cmd in query for cmd in ['analyze', 'evaluate', 'assess']):
            return "analysis"
        return "general"

    def _assess_sensitivity(self, query: str) -> str:
        """Assess the sensitivity level of the query"""
        sensitive_terms = ['personal', 'private', 'confidential', 'secret']
        if any(term in query.lower() for term in sensitive_terms):
            return "high"
        return "low"

    def _extract_domain_context(self, query: str) -> str:
        """Extract domain context from query"""
        domains = {
            'healthcare': ['medical', 'health', 'patient', 'doctor'],
            'finance': ['money', 'financial', 'bank', 'investment'],
            'technology': ['tech', 'software', 'computer', 'digital']
        }
        
        query_lower = query.lower()
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        return "general" 