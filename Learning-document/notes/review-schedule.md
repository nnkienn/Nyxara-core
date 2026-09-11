# 🔁 Lịch ôn cách quãng (spaced repetition)

> Nguồn gốc: [LEARNING_ROADMAP.md § Phương pháp học 2.0](../LEARNING_ROADMAP.md) (thêm
> 2026-08-28, sau khi nhận ra 6.5 tuần đầu đọng lại yếu). Cách dùng ở đầu mỗi buổi:
> 1. Xem hàng nào có ngày ôn (+1/+3/+7/+14) ≤ hôm nay và chưa tick.
> 2. Làm **(b) giảng lại** (đóng tài liệu, nói/viết lại nguyên lý) cho mọi hàng tới hạn.
> 3. Với hàng ở cột +7 hoặc +14: thêm **(c) code-tay-lại** phần lõi thuật toán (10-15 phút,
>    không nhìn file cũ), rồi so với code thật.
> 4. Tick ✅ vào đúng cột ngày đã ôn xong. Nếu giảng lại/code lại không trôi chảy → đừng tick,
>    quay lại đọc note gốc củng cố trước, ôn lại hôm sau.

| Kỹ thuật | Xong ngày | +1 | +3 | +7 | +14 | Ghi chú |
|---|---|---|---|---|---|---|
| BM25 scoring (IDF, k1, b) | 2026-08-03 | — | — | — | — | *(đã qua ngày, ôn khi tới lượt active-recall)* |
| RRF (Reciprocal Rank Fusion) | 2026-08-03 | — | — | — | — | |
| Cross-encoder rerank (bi- vs cross-encoder) | 2026-08-04 | — | — | — | — | |
| CRAG state machine (`decide()`, `attempts` guard) | 2026-08-12 | — | — | — | — | |
| Incremental ingest / multi-store diff (`manifest` = `{tenant:{doc:{idx:hash}}}`, `diff_manifest`, `to_upsert/skip/delete`) | 2026-09-02 | ⚠️ 2026-09-03 **TRƯỢT rồi vá** | ✅ 2026-09-04 *(ôn bù: 9.5/10)* | ⚠️ 2026-09-09 *(hiểu: 2/3 · **chưa code-tay-lại**)* | ⬜ 2026-09-16 | Qua cổng Trạm 1 ngày 02/09 nhưng +1 hôm sau trượt. Lẫn `to_upsert`/`to_delete` **lần thứ 4** và đảo ngược bền/dễ vỡ. **+7 (09/09):** câu `to_upsert`/`to_delete` và câu hash → ✅. Câu "quyết định skip đọc từ đâu" → **❌ lần thứ 2** (xem [Cặp 12](./the-phan-biet.md)), đã vá bằng bài đo. **Mốc +7 CHƯA tick sạch: còn nợ code-tay-lại `get_doc_manifest` + 3 dòng quyết định của `ingest_document`.** *(cũ)* Đã vá bằng drill ([the-phan-biet.md](./the-phan-biet.md) Cặp 1, 2, 8) → 11/12. **Chưa tick sạch — phải ôn bù 04/09 rồi mới tính +3.** |
| Retrieval 2 tầng (rẻ-rộng Dense+BM25+RRF → đắt-hẹp cross-encoder) + hợp đồng return giữa 2 retriever | 2026-09-02 | ⚠️ 2026-09-03 **TRƯỢT rồi vá** | ✅ 2026-09-04 *(ôn bù: 9.5/10)* | ⚠️ 2026-09-09 *(hiểu: 1/3 sạch · **chưa code-tay-lại**)* | ⬜ 2026-09-16 | +1 trượt: tưởng BM25 là model / cross-encoder không phải, và cross-encoder "đắt và **rộng**". **+7 (09/09):** RRF ✅. BM25-không-phải-model ✅ nhưng **lấy nhầm công thức RRF `1/(k+rank)` gán cho BM25** (núm BM25 là `k1`, `b`). Cặp 4 **tái phát nửa vế**: đúng "đắt + hẹp", sai "tính sẵn được" — mà chính vế sai đó mới là **nguyên nhân** của hai vế đúng. **Còn nợ code-tay-lại RRF.** *(cũ)* Đã vá bằng drill (Cặp 3, 4, 5, 6) → 11/12. **Chưa tick sạch — ôn bù 04/09.** |
| Vòng đời trạng thái: ephemeral (RAM) vs durable (đĩa) · stale state · `lifespan` mở-và-đóng | 2026-09-06 | ⚠️ 2026-09-07 **TRƯỢT 1/3** | ✅ 2026-09-09 *(vá bằng bài đo, không giảng suông)* | ⬜ 2026-09-13 | ⬜ 2026-09-20 | Bug #25 + #31. Lần đầu trả lời **sai 2/4** ô bảng (tưởng `InMemoryDocStore` trên đĩa, tưởng `grader` là nơi giữ trạng thái, **bỏ sót manifest**). Mốc +3 phải **code tay lại** khối shutdown trong `lifespan`, không giảng lại suông. **+1 (07/09) TRƯỢT:** tưởng quyết định skip đọc 3 kho (thực ra đọc **manifest**); nói nhầm fix sang tầng retrieval. Ôn bù dời sang 09/09 (08/09 nghỉ OT). **+3 (09/09):** bug #31 ✅ ngay. Nhưng "sau fix #25 manifest sống ở đâu" → **❌ trả lời "trên đĩa, restart vẫn còn"** (mô tả trạng thái TRƯỚC fix). Vá bằng 5 kịch bản chạy thật → tự giảng lại đúng bằng lời mình. **Mốc +7 (13/09) vẫn phải code-tay-lại khối shutdown `lifespan`.** |
| Hợp đồng return giữa 2 tầng · additive vs breaking change · integration test vs unit test | 2026-09-06 | ⚠️ 2026-09-07 (đọc lướt) | ✅ 2026-09-09 *(9/10)* | ⬜ 2026-09-13 | ⬜ 2026-09-20 | Bug #30. Chỗ vấp: gọi hàm mà **không hứng giá trị trả về** (lần thứ 3 dính dạng "chưa nối dây"). Ôn kèm câu: *test chỉ bắt được bug nằm trên đường nó đi qua.* **+1 (07/09):** sai câu `chunk_count` — chọn "số chunk ghi vào kho", thực ra là **số nhát cắt**. Lỗi đọc lướt, không phải lẫn khái niệm. Xem [Cặp 11](./the-phan-biet.md). **+3 (09/09):** `chunk_count` = nhát cắt ✅ (đã sạch) · additive ✅ nhưng **không nêu được tiêu chí** — tiêu chí là *caller cũ có gãy không*; breaking tệ nhất là **giữ nguyên tên, đổi ý nghĩa**. |
| Thread-safety: `def` vs `async def` · threadpool vs event loop · đọc-sửa-ghi không nguyên tử · `Lock` | 2026-09-06 | ✅ 2026-09-07 *(tự đo, không giảng suông)* | ⚠️ 2026-09-09 *(hiểu ✅ · **chưa code-tay-lại**)* | ⬜ 2026-09-13 | ⬜ 2026-09-20 | Trạm 4d + bug #29. Mốc +3 phải **code tay lại** cả `Lock` lẫn test race (kể cả mẹo `setswitchinterval` — thiếu nó test **xanh giả**). Câu chốt tự kiểm: *vì sao khoá TO chứ không chỉ khoá dòng nguy hiểm nhất?* **+1 (07/09):** ban đầu sai **4 lượt liên tiếp**, đảo ngược có hệ thống, kể cả ngay sau khi đọc bảng. Chỉ vá được khi **tự đo**: `def` 2.05s vs `async def` 6.02s. → [Cặp 10](./the-phan-biet.md). **+3 (09/09):** cả `def`/`async def` (2.05s/6.02s) lẫn câu "vì sao khoá TO" đều trả lời **đầy đủ 3 tầng, không thiếu ý nào** — câu mạnh nhất buổi. **Nhưng mốc +3 yêu cầu code-tay-lại `Lock` + test race: CHƯA làm, còn nợ.** |
| CRAG closure vs state (`build_graph` 1 lần lúc boot · `candidate_k` đông cứng · van `max_attempts`) | 2026-09-04 | ✅ 2026-09-05 *(code tay, không chỉ giảng lại)* | ⏭️ dời 08/09 → **09/09 vẫn chưa trả** (hiểu ✅, chưa code tay) | ⚠️ 2026-09-11 *(hiểu phải dựng lại bằng trace · code tay: schema ✅ sau 4 lượt · `make_grade_node` **chưa**)* | ⬜ 2026-09-18 | **+7 (11/09) KHÔNG TICK:** đóng sách thì không bắt đầu được, nhầm node `retrieve` với retriever (BM25/RRF). Dựng lại bằng chạy graph thật in ĐỌC/GHI từng node → hiểu đủ 4 key. Code tay Phần 1 (schema) xanh lượt 4; **Phần 2 `make_grade_node` còn nợ**, chấm bằng [drills/2026-09-11-crag-cham.py](../drills/2026-09-11-crag-cham.py). Xem § Buổi 2026-09-11 ở công ty bên dưới. Trạm 3 xong phần **hiểu**, chưa qua phần **làm**. Cặp 9 drill 2 vòng vẫn còn sai `max_attempts` + bài closure Python thuần. Mốc +1 (05/09) phải kèm **code tay bản fix #26**, không chỉ giảng lại. | **+3 (09/09):** `max_attempts` = closure → ✅ **SẠCH lần đầu** sau khi sai dai từ 03/09. Nhưng phần **code tay** dời lần thứ 3 (07→08→09/09) — ưu tiên trả trước tiên. *(cũ)* **+3 chưa làm 07/09** (hết giờ, buổi bị ôn bù + drill cú pháp ăn hết) — phải **code tay lại**, dời sang 08/09.

