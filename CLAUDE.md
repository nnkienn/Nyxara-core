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

## 3.5 Cách trace lại 1 luồng đã học (ôn hiểu sâu / quay lại sau nghỉ)

Mẫu đã dùng thật, hiệu quả tốt: [Learning-document/notes/pipeline/00-trace-exercises.md](Learning-document/notes/pipeline/00-trace-exercises.md).

**Cách làm:**
1. Cài **≥3 lỗi/mô tả lệch thật** vào note tổng hợp đã viết trước đó — không phải lỗi ngẫu
   nhiên, phải là loại hay gặp thật: tên hàm nói dối hành vi, tính năng tưởng đã nối mà chưa,
   mô tả concurrency/thứ tự chạy sai...
2. Chia câu hỏi theo **trạm**, đúng thứ tự luồng chạy thật (vd ingest → retrieval → CRAG → API).
   Mỗi câu bắt **đọc thân hàm thật** (không tin tên hàm, không tin note) — nhiều câu phải điền
   bảng trace cụ thể (số liệu/giá trị thật), không trả lời chung chung.
3. Khi user bí: gợi ý **hướng nhìn**, không đưa đáp án — giữ đúng luật ở §2.
4. Xong 1 trạm: tự sửa note sai bằng lời mình (không copy) + ghi bug mới vào `bug-log.md` +
   cập nhật trạng thái thật vào roadmap (có thể phải hạ ✅ xuống ⏳/⚠️ nếu note cũ nói sai).

**Dấu hiệu cần dừng lại đổi cách (đã gặp thật, 2026-08-28):** nếu user vấp **liên tục** (2+ lần
mớm hỏi vẫn sai) ở **cú pháp Python cơ bản** (dict/set/list comprehension, `enumerate`, `()` gọi
hàm vs `[]` index...) chứ không phải logic RAG — đây là phản xạ cú pháp bị mai một do lâu không
tự gõ, KHÔNG phải mất hiểu biết RAG. Đừng ép tiếp tục bài trace (gây nản, chỉ ra đoán mò). Hỏi
user có muốn tạm dừng, làm 5-6 bài khởi động cú pháp ngắn, tách biệt khỏi domain RAG, hỏi
nhanh-sửa nhanh (không phải vòng 6 bước chậm) — xong quay lại bài trace, thường sẽ mượt lại ngay.

---

## 3.6 Phương pháp học 2.0 — lớp đọng lại (thêm 2026-08-28)

> Phát hiện 2026-08-28: xây được thật (66 test, note dài) nhưng user tự nhận **đọng lại yếu**.
> Gốc rễ: thiếu retrieval practice + spaced repetition, và hint-chain Socratic quá vụn (chậm,
> không test hiểu thật). Vòng 6 bước + code tay + Socratic **vẫn giữ nguyên** — thêm đúng 2 lớp
> còn thiếu. Chi tiết đủ: [LEARNING_ROADMAP.md § Phương pháp học 2.0](Learning-document/LEARNING_ROADMAP.md).

**Bắt buộc áp dụng từ 2026-09-01:**
1. **Full-attempt trước, sửa 1 lần sau.** Đưa 1 câu hỏi/tình huống đầy đủ, KHÔNG chẻ nhỏ thành
   chuỗi câu con liên tiếp. User tự làm hết khả năng → Claude sửa **1 lần**, đủ mọi lỗi cùng lúc.
2. **Giảng lại (teach-back)** cuối mỗi kỹ thuật — đóng tài liệu, tự giảng nguyên lý/WHY bằng lời
   mình (KHÔNG phải chép code từ trí nhớ — giữ đúng luật "nhớ hết code vô nghĩa").
3. **Code-tay-lại phần lõi** (chỉ công thức/vòng lặp đã đánh dấu code-tay lúc xây đầu, KHÔNG
   phải cả file/class/plumbing) — làm trong buổi ôn cách quãng, không phải mỗi buổi.
4. **Spaced repetition có lịch** — [Learning-document/notes/review-schedule.md](Learning-document/notes/review-schedule.md),
   mốc +1/+3/+7/+14 ngày. Đầu mỗi buổi check file này trước khi học mới.
5. **Checkpoint đóng-sách** — không qua kỹ thuật/phase mới nếu giảng lại (mục 2) chưa trôi chảy.
6. **(vá 2026-09-01, sau lần áp dụng đầu tiên thất bại)** Trong 1 buổi: chỉ mở **1 file/1 khái
   niệm** tại 1 thời điểm — không hỏi 1 câu ghép nhiều tầng suy luận bắt nhảy qua >1 file cùng
   lúc mà chưa giải thích. LUÔN giải thích ngữ cảnh/khái niệm bằng lời trước (được phép theo §2
   mục 1), rồi mới hỏi — kể cả khi đang dùng "full-attempt" (mục 1), câu hỏi đưa ra phải đã được
   giải thích đủ để hiểu **đang hỏi gì**, không chỉ đưa thẳng câu hỏi trần trụi.

---

## 3.7 Cách bắt đầu 1 buổi học (chốt 2026-09-01)

