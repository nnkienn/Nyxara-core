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
| CRAG closure vs state (`build_graph` 1 lần lúc boot · `candidate_k` đông cứng · van `max_attempts`) | 2026-09-04 | ✅ 2026-09-05 *(code tay, không chỉ giảng lại)* | ⏭️ dời 08/09 → **09/09 vẫn chưa trả** (hiểu ✅, chưa code tay) | ⚠️→✅ 2026-09-11 → **trả xong 13/09 00:05** *(schema ✅ 4 lượt · `make_grade_node` ✅ XANH 3/3 — nhưng phải đỡ bằng khung điền chỗ trống + 3 lượt nhắc)* | ⬜ 2026-09-18 **ĐÓNG SÁCH, KHÔNG khung** | **+7 (11/09) KHÔNG TICK:** đóng sách thì không bắt đầu được, nhầm node `retrieve` với retriever (BM25/RRF). Dựng lại bằng chạy graph thật in ĐỌC/GHI từng node → hiểu đủ 4 key. Code tay Phần 1 (schema) xanh lượt 4; **Phần 2 `make_grade_node` còn nợ**, chấm bằng [drills/2026-09-11-crag-cham.py](../drills/2026-09-11-crag-cham.py). Xem § Buổi 2026-09-11 ở công ty bên dưới. Trạm 3 xong phần **hiểu**, chưa qua phần **làm**. Cặp 9 drill 2 vòng vẫn còn sai `max_attempts` + bài closure Python thuần. Mốc +1 (05/09) phải kèm **code tay bản fix #26**, không chỉ giảng lại. | **+3 (09/09):** `max_attempts` = closure → ✅ **SẠCH lần đầu** sau khi sai dai từ 03/09. Nhưng phần **code tay** dời lần thứ 3 (07→08→09/09) — ưu tiên trả trước tiên. *(cũ)* **+3 chưa làm 07/09** (hết giờ, buổi bị ôn bù + drill cú pháp ăn hết) — phải **code tay lại**, dời sang 08/09.

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

## 🧭 Từ 2026-09-17: lịch ôn chuyển sang NGÂN HÀNG CÂU HỎI (bảng dưới là LOG, không thêm cột)

> Thiết kế lại 17/09 — nguồn sự thật: [LEARNING_ROADMAP.md § THIẾT KẾ LẠI 2026-09-17](../LEARNING_ROADMAP.md).
> Ôn = tự trả lời câu trong [interview-questions.md](../interview-questions.md) (nói to, đóng sách) + **bài bảng trắng 5'**
> (viết lõi 1 hàm, không chạy, sai cú pháp không sao). Hẹn lại theo kết quả: ❌ +2 ngày · ⚠️ +5 ngày · ✅ +14 ngày.
> Các hàng ⬜ quá hạn ở bảng dưới **không trả theo lịch cũ** — đã quy đổi thành câu hỏi/bài bảng trắng trong hàng đợi ôn.

---

## 📌 Kế hoạch 2026-09-14 (T2) — MỐC 2: Metadata filtering 🔴 (hộp cứng 8h)

> Thứ tự do user chốt tối 13/09: **sáng sớm ở nhà = kỹ thuật mới** · **ở công ty = trace trạm 5** ·
> tối = tiếp mốc 2. Đúng §3.9 — ca chú ý cao nhất dành cho việc nạp cái mới, trace đẩy xuống ca sau.
> Hộp 8h ở nhịp ngày thường (~2h30 giờ-mốc/ngày) → mốc 2 dự kiến đóng **17/09**, tức checkpoint 17/09 = **2/4**.
> ⚠️ Đây là mốc để **đo giả định 6h/mốc**: mốc 1 vừa tiêu 6h30 cho một mốc "dễ". Ghi giờ-mốc thật mỗi ca.


### 🎒 Bộ câu hỏi soạn sẵn cho ca sáng 14/09 *(soạn tối 13/09 — Claude mai đọc thẳng, không nghĩ lại)*

