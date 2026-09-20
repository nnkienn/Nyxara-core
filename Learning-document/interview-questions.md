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
> 4. **Hẹn lại (từ 17/09):** ❌ → +2 ngày · ⚠️ → +5 ngày · ✅ → +14 ngày. Ghi vào cột trạng thái, vd `❌→19/09`.
>
> 🧭 **Từ 17/09 đích là AI Engineer mức Mid** ([LEARNING_ROADMAP § THIẾT KẾ LẠI](./LEARNING_ROADMAP.md)): ưu tiên 🟢 + 🟡 trước,
> 🔴 để sau. Mục 11-18 thêm 17/09 theo 5 vòng phỏng vấn thật (roadmap mục K). Câu *(lát N)* = chưa học, đừng ôn trước.
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
| 1.4 | 🟡 | Recursive splitter thật gồm **2 bước**, không phải 1 — kể ra. Vì sao thiếu bước gộp thì kết quả vô dụng? | bug-log | ⚠️ 18/09 → hẹn **23/09** *(kể đúng 2 bước, nhưng "không gộp lại được" mới là chép lại đề — thiếu HẬU QUẢ: mẩu 1 chữ → vector vô nghĩa)* |
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
| 3.5 | 🟡 | RRF gộp kết quả bằng cách nào? Vì sao dùng **thứ hạng** chứ không dùng **điểm số**? | phan-biet Cặp 5 | ⚠️ 18/09 → hẹn **23/09** *(vế WHY lần đầu trả lời sạch: "2 nhánh trả đại lượng khác nhau". Công thức lệch: nói "1/k+60", đúng là `1/(k+rank)` với `k`=60)* |
| 3.6 | 🔴 | RRF có hằng số `k` — nó làm gì? Đặt quá nhỏ / quá lớn thì sao? | algorithms | ⬜ |
| 3.7 | 🔴 | Nếu `doc_count` của BM25 bị đếm sai, kết quả xếp hạng sai kiểu gì? Ai phát hiện ra? | bug #29 | ⬜ |
| 3.8 | 🟡 | BM25 khớp theo **mặt chữ** hay theo **nghĩa**? Cho một truy vấn mà nó trả về **rỗng** dù kho có đúng tài liệu đó. | phan-biet Cặp 15 | ❌ 18/09 → hẹn **20/09** *(trả lời ngược: "BM25 chính xác về ngữ nghĩa")* |
| 3.9 | 🔴 | `tenant_id` chặn tài liệu tenant khác — ở nhánh Qdrant và nhánh BM25 là **cùng một cơ chế** không? Nêu tên file/dòng. | phan-biet Cặp 15 | ❌ 18/09 → hẹn **20/09** *(nói BM25 "search xong mới lọc"; thực ra PHÂN VÙNG bằng khoá dict, không có bước lọc nào)* |

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

## 11. Lý thuyết LLM *(🟢 đọc hiểu — slot công ty 10-11/2026)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 11.1 | 🟢 | LLM sinh chữ thế nào? "Dự đoán token tiếp theo" nghĩa là gì? | — | ⬜ |
| 11.2 | 🟢 | Token là gì? Vì sao tiếng Việt thường tốn nhiều token hơn tiếng Anh cho cùng một câu? | — | ⬜ |
| 11.3 | 🟡 | BPE, WordPiece, tokenization theo ký tự — khác nhau và đánh đổi gì? | — | ⬜ |
| 11.4 | 🟢 | Temperature và top-p là gì? Tăng/giảm thì đầu ra đổi thế nào? Khi nào đặt temperature = 0? | — | ⬜ |
| 11.5 | 🟢 | Context window là gì? Vượt quá thì chuyện gì xảy ra? Tài liệu dài thì xử lý thế nào? | — | ⬜ |
| 11.6 | 🟡 | Self-attention làm gì? Q, K, V là gì? Vì sao chi phí tăng theo bình phương độ dài? | — | ⬜ |
| 11.7 | 🟡 | Encoder-only, decoder-only, encoder-decoder khác nhau thế nào? Mỗi loại dùng cho việc gì? (gợi ý nối: bi-encoder BGE vs LLM sinh chữ) | — | ⬜ |
| 11.8 | 🟡 | KV cache là gì? Vì sao nó làm suy luận nhanh hơn, và đổi lại tốn gì? | — | ⬜ |
| 11.9 | 🟡 | Time to first token (TTFT) và tokens/giây khác nhau thế nào? Người dùng cảm nhận cái nào? | — | ⬜ |
| 11.10 | 🔴 | Mixture of Experts (MoE) tiết kiệm ở đâu? | — | ⬜ |

