# 🎤 Ngân hàng câu hỏi phỏng vấn — Junior → Senior AI Engineer

> **Tạo 2026-09-06.** Mục đích: biến thứ đã xây thành thứ **nói ra được** trong phòng phỏng vấn
> (qua Tết ~đầu 2027, xem [LEARNING_ROADMAP.md § DEADLINE](./LEARNING_ROADMAP.md)).
>
> ## Cách dùng — ĐỌC TRƯỚC KHI DÙNG
>
> File này **cố ý không có đáp án**. Đáp án nằm trong note bạn đã tự viết
> ([algorithms.md](./notes/algorithms.md) · [glossary.md](./notes/glossary.md) ·
> [bug-log.md](./notes/bug-log.md) · [pipeline/](./notes/pipeline/) ·
> [the-phan-biet.md](./notes/the-phan-biet.md)), và cột **Note** trỏ thẳng tới đó.
>
> **Quy trình bắt buộc cho mỗi câu — đúng thứ tự này:**
> 1. **Đóng hết tài liệu.** Trả lời **thành tiếng** hoặc gõ ra, hết khả năng.
> 2. **Rồi mới** mở note đối chiếu.
> 3. Chấm vào cột trạng thái: ✅ trôi chảy · ⚠️ nói được nhưng lắp bắp/thiếu ý · ❌ không nói được.
> 4. Câu ❌ và ⚠️ → đưa vào vòng ôn kế tiếp. Câu ✅ → ôn lại sau 7 ngày.
>
> ⚠️ **Đọc câu hỏi rồi đọc luôn đáp án = vô ích.** Cảm giác "à đúng rồi, mình biết mà" là
> *ảo giác quen thuộc*, không phải trí nhớ. Chính nó làm hỏng 6.5 tuần đầu của dự án này.
> Phải **cố nhớ ra trước**, kể cả khi nhớ sai — nhớ sai rồi được sửa còn đọng hơn đọc đúng 10 lần.
>
> **Mức độ:** 🟢 Junior (định nghĩa, biết là gì) · 🟡 Mid (biết *vì sao*, so sánh được, biết đánh đổi)
> · 🔴 Senior (thiết kế, chẩn đoán, biết cái giá và khi nào KHÔNG dùng).
>
> **Thêm câu mới sau mỗi kỹ thuật học xong** — đó là một phần của bước 6 DOCUMENT.

---

## 1. Chunking

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 1.1 | 🟢 | Chunking là gì, vì sao không nhét cả document vào một embedding? | algorithms | ⬜ |
| 1.2 | 🟢 | `size` và `overlap` là gì? Vì sao cần overlap? | algorithms | ⬜ |
| 1.3 | 🟡 | Fixed-size vs Recursive chunking khác nhau chỗ nào? Kể một tình huống fixed-size cắt hỏng nghĩa. | 01-ingest | ⬜ |
| 1.4 | 🟡 | Recursive splitter thật gồm **2 bước**, không phải 1 — kể ra. Vì sao thiếu bước gộp thì kết quả vô dụng? | bug-log | ⬜ |
| 1.5 | 🟡 | Overlap quá lớn thì hỏng gì? Quá nhỏ thì hỏng gì? | algorithms | ⬜ |
| 1.6 | 🔴 | Chọn `size` cho một corpus mới thì căn cứ vào đâu? (gợi ý: giới hạn model, độ dài câu hỏi, chi phí) | — | ⬜ |
| 1.7 | 🔴 | Khi nào Document-based (theo heading) tốt hơn Recursive? Khi nào tệ hơn? | — | ⬜ |
| 1.8 | 🔴 | Semantic chunking đắt hơn hẳn — lấy gì để biện minh cho chi phí đó? Đo bằng chỉ số nào? | — | ⬜ |
| 1.9 | 🔴 | *(chưa học)* Document có **bảng** — vì sao flatten bảng thành text là mất nghĩa? Giữ cấu trúc bảng qua chunking bằng cách nào? | — | ⬜ |
| 1.10 | 🔴 | *(chưa học)* Header/footer/số trang lặp ở mọi trang PDF — không lọc thì hỏng gì ở tầng retrieval? | — | ⬜ |
| 1.11 | 🔴 | *(chưa học)* Khi nào cần OCR? OCR sai một chữ thì sai lan xuống những khâu nào? | — | ⬜ |

