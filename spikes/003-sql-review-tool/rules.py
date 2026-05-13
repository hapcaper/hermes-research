"""SQL Review Rules — detection patterns for common anti-patterns."""

from typing import List, Tuple

RuleResult = Tuple[str, str, str]  # (rule_id, severity, message)

def check_select_star(sql: str) -> List[RuleResult]:
    """Detect SELECT * patterns."""
    results = []
    import re
    # Find all SELECT * patterns (with optional column list before *)
    pattern = r'SELECT\s+\*'
    matches = re.finditer(pattern, sql, re.IGNORECASE)
    for match in matches:
        results.append((
            "SQL001",
            "🟡 MEDIUM",
            f"SELECT * detected at position {match.start()}. Prefer explicit column names for clarity and performance."
        ))
    return results

def check_missing_limit(sql: str) -> List[RuleResult]:
    """Detect SELECT without LIMIT on potentially large tables."""
    results = []
    import re
    # Simple heuristic: SELECT without LIMIT and without aggregation
    has_select = re.search(r'SELECT\s+', sql, re.IGNORECASE)
    has_limit = re.search(r'LIMIT\s+\d+', sql, re.IGNORECASE)
    has_aggregate = re.search(r'\b(COUNT|SUM|AVG|MIN|MAX|GROUP BY)\b', sql, re.IGNORECASE)
    # Exclude subqueries that likely have limits
    has_where = re.search(r'WHERE', sql, re.IGNORECASE)
    
    if has_select and not has_limit and not has_aggregate:
        # Only warn if there's a WHERE clause (indicating row filtering)
        if has_where:
            results.append((
                "SQL002",
                "🟡 MEDIUM",
                "SELECT without LIMIT clause may return unbounded rows. Consider adding LIMIT to prevent memory issues."
            ))
    return results

def check_like_prefix_wildcard(sql: str) -> List[RuleResult]:
    """Detect LIKE patterns starting with wildcard — prevents index usage."""
    results = []
    import re
    pattern = r"LIKE\s+['\"]%"
    matches = re.finditer(pattern, sql, re.IGNORECASE)
    for match in matches:
        results.append((
            "SQL003",
            "🔴 HIGH",
            f"LIKE with leading wildcard at position {match.start()} cannot use indexes. Rewrite as LIKE 'prefix%' or use FULLTEXT index."
        ))
    return results

def check_subquery_in_select(sql: str) -> List[RuleResult]:
    """Detect correlated subqueries in SELECT — often slow."""
    results = []
    import re
    # Find SELECT ... (SELECT ... FROM ...) patterns
    pattern = r'SELECT\s+.*?\([^)]*SELECT[^)]*\)'
    matches = re.finditer(pattern, sql, re.IGNORECASE | re.DOTALL)
    for match in matches:
        results.append((
            "SQL004",
            "🟡 MEDIUM",
            f"Subquery in SELECT clause at position {match.start()}. Consider JOIN or EXISTS for better performance."
        ))
    return results

def check_update_without_where(sql: str) -> List[RuleResult]:
    """Detect UPDATE without WHERE — potentially destructive."""
    results = []
    import re
    pattern = r'UPDATE\s+\w+\s+SET\s+(?!.*WHERE)'
    if re.search(pattern, sql, re.IGNORECASE):
        results.append((
            "SQL005",
            "🔴 HIGH",
            "UPDATE without WHERE clause will modify ALL rows. This is likely unintended."
        ))
    return results

def check_delete_without_where(sql: str) -> List[RuleResult]:
    """Detect DELETE without WHERE — potentially destructive."""
    results = []
    import re
    pattern = r'DELETE\s+FROM\s+\w+\s*(?!.*WHERE)'
    if re.search(pattern, sql, re.IGNORECASE):
        results.append((
            "SQL006",
            "🔴 HIGH",
            "DELETE without WHERE clause will remove ALL rows. This is likely unintended."
        ))
    return results

def check_or_condition(sql: str) -> List[RuleResult]:
    """Detect OR conditions that may cause full table scans."""
    results = []
    import re
    # OR in WHERE clause without proper indexing
    or_count = len(re.findall(r'\bOR\b', sql, re.IGNORECASE))
    if or_count >= 3:
        results.append((
            "SQL007",
            "🟡 MEDIUM",
            f"Multiple OR conditions ({or_count}) detected. Consider using IN() or UNION for better index usage."
        ))
    return results

def check_implicit_type_conversion(sql: str) -> List[RuleResult]:
    """Detect string comparison with numeric values or vice versa."""
    results = []
    import re
    # E.g., WHERE phone = 13800138000 (phone should be string)
    # Look for numeric literals compared without explicit CAST
    pattern = r'(?:WHERE|AND|OR)\s+\w+\s*=\s*\d+'
    matches = re.finditer(pattern, sql, re.IGNORECASE)
    for match in matches:
        results.append((
            "SQL008",
            "🟡 MEDIUM",
            f"Possible implicit type conversion at position {match.start()}. Ensure column types match literal types."
        ))
    return results

def run_all(sql: str) -> List[RuleResult]:
    """Run all rules on a SQL statement."""
    all_results = []
    all_results.extend(check_select_star(sql))
    all_results.extend(check_missing_limit(sql))
    all_results.extend(check_like_prefix_wildcard(sql))
    all_results.extend(check_subquery_in_select(sql))
    all_results.extend(check_update_without_where(sql))
    all_results.extend(check_delete_without_where(sql))
    all_results.extend(check_or_condition(sql))
    all_results.extend(check_implicit_type_conversion(sql))
    return all_results