## 12. Evaluation *(lát 1 + 3)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 12.1 | 🟢 | Hit@k, Recall@k, MRR, NDCG — mỗi cái đo gì? *(lát 1)* | — | ⬜ |
| 12.2 | 🟡 | Dựng golden dataset thế nào? Vì sao phải versioned, và sửa lén golden thì hỏng gì? *(lát 1)* | — | ⬜ |
| 12.3 | 🟡 | Đánh giá một chatbot/RAG thế nào — tách tầng retrieval và tầng generation ra sao? *(lát 1, 3)* | — | ⬜ |
| 12.4 | 🟡 | LLM-as-judge là gì? Judge lệch theo những kiểu nào? Làm sao biết judge đáng tin? *(lát 3)* | — | ⬜ |
| 12.5 | 🟡 | Faithfulness đo gì? Khác answer correctness chỗ nào? *(lát 3)* | — | ⬜ |
| 12.6 | 🟡 | Phát hiện và giảm bịa (hallucination) bằng những cách nào? *(lát 3)* | — | ⬜ |
| 12.7 | 🔴 | Chatbot trả lời **tự tin nhưng sai** — debug theo thứ tự nào? *(lát 3)* | — | ⬜ |
| 12.8 | 🔴 | A/B hai cấu hình retrieval: vì sao chỉ đổi **một** biến? Chênh 2% thì đã tin được chưa? *(lát 1)* | — | ⬜ |
| 12.9 | 🔴 | Retrieval đang recall 60% — chẩn đoán thế nào? *(lát 1-2)* | — | ⬜ |

## 13. Agent & tool use *(lát 5)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 13.1 | 🟢 | Hệ thống thế nào thì gọi là "agentic"? Ngoài LLM, agent cần những thành phần gì? | — | ⬜ |
| 13.2 | 🟡 | Agent quyết định gọi tool nào bằng cách nào? Structured output giúp gì? | — | ⬜ |
| 13.3 | 🟡 | **Khi nào agent là lựa chọn SAI?** | — | ⬜ |
| 13.4 | 🟡 | Chặn vòng lặp vô hạn / đặt điều kiện dừng thế nào? *(nối: van `max_attempts` của CRAG)* | bug #26 | ⬜ |
| 13.5 | 🟡 | Tool lỗi thì retry thế nào? Idempotency là gì và vì sao cần khi retry? | — | ⬜ |
| 13.6 | 🔴 | Rủi ro bảo mật lớn nhất của agent có gọi tool? Sandbox tool thế nào? | — | ⬜ |
| 13.7 | 🟡 | MCP là gì, giải quyết vấn đề gì so với tự định nghĩa tool trong từng app? | — | ⬜ |
| 13.8 | 🔴 | Theo dõi agent chạy trên production bằng gì (trace từng bước)? | — | ⬜ |

## 14. Chi phí & độ trễ *(lát 6)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 14.1 | 🟢 | Giảm chi phí token bằng những cách nào? | — | ⬜ |
| 14.2 | 🟡 | Giảm độ trễ app LLM bằng những cách nào? Streaming giúp gì? | — | ⬜ |
| 14.3 | 🟡 | Đo từng lần gọi LLM trong pipeline nhiều bước để tìm nút cổ chai thế nào? p50 vs p95? | — | ⬜ |
| 14.4 | 🟡 | Caching thường vs semantic caching — ngưỡng tương đồng đặt sai thì hỏng gì? Prompt caching là gì? | — | ⬜ |
| 14.5 | 🟡 | Khi nào model nhỏ/mã nguồn mở là "đủ tốt"? Model routing (tiering) là gì? | — | ⬜ |
| 14.6 | 🔴 | Ước ngân sách: RAG cho 300.000 văn bản pháp luật, 10.000 câu hỏi/ngày — nêu từng khoản và giả định. | — | ⬜ |
| 14.7 | 🔴 | App nhận 1 triệu query/ngày — tối ưu chi phí theo thứ tự nào? | — | ⬜ |

## 15. Guardrails & monitoring *(lát 3, 6)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 15.1 | 🟢 | Prompt injection là gì? Khác jailbreak thế nào? | — | ⬜ |
| 15.2 | 🟡 | Chống prompt injection bằng những lớp nào? Vì sao không có lớp nào đủ một mình? | — | ⬜ |
| 15.3 | 🟡 | Xử lý PII trong prompt và trong log thế nào? | — | ⬜ |
| 15.4 | 🟡 | Đo tỉ lệ bịa **trên production** (không có đáp án chuẩn) bằng cách nào? | — | ⬜ |
| 15.5 | 🔴 | Thử model/prompt mới trước khi rollout hết thế nào? | — | ⬜ |