## 2. Embedding & Vector store

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 2.1 | 🟢 | Embedding là gì? Vì sao so sánh vector lại ra được "gần nghĩa"? | glossary | ⬜ |
| 2.2 | 🟢 | Cosine similarity vs Euclidean — cái nào dùng cho embedding, vì sao? | algorithms | ⬜ |
| 2.3 | 🟡 | Vì sao query và document phải dùng **cùng một** model embedding? | — | ⬜ |
| 2.4 | 🟡 | Tenant isolation làm bằng cách nào trong vector store? Nếu quên thì hậu quả là gì? | bug #13 | ⬜ |
| 2.5 | 🟡 | Vector store trả về ID nội bộ thay vì `doc_id` gốc thì hỏng ở đâu? | bug #17 | ⬜ |
| 2.6 | 🔴 | HNSW đánh đổi gì so với tìm kiếm vét cạn? Khi nào chấp nhận được, khi nào không? | — | ⬜ |
| 2.7 | 🔴 | Đổi model embedding cho hệ thống đang chạy — cần làm gì với dữ liệu cũ? Vì sao? | — | ⬜ |

## 3. Lexical search & Hybrid

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 3.1 | 🟢 | BM25 là **model AI** hay **công thức toán thuần**? | phan-biet Cặp 3 | ⬜ |
| 3.2 | 🟡 | IDF nghĩa là gì? Vì sao từ hiếm được điểm cao hơn? | algorithms | ⬜ |
| 3.3 | 🟡 | `k1` và `b` điều khiển cái gì? | algorithms | ⬜ |
| 3.4 | 🟡 | Kể một truy vấn mà **dense thua BM25**, và một truy vấn ngược lại. | algorithms | ⬜ |
| 3.5 | 🟡 | RRF gộp kết quả bằng cách nào? Vì sao dùng **thứ hạng** chứ không dùng **điểm số**? | phan-biet Cặp 5 | ⬜ |
| 3.6 | 🔴 | RRF có hằng số `k` — nó làm gì? Đặt quá nhỏ / quá lớn thì sao? | algorithms | ⬜ |
| 3.7 | 🔴 | Nếu `doc_count` của BM25 bị đếm sai, kết quả xếp hạng sai kiểu gì? Ai phát hiện ra? | bug #29 | ⬜ |

## 4. Reranking

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 4.1 | 🟡 | Bi-encoder vs Cross-encoder: cái nào **pre-compute trước** được, cái nào không? Vì sao? | phan-biet Cặp 4 | ⬜ |
| 4.2 | 🟡 | Cross-encoder **rẻ-rộng** hay **đắt-hẹp**? Nó đứng tầng mấy trong pipeline? | phan-biet Cặp 4 | ⬜ |
| 4.3 | 🟡 | Vì sao phải 2 tầng (rẻ-rộng → đắt-hẹp)? Bỏ tầng 1, cho cross-encoder chấm hết kho thì sao? | 02-retrieval | ⬜ |
| 4.4 | 🟡 | `candidate_k` và `top_k` khác nhau thế nào? Hợp đồng return giữa 2 retriever là gì? | 02-retrieval | ⬜ |
| 4.5 | 🔴 | Cross-encoder **không** làm được việc gì mà CRAG grader làm được? | phan-biet Cặp 6 | ⬜ |
| 4.6 | 🔴 | Rerank thêm độ trễ. Lấy gì để quyết định có đáng hay không? | — | ⬜ |

