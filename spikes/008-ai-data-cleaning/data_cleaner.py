#!/usr/bin/env python3
"""
Spike 008: AI Data Cleaning Tool - Technical Validation (Pure Python, no pandas)
Validates: Given messy CSV data, when cleaned, then issues are detected and fixed.
"""

import csv
import re
from datetime import datetime
from typing import List, Dict, Tuple
import sys
import io

class DataCleaner:
    def __init__(self, rows: List[Dict], headers: List[str]):
        self.rows = rows
        self.headers = headers
        self.issues = []
        self.original_count = len(rows)
    
    def detect_all_issues(self) -> List[Dict]:
        """Detect all data quality issues."""
        self.issues = []
        
        # 1. Empty cells - count missing per column
        for col in self.headers:
            empty_count = sum(1 for row in self.rows if not str(row.get(col, '')).strip())
            null_count = sum(1 for row in self.rows if row.get(col) is None or row.get(col) == '')
            total_missing = empty_count + null_count
            if total_missing > 0:
                pct = total_missing / len(self.rows) * 100
                self.issues.append({
                    'type': 'empty_cells',
                    'column': col,
                    'count': total_missing,
                    'percentage': round(pct, 1),
                    'severity': 'HIGH' if pct > 20 else 'MEDIUM' if pct > 5 else 'LOW',
                    'suggestion': f'Fill {total_missing} missing values or remove rows'
                })
        
        # 2. Phone format detection
        phone_cols = []
        for col in self.headers:
            samples = [str(row.get(col, '')).strip() for row in self.rows[:10] if row.get(col)]
            phone_patterns = [
                (r'^\d{11}$', '13812345678'),
                (r'^\d{3}-\d{4}-\d{4}$', '138-1234-5678'),
                (r'^\d{3}\s\d{4}\s\d{4}$', '138 1234 5678'),
                (r'^\+86\s?\d{11}$', '+86 13812345678'),
            ]
            formats_found = set()
            for val in samples:
                for pattern, _ in phone_patterns:
                    if re.match(pattern, val):
                        formats_found.add(pattern)
            if len(formats_found) > 1:
                phone_cols.append(col)
                self.issues.append({
                    'type': 'inconsistent_format',
                    'column': col,
                    'count': 'multiple formats',
                    'severity': 'MEDIUM',
                    'suggestion': 'Standardize phone format to 13812345678'
                })
        
        # 3. Date format detection
        date_formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y%m%d']
        for col in self.headers:
            samples = [str(row.get(col, '')).strip() for row in self.rows[:10] if row.get(col)]
            formats_found = set()
            for val in samples:
                for fmt in date_formats:
                    try:
                        datetime.strptime(val, fmt)
                        formats_found.add(fmt)
                        break
                    except:
                        pass
            if len(formats_found) > 1:
                self.issues.append({
                    'type': 'inconsistent_date',
                    'column': col,
                    'count': 'multiple formats',
                    'severity': 'HIGH',
                    'suggestion': 'Standardize date format to YYYY-MM-DD'
                })
        
        # 4. Duplicate detection (exact rows)
        seen = []
        dup_indices = []
        for i, row in enumerate(self.rows):
            row_key = tuple(sorted(row.items()))
            if row_key in seen:
                dup_indices.append(i)
            else:
                seen.append(row_key)
        if dup_indices:
            self.issues.append({
                'type': 'duplicates',
                'column': 'ALL',
                'count': len(dup_indices),
                'percentage': round(len(dup_indices) / len(self.rows) * 100, 1),
                'severity': 'HIGH',
                'suggestion': f'Remove {len(dup_indices)} duplicate rows'
            })
        
        # 5. Whitespace issues
        for col in self.headers:
            whitespace_count = sum(1 for row in self.rows 
                                   if isinstance(row.get(col), str) 
                                   and (row[col].startswith(' ') or row[col].endswith(' ')))
            if whitespace_count > 0:
                self.issues.append({
                    'type': 'whitespace',
                    'column': col,
                    'count': whitespace_count,
                    'severity': 'LOW',
                    'suggestion': 'Strip leading/trailing whitespace'
                })
        
        return self.issues
    
    def clean(self) -> List[Dict]:
        """Apply cleaning fixes."""
        rows = [row.copy() for row in self.rows]
        issue_types_fixed = {i['type'] for i in self.issues}
        
        # Remove duplicates first
        if 'duplicates' in issue_types_fixed:
            seen = []
            unique_rows = []
            for row in rows:
                row_key = tuple(sorted(row.items()))
                if row_key not in seen:
                    seen.append(row_key)
                    unique_rows.append(row)
            rows = unique_rows
        
        # Fix issues
        for issue in self.issues:
            col = issue['column']
            if issue['type'] == 'empty_cells':
                # Fill with 'Unknown' for object columns
                for row in rows:
                    if not str(row.get(col, '')).strip():
                        row[col] = 'Unknown'
            
            elif issue['type'] == 'whitespace':
                for row in rows:
                    if isinstance(row.get(col), str):
                        row[col] = row[col].strip()
            
            elif issue['type'] == 'inconsistent_format':
                # Standardize phone
                def standardize_phone(val):
                    val = re.sub(r'[\s\-\(\)]', '', str(val))
                    if val.startswith('+86'):
                        val = val[3:]
                    return val
                for row in rows:
                    if col in row and row[col]:
                        row[col] = standardize_phone(row[col])
            
            elif issue['type'] == 'inconsistent_date':
                def standardize_date(val):
                    val = str(val).strip()
                    for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%Y%m%d']:
                        try:
                            return datetime.strptime(val, fmt).strftime('%Y-%m-%d')
                        except:
                            pass
                    return val
                for row in rows:
                    if col in row and row[col]:
                        row[col] = standardize_date(row[col])
        
        return rows
    
    def generate_report(self) -> Dict:
        """Generate a quality report."""
        total_cells = len(self.rows) * len(self.headers)
        issue_count = sum(i['count'] if isinstance(i['count'], (int, float)) else 0 for i in self.issues)
        
        return {
            'original_rows': self.original_count,
            'cleaned_rows': len(self.rows),
            'total_columns': len(self.headers),
            'issue_count': len(self.issues),
            'cells_affected': issue_count,
            'quality_score': max(0, 100 - round(issue_count / max(total_cells, 1) * 100, 1)),
            'issues': self.issues
        }


