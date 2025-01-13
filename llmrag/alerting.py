class EthicalAlertSystem:
    def check_thresholds(self, context: Dict[str, Any]):
        """Check if any ethical thresholds are breached"""
        if context["safety_score"] < 0.8:
            self._send_alert("Safety score below threshold")
            
        if context["privacy_impact"] > 0.7:
            self._send_alert("High privacy impact detected") 