"""diff_manifest: 4 tình huống, in ra to_upsert / to_skip / to_delete.

Cách chạy:
    .venv/bin/python Learning-document/drills/2026-09-07-diff-manifest.py

⚠️ VIẾT DỰ ĐOÁN 4 DÒNG RA TRƯỚC RỒI MỚI CHẠY. Chạy trước = mất sạch giá trị bài này.
"""

from app.application.ingestion.pipeline import diff_manifest

CASES = [
    ("a. y hệt, không đổi gì",
     {"0": "h0", "1": "h1", "2": "h2"},
     {"0": "h0", "1": "h1", "2": "h2"}),

    ("b. sửa nội dung chunk giữa",
     {"0": "h0", "1": "h1", "2": "h2"},
     {"0": "h0", "1": "hX", "2": "h2"}),

    ("c. rút 3 chunk còn 2",
     {"0": "h0", "1": "h1", "2": "h2"},
     {"0": "h0", "1": "h1"}),

    ("d. thêm 3 chunk thành 4",
     {"0": "h0", "1": "h1", "2": "h2"},
     {"0": "h0", "1": "h1", "2": "h2", "3": "h3"}),
]

for label, old, new in CASES:
    to_upsert, to_skip, to_delete = diff_manifest(old, new)
    print("{:<32} upsert={:<10} skip={:<14} delete={}".format(
        label, str(sorted(to_upsert)), str(sorted(to_skip)), str(sorted(to_delete))))