User chỉ cần gõ 1 trong 3 câu sau, không cần nhắc lại luật mỗi lần — Claude tự làm đúng quy trình:

- **"Bắt đầu buổi học hôm nay"** → (1) check `Learning-document/notes/review-schedule.md`, mục
  nào tới hạn (+1/+3/+7/+14) thì giảng lại (+ code-tay-lại nếu tới hạn +7/+14) trước khi học
  mới; (2) check `LEARNING_ROADMAP.md` (bảng checklist cuối file) + `00-trace-exercises.md`,
  tiếp tục đúng chỗ đang dở; (3) áp đủ Method 2.0 (§3.6).
- **"Hôm nay chỉ ôn lại"** → chỉ làm bước (1) ở trên, không học kỹ thuật mới.
- **"Dừng ở đây"** → ghi lại đúng chỗ dừng vào file trạng thái liên quan (trace-exercise/
  roadmap/review-schedule) trước khi kết thúc, để buổi sau tiếp đúng mạch không phải dò lại.

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

> ⏰ **Deadline thật (không phải tự đặt suông, cập nhật 2026-08-28):** qua Tết (~đầu 2027) user
> nghỉ việc đi phỏng vấn Senior AI Engineer. Hạn xong nội dung toàn bộ Phase 0-8 (+ Port Phase 9):
> **31/12/2026**, trễ tối đa tới **30/01/2027**. Không cắt kỹ thuật, giữ nguyên vòng 6 bước. Cam
> kết 3-4h/ngày, mỗi ngày — rủi ro số 1 là nghỉ dài, không phải phương pháp. Mốc theo tháng +
> toán chi tiết: [LEARNING_ROADMAP.md § DEADLINE ÉP TIẾN ĐỘ](Learning-document/LEARNING_ROADMAP.md).
> Lệch mốc tháng quá 3-4 ngày → dừng lại re-plan cùng nhau, đừng để trôi âm thầm.

- ✅ Phase 0 ingest (dedup · incremental · multi-store delete-aware) · Phase 1 (Embedding/Qdrant/tenant)
- ✅ Phase 2.1 Hybrid+RRF · 2.2 Rerank · 2.3 CRAG · `/ingest` + `/ask` chạy thật qua HTTP
- 🔨 **Đang làm:** trace lại toàn luồng — xem [Learning-document/notes/pipeline/00-trace-exercises.md](Learning-document/notes/pipeline/00-trace-exercises.md).
  **2026-09-02: Trạm 1 XONG HẲN** — 1a/1b/1c + teach-back qua cổng đóng-sách Method 2.0. Đã
  thêm hàng "Incremental ingest / multi-store diff" vào review-schedule (mốc +1/+3/+7/+14 từ
  2026-09-02). Chỗ user vấp nhiều nhất và đã gỡ được: `to_delete` chỉ chứa index biến mất hẳn
  (không phải hash, không phải "đổi nội dung"); manifest lưu hash để bắt "sửa tại chỗ".
  **2026-09-02 ca 1 (13-15h): Trạm 2 (Retrieval) XONG HẲN luôn** — 2a/2b/2c + teach-back.
  Đã sửa 3 chỗ sai "song song" trong `02-retrieval.md`. 2 chỗ user lẫn nặng, đã gỡ, cần ôn lại:
  (a) tưởng cross-encoder "rẻ và rộng" — thực ra ĐẮT+HẸP, không pre-compute được vì cần cả
  query lẫn doc cùng lúc; (b) tưởng cross-encoder là RRF / thuộc CRAG — thực ra RRF là toán
  thuần gộp rank, còn cross-encoder thuộc Trạm 2 và chỉ biết *xếp hạng*, không biết nói "cả đám
  đều tệ" (đó mới là việc của CRAG grader).
  **2026-09-03 ca sáng (6h15-7h15): mốc ôn +1 TRƯỢT 3/4** dù hôm trước vừa qua cổng đóng-sách
  cả 2 trạm. Cả 4 lỗi cùng loại: **lẫn 2 thứ na ná nhau**, không phải quên. Đã tạo
  [Learning-document/notes/the-phan-biet.md](Learning-document/notes/the-phan-biet.md) (8 cặp dễ
  lẫn) + chạy drill phân biệt 12 câu → **1/4 lên 11/12 trong 1 vòng**. Luật mới rút ra đã ghi vào
  [review-schedule.md](Learning-document/notes/review-schedule.md) § "Luật bổ sung".
  **Trạm 3 (CRAG) hoãn sang ca tối — không mở trạm mới trong buổi mốc ôn bị trượt.** Trạm 4 chưa đụng.
  ⚠️ **04/09 phải ôn bù** 2 kỹ thuật này trước, chưa được tính mốc +3.
  (2026-09-01 đã chèn 1 đợt drill cú pháp Python giữa buổi — xem §3.5. Cấu trúc dict-vs-list
  vẫn còn lệch lai rai khi trace, sửa 1 lần là ra.)
- ⏳ Kế tiếp: Trạm 2 (Retrieval) → Trạm 3 (CRAG) → Trạm 4 (API) → fix bug #25
  → Phase 2.4 (Metadata filter → MMR) → Phase 3 (Eval)

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