> Thêm hàng mới mỗi khi 1 kỹ thuật qua checkpoint (e) trong roadmap. Đừng xoá hàng cũ dù đã
> ôn hết 4 mốc — giữ lại làm log, chỉ ngừng thêm cột ôn tiếp.

---

## 🃏 Luật bổ sung (thêm 2026-09-03, sau khi mốc +1 đầu tiên trượt)

Mốc +1 đầu tiên áp dụng thật đã **trượt 3/4 câu** dù hôm trước đã qua cổng đóng-sách. Rút ra:

1. **Qua cổng đóng-sách KHÔNG có nghĩa là đã đọng lại.** Cổng chỉ chứng minh "hiểu được ngay sau
   khi vừa được sửa". Mốc +1 hôm sau mới là phép thử thật. Đừng coi cổng là xong.
2. **Phân loại lỗi trước khi chữa.** Lỗi *quên* (không nhớ ra) ≠ lỗi *phân biệt* (lẫn 2 thứ na ná
   nhau). Nếu các câu sai đều có dạng "chọn nhầm giữa A và B" → **đừng giải thích lại**, giải
   thích lại không ăn (đã thử, 12 tiếng sau vẫn lẫn). Chuyển sang **drill phân biệt**:
   ~12 câu ép chọn A/B, trả lời liên tục, sửa 1 lượt cuối. Nội dung lấy từ
   [the-phan-biet.md](./the-phan-biet.md). Hiệu quả thật: 1/4 → 11/12 trong 1 vòng.
   Cùng cơ chế với drill cú pháp Python (§3.5 CLAUDE.md) — chỉ khác nội dung.
3. **Trượt +1 thì không tick, và chèn 1 buổi "ôn bù" ngày hôm sau** trước khi tính tiếp mốc +3.
   Ghi rõ trượt ở cặp/khái niệm nào vào cột Ghi chú — để lần sau nhắm thẳng vào đó.
4. **Không mở trạm/kỹ thuật mới trong buổi mà mốc ôn bị trượt.** Ưu tiên vá nền trước
   (đúng §3.6 mục 5 — checkpoint đóng-sách). Đã áp dụng thật sáng 03/09: hoãn Trạm 3 sang ca tối.

---

## 🏢 Buổi 2026-09-11 (T6) — ở công ty (10:07 → 17:25)

