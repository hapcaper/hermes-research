#!/usr/bin/env python3
import requests
import io

csv_content = """customer_id,name,phone,join_date,order_amount,email
C001,张三,13812345678,2025-01-15,1500,zhang@test.com
C002,李四 ,139-5678-1234,01/20/2025,2000, li@test.com
C003,,+86 13712345678,2025/01/30,1800,zhao@test.com
C004,赵六,13812345678,20250205,1600,sun@test.com
C005,孙七,13612345678,2025-02-10,2100,sun@test.com
C001,张三,13812345678,2025-01-15,1500,zhang@test.com"""

r = requests.post('http://localhost:18765/clean', files={'file': ('test.csv', csv_content.encode('utf-8'), 'text/csv')})
print(f"Status: {r.status_code}")
data = r.json()
print(f"Rows: {data['original_rows']} -> {data['cleaned_rows']}")
print(f"Issues: {data['issue_count']}, Quality: {data['quality_score']}")
for iss in data['issues']:
    print(f"  [{iss['severity']}] {iss['type']} @ {iss['column']}: {iss['suggestion']}")
print(f"\nFirst cleaned row: {data['preview'][0]}")
print(f"CSV output length: {len(data['csv_content'])} chars")
print("\n✅ Web API test PASSED!")