**① Mớm lại cái cũ (2', active recall — đừng bỏ, đây là lúc nối kỹ thuật mới vào cái đã có):**
- Hiện tại một query đi qua Hybrid → RRF → cross-encoder. Trong cả chuỗi đó, chỗ nào **loại bớt tài liệu**,
  và loại dựa trên cái gì? Có chỗ nào loại dựa trên *thuộc tính của tài liệu* (ngôn ngữ, năm, tenant) chưa?
- `tenant_id` hiện đang được dùng ở đâu trong retriever — nó có phải một dạng metadata filtering không?

**② Sau khi Claude giảng 10' (pre-filter vs post-filter), user trả lời — KHÔNG đưa đáp án trước:**
- Kho có 1.000.000 chunk, trong đó 1.000 chunk thuộc tenant A. Query của A, `top_k = 5`.
  Với **post-filter** (search trước, lọc sau): Qdrant tính độ tương đồng trên bao nhiêu vector?
  Số chunk của A còn lại sau khi lọc có thể bằng **0** không — khi nào?
- Với **pre-filter**: con số đó đổi thế nào?
- Cách nào **recall** cao hơn? Cách nào **rẻ** hơn? Vì sao không phải lúc nào cũng chọn cái recall cao hơn?
- Câu chốt: *filter đặt sai chỗ thì hỏng theo kiểu nào — sai kết quả, hay vẫn đúng nhưng thiếu?*

**③ Bài thiết kế — Claude GIẢNG TRƯỚC rồi user chốt (§3.6 mục 7). Ba cách biểu diễn cây predicate:**
| | Hình dạng | Được | Mất |
|---|---|---|---|
| A | dict lồng: `{"and": [{"eq": ["lang","vi"]}, ...]}` | gần JSON, gửi qua HTTP được ngay, dễ in ra đọc | phải tự kiểm tra hình dạng, gõ sai key là lỗi lúc chạy |
| B | tuple: `("and", ("eq","lang","vi"), ...)` | ngắn nhất, viết test nhanh | khó đọc khi lồng sâu, không tự mô tả |
| C | class `And/Or/Not/Eq` | rõ ràng nhất, IDE gợi ý được, khó dùng sai | nhiều code khung, chuyển từ JSON sang phải viết thêm một lớp |
> Claude nêu khuyến nghị + lý do, **user chốt**. Không tự chọn hộ.

**④ Bước 1 code tay — chỉ đưa KHUNG CHỮ KÝ, không mô tả thuật toán (§2):**
```python
def danh_gia(predicate, metadata: dict) -> bool:
    ...
```
Nhắc user một câu duy nhất: *cấu trúc này lồng nhau, và bạn vừa viết một hàm tự gọi lại chính nó tối qua.*
**Ba ca thử thì user tự nghĩ ra** — không được liệt kê hộ (§2).

**⑤ Nếu user tắc quá 5':** hỏi ngược *"một nút `and` cần biết gì từ các nút con của nó để tự quyết định?"*
— không chỉ dòng, không viết mẫu.

**⑥ Luật vận hành bắt buộc, rút ra tối 13/09 ([bug #35](./bug-log.md)):** trước khi tin bất cứ câu *"done"* nào
về file đang mở trong VS Code → chạy `stat -f "%Sm" <file>` xem mtime. Tối 13/09 mất ~30' vì một tab mở từ 06/09
ghi đè bản fix. Và **Claude không tự sửa file user đang mở**, trừ khi user nói rõ.

---

**☀️ Ca sáng sớm (~1h, ở nhà) — KHỞI ĐỘNG MỐC 2, không trace:**
1. **10' Claude giảng khái niệm trước** (đúng §3.6 mục 7 — đây là loại user chưa có vật liệu trong repo để tự suy):
   metadata filtering là gì · **pre-filter vs post-filter** khác nhau thế nào về **recall** và về **chi phí** ·
   vì sao Qdrant có `Filter` riêng mà vẫn phải tự viết predicate ở tầng application.
2. **Bước 1 CODE TAY bắt đầu ngay** — cây predicate (`Filter predicate tree` như roadmap ghi):
   tự viết hàm **đánh giá một predicate trên metadata của một chunk**, dạng cây lồng nhau `AND` / `OR` / `NOT`
   + toán tử lá (`eq`, `gt`, `in`...). **Đây lại là đệ quy** — cùng khuôn `split_by_separators` vừa làm xong đêm qua,
   dùng luôn đà đó.
3. Không đụng Qdrant trong ca sáng. Chỉ dict Python thuần + in ra.

**🏢 Ca công ty — TRẠM 5 trace** ([pipeline/05-chunking.md](./pipeline/05-chunking.md)): 4 lỗi cài + 5a/5b/5c/5d.
Trong đó **5b có bài đóng-sách 10'** — món code tay của mốc 1 mà Claude làm hộ tối 13/09, phải tự viết lại.
⚠️ Máy công ty là Fedora → **`git pull` trước** (tối 13/09 có 5 commit).

**🌙 Ca tối — tiếp mốc 2:** bước 2 BUG CỐ Ý + bước 3 DEBUG BẰNG TAY (in kết quả từng nút của cây predicate).

**Chia hộp 8h (ghi ra để biết lúc nào phải dừng):**
| Bước | Nội dung | Hộp |
|---|---|---|
| 1 | Code tay: đánh giá cây predicate trên dict metadata | 3h |
| 2 | Bug cố ý (gợi ý hướng: nhánh `OR` cư xử như `AND`, hoặc quên `NOT`) | 30' |
| 3 | Debug bằng tay: in kết quả từng nút, tự tìm chỗ hỏng | 45' |
| 4 | Fix + giải thích bug đó làm sai kết quả gì | 30' |
| 5 | Test: regression đúng ca bug + **so pre-filter vs post-filter trên cùng bộ dữ liệu** | 1h30 |
| 6 | Document: `algorithms.md` (WHY) · `glossary.md` · `bug-log.md` · thêm câu vào `interview-questions.md` | 45' |
| 7 | **Nối vào luồng thật** (§3.8): đẩy predicate xuống Qdrant `Filter` trong retriever, trace từ HTTP xuống | 1h |
> Hết 8h là **dừng**, phần dở ghi thành nợ trong roadmap, sang mốc 3. Không gia hạn.

**Chi phí cố định mỗi ngày (đừng để phình):** 10' drill nền + 20' ôn. Hôm nay 3 hàng `+7` đã dời từ 13/09
(`lifespan` code-tay khối shutdown · hợp đồng return · thread-safety) — trả **1 hàng**, hai hàng còn lại ghi rõ là dời.

### 🔁 RE-PLAN 19:15 ngày 14/09 — mất cả ca sáng, ca duy nhất là 21:00-00:00

> **Chuyện gì đã xảy ra:** sáng lên công ty `git pull` không thấy gì mới — 7 commit tối 13/09
> (gồm Trạm 5, bộ câu hỏi ca sáng, và code mốc 1 vừa đóng) **chưa được push**, `origin/main` còn
> đứng ở `d088681` ngày 12/09. Mất trọn ca công ty. Ca sáng ở nhà cũng không chạy.
> → **Giờ-mốc ngày 14/09 tính tới 19:15 = 0.**
> **Luật rút ra ([bug #36](./bug-log.md)):** kết thúc ca ở máy nào cũng phải `git push` **ngay trong
> ca đó**, không để sang hôm sau. Commit chỉ nằm ở máy đó = coi như chưa làm, vì máy kia không thấy.

**Ca tối nay bắt đầu 21:00 → rơi vào ô ❌ của §3.9** (user báo **không OT**, đầu óc còn ổn — nên áp
luật ở mức vừa, không cắt hết). Điều chỉnh:

| Mục kế hoạch gốc | Tối nay | Lý do |
|---|---|---|
| ③ bài thiết kế (chọn kiểu biểu diễn cây predicate) | ❌ **bỏ khỏi ca này** — Claude chốt hộ (xem dưới) | §3.9: bài thiết kế không làm sau 21h |
| ① mớm cái cũ + ② số học pre/post-filter | ✅ giữ | lý luận, không phải đọc code lạ |
| ④ code tay `danh_gia` | ✅ giữ, hộp thu còn ~1h45 | lúc đó đã là "thứ vừa hiểu trong ngày" |
| Trạm 5 trace (4 lỗi cài + 5a-5d) | ⏭️ dời sáng 15/09 | trace **code cũ** — §3.9 bắt để lúc tỉnh |
| Bước 2 (bug cố ý) + bước 3 (debug tay) | ⏭️ dời 15/09 | không nhét vào phần đuôi ca đêm |

**Hộp ca 21:00-00:00 (3h) — hết hộp là dừng, phần dở ghi thành nợ:**

| Giờ | Việc | Ô §3.9 |
|---|---|---|
| 21:00-21:20 | Ôn `+7` hàng **Vòng đời trạng thái**: code tay lại khối shutdown `lifespan` (đóng sách) + trả lời vì sao dựng app lần 2 nổ CUDA OOM | ✅ retrieval practice |
| 21:20-21:30 | Drill nền 10' — cú pháp đọc-chạy trên `dict` lồng (không đụng đệ quy, không mớm lời giải) | ✅ drill |
| 21:30-21:45 | Claude giảng: metadata filtering · **pre-filter vs post-filter** (recall ↔ chi phí) · vì sao Qdrant có `Filter` mà vẫn phải tự viết predicate ở tầng application | ✅ giảng |
| 21:45-22:00 | Câu ② — full-attempt, user trả lời trước, Claude sửa **1 lần** | ✅ lý luận |
| 22:00-23:40 | **Bước 1 CODE TAY** `danh_gia(predicate, metadata) -> bool` | ⚠️ gốc là ❌ sau 21h, mở vì user báo không OT + đây là code **tự viết**, không phải code lạ phải nạp |
| 23:40-00:00 | Ghi sổ giờ · ghi nợ sang 15/09 · commit **và `git push`** | ✅ ghi note |

**Hai hàng `+7` còn lại (hợp đồng return · thread-safety `Lock` + test race) — DỜI, chưa trả.**
Ghi rõ ở đây để không tự lừa là đã trả hết: cả hai đã dời từ 13/09, nay dời tiếp sang 15/09.

**③ Kiểu biểu diễn cây predicate — Claude chốt 19:15 (user có quyền lật, nói một câu là đổi):**

Chọn **A — dict lồng kiểu JSON**: `{"and": [{"eq": ["lang", "vi"]}, {"gt": ["year", 2020]}]}`

Giá cụ thể của từng phương án, đo bằng *số dòng phải viết trước khi chạm được kỹ thuật thật*:
- **A**: 0 dòng phụ. Predicate đến từ body HTTP vốn đã là JSON, và bước 7 của hộp (đẩy xuống
  `Filter` của Qdrant) cũng là dịch dict → dict. Giá phải trả: hình dạng không được kiểm, gõ sai
  key thì lỗi lúc chạy — chấp nhận được vì bước 2-3 của vòng 6 bước **cố tình** đi tìm bug.
- **C (class `And/Or/Not/Eq`)**: rõ nhất, nhưng phải viết thêm ~40-60 dòng lớp dịch JSON → object
  **trước khi** viết được dòng đệ quy đầu tiên. Đó là plumbing, không phải kỹ thuật đang học.
- **B (tuple)**: ngắn nhất khi gõ, nhưng bước 3 là *in kết quả từng nút* — tuple lồng sâu in ra
  gần như không đọc được. Tự bắn vào chân đúng bước debug.

Khung chữ ký duy nhất được đưa (§2 mục 4), không kèm mô tả thuật toán:
```python
def danh_gia(predicate, metadata: dict) -> bool:
    ...
```
**Ba ca thử user tự nghĩ** — không liệt kê hộ.


### ⏸️ CHỖ DỪNG ca sáng 15/09 (5:25-6:35, ~1h10) — đọc dòng này trước khi làm tiếp ở công ty

**Đã xong:**
1. **Giảng mốc 2** (~25'): metadata filtering là gì · lọc theo **thuộc tính** (nhị phân) khác xếp hạng
   theo **độ giống** (điểm số) · pre vs post · vì sao pre không miễn phí (đồ thị HNSW đứt đường khi
   filter hẹp → kho tự chuyển sang quét thẳng) · vì sao có `Filter` của Qdrant vẫn phải tự viết
   predicate ở tầng application (5 lý do, quan trọng nhất: **hybrid có 2 nhánh**, chỉ Qdrant lọc thì
   BM25 vẫn trả về rồi RRF trộn vào).
2. **Full-attempt 5 câu → chấm 2/5.** Ba lỗi phải nhớ:
   - **RRF ăn THỨ HẠNG, không ăn điểm** — `dense_ranked = [hit.id for hit in dense_hits]` vứt `hit.score`
     ngay tại đó; chữ ký `reciprocal_rank_fusion(ranked_lists: list[list[str]], ...)` chỉ có chuỗi id.
     ⚠️ **Lần thứ 2 dính** (09/09 gán nhầm `1/(k+rank)` cho BM25) → lỗi **phân biệt**, phải drill ép chọn,
     chưa thêm vào [the-phan-biet.md](./the-phan-biet.md) — **NỢ**.
   - **`tenant_id` là PRE-filter**, user trả lời post. Nằm ở `QdrantStore.search` (`query_filter=filter`
     truyền vào `query_points`), KHÔNG nằm ở `RerankingRetriever` — chỗ đó `tenant_id` chỉ đi xuyên qua.
   - **Nhánh BM25 không lọc — nó PHÂN VÙNG**: `self.index.get(tenant_id, {})`, tenant là khoá ngoài cùng.
     → repo đang dùng **2 cơ chế khác nhau cho cùng 1 luật** ở 2 nhánh hybrid. Thêm `lang`/`year` vào là
     hai nhánh lệch nhau ngay. **Đây là chỗ mốc 2 sẽ đâm vào.**
3. **Gỡ được bí kiểu A (logic đệ quy)** — user tự nói ra: *"cần hàm biến dict thành true/false"* →
   *"nó tên là `danh_gia`"*. Tự phát hiện đệ quy, không bị mớm.
4. **Drill cú pháp vòng 1** ([2026-09-15-cu-phap-dict-long.py](../drills/2026-09-15-cu-phap-dict-long.py)):
   **đúng hẳn 2/13**. Năm lỗi gốc: L1 quên nấc index · L2 `in` trên dict hỏi key · L3 đếm index từ 1 ·
   L4 `[...]` là list không phải dict · L5 `print` trong `for` ra nhiều dòng.
   ⚠️ File này **không chạy được** — user ghi chú chèn vào dòng code ở bài 10. Không sửa, để nguyên làm chứng.
5. **Giảng "cái thang"** — mô hình một cái chung vá cả 5 lỗi: mỗi cặp `[...]` tụt đúng 1 nấc; dict mở bằng
   **tên**, list mở bằng **số thứ tự**, cùng ký hiệu `[]` nhưng hai việc khác nhau; nấc so le dict→list→dict.

**Dừng ở đâu:** vừa giảng xong "cái thang", user **chưa làm** drill vòng 2. Rồi ngủ quên tới 07:47.

**➡️ VÀO CA CÔNG TY LÀM ĐÚNG THỨ TỰ NÀY:**
1. **[2026-09-15-cu-phap-vong-2.py](../drills/2026-09-15-cu-phap-vong-2.py)** (~15') — 10 bài, dữ liệu đổi hình,
   nhắm đúng L1-L5. Bài 8 vs 9 là cặp ép chọn cho L5. **Đếm ngoặc → nói đang ở nấc mấy → mới trả lời**,
   ghi cả số nấc vào dòng dự đoán.
2. **Chỉ khi vòng 2 sạch** mới gõ `danh_gia(predicate, metadata) -> bool`. Lý do không đảo thứ tự: L1+L3 chưa
   chắc mà viết đệ quy trên cây = **sai âm thầm**, hàm vẫn trả `True`/`False`, không nổ phát nào.
3. Ba ca thử **user tự nghĩ** — không liệt kê hộ.

**Nợ chưa trả (đừng để trôi tiếp):** 3 hàng `+7` (`lifespan` code-tay khối shutdown · hợp đồng return ·
thread-safety `Lock`+test race) — dời từ 13/09, qua 14/09, nay sang 15/09. · Trạm 5 trace. ·
Cặp phân biệt **RRF rank ↔ score** chưa thêm vào `the-phan-biet.md`. · `eq/ne/gt/gte/lt/lte/in` chưa thêm
vào `glossary.md`.

### 🏢 Ca công ty 15/09 — drill vòng 2 xong, ĐỔI THỨ TỰ bước 1 mốc 2 (user chốt)

- Drill vòng 2 + các câu kiểm tra: L1-L5 cơ bản qua; lòi thêm **Cặp 14** (tưởng `q` là cả `qua`) — đã ghi
  vào [the-phan-biet.md](./the-phan-biet.md), Claude viết hộ, **chưa teach-back**.
- Bài cây `p2` ([2026-09-15-predicate-cay.py](../drills/2026-09-15-predicate-cay.py)): tắc ở nấc `[0]`
  (quên tụt nấc, L1), user báo *"phức tạp quá"*. **Gốc khó là độ sâu lồng 6 nấc, không phải kỹ thuật lọc.**
- **Quyết định (user chốt, Claude khuyến nghị B):** bước 1 code tay chia đôi —
  1. **Phẳng trước (ca công ty):** `bo_loc = [{"eq": ["lang","vi"]}, {"gt": ["year",2020]}]`, tất cả phải
     đúng (ngầm AND). Cùng hình dạng `qua` vừa luyện, sâu 3 nấc, không đệ quy.
  2. **Lồng sau (ca tối):** `and`/`or`/`not` đệ quy, dùng lại file cây `p2`. `not` bọc list: `{"not": [pred]}`.
     ⚠️ §3.9: chỉ làm lồng nếu tối bắt đầu ~19h, không OT. Sau 21h/OT → thay bằng test cho bản phẳng.
- **Không phải bỏ bước** — vòng 6 bước giữ nguyên, chỉ đổi thứ tự độ khó.
- **Nói thẳng:** phẳng + lồng hôm nay mới là **bước 1 (hộp 3h)** của hộp 8h. Bước 2-7 (bug cố ý · debug ·
  fix · test so pre/post · document · nối Qdrant **và** BM25) còn ~5h → mốc 2 **không đóng được tối 15/09**,
  dự kiến 16-17/09, đúng dự báo checkpoint 17/09.

**⏸️ CHỖ DỪNG ca công ty 15/09 — bước 1 bản phẳng, đang ráp NÚT LÁ (chưa gõ hàm):**
- Giảng bản phẳng bằng code lần 1 → user *"khó hiểu quá"* (Claude đổ quá nhiều chữ mới 1 lượt: nút lá,
  predicate, `gt`, bộ lọc, chữ ký). **Đổi sang ẩn dụ bảo vệ cửa** (tờ luật = `bo_loc`, dòng luật = điều kiện,
  thẻ tên = `metadata`) → vào ngay, tự nói ra "phải đạt cả 2 luật".
- Đã tự gõ được, từng mẩu: `metadata["year"]` · `metadata["year"] < 2010` · `dieu_kien["lt"][0]` ·
  `ten_truong = dieu_kien["lt"][0]` rồi `metadata[ten_truong]`.
- Vấp trên đường: dịch `{"eq": ["lang","vi"]}` thành "phải bằng lang" (lẫn **chỗ nhìn** với **thứ để so**) ·
  gõ `dieu_kien["lt"]["year"]` (dùng tên trên list — Cặp 13b) · tưởng cần `isinstance` để ra True/False ·
  `list(metadata.keys())[1]` — **lấy tên dòng từ THẺ thay vì từ LUẬT**, chạy ra đúng do may (chép khuôn bài 6).
  Mấy lượt cuối là dấu hiệu mỏi → dừng.
- **Làm tiếp từ đây:** (1) biểu thức lấy `2010` = `[1]`; (2) ráp một dòng so sánh không gõ cứng chữ nào;
  (3) phép cũng phải lấy từ luật (`lt`/`gt`/`eq` là key duy nhất — món `list(d.keys())[0]`), rồi chọn dấu theo
  phép; (4) mới gõ `khop(bo_loc, metadata) -> bool` = vòng `for` qua list luật (hình dạng `qua`).
- **Luật dạy rút ra:** với user lúc mỏi, ẩn dụ đời thường + **một mẩu gõ mỗi lượt** chạy được; giảng bằng
  bảng thuật ngữ thì không.

**⏸️ CHỖ DỪNG ca tối 15/09 (20:40-21:09, không OT) — file đề duy nhất [2026-09-15-toi-mot-luat.py](../drills/2026-09-15-toi-mot-luat.py):**
- User báo *"nhiều đề quá có khi tôi nhầm"* → gom hết vào 1 file, bước 1-4. **Giữ cách này: 1 file đề, không rải đề trong chat.**
- ✅ **Bước 2** (`gia_tri`, so sánh) · ✅ **Bước 3 mẩu (a)** `phep = list(dieu_kien.keys())[0]` · ✅ **mẩu (b)** thay
  `"lt"` bằng `dieu_kien[phep]`. Claude chạy: luật `lt` → `False` đúng; đổi sang `gt` → **không sập** nhưng vẫn
  `False` (vẫn dùng dấu `<`) — đó đúng là việc của mẩu (c).
- Vấp: `isinstance` thay cho `<` (**2 lần** — tưởng phải có hàm mới ra True/False; vá bằng chạy `kq = a < b`) ·
  hai vế ngược (`gia_tri < gia_tri_the`), rồi sửa bằng đổi dấu thay vì đổi vế · `[1]` trên list key dài 1 ·
  thay **cả vế phải** bằng `phep` thay vì chỉ chữ trong ngoặc · **dán cả mũi tên giải thích của Claude vào code**
  (lặp lỗi 06/09) · **xoá mất dòng `gia_tri_the`** đang có người dùng (lặp lỗi cũ). Từ 21:04 là lỗi thao tác
  liên tiếp → dừng code theo §3.9.
- **Sáng 16/09 làm tiếp:** mẩu (c) chọn dấu theo `phep` (`lt` `<` · `gt` `>` · `eq` `==`) — kiểm bằng luật `gt`
  phải ra `True` → bước 4 `khop(bo_loc, metadata)`. Sau đó mới tới bản lồng.
- **Ca 22:00-23:00 tối nay:** không code mới — giảng lại bằng lời "một luật = 3 mảnh, mảnh nào lấy từ luật / từ thẻ" ·
  teach-back Cặp 14 · commit **và push**.

**⏸️ DỪNG HẲN 15/09 ~22:45 — user: *"hết nổi rồi"*.** File giảng lại
[2026-09-15-toi-giang-lai.md](../drills/2026-09-15-toi-giang-lai.md) mới làm A1-A4:
- A1 ✅ (sau 2 lần lẫn: "3 mảnh" ≠ `lt/gt/eq` · ≠ "dict/list/value").
- A2 ❌ còn *"lớn hơn **5**"* — **lấy số trên THẺ đặt vào LUẬT, lần thứ 3 trong tối** → lỗi phân biệt, cần drill ép chọn luật↔thẻ.
- A3 ❌ `list(dieu_kien.keys[0])` → `TypeError` (thiếu `()` của `keys`, `[0]` đặt trong ngoặc — Cặp 13).
- A4 ❌ `phep[0]` → `'g'` (index chuỗi thay vì mở luật); thiếu biểu thức lấy `3`.
- A5 → C4 chưa làm.

**➡️ SÁNG 16/09 (bắt đầu 4:00, ca tỉnh) — làm đúng thứ tự:**
1. **~25', hộp cứng:** sửa A2/A3/A4 + làm A5 → C4 **đóng sách** → Claude chấm **một lần**, chạy thật câu nào có code.
   Nếu câu luật↔thẻ vẫn sai → Claude dựng 5 câu ép chọn "mảnh này nằm trên LUẬT hay THẺ", không giảng lần 3.
2. **Mẩu (c)** trong [2026-09-15-toi-mot-luat.py](../drills/2026-09-15-toi-mot-luat.py): chọn dấu theo `phep`.
   Claude kiểm bằng 3 luật: `lt` → `False` · `gt` → `True` · `eq` trên `"lang"` → `True`.
3. **Bước 4** `khop(bo_loc, metadata) -> bool` — vòng `for` qua list luật (hình dạng `qua`). Ca thử user tự nghĩ.
4. Còn giờ mới sang bản **lồng** (`and`/`or`/`not`, file cây `p2`).
- Giữ cách dạy đã chạy: **1 file đề**, mỗi lượt 1 mẩu, ẩn dụ bảo vệ cửa, Claude chạy code hộ.

**⏸️ CHỖ DỪNG ca sáng 16/09 (05:22-06:45, ~1h25 — user đi làm) — MẨU (c) ĐÓNG:**

- **Chấm giảng lại** [2026-09-15-toi-giang-lai.md](../drills/2026-09-15-toi-giang-lai.md): A1 ✅ · A2 ✅ (đã hết lỗi "lớn hơn 5") ·
  A3 A4 A7 A8 ⚠️ *(biểu thức đúng nhưng chỉ trả lời 1 trong 2-3 ý của đề — lỗi **đọc đề**, không phải lỗ hiểu)* ·
  **A5 ❌** `metadata["tentruong"]` (nháy) · **A6 ❌** sai vế · B1 ⚠️ (gọi `phep` là dict) · **B2 ❌** đảo `gt`/`lt` 2 ô ·
  **B3 ❌** `bo_loc.keys()` trả lời `eq gt lt` (thật ra `AttributeError`, list không có `.keys()`) · B4 ✅ · B5 ⚠️ · **phần C bỏ trống**.
- ⚠️ **Hai lỗi RA ĐỀ của Claude, đừng lặp:** A7 — đảo thẻ theo cách trong đề thì `[1]` vẫn ra `lang_count`, không bẫy được
  (bản đảo đúng: `{"lang","year","lang_count"}` → ra `'year'`). Ván 3 câu 14 — chữ `"lang_count"` có trên **cả hai** giấy nên
  câu hỏi vô nghĩa; hỏi đúng phải là *"lúc chạy, chữ đó được nhặt ra từ đâu"*.
- **Drill ép chọn mới** [2026-09-16-ep-chon-phep-va-giay.py](../drills/2026-09-16-ep-chon-phep-va-giay.py) — **đây là chỗ lòi ra cái lủng thật:**
  - Ván 1 (phép → dấu): **6/6**. ⇒ chẩn đoán ban đầu của Claude ("dán ngược nhãn `gt`/`lt`, giống Cặp 10") là **SAI**.
  - Ván 2 (ra True/False): **2/6**, và 6/6 câu khớp **đúng khít** cột `luat ? the` khi Claude chạy thử cả hai chiều
    ⇒ lỗ thật = **vế nào đứng trước dấu so sánh**. 11/12 (`eq`) sống sót chỉ vì `eq` đối xứng — đừng để nó che chẩn đoán.
  - Ván 3 (LUAT/THE): 6/7 *(câu 14 là đề hỏng)* · câu 19 trả lời **1** ✅ — nắm đúng "chỉ một mảnh lấy từ thẻ".
  - Ván 4 (nháy/không nháy): **2/4**, câu 20 và 21 **đảo chỗ cho nhau** — đúng lại bug A5 tối qua.
- **Cái vá được lỗ (dùng lại kiểu này):** giảng bằng lời + SQL/Qdrant + `a < b ≡ b > a` → user nói thẳng ***"bạn nói tôi éo hiểu"***.
  Đổi sang **kho 3 bài (2015/2021/2022) + luật `year > 2020`, chạy thật cả hai chiều, in ra ai lọt cửa**: cách B cho đúng bài 2015 vào và
  chặn hai bài mới → *"người ta xin tin mới, nó đưa bài cũ, không nổ không đỏ"*. Rồi hỏi đúng 2 câu tiếng Việt (*"bài 2019 có mới hơn 2020 không?"*).
  User tự phát biểu **"7 là False"** → sửa lại ván 2 **6/6**. Ván 4 vá y hệt: chạy thật cho thấy `KeyError` (có tra, sai tên) vs `NameError` (chưa tra, không có biến).
- **Mẩu (c) ĐÓNG** trong [2026-09-15-toi-mot-luat.py](../drills/2026-09-15-toi-mot-luat.py): `if/elif` rẽ theo `phep`, thẻ đứng trước.
  Claude chạy 3 luật, chỉ đổi dòng `dieu_kien`: `lt`→`False` · `gt`→`True` · `eq`→`True` — **đúng cả 3 hợp đồng**.
  - Chuỗi đỏ đi qua, mỗi lượt sửa 1 thứ: `else if` → `elif` · thiếu `:` · `=` → `==` · `return` ngoài hàm → `ket_qua =` ·
    **ghi sẵn `True`/`False` trong nhánh thay vì đi so thật** (user tự nói "sai" khi được hỏi ca `year=2005`) ·
    **xoá nhầm dòng `print(ket_qua)` — lần thứ 5 xoá trúng dòng đang có người dùng.**
  - Phần **ruột đúng ngay lần đầu** (3 phép, 3 dấu, thẻ đứng trước); mọi vòng đỏ đều là **vỏ cú pháp**.
- **Luật dạy rút ra (khớp với hôm qua):** với user, **giải thích dài = hỏng**. Cái ăn tiền là *chạy thật → in hậu quả → hỏi 1 câu tiếng Việt*.
  Ba lần trong buổi này đều vá được bằng đúng công thức đó.

**➡️ LÀM TIẾP (ca công ty 16/09, theo thứ tự):**
1. **Bước 4** `khop(bo_loc, metadata) -> bool` — vòng `for` qua **cả tờ luật**, tất cả đạt mới cho vào. Ca thử user tự nghĩ.
2. Xong mới sang **bản lồng** `and`/`or`/`not` (file cây `p2`).
3. Rồi mới tới bước 2-7 của hộp 8h (bug cố ý · debug · fix · test pre/post · document · nối Qdrant **và** BM25).
- ⬜ **Ôn +14 tới hạn 16/09 — CHƯA LÀM:** *Incremental ingest* và *Retrieval 2 tầng* (cả hai còn nợ code-tay-lại từ mốc +7).
  Trần ôn 20'/ngày — xếp vào ca công ty hoặc ca tối, đừng để trôi thành nợ ngầm như mốc CRAG bị dời 3 lần.
- ⚠️ **Dòng 14/09 trong [so-gio.md](./so-gio.md) vẫn thiếu** — hỏi user ca tối 14/09 (21:00-00:00) làm thật bao lâu rồi điền, trước khi cộng giờ-mốc của mốc 2.

---

## 🌙 Buổi 2026-09-13 (CN) — sinh nhật vợ, bắt đầu 20:34 *(giờ kết thúc điền khi dừng thật)*

> Kế hoạch 5h (07-08h + 13-17h) **không diễn ra**. Buổi mở 20:34 — trước 21h và không OT, nên theo §3.9
> vẫn là **ca tốt**: được đọc code, code tay, làm bài thiết kế.

> ⚠️ **Lỗi ghi sổ của Claude, user bắt được lúc 22:01:** đã ghi buổi này là "20:34-23:00, ~2h30" trong khi
> **chưa xem đồng hồ** — lúc đó mới 21:55. Cùng lỗi với câu "23:10 rồi, ngủ đi" nói trước đó. **Luật: giờ trong
> sổ phải đến từ lệnh `date`, không được suy từ lượng việc đã làm** — đúng tinh thần luật 05/09 "con số trong
> tài liệu phải đến từ một lần chạy thật".

**1. Drill 5 câu — 1/5** (câu duy nhất đúng còn thiếu dấu nháy đóng). Sai:
- `parts["0"]` — **lặp lại nguyên xi** `docs["0"]` của đêm trước, dù đã đo và đã ghi thành [Cặp 13b](./the-phan-biet.md).
- `.extend` ↔ `.append` **đảo ngược hoàn toàn** (đoán `extend` nổ, `append` ra `['a','b','c']`; thật ra ngược lại,
  `append` cho `['a', ['b','c']]` — dài 2, list lồng list). Đây là cặp nằm **ngay trong** `split_by_separators`.
- `chunks.len()` thay vì `len(chunks)` · `separators[1:]` tưởng là dict và tưởng ra một chuỗi.
→ Vá bằng chạy thật + in ra, không giảng.

**2. Câu hỏi của user giữa buổi: "liệu tới Tết kịp?"** → tính lại bằng số thật (~15'):
giờ học 03→13/09 = **2.54h/ngày** (cam kết 3h/6h) · giờ-mốc 11→13/09 = **1.11h/ngày**. Ở nhịp thật,
nội dung xong **02/03/2027 = sau Tết 24 ngày**. Chỉ nhịp 3h thường + 6h cuối tuần mới về đích 03/01/2027.
**User đã đọc bảng và chọn: ưu tiên hiểu, chấp nhận trễ** (*"thà hiểu còn hơn đua thời gian"*). Ghi lại,
không tranh luận thêm trong buổi.

**3. B5 — user chọn phương án C** (không chọn B mình khuyến nghị): *"chơi luôn C cho máu, dễ quá học làm chi"*.
Tách thành **C1** (`re.split` giữ dấu tách, ~40') và **C2** (offset để trích dẫn ngược, ~3-4h → **mốc riêng**,
đi cùng Metadata filtering). Làm C1 tối nay.

**4. C1 ✅ XANH 5/5** — `"".join(kq) == text` đúng cả 5 ca (gồm ca **không có dấu tách nào** và ca **mở đầu bằng dấu tách**):
- Cơ chế: `mau = "(" + re.escape(sep) + ")"` → `re.split(mau, text)` giữ dấu tách thành ô riêng → vòng lặp
  **gom-và-chốt** dán dấu tách vào cuối mẩu trước.
- ⭐ **Vòng lặp đó user tự nghĩ ra**, tự nhận ra nó cùng khuôn với `merge_pieces` mình viết 07/09
  (gom vào biến tạm → gặp dấu hiệu thì chốt → hết vòng chốt phần sót). Bốn lượt sửa sau đó **không có lỗi logic nào**:
  `re.sub` thay `re.escape` · `=` thay `==` · thiếu hẳn bước 3 · `tamp`/`temp` thay `tam` · `if temp:` không kéo ra khỏi vòng lặp.

**5. 🔑 Bài học phương pháp lớn nhất buổi (user nói thẳng giữa chừng):**
*"tại sao phải thay vậy nhỉ tôi chưa hiểu... cứ chép và gõ lại cũng không hiểu được gì cả."*
Claude đã giao bước gõ **trước khi** cho thấy hậu quả. Cái vá được: chạy cùng văn bản qua **đường ống thật**
(`split_by_separators` → `merge_pieces`) ở hai bản cũ/mới → chỉ vào chunk hỏng `'Hà Nội là thủ đô Huế là cố đô'`
(hai sự thật dính làm một, rồi đem đi nhúng vector và dán vào prompt). Khi user vẫn chưa thấy chỗ mất
(*"tôi có thấy dấu chấm nào đâu"*) thì **thu nhỏ ví dụ còn 3 ký tự**: `"A.B"` → `['A','B']` → dán lại `'AB'`.
→ Đã ghi thành memory: **cho thấy hậu quả trước, giao bước gõ sau**.

**Ca đệ quy 2 tầng cũng lossless:** `'Meo thich ngu\n\nCho thich chay'` → `['Meo ', 'thich ', 'ngu\n\n', 'Cho ', 'thich ', 'chay']`,
`"".join(kq)==text` → **True**. `\n\n` được giữ đúng dù cắt ở tầng đệ quy sâu hơn.

⚠️ **`pytest` toàn bộ: 70 passed, 1 FAILED** — `test_splits_by_paragraph_then_word` mong `["Meo","thich",…]`
(hành vi cũ, nuốt dấu tách) nhưng nay ra `['Meo ','thich ','ngu\n\n',…]`. **Test cũ chính là caller bị gãy**
→ gặp thật bài *additive vs breaking* đã ôn 09/09. Câu hỏi giao cho user trả lời đầu buổi sau:
**đây là additive hay breaking, tiêu chí phân biệt là gì?** (đừng sửa test trước khi trả lời).

**6. B8 — NỐI `/ingest` ✅ (21:58, khôi phục lại 22:14 sau khi bị tab chết đè):**
`/ingest` giờ cắt bằng `recursive_chunk` (bọc `split_by_separators` + `merge_pieces`, user tự viết hàm bọc,
xanh ngay lượt đầu). → Câu trong CLAUDE.md §3.8 *"`split_by_separators` có test xanh nhưng không nơi nào gọi"*
**hết đúng từ tối nay**. Kèm `# TODO(B6)` + [bug #34](./bug-log.md) cho `chunk_overlap` bị nhận rồi bỏ qua.

**7. Sửa `test_splits_by_paragraph_then_word` + thêm assert tính chất** `"".join(result) == text`.
Vấp: lần đầu **thêm** assert mới mà **giữ** assert cũ (hai lời hứa cãi nhau, không bao giờ cùng xanh) ·
`assert.` thừa dấu chấm → `SyntaxError`. → **Suite cuối buổi: 71 passed** (đo thật 22:26).

**8. 🚨 [Bug #35](./bug-log.md) — tab VS Code chết từ 06/09 ghi đè bản fix của Claude lúc 22:12.**
Bài học vận hành: **`stat` mtime trước khi tin bất cứ câu "done" nào** về file đang mở trong VS Code.
Việc đầu buổi 14/09: đóng hết tab mở từ trước 12/09.

**9. B3 + B4 ✅ — MỐC 1 ĐÓNG lúc 22:33** *(Claude gõ hộ, user đã nói "mệt quá rồi, fix all đi" — xem việc đóng-sách sáng mai)*:
- **Bug thật tìm ra bằng quét 80 ca, không đoán:** "chunk rỗng" cũ đã tự khử theo C1 (vì `str.split` mới là thứ đẻ ra mẩu `''`).
  Thứ còn lại là họ hàng của nó: **chunk không chứa chữ nào** — văn bản mở đầu bằng dấu tách → `temp` gom được mỗi
  dấu tách rồi chốt luôn → `[' ', 'mo ', ...]`. Vector của khoảng trắng, vẫn chiếm ô trong kho, vẫn được trả về.
- **Fix 2 chỗ, giữ nguyên tính chất lossless:** chỉ chốt khi `temp.strip()` có chữ · phần sót cuối không có chữ thì
  dán vào chunk trước (`ghep[-1] += temp`) thay vì đứng riêng. Quét lại 80 ca: **0 chunk trắng, 0 mất chữ**.
- **5 test mới** (ca gộp thường · ca túi cuối · mẩu dài hơn size giữ nguyên · regression chunk-không-có-chữ ·
  tính chất `"".join == text`). **Đã chứng minh test đỏ được** bằng cách chạy lại logic cũ. Suite: **76 passed**.
- ⚠️ `CHUNK > size` khi `size=3` **không phải bug** — đúng thiết kế user tự chốt 07/09: *size là TRẦN, thà túi lưng
  còn hơn chém đôi một từ*.

**📌 VIỆC ĐẦU TIÊN SÁNG 14/09 (10', đóng sách, trước khi mở Metadata):** tự viết lại một mình đúng 2 dòng fix trên —
điều kiện chốt `temp` khi gặp dấu tách, và cách xử lý phần sót không có chữ. Không mở file, viết ra giấy/editor trống
rồi so. Đây là phần code tay của mốc 1 mà tối nay Claude làm hộ.

**Còn nợ sang buổi sau:**
- ~~Xoá dòng debug `print("PARTS:", parts)`~~ ✅ xong cuối buổi.
- ~~Sửa `test_splits_by_paragraph_then_word`~~ ✅ · ~~B8 nối `/ingest`~~ ✅ — **chỉ còn B3 (bug chunk rỗng) + B4 (test `merge_pieces`)** là đóng mốc 1.
- **B3 bug chunk rỗng** — giờ đã có ca tái hiện chắc chắn: `'.Mo dau bang dau cham'` → `['.', 'Mo dau...']`,
  chunk đầu **chỉ có mỗi dấu chấm**. Vá 1 phát là xong.
- **B6 overlap** (chưa đụng) · **B4** 2 test + regression · **B8** nối `/ingest` → mới đóng được mốc 1.
- **C2 (offset)** = mốc mới, chưa xếp lịch. Trước khi code C2 phải trả lời: đổi `list[str]` → chunk có offset là
  **additive hay breaking**? (tiêu chí: *caller cũ có gãy không* — ôn 09/09).

---

## 📌 Kế hoạch CN 2026-09-13 — chốt 00:35 (5h: 07:00-08:00 · 13:00-17:00)

> Giữa ngày đi câu cá (08:30 → ~13:00). 5h < sàn cuối tuần 6h → nợ nhích lên ≈ **8h59**, không trả được.
> Phương án B **mức 1 đã bật** (dời Versioning sang T10) — xem § RECALC 13/09 trong
> [LEARNING_ROADMAP.md](../LEARNING_ROADMAP.md). **Không re-plan lại trong buổi**, recalc đã làm xong đêm nay.
> Mục tiêu duy nhất của buổi: **đóng mốc 1** (quá hạn) rồi mở được mốc 2.

**Ca sáng 07:00-08:00 — ca tỉnh nhất, dành cho việc cần chú ý nhất (3 câu THIẾT KẾ):**
1. **10'** drill ép chọn [Cặp 13 + 13b](./the-phan-biet.md) — `()` chạy ↔ `[]` tra · trong `[]` để số hay khoá chuỗi.
   Vòng đêm 12/09 là 7/9 và lòi luật sai; phải sạch trước khi code.
2. **B5 giữ separator** — bài thiết kế. **Claude giảng trước**: liệt kê phương án + cái giá của từng cái +
   khuyến nghị, rồi user chọn (luật rút ra 06/09, tái phạm 11/09 — không Socratic thuần cho bài thiết kế).
3. **B6 overlap** — cùng cách: giảng phương án trước, user chọn.

**Ca chiều 13:00-17:00 (4h):**
4. **20' ôn** (trần 20'/ngày). Hôm nay **3 hàng cùng đến hạn +7**: `lifespan` · hợp đồng return · thread-safety.
   Không đủ giờ cho cả 3 → ưu tiên hàng `lifespan`, vì mốc +7 của nó ghi rõ phải **code-tay-lại khối shutdown**,
   không giảng suông. Hai hàng còn lại dời 14/09, ghi rõ là dời chứ không tick.
5. **B7 + B3** — mẩu dài hơn `size` · `merge_pieces` bug **chunk rỗng** (mẩu đầu tiên dài hơn `size`).
   Bản đóng sách sáng 11/09 bị VS Code làm cụt → làm lại từ đầu, code tay.
6. **B4** 2 test (ca gộp thường · ca túi cuối) + **regression test** cho bug chunk rỗng → `pytest -q` **toàn bộ**,
   không giới hạn thư mục, và đọc `git diff` trước khi commit (luật bug #27).
7. **B8 nối `split_by_separators` vào `/ingest`** → **đóng mốc 1** ✅ (ghi giờ-mốc thật vào [so-gio.md](./so-gio.md)).
8. Còn giờ (dự kiến ~1h) → mở **mốc 2 Metadata filtering 🔴** (hộp 8h), bước 1-2 của vòng 6 bước.

**Chặn đúng những chỗ đã ăn giờ tuần này:**
- ⛔ Không mở lại trạm trace cũ. ⛔ Không "ngày vá nền" đứng riêng — nền vá bằng 10' drill + chính phần code tay.
- ⛔ Bug gặp dọc đường → [bug-log.md](./bug-log.md), **không fix**, trừ khi chặn mốc 1 (bug #33 đang ở hàng đợi).
- ⛔ Không viết lại kế hoạch/re-plan trong buổi. Hết hộp giờ mốc 1 → ghi phần dở thành nợ, sang mốc 2.
- 📵 Bước 0 **chưa làm** từ 11/09: 2 bản nháp kẹt trong VS Code Backups (`ingest.py` 06/09 · drill `merge-pieces`).
  **Revert, KHÔNG Overwrite** — Overwrite `ingest.py` là app không khởi động. Làm trước khi gõ dòng code đầu tiên.

---

## 🌙 Buổi 2026-09-12 (T7) — đi làm cả ngày, học 23:13 → 00:20 (~1h)

> Thứ Bảy 6h **mất trọn** (đi làm, đã báo trước tối 11/09). Buổi mở lúc 23:13 → áp
> [§3.9](../../CLAUDE.md) ngay từ đầu: **không** đọc code lạ, **không** 3 câu thiết kế của mốc 1
> (separator · overlap · mẩu dài hơn `size`), **không** nối `/ingest`. Đổi sang drill + code tay
> mẩu nhỏ đang dở. **Giờ-mốc = 0** — mốc 1 quá hạn 1 ngày (hạn 12/09).

**1. Drill ép chọn (~12', 10 + 9 ô)** — nhắm lỗ `set .add` bỏ trùng và `()` ↔ `[]`:
- Vòng 1: **7/10**. Sai: `d("x")` (ô 3) · chọn **list + `.append`** cho việc gom `doc_id` bỏ trùng (ô 8),
  **ngược với chính ô 1 vừa trả lời đúng** (set `.add` trùng → `len` không tăng). Bỏ trống ô `set()` ↔ `{}`.
- ⚠️ Ô 3 sai mà ô 9 (`state["query"]`) đúng → thứ đọng lại đang là **chuỗi chữ gõ tối qua**, chưa phải luật.
- Vòng 2: **7/9**, và lần này lòi ra **cái luật user đang dùng: *"có dấu `:` là dict → `[]`, còn lại `()`"***
  → gãy ở `separators()` (list không có `:`). Vá bằng bảng số thật `not callable` / `not subscriptable`.
- Ngay sau đó: `docs["0"]` → nhét **chuỗi** vào chỗ cần **số thứ tự**. → ghi thành
  [Cặp 13 + 13b](./the-phan-biet.md) kèm output thật.

**2. `make_grade_node` 2d ✅ XANH 3/3** (`[10,20,40]` · `[10]` · `[10]`, `attempts cuối=3/1/1`):
- 2 ô đầu (`"verdict": verdict`, `"grades": grades`) tự điền đúng. Tự xoá được 2 chỗ làm file nổ
  (chữ `←` chép vào code · `import grader`).
- Tắc ở 3 ô còn lại — *"khó hiểu quá"* với khung 5 ô một lượt → **tách thành 3 câu chọn 1-trong-3/2**
  (`"INCORRECT"` · `*` · `return`) thì làm đúng cả 3. **Bài học dẫn: khuya thì mỗi lượt CHỈ một ô.**
- Máy chấm bắt được 2 lỗi nối tiếp, cả hai đều là **van `attempts` không đóng**:
  (1) `GraphRecursionError`, nhật ký phồng `[10,20,40,80,…,40960]` → thiếu hẳn khoá `attempts`;
  (2) `NameError: name 'attempts' is not defined` → ghi khoá đúng nhưng **tên bên phải chưa tồn tại**
  (chưa lấy từ state) — cùng họ "chưa nối dây";
  (3) ghi `attempts` **đúng bằng** giá trị đọc ra → con đếm đứng yên, `attempts cuối=0` in ngay trong
  nhật ký mà lượt đầu **đọc qua không thấy** (2 lượt liên tiếp sửa nửa chỉ dẫn) → phải trích đúng ô + mũi tên mới sửa.
- **Giảng lại ✅ cả 2 câu:** vì sao `attempts` ghi mọi lượt mà `candidate_k` chỉ ghi khi INCORRECT ·
  `max_attempts` = **closure** (đông cứng lúc `build_graph` ở boot) vs `attempts` = **state** (riêng mỗi request).
  → **Cặp 9 sạch lần thứ 2**, lần này có code xanh chứng minh. Nợ ôn +7 CRAG (treo từ 11/09) **trả xong**.

**Số thật cuối buổi:** nợ giờ ≈ **7h59 → vượt trần 6h lần đầu** (xem [so-gio.md](./so-gio.md)).
Mốc 1 còn nguyên: B3 bug chunk rỗng · B4 2 test + regression · B5/B6/B7 (3 câu thiết kế) · B8 nối `/ingest`.
**Checkpoint 17/09** cần ~20h30 giờ-mốc (mốc 1 ~2h30 + Metadata 8h + Document-based 5h + MMR 5h) nhưng
13→17/09 chỉ có ~14h45 (CN 4h45 + 4×2h30) **trước khi trừ trả nợ** → **nhiều nhất 3/4, thực tế 2/4-3/4**
→ **phương án B gần như chắc bật** (dời Versioning, có thể thêm Temporal).

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
- **B2 phần 2 — 2a (vỏ `make_grade_node`) ✅ 00:09 ngày 12/09**, sau khi Claude đổi sang **khung điền chỗ trống**
  (ví dụ "quán chào" + bảng đối chiếu → user: *"khó hiểu quá, bên kia dễ hơn"*; khung 3 chỗ trống thì làm được).
  Vấp: xoá mất dòng `...` → `IndentationError: expected an indented block` (thân hàm trong rỗng) → thêm lại là chạy.
  Máy chấm in `dùng BÀI CỦA BẠN` ✅. ⚠️ 2 kịch bản báo **XANH GIẢ**: `verdict=None`, `attempts=0` — node chưa chấm
  gì, nhật ký `[10]` khớp chỉ vì graph đi thẳng. *(Claude dự đoán sai "3 kịch bản sẽ NỔ" — LangGraph bản này coi
  `None` là "không cập nhật state".)*
- **2b (lấy key từ `state`) ✅ 00:15** — lượt đầu `state(query)` / `state(retrieved_docs)`: **ngoặc tròn** thay ngoặc
  vuông + **thiếu dấu nháy** (dù khung ghi `[ ]` và đã nhắc nháy). Claude cho chạy ví dụ danh bạ: `danh_ba("Lan")` →
  `TypeError: 'dict' object is not callable` · `danh_ba[Lan]` → `NameError` · `danh_ba["Lan"]` → `0901` → sửa đúng
  ngay lượt sau: `state["query"]`, `state["retrieved_docs"]`. Graph chạy không nổ, vẫn xanh giả (đúng dự đoán — hiệu quả
  chỉ thấy từ 2c). Lỗi `()` gọi hàm ↔ `[]` tra dict là **lần thứ 2 trong 24h** (`current(piece)` tối 11/09).
- ⚠️ **§3.9 mục 5 chạm tại 00:15:** 2 lượt liên tiếp dính lỗi **nhìn** (2a xoá mất `...` có sẵn trong khung · 2b gõ `( )`
  dù khung ghi `[ ]`). Claude khuyên dừng sau 2b; user quyết.
- **2c (gọi grader + `decide`) — logic ✅ 00:22, nhưng file thật chưa chạy được:** `grades = grader.grade(query, docs)` ·
  `verdict = decide(grades, correct_threshold, incorrect_threshold)`. Chạy máy chấm trên **bản sao** đã bỏ 2 chỗ lỗi bên dưới →
  in đúng `CHẤM: [F,F,F] INCORRECT` · `[T,T,T] CORRECT` · `[T,F,F] AMBIGUOUS`. Hai lỗi **không phải logic** trong file thật:
  (1) **chép nguyên chữ chú thích `← dòng tạm...` của Claude vào code** → `SyntaxError: invalid character '←'`. Lần thứ 2
  dính kiểu "copy lời giải thích như thể là code" (lần 1: 06/09). **Lỗi của Claude:** khung *để gõ theo* không được có
  mũi tên chú thích trên dòng code — dùng `#` hoặc ghi ngoài khối.
  (2) tự thêm `from app.domain.ports.grader import grader` → `ImportError`: module chỉ có **class `Grader`** (cái khuôn /
  port), không có `grader`. Còn `grader` trong `make_grade_node` là **tham số** do `build_graph` truyền vào — không cần
  import. Cùng họ "tên na ná → tưởng là một thứ" (Cặp 12 · `fixed_size_chunk` gắn nhầm retriever).
- ⚠️ §3.9 mục 5: **lượt thứ 3 liên tiếp** dính lỗi không-phải-logic (00:22).
- ⬜ Còn: sửa 2 chỗ trên (xoá chữ sau `print(...)` · xoá dòng import) → **2d** dựng dict kết quả (`candidate_k` chỉ khi
  INCORRECT) → bỏ dòng `print` tạm.
- ⬜ **Bước 0 chưa làm**: 2 bản nháp kẹt (`ingest.py` 06/09 · drill `merge-pieces` 07:38) vẫn còn trong VS Code Backups lúc 00:09.
- **Rút ra về cách dẫn:** với user này lúc khuya, **khung điền chỗ trống** ăn hơn ví dụ song song + bảng đối chiếu
  (bảng đối chiếu bắt nạp 2 đoạn code cùng lúc — đúng loại việc §3.9 cấm sau 21h).

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
