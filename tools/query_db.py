import sqlite3
from tabulate import tabulate
import click

@click.group()
def cli():
    """Ethical Framework Database Query Tool"""
    pass

@cli.command()
def show_tables():
    """Show all tables in the database"""
    conn = sqlite3.connect('ethical_framework.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("\nTables in database:")
    for table in tables:
        print(f"- {table[0]}")
    conn.close()

@cli.command()
@click.argument('table_name')
def show_schema(table_name):
    """Show schema for a specific table"""
    conn = sqlite3.connect('ethical_framework.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"\nSchema for {table_name}:")
    headers = ['ID', 'Name', 'Type', 'NotNull', 'DefaultValue', 'PK']
    print(tabulate(columns, headers=headers, tablefmt='psql'))
    conn.close()

@cli.command()
@click.argument('domain', default='all')
@click.option('--limit', default=5, help='Number of records to show')
def recent_evaluations(domain, limit):
    """Show recent ethical evaluations"""
    conn = sqlite3.connect('ethical_framework.db')
    cursor = conn.cursor()
    
    if domain.lower() == 'all':
        query = """
        SELECT timestamp, domain, query_text, safety_score, privacy_impact
        FROM ethical_evaluations
        ORDER BY timestamp DESC
        LIMIT ?
        """
        cursor.execute(query, (limit,))
    else:
        query = """
        SELECT timestamp, domain, query_text, safety_score, privacy_impact
        FROM ethical_evaluations
        WHERE domain = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """
        cursor.execute(query, (domain, limit))
    
    rows = cursor.fetchall()
    headers = ['Timestamp', 'Domain', 'Query', 'Safety', 'Privacy']
    print(tabulate(rows, headers=headers, tablefmt='psql'))
    conn.close()

@cli.command()
def compliance_stats():
    """Show compliance statistics"""
    conn = sqlite3.connect('ethical_framework.db')
    cursor = conn.cursor()
    query = """
    SELECT 
        domain,
        COUNT(*) as total,
        AVG(safety_score) as avg_safety,
        AVG(privacy_impact) as avg_privacy,
        AVG(bias_assessment) as avg_bias
    FROM ethical_evaluations
    GROUP BY domain
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    headers = ['Domain', 'Total', 'Avg Safety', 'Avg Privacy', 'Avg Bias']
    print(tabulate(rows, headers=headers, tablefmt='psql'))
    conn.close()

if __name__ == '__main__':
    cli() 