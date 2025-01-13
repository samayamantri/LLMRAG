import sqlite3
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class EthicalFrameworkAnalyzer:
    def __init__(self, db_path='ethical_framework.db'):
        self.db_path = db_path
        
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_recent_evaluations(self, limit=10):
        """Get most recent ethical evaluations"""
        conn = self.get_connection()
        query = """
        SELECT timestamp, query_text, domain, safety_score, privacy_impact, bias_assessment
        FROM ethical_evaluations
        ORDER BY timestamp DESC
        LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        return df
    
    def get_domain_statistics(self):
        """Get statistics by domain"""
        conn = self.get_connection()
        query = """
        SELECT 
            domain,
            COUNT(*) as total_evaluations,
            AVG(safety_score) as avg_safety,
            AVG(privacy_impact) as avg_privacy,
            AVG(bias_assessment) as avg_bias
        FROM ethical_evaluations
        GROUP BY domain
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_compliance_analysis(self):
        """Analyze compliance results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT audit_trail FROM ethical_evaluations")
        rows = cursor.fetchall()
        
        compliance_stats = {
            'total': 0,
            'compliant': 0,
            'non_compliant': 0,
            'by_domain': {}
        }
        
        for row in rows:
            audit_trail = json.loads(row[0])
            domain = audit_trail['domain']
            compliance_results = audit_trail['compliance_results']
            
            if domain not in compliance_stats['by_domain']:
                compliance_stats['by_domain'][domain] = {
                    'total': 0,
                    'compliant': 0,
                    'non_compliant': 0
                }
            
            compliance_stats['total'] += 1
            compliance_stats['by_domain'][domain]['total'] += 1
            
            # Check if all compliance checks passed
            if all(compliance_results.values()):
                compliance_stats['compliant'] += 1
                compliance_stats['by_domain'][domain]['compliant'] += 1
            else:
                compliance_stats['non_compliant'] += 1
                compliance_stats['by_domain'][domain]['non_compliant'] += 1
        
        conn.close()
        return compliance_stats
    
    def plot_safety_trends(self):
        """Plot safety score trends over time"""
        conn = self.get_connection()
        df = pd.read_sql_query("""
            SELECT timestamp, safety_score, privacy_impact, bias_assessment
            FROM ethical_evaluations
            ORDER BY timestamp
        """, conn)
        conn.close()
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['timestamp'], df['safety_score'], label='Safety Score')
        plt.plot(df['timestamp'], df['privacy_impact'], label='Privacy Impact')
        plt.plot(df['timestamp'], df['bias_assessment'], label='Bias Assessment')
        
        plt.title('Ethical Metrics Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Score')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    analyzer = EthicalFrameworkAnalyzer()
    
    print("\n=== Recent Evaluations ===")
    recent = analyzer.get_recent_evaluations()
    print(recent)
    
    print("\n=== Domain Statistics ===")
    domain_stats = analyzer.get_domain_statistics()
    print(domain_stats)
    
    print("\n=== Compliance Analysis ===")
    compliance_stats = analyzer.get_compliance_analysis()
    print(json.dumps(compliance_stats, indent=2))
    
    print("\n=== Generating Safety Trends Plot ===")
    analyzer.plot_safety_trends()

if __name__ == "__main__":
    main() 