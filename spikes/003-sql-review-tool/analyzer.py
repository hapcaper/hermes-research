"""SQL Review Analyzer — applies rules to SQL and formats output."""

import sys
import json
from rules import run_all

def analyze_sql(sql: str, verbose: bool = False) -> dict:
    """Analyze a SQL statement and return structured results."""
    results = run_all(sql)

    # Group by severity
    high = [r for r in results if '🔴 HIGH' in r[1]]
    medium = [r for r in results if '🟡 MEDIUM' in r[1]]
    low = [r for r in results if '🟢 LOW' in r[1]]

    return {
        "sql": sql.strip(),
        "total_issues": len(results),
        "high": high,
        "medium": medium,
        "low": low,
        "risk_score": len(high) * 10 + len(medium) * 3 + len(low) * 1,
        "recommendation": get_recommendation(high, medium)
    }

def get_recommendation(high: list, medium: list) -> str:
    if len(high) >= 2:
        return "🔴 DO NOT DEPLOY — Critical issues must be fixed before production"
    elif len(high) == 1:
        return "🟡 REVIEW NEEDED — Fix the high-severity issue before deploying"
    elif len(medium) >= 3:
        return "🟡 REVIEW NEEDED — Multiple medium issues detected"
    elif len(medium) > 0:
        return "🟢 MOSTLY OK — Minor issues, consider addressing before production"
    else:
        return "✅ LOOKS GOOD — No obvious issues detected"

def print_report(result: dict):
    """Print a human-readable report."""
    print("\n" + "=" * 60)
    print("SQL REVIEW REPORT")
    print("=" * 60)
    print(f"\n📝 SQL: {result['sql'][:80]}{'...' if len(result['sql']) > 80 else ''}")
    print(f"⚠️  Issues Found: {result['total_issues']}")

    if result['high']:
        print(f"\n🔴 HIGH Severity ({len(result['high'])}):")
        for rule_id, severity, msg in result['high']:
            print(f"  [{rule_id}] {msg}")

    if result['medium']:
        print(f"\n🟡 MEDIUM Severity ({len(result['medium'])}):")
        for rule_id, severity, msg in result['medium']:
            print(f"  [{rule_id}] {msg}")

    if result['low']:
        print(f"\n🟢 LOW Severity ({len(result['low'])}):")
        for rule_id, severity, msg in result['low']:
            print(f"  [{rule_id}] {msg}")

    print(f"\n💡 {result['recommendation']}")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py \"SELECT * FROM users WHERE age > 18\"")
        print("\nBuilt-in test cases:")
        test_cases = [
            "SELECT * FROM users",
            "SELECT * FROM orders WHERE id IN (SELECT id FROM items WHERE price > 100)",
            "SELECT * FROM products WHERE name LIKE '%apple%'",
            "UPDATE employees SET salary = 5000",
            "DELETE FROM logs",
            "SELECT name, email FROM users WHERE status = 1 LIMIT 10",
        ]
        print()
        for i, sql in enumerate(test_cases, 1):
            print(f"{i}. {sql}")
        print()
        sys.exit(1)

    sql = sys.argv[1]
    result = analyze_sql(sql)
    print_report(result)

    # Also print JSON for programmatic use
    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
