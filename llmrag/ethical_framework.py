from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import sqlite3  # For local storage, can be replaced with other databases
from enum import Enum
import json

class SensitivityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class DomainType(Enum):
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    LEGAL = "legal"
    EDUCATION = "education"
    GENERAL = "general"
    TECHNOLOGY = "technology"
    MLM_BEAUTY_WELLNESS = "mlm_beauty_wellness"

@dataclass
class EthicalGuideline:
    domain: DomainType
    restricted_terms: List[str]
    required_disclaimers: List[str]
    min_safety_score: float
    max_privacy_impact: float
    compliance_rules: Dict[str, Any]
    regulatory_requirements: Dict[str, Any]

@dataclass
class EthicalContext:
    bias_assessment: float
    privacy_impact: float
    safety_score: float
    transparency_level: float
    sensitivity_level: SensitivityLevel
    domain_specific_compliance: Dict[str, bool]
    recommendations: Dict[str, Any]
    audit_trail: Dict[str, Any]

class EthicalFramework:
    def __init__(
        self,
        framework_type: str = "default",
        db_path: str = "ethical_framework.db",
        guidelines_path: Optional[str] = None
    ):
        self.framework_type = framework_type
        self.db_path = db_path
        self.guidelines_path = guidelines_path or "ethical_guidelines.json"
        self.initialize_database()
        self.guidelines = self.load_ethical_guidelines()
        
    def initialize_database(self):
        """Initialize database for storing ethical evaluations and audit trail"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for storing ethical evaluations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ethical_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                query_text TEXT,
                domain TEXT,
                sensitivity_level TEXT,
                safety_score REAL,
                privacy_impact REAL,
                bias_assessment REAL,
                recommendations TEXT,
                audit_trail TEXT
            )
        ''')
        
        # Create table for compliance rules
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                rule_type TEXT,
                rule_definition TEXT,
                last_updated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    def load_ethical_guidelines(self) -> Dict[str, EthicalGuideline]:
        """Load domain-specific ethical guidelines"""
        # First load default guidelines
        guidelines = self._get_default_guidelines()
        
        try:
            # Try to load additional guidelines from file
            with open(self.guidelines_path, 'r') as f:
                guidelines_data = json.load(f)
            
            # Update guidelines with file data
            for domain, data in guidelines_data.items():
                guidelines[domain] = EthicalGuideline(
                    domain=DomainType(domain),
                    restricted_terms=data['restricted_terms'],
                    required_disclaimers=data['required_disclaimers'],
                    min_safety_score=data['min_safety_score'],
                    max_privacy_impact=data['max_privacy_impact'],
                    compliance_rules=data['compliance_rules'],
                    regulatory_requirements=data['regulatory_requirements']
                )
        except FileNotFoundError:
            # If file not found, we already have default guidelines
            pass
        except Exception as e:
            print(f"Warning: Error loading guidelines file: {e}")
            # Continue with default guidelines
            pass
        
        return guidelines

    def evaluate(self, query: Dict[str, Any], context_type: str) -> EthicalContext:
        """Comprehensive ethical evaluation"""
        try:
            domain = DomainType(context_type)
        except ValueError:
            domain = DomainType.GENERAL
        
        query_text = query['query']
        
        # Get domain-specific guidelines, fallback to general if not found
        domain_guidelines = self.guidelines.get(
            domain.value,
            self.guidelines.get('general', self.guidelines[DomainType.GENERAL.value])
        )
        
        # Perform evaluations
        bias_score = self._assess_bias(query)
        privacy_score = self._assess_privacy_impact(query)
        safety_score = self._calculate_safety_score(query)
        
        # Check domain-specific compliance
        compliance_results = self._check_domain_compliance(
            query_text,
            domain,
            domain_guidelines
        )
        
        # Generate audit trail
        audit_trail = self._generate_audit_trail(
            query_text,
            domain,
            bias_score,
            privacy_score,
            safety_score,
            compliance_results
        )
        
        # Store evaluation in database
        self._store_evaluation(
            query_text,
            domain,
            safety_score,
            privacy_score,
            bias_score,
            audit_trail
        )
        
        # Determine sensitivity level based on domain
        if domain == DomainType.MLM_BEAUTY_WELLNESS:
            sensitivity = self._assess_mlm_sensitivity(query)
        else:
            sensitivity = self._determine_sensitivity_level(query, domain)
        
        return EthicalContext(
            bias_assessment=bias_score,
            privacy_impact=privacy_score,
            safety_score=safety_score,
            transparency_level=self._assess_transparency(query),
            sensitivity_level=sensitivity,
            domain_specific_compliance=compliance_results,
            recommendations=self._generate_domain_specific_recommendations(
                query,
                context_type,
                compliance_results,
                domain
            ),
            audit_trail=audit_trail
        )

    def _check_domain_compliance(
        self,
        query_text: str,
        domain: DomainType,
        guidelines: EthicalGuideline
    ) -> Dict[str, bool]:
        """Check compliance with domain-specific rules"""
        compliance_results = {}
        
        # Check for restricted terms
        restricted_terms_found = [
            term for term in guidelines.restricted_terms
            if term.lower() in query_text.lower()
        ]
        compliance_results["no_restricted_terms"] = len(restricted_terms_found) == 0
        
        # Check regulatory compliance
        for reg, rules in guidelines.regulatory_requirements.items():
            compliance_results[f"compliant_with_{reg}"] = self._check_regulatory_compliance(
                query_text,
                rules
            )
            
        return compliance_results

    def _generate_audit_trail(
        self,
        query_text: str,
        domain: DomainType,
        bias_score: float,
        privacy_score: float,
        safety_score: float,
        compliance_results: Dict[str, bool]
    ) -> Dict[str, Any]:
        """Generate detailed audit trail"""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "query_text": query_text,
            "domain": domain.value,
            "scores": {
                "bias": bias_score,
                "privacy": privacy_score,
                "safety": safety_score
            },
            "compliance_results": compliance_results,
            "framework_version": "1.0",
            "guidelines_version": "1.0"
        }

    def _store_evaluation(
        self,
        query_text: str,
        domain: DomainType,
        safety_score: float,
        privacy_score: float,
        bias_score: float,
        audit_trail: Dict[str, Any]
    ):
        """Store evaluation results in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ethical_evaluations (
                timestamp,
                query_text,
                domain,
                safety_score,
                privacy_impact,
                bias_assessment,
                audit_trail
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.utcnow().isoformat(),
            query_text,
            domain.value,
            safety_score,
            privacy_score,
            bias_score,
            json.dumps(audit_trail)
        ))
        
        conn.commit()
        conn.close()

    def validate_response(self, response: Dict[str, Any], ethical_context: EthicalContext) -> Dict[str, Any]:
        """Validate response against ethical guidelines"""
        # Add validation metrics to the response
        response["validation"] = {
            "passed_ethical_check": True,
            "ethical_score": ethical_context.safety_score,
            "privacy_compliance": ethical_context.privacy_impact > 0.7,
            "bias_assessment": ethical_context.bias_assessment
        }
        
        return response

    def _assess_bias(self, query: Dict[str, Any]) -> float:
        """Assess potential bias in the query"""
        # Simple implementation for demonstration
        content = query['query'].lower()
        bias_triggers = ['always', 'never', 'all', 'none', 'everyone', 'nobody']
        bias_count = sum(1 for trigger in bias_triggers if trigger in content)
        return max(0.0, min(1.0, 1.0 - (bias_count * 0.2)))

    def _assess_privacy_impact(self, query: Dict[str, Any]) -> float:
        """Assess privacy implications"""
        content = query['query'].lower()
        privacy_triggers = ['personal', 'private', 'confidential', 'secret', 'data']
        privacy_mentions = sum(1 for trigger in privacy_triggers if trigger in content)
        return max(0.0, min(1.0, 1.0 - (privacy_mentions * 0.25)))

    def _calculate_safety_score(self, query: Dict[str, Any]) -> float:
        """Calculate overall safety score"""
        return (self._assess_bias(query) + self._assess_privacy_impact(query)) / 2

    def _assess_transparency(self, query: Dict[str, Any]) -> float:
        """Assess transparency level"""
        # Simple implementation
        return 0.9  # High transparency for demonstration

    def _generate_recommendations(self, query: Dict[str, Any], context_type: str) -> Dict[str, Any]:
        """Generate ethical recommendations"""
        return {
            "warnings": [],
            "suggestions": ["Consider providing more context for better results"],
            "context_specific_notes": [f"This query is being processed in {context_type} context"]
        } 

    def _check_mlm_compliance(self, query_text: str, guidelines: EthicalGuideline) -> Dict[str, bool]:
        """Check MLM-specific compliance"""
        compliance_results = {}
        
        # Check product claims
        product_claim_triggers = [
            "guarantee", "cure", "heal", "treat", "permanent", 
            "miracle", "instant", "100%"
        ]
        has_product_claims = any(trigger in query_text.lower() 
                               for trigger in product_claim_triggers)
        
        # Check income claims
        income_claim_triggers = [
            "guaranteed income", "easy money", "quit your job",
            "be your own boss", "financial freedom"
        ]
        has_income_claims = any(trigger in query_text.lower() 
                              for trigger in income_claim_triggers)
        
        # Check required disclaimers
        required_disclaimers = set(guidelines.required_disclaimers)
        present_disclaimers = set(d for d in required_disclaimers 
                                if d.lower() in query_text.lower())
        
        compliance_results.update({
            "compliant_product_claims": not has_product_claims,
            "compliant_income_claims": not has_income_claims,
            "has_required_disclaimers": len(present_disclaimers) == len(required_disclaimers),
            "ftc_compliant": self._check_ftc_compliance(query_text),
            "fda_compliant": self._check_fda_compliance(query_text)
        })
        
        return compliance_results

    def _check_ftc_compliance(self, query_text: str) -> bool:
        """Check FTC compliance for MLM communications"""
        ftc_violations = [
            "guaranteed income",
            "no risk",
            "everyone succeeds",
            "no experience needed",
            "automatic success"
        ]
        return not any(violation in query_text.lower() for violation in ftc_violations)

    def _check_fda_compliance(self, query_text: str) -> bool:
        """Check FDA compliance for beauty and wellness claims"""
        fda_violations = [
            "cures",
            "treats disease",
            "medical grade",
            "therapeutic",
            "healing properties"
        ]
        return not any(violation in query_text.lower() for violation in fda_violations)

    def _assess_mlm_sensitivity(self, query: Dict[str, Any]) -> SensitivityLevel:
        """Assess sensitivity level for MLM content"""
        content = query['query'].lower()
        
        critical_triggers = ["medical claim", "income guarantee", "cure"]
        high_triggers = ["testimonial", "before after", "income claim"]
        medium_triggers = ["business opportunity", "product benefits"]
        
        if any(trigger in content for trigger in critical_triggers):
            return SensitivityLevel.CRITICAL
        elif any(trigger in content for trigger in high_triggers):
            return SensitivityLevel.HIGH
        elif any(trigger in content for trigger in medium_triggers):
            return SensitivityLevel.MEDIUM
        return SensitivityLevel.LOW

    def _generate_mlm_recommendations(self, query: Dict[str, Any], compliance_results: Dict[str, bool]) -> Dict[str, Any]:
        """Generate MLM-specific recommendations"""
        recommendations = {
            "warnings": [],
            "suggestions": [],
            "required_actions": []
        }
        
        if not compliance_results.get("compliant_product_claims", True):
            recommendations["warnings"].append(
                "Product claims may violate FDA/FTC guidelines"
            )
            recommendations["required_actions"].append(
                "Remove or modify product efficacy claims"
            )
        
        if not compliance_results.get("compliant_income_claims", True):
            recommendations["warnings"].append(
                "Income claims may violate FTC guidelines"
            )
            recommendations["required_actions"].append(
                "Include income disclaimer and typical results"
            )
        
        if not compliance_results.get("has_required_disclaimers", True):
            recommendations["suggestions"].append(
                "Add required disclaimers to maintain compliance"
            )
        
        return recommendations 

    def _get_default_guidelines(self) -> Dict[str, EthicalGuideline]:
        """Return default guidelines if file not found"""
        return {
            "general": EthicalGuideline(
                domain=DomainType.GENERAL,
                restricted_terms=[
                    "guarantee",
                    "promise",
                    "always",
                    "never"
                ],
                required_disclaimers=[
                    "Individual results may vary",
                    "This is not professional advice"
                ],
                min_safety_score=0.7,
                max_privacy_impact=0.5,
                compliance_rules={
                    "general": {
                        "truth_verification": True,
                        "privacy_protection": True
                    }
                },
                regulatory_requirements={
                    "general": {
                        "required_terms": [],
                        "forbidden_terms": [],
                        "data_handling": ["basic_protection"]
                    }
                }
            ),
            "mlm_beauty_wellness": EthicalGuideline(
                domain=DomainType.MLM_BEAUTY_WELLNESS,
                restricted_terms=[
                    "guaranteed income",
                    "miracle cure",
                    "instant results"
                ],
                required_disclaimers=[
                    "Individual results may vary",
                    "Income claims are not typical"
                ],
                min_safety_score=0.9,
                max_privacy_impact=0.4,
                compliance_rules={
                    "ftc": {
                        "income_claims_verification": True,
                        "product_claims_verification": True
                    }
                },
                regulatory_requirements={
                    "ftc_mlm": {
                        "required_terms": ["results may vary"],
                        "forbidden_terms": ["guaranteed"],
                        "data_handling": ["verification"]
                    }
                }
            )
        } 

    def _generate_domain_specific_recommendations(
        self,
        query: Dict[str, Any],
        context_type: str,
        compliance_results: Dict[str, bool],
        domain: DomainType
    ) -> Dict[str, Any]:
        """Generate domain-specific recommendations"""
        if domain == DomainType.MLM_BEAUTY_WELLNESS:
            return self._generate_mlm_recommendations(query, compliance_results)
        return self._generate_recommendations(query, context_type)

    def _determine_sensitivity_level(self, query: Dict[str, Any], domain: DomainType) -> SensitivityLevel:
        """Determine sensitivity level based on content and domain"""
        content = query['query'].lower()
        
        # Default sensitivity triggers
        critical_triggers = ["confidential", "secret", "private", "sensitive"]
        high_triggers = ["personal", "important", "restricted"]
        medium_triggers = ["internal", "company", "business"]
        
        if any(trigger in content for trigger in critical_triggers):
            return SensitivityLevel.CRITICAL
        elif any(trigger in content for trigger in high_triggers):
            return SensitivityLevel.HIGH
        elif any(trigger in content for trigger in medium_triggers):
            return SensitivityLevel.MEDIUM
        return SensitivityLevel.LOW

    def _check_regulatory_compliance(self, query_text: str, rules: Dict[str, Any]) -> bool:
        """
        Check if query complies with regulatory requirements
        
        Args:
            query_text: The text to check
            rules: Dictionary containing regulatory rules
            
        Returns:
            bool: True if compliant, False otherwise
        """
        query_lower = query_text.lower()
        
        # Check required terms
        required_terms = rules.get('required_terms', [])
        has_required_terms = all(
            term.lower() in query_lower 
            for term in required_terms
        )
        
        # Check forbidden terms
        forbidden_terms = rules.get('forbidden_terms', [])
        has_forbidden_terms = any(
            term.lower() in query_lower 
            for term in forbidden_terms
        )
        
        # Check data handling requirements
        data_handling = rules.get('data_handling', [])
        data_handling_terms = {
            'encryption': ['encrypted', 'secure', 'protected'],
            'logging': ['logged', 'tracked', 'monitored'],
            'verification': ['verified', 'validated', 'confirmed'],
            'basic_protection': ['private', 'confidential']
        }
        
        data_handling_compliance = True
        for requirement in data_handling:
            if requirement in data_handling_terms:
                required_handling_terms = data_handling_terms[requirement]
                if not any(term in query_lower for term in required_handling_terms):
                    data_handling_compliance = False
                    break
        
        # Query is compliant if it:
        # 1. Has all required terms (or no required terms specified)
        # 2. Has no forbidden terms
        # 3. Meets data handling requirements
        return (
            (not required_terms or has_required_terms) and
            not has_forbidden_terms and
            data_handling_compliance
        )