## 5. CRAG / agentic retrieval

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 5.1 | 🟢 | CRAG khác RAG thường ở chỗ nào? | 03-crag | ⬜ |
| 5.2 | 🟡 | `decide()` phân 3 nhánh dựa trên cái gì? Ngưỡng đặt sai thì hỏng kiểu gì? | 03-crag | ⬜ |
| 5.3 | 🟡 | Vì sao phải có `max_attempts`? Bỏ nó đi thì chuyện gì xảy ra? | 03-crag | ⬜ |
| 5.4 | 🟡 | Trong LangGraph, node **ghi** vào state bằng cách nào? `state.get()` là đọc hay ghi? | bug #26 | ⬜ |
| 5.5 | 🔴 | Node trả về một khoá **không khai báo** trong schema state → LangGraph làm gì? Vì sao lỗi này nguy hiểm? | bug #26 | ⬜ |
| 5.6 | 🔴 | Vì sao việc "nới rộng khi retry" phải nằm ở `grade_node` chứ không phải `retrieve_node`? | bug #26 | ⬜ |
| 5.7 | 🔴 | Hệ thống tự chấm `INCORRECT` 3 lần rồi vẫn trả lời — vấn đề ở đâu? Nên làm gì thay vì im lặng? | 03-crag | ⬜ |

## 6. Ingest pipeline

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 6.1 | 🟢 | Ingest gồm những bước nào, theo thứ tự? | 01-ingest | ⬜ |
| 6.2 | 🟡 | Incremental ingest là gì? Không có nó thì mỗi lần ingest lại tốn gì? | 01-ingest | ⬜ |
| 6.3 | 🟡 | Manifest lưu **hash** thay vì chỉ lưu danh sách index — bắt thêm được tình huống nào? | phan-biet Cặp 2 | ⬜ |
| 6.4 | 🟡 | Sửa nội dung một chunk tại chỗ → nó vào `to_upsert` hay `to_delete`? Còn cắt ngắn document? | phan-biet Cặp 1 | ⬜ |
| 6.5 | 🔴 | Multi-store (BM25 + vector + doc store): xoá một doc phải xoá ở đâu? Sót một chỗ thì triệu chứng là gì? | bug #20 | ⬜ |
| 6.6 | 🔴 | Manifest bền (đĩa) mà 3 kho dễ vỡ (RAM) → hỏng thế nào sau restart? Hai cách sửa và cái giá từng cách? | bug #25 | ⬜ |

## 7. API & runtime

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 7.1 | 🟢 | `lifespan` của FastAPI chạy mấy lần trong đời một process? Phần trước/sau `yield` khác nhau gì? | 04-api | ⬜ |
| 7.2 | 🟡 | Vì sao dựng model/kho trong `lifespan` thay vì trong handler? | 04-api | ⬜ |
| 7.3 | 🟡 | Handler viết `def` vs `async def` — FastAPI chạy chúng khác nhau ra sao? | Trạm 4d | ⬜ |
| 7.4 | 🔴 | Gọi một hàm **chặn** bên trong `async def` thì chuyện gì xảy ra với các request khác? Kể bằng số. | Trạm 4d | ⬜ |
| 7.5 | 🔴 | `closure` / `app.state` = trạng thái của **cả server**, `state` của request = trạng thái **một lượt chạy**. Đại lượng nào nên nằm ở đâu, và vì sao đặt nhầm là rò rỉ giữa người dùng? | bug #26, #28 | ⬜ |
| 7.6 | 🔴 | Không nhả model GPU lúc shutdown → triệu chứng gì? | bug #31 | ⬜ |

