# application/chunking

Phase 0 — Foundation & Ingestion. "Rác vào = rác ra": retrieval giỏi tới đâu cũng vô nghĩa nếu
chunk sai.

| File (sẽ build) | Kỹ thuật | Ưu tiên |
|---|---|---|
| `recursive_chunker.py` | tách theo phân cấp separator (`\n\n`→`\n`→` `), sliding window overlap | 🔴 ⭐ bắt đầu tại đây |
| `semantic_chunker.py` | cắt theo điểm gãy ngữ nghĩa (embedding distance giữa câu) | 🟡 |
| `proposition_chunker.py` | LLM tách doc thành mệnh đề atomic | 🟢 |

**Code tay trước:** đừng gọi `RecursiveCharacterTextSplitter` — tự viết `recursive_chunk(text, size, overlap)`.
