# LLMRAG - Ethical AI Query Processing Middleware

LLMRAG is a powerful middleware system that enhances AI chat assistants with ethical considerations, compliance checks, and contextual awareness. It processes queries through a comprehensive ethical framework before they reach the language model, ensuring responsible and compliant AI interactions.

## 🌟 Key Features

### 🛡️ Ethical Framework
- Real-time ethical evaluation of queries
- Domain-specific compliance checks (Healthcare, Finance, MLM, etc.)
- Bias detection and mitigation
- Privacy impact assessment
- Safety score calculation

### 📊 Metadata Enrichment
- Automatic context detection
- Query classification
- Sensitivity assessment
- Domain-specific tagging
- Audit trail generation

### 🔍 Compliance Management
- FTC compliance for MLM
- FDA guidelines for health claims
- HIPAA considerations for healthcare
- Financial regulatory compliance
- Automated compliance reporting

### 📈 Monitoring & Analytics
- Real-time ethical metrics
- Compliance tracking
- Safety trend analysis
- Domain-specific reporting
- Audit trail management

## 🚀 Quick Start

### Installation
```bash
pip install llmrag
```

### Basic Usage
```python
from llmrag import LLMRAGClient

# Initialize the client
rag_client = LLMRAGClient(
    ethical_framework="default",
    metadata_schema="standard"
)

# Process a query
result = rag_client.process_query(
    query="Your query here",
    context_type="general",
    additional_context={
        "user_role": "end_user",
        "purpose": "chat_interaction"
    }
)
```

## 🔌 Integration Guide

### 1. Basic Chat Assistant Integration
```python
from llmrag import LLMRAGClient

class YourChatAssistant:
    def __init__(self):
        self.rag_client = LLMRAGClient()
        
    async def process_message(self, user_message: str):
        # Process through ethical framework
        ethical_result = self.rag_client.process_query(
            query=user_message,
            context_type="general"
        )
        
        # Check safety thresholds
        if ethical_result['safety_metrics']['safety_score'] < 0.7:
            return {
                "status": "rejected",
                "reason": ethical_result['ethical_context'].recommendations
            }
        
        # Your existing chat logic here
        response = await self.your_chat_logic(
            message=user_message,
            context=ethical_result['response']['context']
        )
        
        return {
            "status": "success",
            "response": response,
            "safety_metrics": ethical_result['safety_metrics']
        }
```

### 2. MLM/Beauty Industry Integration
```python
from llmrag import LLMRAGClient

class MLMChatAssistant:
    def __init__(self):
        self.rag_client = LLMRAGClient(
            ethical_framework="default",
            metadata_schema="standard",
            rag_config={"domain": "mlm_beauty_wellness"}
        )
    
    async def process_message(self, message: str, user_context: dict):
        result = self.rag_client.process_query(
            query=message,
            context_type="mlm_beauty_wellness",
            additional_context={
                "user_role": user_context.get("role"),
                "purpose": user_context.get("purpose")
            }
        )
        
        # Check MLM-specific compliance
        if not result['ethical_context'].domain_specific_compliance.get("ftc_compliant"):
            return {
                "status": "compliance_warning",
                "message": "Message contains non-compliant MLM claims",
                "recommendations": result['ethical_context'].recommendations
            }
            
        return {
            "status": "success",
            "response": result['response']['response'],
            "compliance_metrics": result['ethical_context'].domain_specific_compliance
        }
```

### 3. Integration with Monitoring
```python
from llmrag import LLMRAGClient, EthicalMonitoring, EthicalAlertSystem

class MonitoredChatAssistant:
    def __init__(self):
        self.rag_client = LLMRAGClient()
        self.monitoring = EthicalMonitoring()
        self.alert_system = EthicalAlertSystem()
    
    async def process_message(self, message: str):
        # Process query
        result = self.rag_client.process_query(message)
        
        # Log evaluation
        self.monitoring.log_evaluation(result)
        
        # Check ethical thresholds
        alerts = self.alert_system.check_thresholds(result)
        if alerts:
            return {
                "status": "alert",
                "alerts": alerts,
                "recommendations": result['ethical_context'].recommendations
            }
        
        return {
            "status": "success",
            "response": result['response']['response'],
            "metrics": result['safety_metrics']
        }
```

## 📊 Monitoring & Analysis

### Database Analysis Tools
```bash
# View recent evaluations
python tools/query_db.py recent-evaluations

# Show compliance statistics
python tools/query_db.py compliance-stats

# Analyze trends
python tools/analyze_evaluations.py
```

### Using DB Browser for SQLite
```bash
# For macOS
brew install --cask db-browser-for-sqlite

# For Ubuntu
sudo apt-get install sqlitebrowser
```

## 📝 Best Practices

1. **Always Provide Context**
   - Specify domain type
   - Include user role
   - Add interaction purpose

2. **Handle Compliance Failures**
   - Implement graceful fallbacks
   - Provide clear user feedback
   - Log compliance issues

3. **Monitor Ethical Metrics**
   - Track safety scores
   - Monitor compliance rates
   - Analyze trends

4. **Regular Updates**
   - Keep ethical guidelines current
   - Update compliance rules
   - Maintain audit trails

## 🔧 Configuration

### Custom Ethical Guidelines
Create domain-specific guidelines in ethical_guidelines.json:
```json
{
    "your_domain": {
        "restricted_terms": [],
        "required_disclaimers": [],
        "min_safety_score": 0.8,
        "compliance_rules": {}
    }
}
```

## 📚 Documentation

- [API Reference](docs/api.md)
- [Ethical Framework Guide](docs/ethical_framework.md)
- [Compliance Rules](docs/compliance.md)
- [Integration Examples](docs/examples.md)

## 📄 License

MIT License - see LICENSE file for details