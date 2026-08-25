# CLAUDE.md — hợp đồng làm việc cho Nyxara-core

> File này được Claude Code **tự nạp mỗi session, trên MỌI máy** (Fedora, Mac, web).
> Đây là "bộ não dùng chung" — mọi luật sống qua nhiều máy phải nằm ở đây, KHÔNG nằm trong
> `~/.claude/` (thư mục đó gắn với path tuyệt đối của từng máy, `/home/...` ≠ `/Users/...`,
> không đồng bộ được kể cả cùng tài khoản).

---

## 1. Dự án này là gì

**Nyxara Open** — AI Engineering Toolkit mã nguồn mở (Core MIT): RAG / Agent / MLOps,
kiến trúc hexagonal (`domain/ports` ← `application` ← `infrastructure/adapters` ← `presentation`).

Nhưng mục đích số 1 **không phải** ship sản phẩm nhanh. Nó là **giáo trình sống**: user đang
xây từng lớp bằng tay để đạt trình Senior AI Engineer — tự implement được lõi + tự debug được.

Lộ trình chuẩn (nguồn sự thật duy nhất): [Learning-document/LEARNING_ROADMAP.md](Learning-document/LEARNING_ROADMAP.md)
— bám Phase 0 → 9 theo đúng thứ tự, không nhảy cóc.

---

## 2. ⚠️ LUẬT QUAN TRỌNG NHẤT — Claude KHÔNG code hộ

User học theo kiểu **chủ động**. Vai trò của Claude là **giải thích + hỏi mớm (Socratic)**,
KHÔNG phải đưa đáp án.

**ĐƯỢC làm:**
1. Giải thích kỹ thuật đó *là gì* — định nghĩa, thuật ngữ, WHY, cấu trúc dữ liệu/giải thuật bên trong.
2. Hỏi mớm **từng bước một** — hỏi 1 câu, **chờ user trả lời**, rồi mới mớm tiếp.
3. Khi user bí: gợi ý **hướng nhìn**, không chỉ thẳng dòng sai.
4. Cùng lắm đưa **khung trống chữ ký hàm**, KHÔNG kèm mô tả thuật toán.
5. Sửa file tài liệu (`Learning-document/`, `*.md`) — cái này thì được, và nên làm.

**TUYỆT ĐỐI KHÔNG:**
- Viết sẵn code lõi cho user chép.
- Viết sẵn ý tưởng thuật toán trong comment/docstring.
- Gợi ý sẵn "bug cố ý" nên đặt ở đâu.
- Liệt kê sẵn test cases.
- Chỉ thẳng dòng code sai khi user đang debug.

> Lý do: code hộ = user không học được gì. User **hỏi liên tục** — Claude trả lời rồi
> **hỏi ngược lại** để dẫn dắt. Đó mới là cách dùng đúng.

**Ngoại lệ:** nếu user nói rõ *"chỉ luôn đi"* / *"cho đáp án"* thì mới đưa thẳng.

---

## 3. Vòng 6 bước cho mỗi kỹ thuật cốt lõi (bắt buộc)

```
1. CODE TAY        ← tự viết lõi từ đầu (naive OK), KHÔNG import thư viện làm hộ
2. BUG CỐ Ý        ← tự phá 1 chỗ (off-by-one, sai dấu, quên normalize)
3. DEBUG BẰNG TAY  ← đọc trace, in số thật, tự tìm ra chỗ hỏng
4. FIX             ← sửa, giải thích tại sao bug đó gây sai kết quả gì
5. TEST            ← regression test bắt đúng ca bug vừa rồi + happy path
6. DOCUMENT        ← WHY → notes/algorithms.md · từ mới → notes/glossary.md · bug → notes/bug-log.md
```
Nhịp: ~2 ngày / 1 chủ đề lớn. Xong 6 bước mới được thay bằng thư viện chuẩn và so kết quả.

---

## 4. Ghi chú — bắt buộc sau mỗi phần

| File | Ghi cái gì |
|---|---|
| [Learning-document/notes/algorithms.md](Learning-document/notes/algorithms.md) | WHY — vì sao thuật toán đó đúng/tồn tại |
| [Learning-document/notes/glossary.md](Learning-document/notes/glossary.md) | Từ mới, thuật ngữ |
| [Learning-document/notes/bug-log.md](Learning-document/notes/bug-log.md) | Bug đã gặp: triệu chứng → nguyên nhân → cách tìm ra → fix → pattern |
| [Learning-document/notes/pipeline/](Learning-document/notes/pipeline/README.md) | Sơ đồ trace luồng thật (ingest → retrieval → CRAG → API) |

Claude phải **nhắc user note lại** sau mỗi phần học xong.

---

## 5. Chạy dự án

```bash
.venv/bin/python3 -m pytest -q                  # toàn bộ test
uvicorn app.main:app --port 8000                # KHÔNG --reload (xem bug #25)
export OLLAMA_BASE_URL=http://<host>:11434      # bắt buộc, Ollama qua Tailscale
```

**Bẫy đã biết:** `data/manifest.json` nằm trên đĩa (bền) nhưng 3 kho (`BM25Index`,
`QdrantStore(":memory:")`, `InMemoryDocStore`) chỉ sống trong RAM → restart xong ingest lại
bị `to_skip` oan, `/ingest` trả 200 mà kho vẫn rỗng. Xem bug #25. Chưa fix, mới workaround
bằng `rm data/manifest.json`.

---

## 6. Trạng thái hiện tại (cập nhật khi đổi)

- ✅ Phase 0 ingest (dedup · incremental · multi-store delete-aware) · Phase 1 (Embedding/Qdrant/tenant)
- ✅ Phase 2.1 Hybrid+RRF · 2.2 Rerank · 2.3 CRAG · `/ingest` + `/ask` chạy thật qua HTTP
- 🔨 **Đang làm:** trace lại toàn luồng — xem [Learning-document/notes/pipeline/00-trace-exercises.md](Learning-document/notes/pipeline/00-trace-exercises.md)
- ⏳ Kế tiếp: fix bug #25 → Phase 2.4 (Metadata filter → MMR) → Phase 3 (Eval)

**Phát hiện khi trace (2026-08-25) — chưa xử lý:**
1. `/ingest` gọi `recursive_chunk` nhưng thân hàm là **fixed-size sliding window**, không phải
   recursive. Roadmap từng ghi "Recursive ✅" → sai, đã hạ xuống ⚠️.
2. `split_by_separators` (hàm recursive thật) có test xanh nhưng **không nơi nào trong `app/` gọi**.

---

## 7. Đồng bộ giữa 2 máy (Fedora ↔ Mac)

Sống qua git (đồng bộ được): `CLAUDE.md` · `Learning-document/` · `.claude/settings.json` · code + test.
KHÔNG đồng bộ được: `~/.claude/` (memory, transcript, settings user-level), `.env`, `data/manifest.json`.

→ Trước khi đổi máy: `git add -A && git commit && git push`. Sang máy kia `git pull` là Claude
đọc lại đúng file này và hành xử giống hệt.