> Công ty rảnh nên học xen kẽ: **10:07-11:50** tại máy · ra quán cà phê đọc
> [phiếu cà phê](https://claude.ai/code/artifact/675cf9c4-7343-4eec-afc5-46ecdaea11ab) (giờ quán chưa ghi) ·
> **16:40-17:25** tại máy. Máy công ty là Fedora; tối học máy khác → `git pull` trước.

**B0 ✅** tạo `.vscode/settings.json` trên máy công ty: auto-save + tắt Copilot + tắt inline suggest
(`.vscode/` bị gitignore — **mỗi máy phải tạo riêng**).

⚠️ **Bản `merge_pieces` đóng sách của sáng nay KHÔNG lên git** —
[drills/2026-09-11-merge-pieces-dong-sach.py](../drills/2026-09-11-merge-pieces-dong-sach.py) bị cụt ở
`if(len(current) + len (` (lỗi VS Code không lưu được trên Mac). Bug chunk rỗng phải làm lại từ đầu.

**B1 — drill list ↔ set ↔ dict: 4/6 → kiểm 0/2 → giảng lại → kiểm 2/3. CHƯA SẠCH, chưa thêm Cặp 13.**
- Câu đáng giá nhất: câu 1 (`a = {}`) trả lời **dict**, câu 6 (`f = {}` rồi `f.add("x")`) **cùng dòng
  tạo** lại coi là set → **suy kiểu từ dòng DÙNG (`.add`) thay vì dòng TẠO**. Biết luật, đọc ngược chiều.
- Kiểm 0/2: `g = {}; g["x"] = 5` đoán nổ (thật `{'x': 5}`) · `{"a":0,"b":0,"a":0,"b":1}` đoán `3, 0` (thật `2 1`).
- Ẩn dụ "ngăn tủ / túi nhãn" **user không hiểu** → đổi sang **sổ ghi chép (list) · danh bạ điện thoại
  (dict) · danh sách điểm danh (set)** thì ăn. User tự rút: *"dict cùng key thì lấy cái sau cùng"* ✅.
- Kiểm 2/3. **Lỗ còn lại duy nhất:** `{"Lan","Minh","Lan"}` rồi `.add("Minh")` → đoán `3`, thật `2` —
  tưởng set chỉ bỏ trùng **lúc tạo**, không bỏ trùng lúc `.add`. → **10' drill nền 12/09 nhắm đúng chỗ này.**

**B2 — ôn +7 CRAG phía GHI: KHÔNG TICK.**
- Đóng sách: *"không biết nên bắt đầu từ đâu luôn"*. Bảng ĐỌC/GHI từng node: `/ask` ✅ · `retrieve`
  **nhầm tầng** — kể BM25 + RRF + `rrf_k` (đó là bên trong `retriever.search`, Trạm 2) · `grade`,
  `generate` không nhớ.
- Gỡ bằng **chạy graph thật, bọc từng node in key ĐỌC/GHI** (không giảng suông) → hiểu đủ 4 key:
  `grades` (grader chấm từng tài liệu) · `verdict` (`decide(grades)`) · `attempts` (+1 ✅) ·
  `candidate_k` — đoán **"+10"** vì bảng Claude đưa chỉ có một cặp `10 → 20` (đề có 2 đáp án — lỗi của
  Claude) → chạy 3 kịch bản ra `[10, 20, 40]` → **×2** · điều kiện ghi ✅, bổ sung: **AMBIGUOUS cũng không ghi**.
- **Câu hỏi hay user tự nêu:** *"grades đã chấm rồi sao còn phải verdict?"* → `grades` trả lời "tài
  liệu **này** tốt không" (N giá trị), `verdict` trả lời "**cả nhóm** đủ tốt chưa" (1 giá trị) vì `route`
  chỉ rẽ theo 1 chữ. Truy tiếp "ai đọc `grades`?" → **không ai** → [bug #33](./bug-log.md), vào hàng đợi.
- **Code tay:** user tự báo *"bay vô code tay không nổi"* → dẫn theo mẩu nhỏ, ví dụ cú pháp lấy từ
  chuyện khác (danh bạ). **Phần 1 (schema) — 4 lượt mới xanh:**
  1. chỉ 3 key → tưởng schema của **riêng `grade`** → cắm vào graph thật: `KeyError: 'retrieved_docs'`
  2. `verdict : "CORRECT" || "INCORRECT" || "AMBIGOUS"` (`SyntaxError` — `||` không phải Python, và đặt
     **giá trị** vào chỗ **kiểu**) · `grades : bool` (thật `list[bool]`) · `attemps` thiếu chữ `t`
  3. `verdict`, `grades` đã sửa đúng; `attemps` **vẫn lọt** → `GraphRecursionError` (bài đo: sai 1 chữ →
     `attempts` bị vứt mỗi vòng → van `max_attempts` không đóng)
  4. ✅ 8/8 key khớp `state.py` · nhật ký `[10, 20, 40]` và `[10]` **XANH**
- **Phần 2 `make_grade_node` — ⬜ CHƯA LÀM.** Dừng theo §3.9 (2-3 lượt liên tiếp dính lỗi nhìn, cuối ngày dài).

**Giờ-mốc hôm nay: ~30'** (chỉ ca 7h sáng). Mốc 1 không tiến thêm phút nào sau 08:00 — cả ngày là ôn.
**User chốt:** *"phải học kĩ thôi chứ không học kiểu bỏ được"* — bác lịch Claude đề xuất dồn 3 bài thiết
kế vào chiều + bỏ B3 để kịp nối `/ingest` tối nay. → Việc không vừa thì trôi nguyên vẹn, không cắt bước.
Hệ quả đã nói thẳng: mốc 1 nhiều khả năng đóng **trưa 12/09** chứ không phải tối 11/09; checkpoint 17/09
trên giấy vẫn vừa nhưng **đệm = 0**.

**Lỗi của Claude (ghi để không lặp):**
1. Nói *"phiên này mở được trên claude.ai/code"* — **sai**, phiên chạy trong VS Code không tự lên web.
   Kênh đúng: bình luận "Send to Claude" trên artifact (khi phiên máy nhà/công ty còn mở).
2. Bảng hỏi quy luật `candidate_k` chỉ đưa **một cặp số** → "+10" và "×2" đều khớp. Hỏi quy luật thì phải
   đưa **≥ 3 điểm dữ liệu**.
3. Ẩn dụ trừu tượng (ngăn tủ dán nhãn, túi nhãn) — user nói thẳng *"dùng từ ngữ kiểu khác đi không hiểu"*.
   Ẩn dụ phải là **đồ vật dùng hằng ngày có đúng cơ chế** (danh bạ: cùng tên thì số mới đè số cũ).
4. Đề xuất **bỏ/dời bước** để kịp mốc — trái ý user. Thiếu giờ thì báo cái giá, không cắt bước.

**📌 Tiếp tục (tối 11/09 hoặc T7 12/09), đúng thứ tự:**
1. **B2 Phần 2 `make_grade_node`** trong [drills/2026-09-11-crag-phia-ghi.py](../drills/2026-09-11-crag-phia-ghi.py),
   dẫn 4 mẩu nhỏ: **2a** vỏ (hàm ngoài nhận `grader`, trả hàm trong) · **2b** lấy key từ `state` · **2c** gọi
   grader + `decide` · **2d** dựng dict kết quả, thêm `candidate_k` chỉ khi INCORRECT. Claude chạy
   [drills/2026-09-11-crag-cham.py](../drills/2026-09-11-crag-cham.py) sau mỗi mẩu. Xong → giảng lại 2-3 dòng.
2. **B3** `merge_pieces` đóng sách — làm lại bug chunk rỗng (mẩu **đầu tiên** dài hơn `size`).
3. **B4** 2 test (ca gộp thường · ca túi cuối) + regression test cho bug chunk rỗng → `pytest` toàn bộ.
4. **B5** giữ separator — bài thiết kế, Claude giảng trước. Chỉ khi buổi bắt đầu ~19h, không OT.
→ **T7 12/09:** 10' drill (set bỏ trùng khi `.add`) · B6 overlap · B7 mẩu dài hơn `size` · **B8 nối `/ingest`**
→ đóng mốc 1 → chiều mở **Metadata filtering** (mốc 2, 🔴 hộp 8h).

**🌙 Tối 11/09 (máy Mac, bắt đầu 23:31) — user chọn code luôn dù §3.9 khuyên ngủ:**
- ⚠️ **Thứ Bảy 12/09 user ĐI LÀM — chỉ lần này, bình thường nghỉ T7.** Tuần này mất ngày 6h.
  Tính lại bằng hộp giờ đã chốt (ngày thường 2h30 giờ-mốc · CN 4h45):
  - tối T7 vẫn học 3h → mốc 1 đóng 12/09 · Metadata 15/09 · Document-based 17/09 → **checkpoint 17/09 = 3/4** (MMR tràn ~3h15)
  - T7 không học → mốc 1 đóng CN 13/09 · Metadata 16/09 · Document-based chưa → **17/09 = 2/4**
  - Vẫn **lạc quan**: phần còn lại của mốc 1 có 3 câu thiết kế (separator · overlap · mẩu dài hơn `size`).
  → Rất có thể **phương án B bật tại 17/09** (thiếu 1 → dời Versioning · thiếu 2 → thêm Temporal).
  Các tuần sau giữ nguyên 6h T7/CN.
- `make_grade_node` (B2 phần 2) là **bài ôn**, **0 giờ-mốc** — làm xong không đẩy mốc 1 phút nào.
- **Máy chấm CRAG đã sửa** (`0fac92b`): trên Mac `.venv` là Python 3.9 → LangGraph đọc kiểu của TypedDict qua
  `sys.modules[tên module]` → nổ `KeyError: 'bai'` cả với bản thật. Đăng ký module trước khi exec → bản thật XANH 3/3.
- **Gốc lỗi VS Code không lưu được** (log: `Unable to write file ... File Modified Since`) — đúng 2 bản nháp kẹt:
  `app/presentation/api/ingest.py` từ **06/09 21:43** (import `app.application.chunking.fixed_size_chunk` →
  chạy thật `ModuleNotFoundError`; file bị sửa từ terminal lúc 21:54 khi đổi tên — bug #32) và drill
  `merge-pieces` 07:38. **Phải Revert cả hai, KHÔNG Overwrite** — Overwrite `ingest.py` là app không khởi động.
  **Luật: Claude không ghi vào file user đang mở trong VS Code.**
- 🔍 **Vì sao tắt Copilot sáng 11/09 KHÔNG ăn, và auto-save cũng không ăn** (tìm ra 00:05 ngày 12/09): VS Code trên
  Mac đang mở **thư mục cha `/Users/nnkienn/Developer`** làm gốc (workspaceStorage xác nhận) → file
  `nyxara-core/.vscode/settings.json` **bị bỏ qua hoàn toàn**. Settings cấp user là `files.autoSave: "onWindowChange"`
  → chỉ lưu khi chuyển cửa sổ. Chữ gợi ý đến từ Copilot có sẵn trong VS Code 1.134 + extension `openai.chatgpt`.
  Hệ quả: câu *"chạy file chưa lưu — đã đóng vĩnh viễn bằng auto-save"* (07/09) **chưa bao giờ đúng trên Mac**.
  → Đã tạo `/Users/nnkienn/Developer/.vscode/settings.json` (ngoài repo, áp cho mọi project trong `Developer`):
  auto-save 1s · tắt Copilot · `editor.inlineSuggest.enabled: false`. Cách sạch hơn: mở VS Code đúng thư mục `nyxara-core`.

---

## 🔨 Buổi 2026-09-10 (T5) — MỐC TỰ KIỂM · chọn NGÀY B (vá nền đọc code)

**Ca chiều 15:12-~17:15 — làm bù cho tối 09/09 (chỉ 30', "hoàn toàn mù"):**
1. Chỗ tắc tối 09/09, user tự chọn: *không hiểu đề bảo làm gì* + *hiểu đề mà không biết bắt đầu* +
   *biết bước mà không gõ ra được* — kẹt **cả 3 tầng cùng lúc**.
2. Trace tay `merge_pieces(["Toi","an","com","roi","di","ngu"], 6)` —
   [drills/2026-09-10-trace-merge-pieces.md](../drills/2026-09-10-trace-merge-pieces.md).
   Cột `current_merge` **đúng 6/6 vòng** (kể cả ca biên `6 <= 6`). Cột `merges` **sai 3 ô**.
   Câu kiểm nhanh (`merges=["A","B"]`, thùng `"CD"`, món `"E"` không vừa) → vẫn bỏ `"E"` lên xe.
3. **6 lỗ hổng lòi ra — KHÔNG lỗ nào là lỗi chunking**, tất cả là *mô hình chạy của Python*:

   | Lỗi | Thuộc về |
   |---|---|
   | Tưởng `current_merge = ""` (dòng 27) chạy lại mỗi vòng | thụt lề = phạm vi |
   | Tưởng dòng 35-36 chạy trong vòng | thụt lề = phạm vi |
   | Tưởng sau dòng 34 xuống dòng 35 (thật ra quay lên 28) | luồng `for` |
   | Dán `"Toian"`+`"di"` thành 1 chuỗi thay vì thêm ô mới | `+=` chuỗi ↔ `append` list |
   | Dòng 33 bỏ **món mới** lên xe thay vì **thùng cũ** — **3 lần** | giá trị biến *tại đúng lúc* dòng chạy |
   | Viết `{"A","B"}` cho list | `{}` set ↔ `[]` list |

4. Thứ gỡ được nút (lại đúng pattern Cặp 10 / Cặp 12): **chạy hàm thật và in ra**, không giảng suông —
   bảng từng dòng bằng `sys.settrace`, rồi dừng *trước* dòng 32/33/34 in biến → thấy `'CD'` còn trong
   thùng lúc dòng 33 chạy.

**Quyết định mốc tự kiểm 10/09 (user chọn):** thêm 1 ngày, **phương án B**. Không chọn A (chỉ vá riêng
hàm này — `split_by_separators` đệ quy sẽ đâm vào đúng bức tường đó, còn khó hơn). Không chọn C (đi tiếp
separator/overlap trên nền lỏng = lặp lại tối 09/09).

**📌 Ca tối 10/09 (~3h) — NGÀY B:**
1. **~30' debugger VS Code** — breakpoint · F10 từng dòng · khung Variables. Khối **thao tác riêng**,
   không trộn vào giữa bài khái niệm. Mục đích: kẹt ở máy kia thì tự xem biến, không phải chờ Claude in bảng.
2. **~1h drill đọc-chạy** — [drills/2026-09-10-doc-chay.py](../drills/2026-09-10-doc-chay.py), 9 bài
   Python thuần, mỗi bài nhắm 1 hàng trong bảng lỗi trên. User dự đoán hết → Claude chạy → so 1 lượt.
3. **~1h đóng file, tự viết lại `merge_pieces`** → debugger đi từng dòng → 2 test đã hẹn từ 07/09
   (ca gộp thường · ca túi cuối).
4. **~15' re-plan tháng 9 bằng số thật** — đệm tháng 9 đã ≈ 0, ngày B phải được trả bằng cái gì lùi lại.

**Vẫn treo, KHÔNG nhét vào tối nay:** 4 món code-tay-lại (bảng ở Buổi 09/09) · **11/09 tới hạn +7 CRAG**.

**🌧️ Ca tối thực tế (máy Mac) — bắt đầu 21:47, chỉ ~1h05 vì ngập → áp CLAUDE.md §3.9:**
chỉ làm **mục 2 (drill đọc-chạy)** — bài nhỏ 3-10 dòng, không phải nạp codebase. Mục 1 (debugger),
mục 3 (tự viết lại `merge_pieces` + 2 test), mục 4 (re-plan tháng 9) **dời sáng 11/09**.

**Kết quả drill đọc-chạy → 8/9 ✅** ([drills/2026-09-10-doc-chay.py](../drills/2026-09-10-doc-chay.py)):

| Bài | Kết quả | Lỗ nền nhắm tới (bảng 6 lỗ ở trên) |
|---|---|---|
| 1a · 1b | ✅ ✅ | dòng gán trong / ngoài `for` — thụt lề = phạm vi |
| 2 | ✅ *(chỉ lệch định dạng: `print` 2 đối số chèn 1 dấu cách, mỗi `print` 1 dòng)* | dòng ngoài `for` chạy 1 lần, sau vòng |
| 3 | ✅ | `+=` chuỗi ↔ `append` list |
| 4a · 4b | ✅ ✅ | giá trị biến tại đúng lúc dòng chạy |
| 5 | ✅ khớp 7/7 dòng | luồng `for` — hết thân vòng thì **quay lên** |
| 6 | ❌ `3 3` (thật `3 2`) | `[]` list ↔ `{}` set |
| 7 | ✅ + trace đủ 4 vòng | `merge_pieces` đội lốt — **đúng chỗ dòng 33** |

→ **Bài 7 là tín hiệu mạnh nhất:** vòng 3 user viết `tui.append(vi) => [7]` **rồi mới** `vi = tien => 5`
— bỏ ví **CŨ** lên túi trước, xong mới đổi. Lỗi "bỏ món mới lên xe thay vì thùng cũ" sai **3 lần** chiều
10/09, tối nay đúng kèm trace từng vòng.
→ **Không có lỗi đọc lướt nào** dù bắt đầu 21:47.

**Bài 6 — lỗ MỚI lòi ra: set ↔ dict.** User tự ghi: *"set là nó gộp giá trị giống nhau theo dạng key
value"*. Phần "loại trùng" đúng; phần **"key value" sai** — set **không có value**, chỉ có phần tử (giống
như chỉ giữ phần *key* của dict). Phân biệt bằng **dấu hai chấm**: `{"x", "y"}` = set · `{"x": 1}` = dict.
🪤 **Bẫy:** `{}` rỗng là **DICT**, không phải set — set rỗng phải viết `set()`. Hệ quả thật cho
`merge_pieces`: lỡ viết `merges = {}` → được dict rỗng → `merges.append(...)` nổ `AttributeError`.
→ Ứng viên cặp phân biệt mới **list ↔ set ↔ dict**, chưa drill.

**Giảng lại "ca túi cuối" qua bài 7 → ✅ user TỰ TÌM RA.** Hỏi: xoá dòng `tui.append(vi)` ngoài vòng
`for` thì mất bao nhiêu → đúng `6` (ví cuối = 5 + 1). Hỏi tiếp: danh sách nào làm túi **rỗng hoàn toàn**?
→ user tự lý luận đúng *"không chạm được nhánh else thì lấy đâu mà nhét tiền"*. Lần đầu lệch số (đọc giới
hạn thành 9 thay vì 7, quên **cộng dồn**) → sửa 1 lượt → `4 1 1 1` / `4 0 1 1` ✅, *"nhiều lắm"*.
→ Đây chính là loại input cho **test "ca túi cuối"** của `merge_pieces`: các mẩu gộp vừa trong 1 chunk →
vòng lặp không bao giờ vào `else` → thiếu khối `if current_merge: merges.append(current_merge)` ngoài vòng
thì hàm `return []`, mất sạch văn bản mà không báo lỗi.

⚠️ **Lỗi của Claude:** gọi dòng bằng **số dòng** trong file drill user đã chèn dự đoán vào → số lệch → user
hiểu nhầm dòng nào bị xoá (*"ý bạn là dòng vi = tien hả"*). **Luật: file đã có chữ user chèn vào thì trích
NGUYÊN VĂN dòng code, không gọi bằng số dòng.** (đã thêm vào CLAUDE.md §3.5)

**Drill ép chọn list ↔ set ↔ dict, 6 câu (~22:35) → 3/6 — CHƯA SẠCH, KHÔNG TICK:**

| Câu | User | Thật | |
|---|---|---|---|
| `x = {}` rồi `x.append(1)` | nổ | `AttributeError` — `{}` rỗng là dict, không có `append` | ✅ |
| `len({"a", "b", "a", "c"})` | 4 | **3** | ❌ |
| `print({"a": 1, "a": 5})` | in cả 2 cặp | **`{'a': 5}`** — key trùng, cái sau đè | ❌ |
| `{"a", "b"}` là gì | set | set | ✅ |
| `len(["a", "b", "a", "c"])` | 3 | **4** | ❌ |
| `merges` khởi tạo bằng | `[]` | `[]` | ✅ *(chưa nêu lý do)* |

→ Câu 2 và 5 **đảo ngược đúng nhau** (set ra 4, list ra 3) — dạng đảo nhãn giống Cặp 10.
→ Câu 2 và 3 sai **dù ~20 phút trước vừa xem demo chạy thật đúng hai hành vi đó** (`{"x","y","x"}` → len 2 ·
`{"x": 1, "x": 2}` → `{'x': 2}`). Bắt đầu 21:47, drill lúc ~22:35 → lẫn lỗi mệt với lỗi hiểu, chưa tách được.
→ **User tự báo ngay sau khi chấm (~22:40):** câu 2 *"biết là set, nhìn nhầm"*; câu 6 lý do *"nhìn dấu
ngoặc; nếu là set thì nuốt mất phần tử trùng"* — **ý đúng** (nhỏ: set không có `append`, set dùng `add`);
*"hoa mắt rồi"*. Câu 3 (dict key trùng thì đè) **chưa được giải thích** → sáng mai nhắm kỹ câu này.
→ **Drill lại sáng 11/09 lúc tỉnh** (CLAUDE.md §3.9: lỗ nền phải drill lúc tỉnh). Sạch thì thêm thành **Cặp 13**
trong the-phan-biet.md.

**📌 11/09 (T6) — theo RE-PLAN 10/09** ([LEARNING_ROADMAP.md § RE-PLAN 2026-09-10](../LEARNING_ROADMAP.md)):
Re-plan tháng 9 **đã làm tối 10/09**. Không còn "ngày B" đứng riêng — nền Python vá **lồng trong** code tay
của từng mốc. Ngày thường 3h = **30' cố định** (10' drill nền + 20' ôn) + **2h30 giờ-mốc**.
1. **10'** drill nền list ↔ set ↔ dict (đổi số; nhắm kỹ **dict key trùng thì đè** — tối 10/09 chưa giải thích).
2. **20'** ôn: **+7 CRAG tới hạn hôm nay** → code-tay-lại phía GHI (`grade_node` ghi `candidate_k` ·
   `candidate_k : int` trong `state.py`). Hết 20' là dừng, dở thì nợ sang 12/09.
3. **2h30 — MỐC 1/12: đóng recursive chunker** (hộp ~3h, tràn ~30' sang 12/09):
   tự viết lại `merge_pieces` đóng file → 2 test (ca gộp thường · **ca túi cuối — loại input user đã tự tìm
   ra tối 10/09**) → giữ separator → overlap → **nối `/ingest`**. Debugger VS Code học **tại chỗ** (~15')
   lúc cần xem biến, không tách 30' riêng.
   ⚠️ Ba câu **thiết kế** nằm trong mốc này (overlap đặt ở đâu · mẩu dài hơn `size` xử lý sao · tham số
   `chunk_overlap` của `/ingest` khi chunker mới chưa dùng) → Claude **GIẢNG TRƯỚC + khuyến nghị** rồi mới
   hỏi (§3.6 mục 7). Không hỏi trần.
   Tràn giờ thì thứ tự giữ: **nối `/ingest` KHÔNG được bỏ** — chưa nối thì mốc đếm là 0.
→ **12/09 (T7, 6h):** ~30' trace qua HTTP + chạy toàn bộ suite → **đóng mốc 1** → mở **Metadata filtering**
  (mốc 2, 🔴, hộp 8h, dự kiến đóng 13/09).

**Kết quả sáng 11/09 (07:06-~07:51, chỉ 45' trước giờ đi làm):**
- **Drill list ↔ set ↔ dict (đổi số) → 4/6.** Câu 3 (dict key trùng thì đè) **đúng** — tối 10/09 sai.
  Sai câu 4 (`d = {}` rồi `.add`) và câu 6 (`{"a": 1}` → trả lời set) — **cùng một niềm tin "thấy `{}`
  là set"**, lần thứ 2.
- **Ép chọn 6 literal → 3/6, đảo ngược đúng chỗ dấu `:`** (`{"x"}` → dict · `{"x": 0}` → set ·
  `{"x": "y"}` → set). Chạy thật in `type()` → user tự nêu luật *"có `:` là dict"* — **thiếu nửa "`{}`
  rỗng cũng là dict"**. **Chưa sạch → drill lại 12/09**; sạch mới thêm Cặp 13 vào the-phan-biet.md.
- **Mốc 1 — tự viết lại `merge_pieces` đóng sách (07:21-07:27):** chạy 5 input cạnh bản thật → **4/5**.
  Đúng: bỏ thùng **CŨ** lên xe rồi mới đổi (chỗ sai 3 lần chiều 10/09) · khối cất túi cuối sau vòng lặp
  (ca túi cuối). **Sai 1 ca:** mẩu **đầu tiên** dài hơn `size` → trả thêm chunk rỗng ở đầu:
  `merge_pieces(['abcdefghijkl', 'xy'], 5)` → `['', 'abcdefghijkl', 'xy']` (thật: `['abcdefghijkl', 'xy']`).
  Đúng con bug của bản Copilot đã xoá 07/09. User tự tìm nguyên nhân — Claude không chỉ dòng (§2).
- Copilot đã tắt trong `.vscode/settings.json` — **chỉ máy Mac** (`.vscode/` bị gitignore, Fedora chưa có).
- **Sửa bug chunk rỗng — 5 lượt, chưa xong:** (1) trỏ nhầm câu điều kiện `len(current) + len(piece) <= size`
  (câu đó đúng, giống bản thật) · (2) *"thùng thì chứa mẩu"* → Claude cho in ra: vòng 1 `current = ''` ngay
  trước `append` · (3) `if current(piece)` — lẫn `()` gọi hàm với câu điều kiện · (4) `if current:` **đúng
  chỗ** nhưng `IndentationError` (dòng `append` không thụt vào) · (5) bản 07:38 thụt **cả** `current = piece`
  vào trong `if` → mẩu đầu dài hơn `size` bị **MẤT**: `['xy']` thay vì `['abcdefghijkl', 'xy']`. Vẫn 4/5 —
  lỗi đổi từ "đẻ thêm chunk rỗng" sang "làm mất mẩu". **Thụt lề = phạm vi** — đúng lỗ nền số 1 của 10/09.
- ⚠️ **VS Code không ghi được xuống đĩa từ 07:25:52** (user đã báo Cmd+S; file không khoá, chỉ có 1 bản).
  Bản mới nhất chỉ nằm trong `~/Library/Application Support/Code/Backups`. Nguyên nhân chưa rõ → **tối kiểm
  trước khi code** (thông báo lỗi góc dưới VS Code · File > Save).
- **Tối 11/09 tiếp mốc 1 từ đúng chỗ này:** đưa `current = piece` về lại nấc của `else` → lưu được thật →
  chạy lại 5 ca → 2 test (ca gộp thường · ca túi cuối) → separator → overlap → nối `/ingest`.

**Lỗi phương pháp của Claude (ghi để không lặp):**
1. Bài tối 09/09 giao **5 việc liền**, trong đó 3 việc là **câu thiết kế** (giữ separator · overlap đặt đâu ·
   mẩu dài hơn `size`) — giao trần, chưa giảng. Tái phạm §3.6 mục 7 lần thứ 3.
2. Tối 09/09 sửa ~3 lần **bằng lời** trước khi chuyển sang chạy thật — luật đã có từ 04/09: trượt 2-3 lượt
   thì thôi bắt tưởng tượng, cho chạy và in ra.
3. Bảng trace dạng TRƯỚC/SAU theo vòng **giấu mất giữa vòng** — đúng chỗ lỗi dòng 33 sống. Vòng lặp có
   nhiều dòng đổi biến thì bảng trace phải có mốc **sau từng dòng đổi biến**, không chỉ đầu/cuối vòng.

---

## 🗄️ (lưu trữ) Kế hoạch 10/09 viết tối 09/09 trên máy Mac — ĐÃ BỊ THAY bởi NGÀY B ở trên

> Viết lúc 22:01 ngày 09/09, **trước** khi ca chiều 10/09 (máy kia) bóc ra 6 lỗ nền Python và chọn
> ngày B. Kế hoạch 5 bước dưới đây **không còn là kế hoạch sống** — giữ lại vì bảng trace, 3 thứ đã
> gỡ, và lý do "nối `/ingest` không được bỏ" vẫn đúng nguyên khi quay lại chunker.

> **Chỗ dừng chính xác tối 09/09 (22:01):** đang trace `merge_pieces`, bảng đã điền **4/7 dòng**.
> User dừng vì *"không đủ tỉnh táo đọc code"*, tự chấp nhận trễ hẹn chunker 1 ngày. Đúng quyết định —
> xem phần "lỗi chú ý" trong [so-gio.md](./so-gio.md).

**Bảng trace đã chốt tới lượt 4** (`pieces = ["Meo","thich","ngu","Cho","thich","chay"]`, `size=10`):

| lượt | `piece` | `len(cm)` | `len(piece)` | tổng | `<=10`? | nhánh | `current_merge` sau | `merges` sau |
|---|---|---|---|---|---|---|---|---|
| 1 | `"Meo"` | 0 | 3 | 3 | ✅ | `if` | `"Meo"` | `[]` |
| 2 | `"thich"` | 3 | 5 | 8 | ✅ | `if` | `"Meothich"` | `[]` |
| 3 | `"ngu"` | 8 | 3 | 11 | ❌ | `else` | `"ngu"` | `["Meothich"]` |
| 4 | `"Cho"` | 3 | 3 | 6 | ✅ | `if` | `"nguCho"` | `["Meothich"]` |
| 5 | `"thich"` | ⬜ | 5 | | | | | |
| 6 | `"chay"` | ⬜ | 4 | | | | | |
| — | *sau vòng lặp* | — | — | — | — | — | ⬜ | ⬜ |

**Ba thứ đã gỡ được trong lúc trace (giữ lại, đừng giảng lại từ đầu):**
1. **`len` vs chỉ số cuối** — user ghi `len("Meo")=2`. `"Meo"` có chỉ số `0,1,2` nhưng **độ dài 3**.
   Hụt 1 ở mọi chuỗi → rẽ nhầm nhánh ở lượt 3.
2. **`current_merge` (túi đang cầm) ≠ `merges` (kệ để túi đã đóng)** — user nhét túi lên kệ ở nhánh
   `if` **2 lần**. Thân nhánh `if` có **đúng 1 dòng** `current_merge += piece`, không có `merges`.
3. **BA chữ `if` trong `merge_pieces`, phân biệt bằng THỤT LỀ** — user bôi đen dòng 35-36 (`if`
   ngoài vòng lặp, 4 dấu cách, chạy **1 lần** sau khi hết lặp) và tưởng đó là nhánh `if` của lượt 4
   (dòng 29, 8 dấu cách, chạy **mỗi lượt**). Câu hỏi user tự đặt ra rất đúng: *"làm gì có đoạn code
   nào nói `len(current_merge)` lượt N = lượt N−1"* → **không có dòng nào cả**; đó là hệ quả của
   `current_merge = ""` nằm **ngang hàng** `for`, chạy 1 lần, và không dòng nào reset nó.
   → **Mẹo đã chốt: thấy khối lệnh, hỏi "nó thụt vào bao nhiêu / sống trong cái gì" TRƯỚC khi hỏi
   "nó làm gì".** Cùng bài với `with` lồng nhau ngày 06/09.

**Thứ tự 10/09 (ước lượng thật, đừng lạc quan):**
1. **5'** — điền nốt lượt 5, 6 + dòng sau vòng lặp. Đã có đà, đừng làm lại từ đầu.
2. **20'** — 2 test cho `merge_pieces`: ca gộp bình thường + **ca túi cuối** (input mà vòng lặp
   KHÔNG BAO GIỜ vào nhánh `else` → chặn đúng con bug thiếu khối dòng 35-36). Câu hỏi để mở sẵn từ
   tối 09/09, trả lời nó là viết được test: ***`if` dòng 35 tồn tại để làm gì?***
3. **30'** — **giữ separator**: `str.split` đang nuốt dấu, ghép chunk lại không ra text gốc.
   Trace lượt 2 cho thấy tận mắt: `"Meothich"` — hai từ dính liền.
4. **30'** — **overlap**. ⚠️ Dán overlap SAU khi gộp thì chunk **vượt `size`**, phá đúng hợp đồng
   hàm vừa hứa. Đây là bug có thật trong bản Copilot đã xoá.
5. **30' — NỐI `/ingest`. KHÔNG ĐƯỢC BỎ.** Xem khối 🚨 ở mục buổi 09/09. Hết giờ thì cắt mục 4,
   **không cắt mục 5** — chưa nối thì cả milestone đếm là 0.

**Quyết định còn treo (từ 07/09):** mẩu tự nó dài hơn `size` thì làm gì? Hiện `merge_pieces` cho
lọt ra nguyên vẹn, vượt `size`. Liên quan thẳng `split_by_separators`.

**Nợ ôn chưa trả (4 món code-tay-lại)** — xem bảng ở mục buổi 09/09. Ưu tiên 1: `grade_node` ghi
state + `candidate_k : int` (phía **GHI** của fix #26).

---

## ✅ Buổi 2026-09-09 (T4) — CA SÁNG 6:00-7:30 ✅ · ❌ CA TỐI 21:30-22:01 (OT) chỉ 30', 0 dòng code (xem 10/09)

> 08/09 nghỉ (OT) → toàn bộ kế hoạch 08/09 dồn sang hôm nay, cộng **6 mốc ôn tới hạn cùng ngày**.
> Chia ca: **sáng = ôn** (block ngắn, cắt ngang được) · **tối = đóng chunker** (cần 3h liền mạch).

**Ca sáng — code-tay CRAG (mốc +3, đã dời 3 lần) → trả được 1/3:**
- ✅ `retrieve_node`: đóng sách gõ ra `state.get("candidate_k", candidate_k)` **đúng nguyên văn** —
  thứ mà 03/09 trả lời ngược cả 4 ô. Phía **ĐỌC** coi như thuộc.
- ❌ `grade_node`: tái hiện chính xác dict **bản TRƯỚC fix**, rơi mất đúng 2 dòng làm nên fix #26
  (`if verdict == "INCORRECT": ket_qua["candidate_k"] = state.get("candidate_k", 0) * 2`).
- ❌ `state.py`: trả lời `attempts : int` (đã có sẵn), đúng là `candidate_k : int`. **Sai vì (2) sai** —
  không ghi khoá mới nào thì không còn gì để khai báo.
- ⚠️ **Vi phạm đóng sách:** `state.py` đang mở sẵn trong IDE, con trỏ ngay dòng `attempts : int` —
  và user chỉ đúng dòng đang nhìn thấy. Mở file mà vẫn sai thì tệ hơn nhắm mắt đoán: chứng tỏ đang
  **đọc cái đang thấy** chứ không **suy từ bước trước xuống**.

> 🧵 **SỢI CHỈ CỦA CẢ BUỔI SÁNG — ghi to, đây là chẩn đoán đáng giá nhất hôm nay:**
> **user nắm chắc phía ĐỌC, hụt phía GHI.** Cặp 12: manifest *bị đọc* thì hiểu, "ai *ghi* vào nó,
> lúc nào" thì trượt 3 lần. Fix #26: `retrieve_node` *đọc* → thuộc nguyên văn; `grade_node` *ghi*
> → rơi mất. **Từ giờ mọi câu hỏi về trạng thái phải hỏi thành cặp: ai đọc? VÀ ai ghi?**

**Lẫn tên lần thứ 3 trong buổi:** `fixed_size_chunk` bị gắn nhầm vào manifest, rồi vào retriever
(*"ủa retriever nó giờ thành fixed_size_chunk rồi mà ta"*). Gốc: rename 06/09 `recursive_chunk` →
`fixed_size_chunk` còn nóng trong đầu nên bám vào mọi chỗ trống. **Mẹo tự kiểm đã chốt: hỏi "cái
này chạy lúc GHI (`/ingest`) hay lúc ĐỌC (`/ask`)?"** — `fixed_size_chunk` có đúng 1 nơi gọi
([ingest.py:31](../../app/presentation/api/ingest.py#L31)), không một dòng nào trong `retrieval/`
hay `generation/`.

**Ca sáng — phần ôn làm được:**
1. **Drill ép chọn 13 câu** gộp cả 6 mốc tới hạn → **9/13**.
2. **Cặp 12 (SỔ ↔ KỆ HÀNG) — cặp mới, sai 3 lần liên tiếp trong một buổi.** Cả 3 lần cùng một
   hướng: gán quyết định skip cho 3 kho thay vì manifest. Giảng 2 lần không ăn.
3. **Vá bằng bài đo** — [drills/2026-09-09-manifest-vs-kho.py](../drills/2026-09-09-manifest-vs-kho.py),
   gọi `ingest_document` thật + `BM25Index` thật, 4 adapter giả, 5 kịch bản. Bảng số thật ở
   [Cặp 12](./the-phan-biet.md). Sau khi thấy số, user **tự giảng lại đúng bằng lời mình**.
4. **Câu chốt user tự nói ra:** *"con số 3 đó là láo — sổ ghi bỏ qua 3 mà kho không có gì; đáng lẽ
   sổ phải rỗng theo cái kho, sổ với kho đi đúng với nhau."*

**⚠️ CÒN NỢ — phần (c) code-tay-lại của 4 hàng, chưa trả hàng nào:**

| Hàng | Mốc | Phải code tay lại | Ưu tiên |
|---|---|---|---|
| CRAG closure ↔ state | +3 — **trả 1/3 sáng 09/09** | ~~`retrieve_node` đọc state~~ ✅ đóng sách gõ đúng nguyên văn · **`grade_node` ghi state + `candidate_k : int` trong `state.py` ❌ chưa thuộc** | **1 — trả nốt** |
| Incremental ingest | +7 | `get_doc_manifest` + 3 dòng quyết định của `ingest_document` | 2 |
| Thread-safety | +3 | `Lock` trên `self` + test race (kèm `setswitchinterval`) | 3 |
| Retrieval 2 tầng | +7 | `reciprocal_rank_fusion` | 4 |

> Bốn món này **không nhét hết vào ca tối được** (ca tối đã có ~2h20 chunker). Chỉ trả **món 1**
> nếu ca tối còn dư; ba món còn lại đẩy sang 10/09 và **ghi vào kế hoạch 10/09 ngay**, đừng để trôi
> thành nợ ngầm như mốc CRAG đã bị dời 3 lần.

> ⏰ **Ca tối bị co lại 21:30-23:00 (~1h30) — OT về trễ.** 1h30 < ước lượng 2h20 → cắt 1 món.
> **User chốt phương án A:** tối nay làm sâu (trace → 2 test → separator → overlap nếu kịp),
> **hoãn nối `/ingest`** sang sáng 10/09.
>
> 🚨 **NỢ NỐI DÂY** *(tối 09/09 ghi là "việc đầu tiên sáng 10/09" — nhưng ngày B đã dời cả chunker; nợ vẫn còn nguyên, trả khi quay lại chunker)*:
> nối recursive chunker vào [`ingest.py:31`](../../app/presentation/api/ingest.py#L31) thay
> `fixed_size_chunk`. **Chưa nối thì recursive chunker đếm là 0 cột mốc, không phải 0.9** — nó
> sẽ thành `split_by_separators` **mồ côi lần thứ hai** (test xanh, không nơi nào gọi, tưởng đã
> có mà chưa từng chạy thật — §3.8 CLAUDE.md).
> ⚠️ Kèm theo, quyết định thiết kế còn treo: `/ingest` nhận `chunk_overlap: int = 20`. Nếu
> recursive chunker chưa có overlap thì tham số đó thành **tham số câm** — nhận rồi lờ đi =
> nói dối bằng chữ ký hàm, đúng loại bug đang chữa (`chunk_count`, `recursive_chunk` không đệ
> quy, `test_..._restart` không restart). Phải xử lý tường minh, không được để im.
> ⚠️ Và kiểm bắt buộc sau khi đổi: ***ai đang hứng giá trị trả về?*** (đã dính 3 lần).
> Giữ `fixed_size_chunk`, KHÔNG xoá — Phase 3 còn benchmark.
>
> ❌ **Kết quả thật ca tối:** chỉ 30', kẹt ngay bước đầu (trace `merge_pieces`), "hoàn toàn mù" —
> không bước nào phía sau được đụng tới. Chẩn đoán + quyết định ở **Buổi 10/09** phía trên.

**📌 Ca tối 19:30-22:30 — ĐÓNG HẲN RECURSIVE CHUNKER** (nguyên kế hoạch 08/09, xem mục dưới):
trace `merge_pieces` (số thật) → 2 test (**ca túi cuối** là test đáng giá) → **giữ separator** →
**overlap** (⚠️ dán sau khi gộp là vượt `size`, phá đúng hợp đồng vừa hứa) → **nối vào `/ingest`**
(⚠️ *ai đang hứng giá trị trả về?* — lỗi "chưa nối dây" đã dính 3 lần). Giữ `fixed_size_chunk`,
KHÔNG xoá (Phase 3 còn benchmark).

**Quyết định còn treo từ 07/09:** mẩu tự nó dài hơn `size` thì làm gì? (hiện `merge_pieces` cho lọt
ra nguyên vẹn, vượt `size`) — liên quan trực tiếp `split_by_separators`.

**Lỗi phương pháp của Claude ca sáng (ghi để không lặp):** dựng bài đo xong lại **bắt user tự chạy**,
user tắc ở đường dẫn + `PYTHONPATH` và nhắn *"KHÓ QUÁ BẠN KHÔNG BIẾT CHẠY SAO"*. Trộn cái khó **thao
tác** vào giữa cái khó **khái niệm** = hỏng cả hai. **Bài đo do Claude dựng thì Claude chạy hộ luôn,**
user chỉ dự đoán và đọc số.

---

## ✅ Buổi 2026-09-04 — đã xong (ôn bù 9.5/10, đã tick +3 cho cả 2 hàng)

## ✅ Buổi 2026-09-05 — đã xong (xem CLAUDE.md §6). Mốc +1 hàng CRAG tick bằng **code tay**, không phải giảng lại suông.

## ✅ Buổi 2026-09-07 (T2, 20:45-22:41 ≈ 2h) — VÁ NỀN + KHỞI ĐỘNG RECURSIVE CHUNKER

> Buổi này **đổi trọng tâm giữa chừng**. Kế hoạch là 40' ôn + 2-3h chunker; thực tế phần ôn trượt
> nặng nên phải vá tại chỗ, rồi lòi thêm lỗ hổng cú pháp Python phải drill riêng. Chunker chỉ kịp
> xong 1 hàm. **Không tiếc giờ** — hai thứ vá được đều là nền, và cái hàm cuối buổi là hàm ĐẦU TIÊN
> user tự viết trọn vẹn không Copilot, không Claude gõ hộ.

**Làm được:**
1. **Drill ép chọn 10 câu** (gộp 3 mốc +1 tới hạn) → **7/10**.
2. **Cặp 10 `def` ↔ `async def`** — sai 4 lượt liên tiếp, **đảo ngược có hệ thống**, kể cả ngay sau
   khi vừa đọc bảng giải thích. Vá được bằng **tự đo**: dựng 2 endpoint thân giống hệt nhau,
   bắn 3 request đồng thời → `def` **2.05s** (song song) vs `async def` **6.02s** (xếp hàng).
   [drills/2026-09-07-def-vs-async.py](../drills/2026-09-07-def-vs-async.py)
3. **`diff_manifest` 4 ca, dự đoán trước rồi chạy → 4/4.** Cặp 1 (`to_upsert`/`to_delete`) **SẠCH** —
   lần sai 06/09 là đọc lướt, không phải lẫn khái niệm. Gỡ khỏi danh sách nợ.
   [drills/2026-09-07-diff-manifest.py](../drills/2026-09-07-diff-manifest.py)
4. **Drill cú pháp Python 6 bài → 6/6** ([drills/2026-09-07-cu-phap.py](../drills/2026-09-07-cu-phap.py)),
   đúng protocol CLAUDE.md §3.5. Lý do phải chèn: user tự báo *"bí rồi"* và chọn *"không nhớ cú pháp"*
   — biết phải làm gì nhưng không nhớ gõ `for`/`if`/`append` ra sao.
5. **`merge_pieces` — user tự viết, chạy đúng.** Bước (b) "gộp mẩu tới gần `size`" của recursive chunker.

**Chốt thiết kế quan trọng (user tự hỏi ra, không cần mớm):** *"phải cắt chữ `ngu` ra à?"*
→ **KHÔNG.** `size` là **TRẦN**, không phải **CHỈ TIÊU**. Thà một túi lưng (8/10) còn hơn một từ bị
chém đôi — vì chém giữa từ chính là việc `fixed_size_chunk` đã làm, và nếu recursive chunker cũng
chém thì nó không hơn gì cái cũ. Đã in ra đối chứng: `Cho t` | `hich chay` (chunk bắt đầu bằng
`hich`, vector của rác) so với cắt đúng ranh giới câu.

**Ba lỗi lặp đáng theo dõi (đều KHÔNG phải lỗi quên):**
- **Đọc lướt.** 3 lỗi thật của buổi đều là *trả lời theo cái mình tưởng đề đang hỏi*. Cùng cơ bắp với
  `recursive_chunk` không đệ quy và bài đo in ra `0.05s` (thực ra là 404) mà vẫn tin là kết quả đo.
- **Trả về CON SỐ thay vì VẬT** — 3 lần trong 1 ngày → đã thành [Cặp 11](./the-phan-biet.md).
- **Chạy file chưa lưu** — 3 lần, ngốn 3 lượt chạy nhầm. Đã bật auto-save trong
  [.vscode/settings.json](../../.vscode/settings.json), coi như đóng vĩnh viễn.

**Chuyện Copilot (ghi để không tái phạm):** giữa buổi user để Copilot gõ hộ `merge_pieces`, tự báo
*"do gợi ý code chứ tôi không biết viết"*, rồi tự quyết **xoá đi tập viết lại**. Quyết định đúng —
bản tự viết sau đó còn **chặt hơn** bản Copilot (có chốt `if current_merge:` chặn túi rỗng, bản
Copilot thiếu nên nhét chuỗi rỗng vào kết quả). **Autocomplete đưa thẳng tới trạng thái "hiểu mà
không code được"** — đúng lỗ hổng user tự chẩn 04/09. Tắt Copilot khi làm phần lõi.

**Suite:** 71 passed (chạy toàn bộ, đo thật 22:45).

---

## 📌 Buổi 2026-09-08 (T3) — HOÀN THÀNH RECURSIVE CHUNKER

> User tự chốt cuối buổi 07/09: *"sáng mai trace 1 tiếng 30 lại cái hàm này và hoàn thành toàn bộ
> recursive chunker, để tối mai qua kiến thức mới."*

**Ca sáng (~1h30) — trace + viết nốt:**
1. **Trace lại `merge_pieces`** (~20'), đúng cách §3.5: đọc thân hàm, điền bảng bằng **số thật**,
   không tin tên biến. Kèm: user **kể lại bằng lời mình** Cặp 10 + Cặp 11 (cuối buổi 07/09 do Claude
   viết lúc user đã mệt — giống cách đã làm với `03-crag.md` ngày 04-05/09).
2. **Viết 2 test cho `merge_pieces`** — việc còn nợ của buổi 07/09 (bước 5/6 TEST):
   - ca gộp bình thường
   - **ca túi cuối**: input mà vòng lặp KHÔNG BAO GIỜ vào nhánh `else` → chặn đúng con bug vừa mắc
     (thiếu phần cất túi sau vòng lặp). Test này mới là cái đáng giá.
3. **Hai việc còn lại của recursive chunker:**
   - **(a) giữ separator** khi cắt — `str.split` đang nuốt mất dấu, ghép lại không ra text gốc
   - **(c) overlap** — ⚠️ nghĩ kỹ chỗ đặt: nếu dán overlap SAU khi gộp thì chunk sẽ **vượt `size`**,
     phá đúng hợp đồng hàm vừa hứa. Đây là bug có thật trong bản Copilot đã xoá.
   - **Quyết định còn treo:** mẩu tự nó dài hơn `size` thì làm gì? (hiện `merge_pieces` cho nó lọt
     ra nguyên vẹn, vượt `size`). Liên quan trực tiếp tới `split_by_separators` — nơi lẽ ra nó đã
     bị cắt nhỏ trước khi tới bước gộp.
4. **Nối vào `/ingest`** thay `fixed_size_chunk`. ⚠️ Kiểm bắt buộc sau khi đổi: *ai đang hứng giá
   trị trả về?* (lỗi "chưa nối dây" đã dính 3 lần). Giữ `fixed_size_chunk`, KHÔNG xoá — Phase 3 còn
   phải benchmark Recursive vs Fixed-size.

**Nợ ôn phải trả trong ngày (đừng để trôi):**
- **Ôn bù** hàng *Vòng đời trạng thái* (07/09 trượt 1/3, chưa tick).
- **Mốc +3 hàng CRAG closure ↔ state** — đã dời từ 07/09. Mốc này phải **code tay lại** phần lõi,
  không giảng lại suông.

**⏱️ Ước lượng thật (làm 07/09 tối, đừng lạc quan lại):** trace+kể lại 30' · 2 test 20' ·
separator 30' · overlap 30' · nối `/ingest` 30' = **~2h20**, cộng nợ ôn ~40' → **~3h**. Ca sáng 1h30
KHÔNG đủ. Nếu sáng chỉ được 1h30 thì cắt theo thứ tự này: giữ **trace + test + separator + overlap**,
đẩy **nối `/ingest`** sang ca tối hoặc 09/09 (nó là nối dây, không phải kỹ thuật).

**Ca tối:** ưu tiên **đóng cho sạch chunker** trước. Chỉ mở Document-based chunking khi chunker đã
xong hẳn và `/ingest` chạy thật qua HTTP.

> 🧭 **Đếm cho đúng luật tiến độ, đừng tự dồn ép:** **recursive chunker CHÍNH LÀ kỹ thuật mới của
> slot 07-08/09** — đã chốt 06/09 rằng nó là milestone riêng ~2-3h, không phải cái đuôi 30' của
> Phase 0. Xong nó ngày 08/09 là **đủ luật "1 kỹ thuật / 2 ngày"**, và mốc tự kiểm **10/09 coi như
> đạt trước hạn**. Document-based chunking là slot **kế tiếp (09-10/09)**, KHÔNG phải món phải nhét
> vào tối 08/09. Nhét kỹ thuật mới lên trên một cái nền dở dang đúng là cái vòng đã ăn hết 5 buổi
> tuần trước (01-05/09).

---

## ✅ Buổi 2026-09-06 (CN, 4h chiều + 2h tối = 6h) — LÀM ĐƯỢC GÌ

> Buổi này **đổi máy** (Fedora mới), nên mất ~40' dựng lại môi trường. `.venv` không đi qua git
> (đúng CLAUDE.md §7) — phải tạo lại và cài `requirements.txt` từ đầu, kể cả tải ~4.4GB weights.

**Xong:**
1. **Trạm 4b** — trace + fix + integration test. Ghi thành [bug #30](./bug-log.md).
2. **Trạm 4c + FIX THẬT bug #25** (treo từ 14/08, 23 ngày). Manifest chuyển từ file trên đĩa
   thành `dict` trong RAM. Kèm test giả lập restart, **và đã chứng minh test đỏ được**.
3. **Phát hiện + fix bug #31** (`lifespan` không có shutdown → CUDA OOM khi dựng app 2 lần).
   Đây là bug **mới toanh**, lòi ra trong lúc viết test cho #25.
4. Suite: **70 passed in 127.34s** (đo thật, chạy toàn bộ, không giới hạn thư mục).

**Ca tối (20:45-22:45) bổ sung:**
5. **Trạm 4d** ✅ — `def` vs `async def`, đo thực nghiệm chặn event loop (2.0s vs 6.0s).
   → **Hết bài trace 4 trạm.**
6. **Fix bug #29** ✅ (race condition `BM25Index`) + test 4 luồng, đã chứng minh test đỏ được
   (`assert 7560 == 8000`). Suite **71 passed**.

**Còn nợ sang buổi sau:**
- ~~Trạm 4d~~ ✅ xong ca tối 06/09.
- ~~Fix bug #29~~ ✅ xong ca tối 06/09. Câu hỏi cần nghĩ trước: khoá cả `add_document` hay khoá nhỏ hơn? Và test bắt
  race phải **assert quá trình** + ép đổi luồng (`sys.setswitchinterval`) + lặp đủ nhiều, không
  thì **xanh giả**. Chỗ đọc-sửa-ghi khác cùng loại: `remove_document` dòng 57 (`doc_count -= 1`).
- Nối `split_by_separators` — chưa đụng.
- ⏰ Mốc ôn **+3** hàng CRAG đến hạn **07/09**, kèm **code-tay-lại** phần lõi.

**Lỗi phương pháp của Claude trong buổi (ghi để không lặp):** hai lần hỏi câu **thiết kế kiến
trúc** (chọn hướng fix #25) trước khi giảng khái niệm — user phải nói thẳng *"không hiểu bạn hỏi
gì"* và *"bạn là giáo sư mà không thể để tôi mù mờ như này được"*. Đúng cái §3.6 mục 6 đã vá
01/09 mà vẫn tái phạm. **Luật cho lần sau: bài thiết kế (chọn giữa nhiều kiến trúc) thì GIẢNG
TRƯỚC — liệt kê các phương án + cái giá của từng cái + khuyến nghị — rồi mới hỏi user chọn.**
Chỉ dùng Socratic thuần cho thứ user đã có đủ vật liệu để tự suy ra.

## 📌 (lưu trữ) Kế hoạch ban đầu buổi 2026-09-06 — ĐÓNG SỔ PHASE 0

> Mục tiêu của buổi này **không phải học thêm**, mà là **dọn sạch tồn đọng** để thứ Hai 07/09 vào
> kỹ thuật mới với sổ sạch. Đừng để nó thành buổi vá nền thứ sáu liên tiếp.

> ⚠️ **Sửa kế hoạch (00:05 ngày 06/09):** Trạm **4a đã làm xong** trong tiếng cuối của buổi 05/09,
> và nó đào ra **bug #29** (race condition ở `BM25Index`) chưa fix. Thứ tự dưới đây đã cập nhật.

1. **~2h — Trạm 4 phần còn lại: 4b, 4c, 4d.** Câu 4c hỏi thẳng về bug #25 nên nó dẫn luôn sang mục 2.
2. **~2h — fix bug #25 thật** + test chặn tái phát. Milestone riêng trong roadmap tháng 9.
3. **~1h30 — fix bug #29** (`threading.Lock`) + test. Nghĩ trước hai câu: khoá cả `add_document`
   hay khoá nhỏ hơn? Và test bắt race bằng cách nào — **lại là assert quá trình**, đồng thời phải
   ép đổi luồng (`sys.setswitchinterval`) + lặp đủ nhiều, nếu không test sẽ **xanh giả**.
4. Còn giờ → nối `split_by_separators` (~30-60', milestone nhỏ nhất còn lại của Phase 0).
5. Mốc ôn **+3** của hàng CRAG rơi vào 07/09 — nhớ code-tay-lại phần lõi, đừng chỉ giảng lại.

> Xong mục 1-3 là **Phase 0 đóng sổ** → thứ Hai 07/09 vào **Document-based chunking**, kỹ thuật
> mới đầu tiên của tháng 9. Tính đến hết 05/09 mới xong 3/13 milestone tháng 9 (Trạm 2, 3, 4a) —
> buổi này quyết định tháng 9 có kịp hay không.

> ⚠️ **Luật mới rút ra tối 05/09 (bug #27):** trước khi commit phải chạy `pytest -q` **toàn bộ**,
> không giới hạn thư mục, và đọc `git diff` chứ đừng tin message mình vừa gõ.

## 📌 (lưu trữ) Buổi 2026-09-05 — thứ tự đã chốt tối 04/09

> **Lý do buổi này đổi trọng tâm:** cuối buổi 04/09 user tự báo — *"tôi chỉ hiểu chứ hoàn toàn
> code lại không được, fix bug không được luôn"*. Đây là đúng lỗ hổng mà cả roadmap tồn tại để
> bịt (mục tiêu là **tự implement lõi + tự debug**, không phải đọc-hiểu). Nên T7 **không trace
> thêm trạm mới** — chuyển sang **làm bằng tay**, lấy chính bug #26 làm bài tập vì nó nhỏ, đã
> hiểu rõ, và có sẵn tiêu chí đúng/sai.

**Ca chiều 14:00-16:30 — CODE TAY (không nhìn gợi ý, sai cũng cứ chạy rồi sửa):**
1. Sửa `retrieve_node` để `candidate_k` đọc được từ `state` (closure tụt xuống làm default).
2. Sửa `grade_node` để khi `verdict == "INCORRECT"` thì ghi `candidate_k` lớn hơn vào state.
3. Chạy lại kịch bản grader-luôn-`False`, tự in ra và tự xác nhận dãy `candidate_k` đã tăng dần.
4. Viết **2 test**: (a) dãy `candidate_k` qua từng vòng là tăng dần — *không* phải chỉ assert
   output cuối (test nhìn output cuối sẽ **xanh giả**, đây là bẫy chính); (b) verdict `CORRECT`
   ngay vòng 1 → retriever chỉ được gọi **đúng 1 lần**.

**Ca tối 19:00-21:30:**
5. Mốc ôn +1 của hàng CRAG (giảng lại **và** code lại phần lõi vừa sửa, không nhìn file).
6. Tự kể lại bug #26 + đoạn sửa `03-crag.md` bằng lời mình (2 file đó hiện do Claude viết).
7. Còn thời gian → mở **Trạm 4 (API)** 4a.

> Nếu ca chiều thấy tắc ở **cú pháp Python** chứ không phải logic → dừng, làm drill cú pháp ngắn
> (§3.5 CLAUDE.md), đúng như đã làm hiệu quả 28/08 và 01/09. Đừng ép tiếp.

## 📌 (lưu trữ) Buổi 2026-09-04 — thứ tự đã chốt tối 03/09

1. **Ôn bù 2 hàng đang treo** (Incremental ingest · Retrieval 2 tầng) — chưa được tick, chưa được
   tính mốc +3. Nhắm thẳng vào cặp đã sai: Cặp 1, 2, 8 và Cặp 3, 4, 5, 6 trong
   [the-phan-biet.md](./the-phan-biet.md). Trôi chảy → tick cột +3 ngày 04/09; không trôi → lại
   ôn bù, đừng tick.
2. **Drill Cặp 9 (state ↔ closure)** — cặp mới thêm tối 03/09, sai 4/4 ô, **chưa drill lần nào**.
   ~6 câu ép chọn state/closure, trả lời liên tục, sửa 1 lượt cuối.
3. **Chỉ khi 1 và 2 xong** mới quay lại phần còn nợ của Trạm 3 (bảng trace số thật + teach-back +
   tự sửa note `03-crag.md` + ghi bug-log) — xem
   [pipeline/00-trace-exercises.md § TRẠM 3](./pipeline/00-trace-exercises.md).

> Ca tối 03/09 dừng sớm vì **mệt**, không phải vì nội dung quá khó — user chọn "mệt, muốn dừng"
> khi được hỏi thẳng. Không suy ra là hụt kiến thức nền LangGraph; tầng đó chưa kiểm tra được.