def parse_csv(content: str) -> Tuple[List[Dict], List[str]]:
    """Parse CSV string into rows and headers."""
    reader = csv.DictReader(io.StringIO(content))
    headers = reader.fieldnames or []
    rows = list(reader)
    return rows, headers


def test_with_sample_data():
    """Test the data cleaner with realistic messy data."""
    print("=" * 60)
    print("SPIKE 008: AI Data Cleaning Tool — Technical Validation")
    print("=" * 60)
    
    # Sample messy CSV data - with TRUE duplicate (row 6 = exact copy of row 1)
    csv_data = """customer_id,name,phone,join_date,order_amount,email
C001,张三,13812345678,2025-01-15,1500,zhang@test.com
C002,李四 ,139-5678-1234,01/20/2025,2000, li@test.com
C003,,+86 13712345678,2025/01/30,1800,zhao@test.com
C004,赵六,13812345678,20250205,1600,sun@test.com
C005,孙七,13612345678,2025-02-10,2100,sun@test.com
C001,张三,13812345678,2025-01-15,1500,zhang@test.com"""
    
    rows, headers = parse_csv(csv_data)
    print(f"\n📊 Input data: {len(rows)} rows, {len(headers)} columns")
    print(f"Headers: {headers}")
    
    # Detect issues
    cleaner = DataCleaner(rows, headers)
    issues = cleaner.detect_all_issues()
    
    print(f"\n🔍 检测到 {len(issues)} 个数据质量问题:")
    for i, issue in enumerate(issues, 1):
        print(f"\n  [{i}] {issue['type'].upper()} @ column '{issue['column']}'")
        print(f"      Severity: {issue['severity']}")
        print(f"      Count: {issue['count']}")
        print(f"      建议: {issue['suggestion']}")
    
    # Clean
    cleaned_rows = cleaner.clean()
    
    print(f"\n✅ 清洗后数据 ({len(cleaned_rows)} rows):")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    writer.writerows(cleaned_rows)
    print(output.getvalue())
    
    # Report
    report = cleaner.generate_report()
    print(f"📋 数据质量报告:")
    print(f"    Quality Score: {report['quality_score']}/100")
    print(f"    Issues Found: {report['issue_count']}")
    print(f"    Rows before/after: {report['original_rows']}/{report['cleaned_rows']}")
    
    # Assertions
    print(f"\n🧪 Validation:")
    
    # Test 1: Empty cells filled
    names = [r['name'] for r in cleaned_rows]
    assert all(n and n.strip() for n in names if n != 'Unknown'), "No empty names should remain"
    print("  ✅ Empty cell filling works")
    
    # Test 2: Phone format standardized
    phones = [r['phone'] for r in cleaned_rows]
    for p in phones:
        assert re.match(r'^\d{11}$', str(p)), f"Phone {p} not standardized to 11 digits"
    print("  ✅ Phone standardization works")
    
    # Test 3: Date format standardized
    dates = [r['join_date'] for r in cleaned_rows]
    for d in dates:
        assert re.match(r'^\d{4}-\d{2}-\d{2}$', str(d)), f"Date {d} not standardized to YYYY-MM-DD"
    print("  ✅ Date standardization works")
    
    # Test 4: Duplicates removed
    assert len(cleaned_rows) == 5, f"Expected 5 rows after dedup, got {len(cleaned_rows)}"
    print("  ✅ Duplicate removal works")
    
    # Test 5: Whitespace trimmed
    emails = [r['email'] for r in cleaned_rows]
    for e in emails:
        assert e == e.strip(), f"Email '{e}' has whitespace"
    print("  ✅ Whitespace trimming works")
    
    print("\n" + "=" * 60)
    print("VERDICT: ALL TESTS PASSED — Technical spike VALIDATED")
    print("=" * 60)
    
    return True


if __name__ == '__main__':
    test_with_sample_data()
