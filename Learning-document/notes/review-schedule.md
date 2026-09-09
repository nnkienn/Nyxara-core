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
| CRAG closure vs state (`build_graph` 1 lần lúc boot · `candidate_k` đông cứng · van `max_attempts`) | 2026-09-04 | ✅ 2026-09-05 *(code tay, không chỉ giảng lại)* | ⏭️ dời 08/09 → **09/09 vẫn chưa trả** (hiểu ✅, chưa code tay) | ⬜ 2026-09-11 | ⬜ 2026-09-18 | Trạm 3 xong phần **hiểu**, chưa qua phần **làm**. Cặp 9 drill 2 vòng vẫn còn sai `max_attempts` + bài closure Python thuần. Mốc +1 (05/09) phải kèm **code tay bản fix #26**, không chỉ giảng lại. | **+3 (09/09):** `max_attempts` = closure → ✅ **SẠCH lần đầu** sau khi sai dai từ 03/09. Nhưng phần **code tay** dời lần thứ 3 (07→08→09/09) — ưu tiên trả trước tiên. *(cũ)* **+3 chưa làm 07/09** (hết giờ, buổi bị ôn bù + drill cú pháp ăn hết) — phải **code tay lại**, dời sang 08/09.

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

## ✅ Buổi 2026-09-09 (T4) — CA SÁNG 6:00-7:30 XONG · CA TỐI 19:30-22:30

> 08/09 nghỉ (OT) → toàn bộ kế hoạch 08/09 dồn sang hôm nay, cộng **6 mốc ôn tới hạn cùng ngày**.
> Chia ca: **sáng = ôn** (block ngắn, cắt ngang được) · **tối = đóng chunker** (cần 3h liền mạch).

**Ca sáng — làm được:**
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
| CRAG closure ↔ state | +3 (dời **lần thứ 3**: 07→08→09/09) | phần lõi fix #26 (`retrieve_node` đọc state · `grade_node` ghi state) | **1 — trả trước** |
| Incremental ingest | +7 | `get_doc_manifest` + 3 dòng quyết định của `ingest_document` | 2 |
| Thread-safety | +3 | `Lock` trên `self` + test race (kèm `setswitchinterval`) | 3 |
| Retrieval 2 tầng | +7 | `reciprocal_rank_fusion` | 4 |

> Bốn món này **không nhét hết vào ca tối được** (ca tối đã có ~2h20 chunker). Chỉ trả **món 1**
> nếu ca tối còn dư; ba món còn lại đẩy sang 10/09 và **ghi vào kế hoạch 10/09 ngay**, đừng để trôi
> thành nợ ngầm như mốc CRAG đã bị dời 3 lần.

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