## 8. Concurrency & thread-safety

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 8.1 | 🟡 | *Lost update* là gì? Kể bằng ví dụ 2 luồng, từng bước một. | bug #29 | ⬜ |
| 8.2 | 🟡 | Vì sao `d[k] = d.get(k, 0) + 1` **không** nguyên tử? | bug #29 | ⬜ |
| 8.3 | 🔴 | Đặt `Lock` ở đâu và vì sao? Tạo `Lock` mới mỗi lần gọi hàm thì sai chỗ nào? | bug #29 | ⬜ |
| 8.4 | 🔴 | Khoá **trọn thân hàm** hay chỉ khoá dòng nguy hiểm nhất? Lý lẽ là gì? | bug #29 | ⬜ |
| 8.5 | 🔴 | Vì sao dùng `with lock:` thay vì `acquire()`/`release()` thủ công? | bug #29 | ⬜ |
| 8.6 | 🔴 | `nonlocal` để sửa biến closure — vì sao **sai** trong web server? Hậu quả với người dùng tiếp theo? | drill closure | ⬜ |

## 9. Testing & debugging

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 9.1 | 🟢 | Unit test vs integration test — khi nào cần cái nào? | bug #30 | ⬜ |
| 9.2 | 🟡 | "Assert kết quả cuối" vs "assert quá trình" — khác nhau ra sao? Cho ví dụ test **xanh giả**. | bug #26 | ⬜ |
| 9.3 | 🟡 | Vì sao phải **thấy test đỏ một lần** trước khi tin nó? Làm cách nào để kiểm chứng? | bug #26, #29 | ⬜ |
| 9.4 | 🔴 | Test cho race condition rất dễ xanh giả — vì sao, và làm sao ép nó lộ ra? | bug #29 | ⬜ |
| 9.5 | 🔴 | Chạy `pytest` theo thư mục con rồi tưởng suite xanh — chuyện gì đã xảy ra thật? | bug #27 | ⬜ |
| 9.6 | 🔴 | Đọc `NameError` / `UnboundLocalError` / `TypeError: 'NoneType' object is not callable` — mỗi cái thường do nguyên nhân gì? | bug #28, #32 | ⬜ |

## 10. Hệ thống & đánh đổi (senior)

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 10.1 | 🔴 | Vẽ toàn bộ luồng `/ask` từ HTTP request tới câu trả lời, gọi tên từng thành phần. | pipeline/ | ⬜ |
| 10.2 | 🔴 | Người dùng báo "câu trả lời sai" — bạn lần theo thứ tự nào để tìm ra khâu nào hỏng? | — | ⬜ |
| 10.3 | 🔴 | Kiến trúc hexagonal: vì sao tầng `application` **không được** import thứ của `presentation`? Vi phạm thì mất gì? | bug 06/09 | ⬜ |
| 10.4 | 🔴 | "Tên nói một đằng, thân làm một nẻo" — kể 3 ca đã gặp thật trong dự án này. | bug #26, #30 | ⬜ |
| 10.5 | 🔴 | Chi phí một truy vấn RAG nằm ở những khâu nào? Cắt khâu nào rẻ nhất mà ít mất chất lượng nhất? | — | ⬜ |
| 10.6 | ⬜ | *(Phase 3 — chưa học)* Đo chất lượng RAG bằng chỉ số gì? Recall@k, MRR, NDCG khác nhau ra sao? | — | ⬜ |
| 10.7 | 🔴 | *(chưa học)* **Khi nào KHÔNG nên dùng RAG?** Context window dài rồi — so RAG vs nhét thẳng document theo 4 trục: chất lượng · chi phí · độ trễ p95 · khả năng trích dẫn nguồn | — | ⬜ |
| 10.8 | 🔴 | *(chưa học)* Đo một **agent nhiều bước** khác đo RAG ở chỗ nào? Kể 3 chỉ số chỉ có ý nghĩa với agent | — | ⬜ |
| 10.9 | 🔴 | *(chưa học)* Agent trả lời **đúng** nhưng đi 11 bước và gọi nhầm tool 3 lần — tính là pass hay fail? Vì sao? | — | ⬜ |

---

## 📋 Nhật ký vấn đáp

Mỗi vòng ghi 1 dòng. Chỉ tính câu **đã đóng tài liệu trả lời trước**.

| Ngày | Phạm vi | ✅ | ⚠️ | ❌ | Câu sai cần nhắm lại |
|---|---|---|---|---|---|
| | | | | | |