## 16. Fine-tune *(🟢 nói được)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 16.1 | 🟡 | Khi nào fine-tune, khi nào prompt, khi nào RAG? Cho ví dụ từng loại. | — | ⬜ |
| 16.2 | 🟢 | LoRA / PEFT là gì? Vì sao train được trên GPU nhỏ? | — | ⬜ |
| 16.3 | 🟢 | Quantization là gì? Đánh đổi kích thước — tốc độ — độ chính xác? | — | ⬜ |
| 16.4 | 🟡 | Instruction tuning khác pre-training thế nào? | — | ⬜ |
| 16.5 | 🔴 | RLHF gồm những bước gì? DPO đơn giản hoá chỗ nào? | — | ⬜ |

## 17. System design AI *(nói 45' — tháng 12 → 01)*

> Mỗi đề: tự nói theo 4 bước **làm rõ yêu cầu → kiến trúc tổng → đi sâu 1 khối → đánh đổi & điểm hỏng**, rồi Claude chấm.

| # | Mức | Đề | Note | Trạng thái |
|---|---|---|---|---|
| 17.1 | 🟡 | Thiết kế hệ thống hỏi đáp tài liệu (RAG) cho một công ty. | — | ⬜ |
| 17.2 | 🟡 | Thiết kế trợ lý tra cứu pháp luật có trích dẫn Điều/Khoản, không được trả lời bằng điều đã hết hiệu lực. | — | ⬜ |
| 17.3 | 🔴 | Scale RAG từ 60K lên 10 triệu văn bản — cái gì gãy trước? | — | ⬜ |
| 17.4 | 🔴 | Thiết kế workflow agent nhiều bước (vd xử lý ticket hỗ trợ: phân loại → soạn trả lời → đẩy người). | — | ⬜ |
| 17.5 | 🔴 | Thiết kế hệ thống xử lý 10.000 file tải lên/tháng (PDF, ảnh scan) để trích thông tin. | — | ⬜ |
| 17.6 | 🔴 | Chat AI cho 1 triệu người dùng/ngày — đánh đổi chất lượng, chi phí, độ trễ. | — | ⬜ |

## 18. Trình bày project & hành vi *(11/2026 → 01/2027, cả tiếng Việt lẫn tiếng Anh)*

| # | Mức | Câu hỏi | Note | Trạng thái |
|---|---|---|---|---|
| 18.1 | 🟢 | Giới thiệu Nyxara-core trong **60 giây**: bài toán → kiến trúc → một con số. | — | ⬜ |
| 18.2 | 🟡 | Đi qua project từ đầu tới cuối. Vì sao chọn hybrid + rerank + CRAG thay vì chỉ vector search? | pipeline/ | ⬜ |
| 18.3 | 🟡 | Bug khó nhất bạn từng tìm ra — triệu chứng, cách lần ra, cách chặn tái phát. | bug-log | ⬜ |
| 18.4 | 🟡 | Nếu làm lại từ đầu, bạn đổi quyết định nào? Vì sao? | — | ⬜ |
| 18.5 | 🟡 | Nyxara-Orchestrator: câu hỏi nghiên cứu là gì, đo bằng gì, kết quả ra sao? | — | ⬜ |
| 18.6 | 🟢 | Vì sao bạn chuyển từ backend sang AI engineering? | — | ⬜ |
| 18.7 | 🟡 | Kể một lần phải làm việc với yêu cầu mơ hồ (STAR). | — | ⬜ |
| 18.8 | 🟡 | Kể một lần sai và bạn sửa thế nào (STAR). | bug-log | ⬜ |

---

## 📋 Nhật ký vấn đáp

Mỗi vòng ghi 1 dòng. Chỉ tính câu **đã đóng tài liệu trả lời trước**.

| Ngày | Phạm vi | ✅ | ⚠️ | ❌ | Câu sai cần nhắm lại |
|---|---|---|---|---|---|
| 2026-09-18 (slot công ty) | RRF · tenant filter · recursive chunking | 0 | 2 | 1 | 3.9 tenant **lọc ↔ phân vùng** (+2 → 20/09) · 3.8 BM25 mặt chữ ↔ nghĩa, **đảo nhãn** (+2 → 20/09) · 3.5 công thức `1/(k+rank)` (+5 → 23/09) · 1.4 thiếu hậu quả (+5 → 23/09) |
| 2026-09-20 (tối, đo lại) | BM25 mặt chữ · tenant filter | 1 | 1 | 0 | 3.8 nói nhầm "rank" thay vì TF/IDF trên mặt chữ, không nêu được BM25 khớp theo cái gì (+5 → 25/09, đo bằng drill ép chọn) · 3.9 ✅ đủ đáp án + lý do (+14 → 04/10) |
