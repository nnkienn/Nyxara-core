# 📖 Glossary — từ điển thuật ngữ

> 1 dòng / thuật ngữ. Gặp từ lạ → thêm ngay. Sắp xếp theo nhóm cho dễ tra.
> Định nghĩa bằng lời của mình, ngắn gọn; chi tiết + công thức để ở [[algorithms]].

## Retrieval / RAG
- **Embedding** — ánh xạ text → vector số (bge-m3: 1024 chiều) học từ hàng tỷ cặp câu.
- **Cosine similarity** — độ giống 2 vector theo góc, bất biến với độ dài.
- **Dense retrieval** — tìm bằng vector (ngữ nghĩa). **Sparse (BM25)** — tìm bằng từ khóa.
- **Hybrid search** — chạy cả dense + sparse rồi gộp.
- **RRF** — Reciprocal Rank Fusion: gộp nhiều bảng xếp hạng qua rank, k=60.
- **Rerank (cross-encoder)** — chấm lại top-k bằng cách đọc query+doc cùng 1 lượt.
- **CRAG** — Corrective RAG: sau khi retrieve, có 1 bước "giám khảo" (LLM) chấm chất lượng
  context; context tệ thì **tự tìm lại rộng hơn** thay vì cứ generate bừa từ context xấu.
- **LLM-as-judge** — dùng chính 1 LLM để chấm/đánh giá (thay vì người) — ở CRAG dùng để chấm
  từng doc CÓ/KHÔNG liên quan tới câu hỏi.
- **Chunk** — 1 mẩu text cắt ra để embed. **Chunking** — cách cắt.
- **MMR** — Maximal Marginal Relevance: chọn top-k đa dạng, tránh trùng.

## State Machine / LangGraph (Phase 2.3)
- **State machine** — hệ thống chạy qua nhiều **trạng thái** (state), mỗi bước xử lý xong thì
  chuyển state, có thể **rẽ nhánh** hoặc **quay lại** — khác code tuyến tính chạy 1 đường thẳng.
- **State** — 1 dict/struct mang dữ liệu xuyên suốt cả graph (ở CRAG: `query`, `retrieved_docs`,
  `verdict`, `attempts`, `answer`...), mỗi node chỉ cập nhật 1 phần, không thay hết.
- **Node** — 1 hàm `(state) -> dict cập nhật`, coi như 1 "trạm" trong graph.
- **Edge** — đường nối 2 node, đi theo hướng cố định, luôn luôn chạy.
- **Conditional edge (router)** — đường nối **có điều kiện**: đọc `state` rồi tự quyết định đi
  tới node nào tiếp theo (không được phép sửa `state`, chỉ được *đọc* rồi trả về tên node).
- **`StateGraph`** — class của LangGraph dùng để khai báo node/edge/conditional-edge, sau đó
  `.compile()` ra 1 graph chạy được (`.invoke(state_ban_đầu)`).
- **`END`** — hằng số đặc biệt của LangGraph đánh dấu "graph dừng ở đây".
- **Cycle guard** — cơ chế chặn vòng lặp chạy mãi (ở CRAG: đếm `attempts`, tới ngưỡng thì buộc
  dừng) — cùng họ với base-case của đệ quy hay visited-set của DFS.
- **Closure** — 1 hàm **nhớ được** biến từ phạm vi hàm cha dù hàm cha đã chạy xong. Dùng để
  node (chỉ nhận đúng 1 tham số `state`) vẫn "mang theo" được các dependency đã inject lúc khởi
  tạo (`retriever`, `grader`...) — viết bằng cách 1 hàm ngoài `return` ra 1 hàm trong.

## Hạ tầng LLM (Phase 2.3)
- **Ollama** — chương trình chạy LLM cục bộ (self-hosted), expose HTTP API (`/api/generate`)
  để gọi model đã tải về (ví dụ `qwen2.5:3b`) mà không cần gửi dữ liệu ra dịch vụ ngoài.
- **Tailscale** — VPN dạng lưới (mesh), nối 2 máy (dù ở 2 nơi khác nhau) vào 1 mạng riêng ảo
  qua Internet, không cần mở port ra ngoài — mỗi máy có 1 IP nội bộ cố định dạng `100.x.x.x`.
- **Quantization (Q4, …)** — nén trọng số model xuống ít bit hơn (ví dụ 4-bit thay vì 16/32-bit)
  → nhẹ hơn, chạy CPU được, đánh đổi 1 phần độ chính xác.

## Kiến trúc
- **Port** — interface (hợp đồng) trong domain. **Adapter** — bản cắm thật ở infrastructure.
- **Hexagonal** — kiến trúc port/adapter, domain không phụ thuộc framework.
- **tenant_id** — namespace cô lập dữ liệu 1 niche (KHÔNG phải customer).
- **Composition root** — nơi dựng & nối các phụ thuộc (ở đây: `app/main.py` startup).

## Eval
- **Golden dataset** — bộ (query, đáp án chuẩn) cố định để đo, versioned.
- **Regression test** — test sinh ra từ 1 bug đã sửa, chặn tái phát.
- **Faithfulness** — câu trả lời có bám context không (RAGAS).
- **Hit@k / MRR / NDCG** — các chỉ số đo chất lượng xếp hạng retrieval.



## Ingestion / Dedup
- **Deduplication (dedup)** — loại bỏ chunk trùng trước khi nạp kho (chunk trùng chiếm slot top-k + tốn tiền embed).
- **Hash set** — tập hợp dùng hash để kiểm tra "đã thấy chưa" trong O(1) (thay vì list phải dò O(n)).
- **Idempotent** — chạy 1 lần hay 100 lần cho cùng kết quả; ingest cùng doc 2 lần không nhân đôi.
- **`set` vs `set()`** — `set` là *kiểu/khuôn*; `set()` tạo *một tập rỗng thật sự*. Gán `seen = set` (thiếu `()`) → `TypeError` khi dùng `in`.

- **Near-duplicate** — 2 chunk *gần* giống (chỉ thừa 1 dấu chấm, khác 1 chữ…); exact-dedup coi là khác nhau → vẫn embed cả 2 → tốn tiền + nhiễu top-k.
- **Edit distance (Levenshtein)** — đo độ **KHÁC** nhau: số phép sửa **tối thiểu** (thêm/xoá/thay 1 ký tự) để biến chuỗi A thành B. Càng nhỏ càng giống; 0 = giống hệt.
- **Dynamic Programming (DP)** — chia bài toán lớn thành các **bài toán con**, lưu kết quả từng bài con vào **bảng** để bài lớn hơn tra lại (không tính lại). Ở edit distance: mỗi ô lưới = distance của "i ký tự đầu A vs j ký tự đầu B".
- **Threshold (ngưỡng)** — con số quyết "gần bao nhiêu thì coi là trùng": `distance ≤ ngưỡng → bỏ`. Cao quá → gộp nhầm chunk khác nghĩa; thấp quá → lọt near-dup. Chọn bằng eval, không chọn bừa.
- **Normalization** — chuẩn hoá text *trước khi so* (lowercase, bỏ dấu câu/khoảng trắng thừa) → ca "khác vặt" thành giống hệt → bắt được bằng hash O(1), đỡ tốn edit distance.


## Retrieval / BM25
- **Sparse retrieval** — tìm bằng **từ khoá** khớp thẳng (doc chứa đúng chữ). Đối lập **dense** (vector, đo góc/ngữ nghĩa). Sparse mạnh ở mã/tên/từ hiếm mà vector thua.
- **Inverted index** — hash map `từ → [danh sách doc chứa từ đó]`. "Ngược" vì bình thường doc→các từ, ở đây lật lại từ→các doc. Tra "từ này ở doc nào" trong O(1), khỏi quét.
- **Term Frequency (TF)** — số **lần** một từ xuất hiện **trong 1 doc**. (đếm *lần*)
- **TF saturation / `k1`** — TF lặp nhiều lần trong 1 doc thì điểm **tăng nhanh lúc đầu rồi chững** (như bát cơm thứ 1 vs thứ 10). `k1` chỉnh tốc độ chững. Chống spam từ khoá.
- **Document Frequency (DF)** — số **doc** chứa từ đó trong kho. (đếm *doc*, KHÁC TF!) VD `"mèo"` có trong 5/1000 doc → DF=5.
- **IDF (Inverse DF)** — nghịch đảo DF: từ **hiếm** (DF thấp) → IDF **cao** → đáng giá; từ **phổ biến** (DF cao, như "và", "con") → IDF gần 0 → bị dìm.
- **Length normalization / `b`** — phạt doc **dài** (dài thì tự nhiên TF cao, không công bằng với doc ngắn đậm đặc). `dl/avgdl` = độ dài doc / độ dài trung bình. `b=0` tắt phạt, `b=1` phạt tối đa, mặc định `b=0.75`.
- **BM25** — công thức chấm điểm sparse, ghép 3 viên gạch: `IDF × (TF bão hoà theo k1) × (phạt độ dài theo b)`. Doc chứa nhiều lần một từ HIẾM và ngắn gọn = điểm cao nhất.

## (Thêm nhóm/từ mới bên dưới)
