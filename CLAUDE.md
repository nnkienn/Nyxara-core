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
5. **(thêm 2026-09-10) Chỉ dòng code bằng NGUYÊN VĂN, không bằng số dòng** — nhất là trong file drill user
   đã chèn dự đoán/ghi chú vào: số dòng lệch ngay, user hiểu nhầm dòng nào (gặp thật tối 10/09: bảo "xoá
   dòng 115" → user tưởng là `vi = tien`). Viết lại cả dòng, kèm mũi tên `← XOÁ dòng NÀY` trong khối code.

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
7. **(vá 2026-09-06, sau khi mục 6 bị tái phạm 2 lần trong 1 buổi)** Phân biệt **câu hỏi TRACE**
   với **câu hỏi THIẾT KẾ**. Câu trace ("dòng này chạy ra gì", "biến này lấy từ đâu") — user có
   đủ vật liệu trong code để tự suy, cứ hỏi thẳng. Câu thiết kế ("nên sửa theo hướng nào", "đặt
   trạng thái ở đâu", "chọn kiểu dữ liệu gì") — user **chưa có vật liệu**, vì đó là kinh nghiệm
   chứ không nằm trong file nào. Với loại này: **GIẢNG TRƯỚC** — liệt kê 2-3 phương án, nêu cái
   giá cụ thể của từng cái (đo bằng số dòng phải sửa / số test gãy / giờ bỏ ra), đưa **khuyến
   nghị kèm lý do** — rồi mới hỏi user chốt. Hỏi trần một câu thiết kế = user đoán mò hoặc tắc.
   Dấu hiệu đã lỡ vi phạm: user trả lời *"không hiểu bạn hỏi gì"* hoặc *"khó quá"*.

---

## 3.8 Trace KHÔNG dừng lại · Ngân hàng câu hỏi phỏng vấn (chốt 2026-09-06)

Bài trace 4 trạm ([00-trace-exercises.md](Learning-document/notes/pipeline/00-trace-exercises.md))
đã xong hết ngày 06/09. Nhưng **trace không phải một giai đoạn đã qua** — nó là thói quen thường trực:

1. **Mỗi kỹ thuật mới học xong đều phải trace lại**, đúng cách ở §3.5: đọc thân hàm thật (không tin
   tên hàm, không tin note), điền bảng bằng **số liệu thật**, tự cài lỗi vào note rồi tìm lại.
   Lý do: 5 bug nặng nhất của dự án (#25 → #32) đều lòi ra **trong lúc trace**, không phải lúc xây.
2. **Kỹ thuật mới cũng phải nối lại vào luồng đang chạy** và trace từ HTTP request xuống — không
   để nó nằm mồ côi. Bài học `split_by_separators`: có test xanh, không nơi nào gọi, tưởng đã có
   mà thực ra chưa bao giờ chạy thật.

**Ngân hàng câu hỏi phỏng vấn:** [Learning-document/interview-questions.md](Learning-document/interview-questions.md)
— 65 câu, chia 10 chủ đề × 3 mức 🟢 Junior / 🟡 Mid / 🔴 Senior. Mục đích: biến thứ **đã xây được**
thành thứ **nói ra được** trong phòng phỏng vấn (qua Tết ~đầu 2027).

- **File cố ý KHÔNG có đáp án.** Đáp án nằm ở note user đã tự viết; cột *Note* trỏ tới đó.
- **Quy trình bắt buộc:** đóng tài liệu → trả lời thành tiếng/gõ ra hết khả năng → **rồi mới** mở
  note đối chiếu → chấm ✅/⚠️/❌ → câu ❌⚠️ vào vòng ôn kế tiếp.
- ⚠️ **Đọc câu hỏi rồi đọc luôn đáp án là vô ích** — cảm giác "à mình biết mà" là *ảo giác quen
  thuộc*, không phải trí nhớ. Đúng thứ đã làm hỏng 6.5 tuần đầu. Phải cố nhớ ra trước, kể cả nhớ sai.
- **Thêm câu mới sau mỗi kỹ thuật học xong** — tính là một phần của bước 6 DOCUMENT (§3).
- Claude được phép dùng file này làm nguồn cho **active-recall giữa buổi** (mớm hỏi kỹ thuật cũ
  ngay trong lúc làm kỹ thuật mới), nhưng **không đọc đáp án hộ** — vẫn theo §2.

> **Về "học nhồi":** user nêu ý này ngày 06/09 vì sốt ruột tiến độ. Ghi rõ để không trôi: **nhồi
> kiểu đọc đi đọc lại chính là thứ đã hỏng 6.5 tuần đầu.** Cái nhanh hơn thật sự là **tự vấn đáp
> có cách quãng** — đã có bằng chứng trong chính dự án này: drill phân biệt đưa 1/4 → 11/12 trong
> **một** vòng, còn giảng lại lần hai thì 12 tiếng sau vẫn lẫn. Nên tăng tốc = tăng **số lần tự
> lôi ra khỏi đầu**, không phải tăng số lần đọc.

---

## 3.9 Xếp việc theo mức tỉnh táo — KHÔNG đọc code lúc mệt (chốt 2026-09-09)

> Đo được thật trong đúng một ngày 09/09: **ca sáng 6:00-7:30** trả lời drill **9/13**, có mấy câu
> rất chắc (khoá `BM25Index` đủ 3 tầng, `retrieve_node` gõ đóng sách đúng nguyên văn). **Ca tối
> 21:30-22:01 sau OT**, cùng một người, bảng trace **lệch một ô mỗi dòng**. User tự báo:
> *"đọc code tối tôi không load nổi"*.

**Điều quan trọng: gần như 100% lỗi ngày 09/09 là lỗi CHÚ Ý, không phải lỗi HIỂU.** Đếm được:
`len("Meo")=2` (đọc chỉ số cuối thay vì độ dài) · kéo ô của lượt 1 xuống lượt 2 · nhét
`current_merge` vào `merges` ở nhánh không hề đụng `merges` (2 lần) · nhìn nhầm `if` dòng 35 (ngoài
vòng lặp) thành `if` dòng 29 (trong vòng lặp) · chọn `attempts` chỉ vì file đang mở ở dòng đó ·
gắn `fixed_size_chunk` vào retriever. **Không lỗi nào trong số này chữa được bằng giảng thêm.**
Chúng chữa bằng **ngủ đủ và làm đúng việc vào đúng giờ**.

> ⚠️ **Sửa lại 2026-09-10 — câu "gần như 100% là lỗi CHÚ Ý" ở trên NÓI QUÁ.** Ca chiều 10/09, lúc
> **tỉnh táo**, user vẫn sai cột `merges` 3 ô, và bóc ra **6 lỗ nền mô hình chạy Python** (thụt lề =
> phạm vi · luồng `for` · `+=` chuỗi ↔ `append` list · giá trị biến tại đúng lúc dòng chạy · `{}` ↔ `[]`) —
> xem [review-schedule.md § Buổi 10/09](Learning-document/notes/review-schedule.md). Tức là **mệt
> KHUẾCH ĐẠI lỗi, nhưng gốc là lỗ hổng HIỂU thật.** Luật xếp việc bên dưới **vẫn giữ nguyên** — chỉ
> sửa lý do: ngủ đủ không tự vá được lỗ nền; lỗ nền phải vá bằng drill đọc-chạy, và drill đó nên
> làm lúc tỉnh để lỗi lòi ra là lỗi hiểu, không lẫn với lỗi mệt.

**Luật xếp việc:**

**Mốc chia KHÔNG phải "sáng / tối" mà là GIỜ BẮT ĐẦU + có OT hay không.** Ca tối bắt đầu ~19h
khi về sớm vẫn là ca tốt — đừng đọc luật này thành "cấm học buổi tối".

| Ca | Hợp với | KHÔNG hợp |
|---|---|---|
| **Sáng, đầu óc sạch** | đọc thân hàm lạ · trace điền bảng số thật · debug · bài thiết kế | — |
| **Tối bắt đầu ~19:00-19:30, về sớm, không OT** | **y như ca sáng** — code tay, đọc code, trace, debug đều được | — |
| **Bắt đầu sau ~21h, hoặc vừa OT về** | drill ép chọn A/B · giảng lại bằng lời · viết note/ghi bug-log · viết test cho thứ **đã hiểu rõ trong ngày** | ❌ **đọc code chưa nạp vào đầu** · ❌ trace code cũ · ❌ bài thiết kế |

> **Bằng chứng cho dòng giữa (đừng cắt ca tối sớm — nó là ca có sản lượng cao nhất dự án này):**
> **05/09 19:55-23:45** — buổi code tay đầu tiên và tốt nhất: drill closure 4/4, tự code xong fix
> bug #26, tự viết 2 test bắt quá trình, phát hiện + fix bug #27.
> **06/09 20:45-22:45** — Trạm 4d + tự fix bug #29 (`Lock`) + test 4 luồng, tự chứng minh test đỏ được.
> **07/09 20:45-22:41** — `merge_pieces`, hàm đầu tiên user tự viết trọn vẹn không Copilot.
> Ca hỏng duy nhất là **09/09 21:30 sau OT** — bắt đầu muộn **và** vừa tan ca.

1. **Việc "nạp code lạ vào đầu" chỉ làm lúc tỉnh.** Đọc thân hàm chưa quen, trace code viết từ buổi
   trước, debug — đây là loại tốn chú ý nhất, và là loại sinh ra lỗi rác phải đi sửa hôm sau.
   Làm nó lúc mệt = tốn giờ thật mà sản lượng gần 0, lại còn ghi note sai vào repo.
2. **Ngoại lệ cho trace:** được trace vào buổi tối **nếu là code chính mình vừa viết trong ngày** —
   lúc đó code đã ở sẵn trong đầu, không phải nạp lại. Còn trace code cũ thì để sáng.
3. **Buổi tối vẫn tính giờ, chỉ đổi nội dung.** Đừng bỏ buổi (nợ giờ là deadline lùi thật, §sổ giờ),
   cũng đừng ép đọc code. Đổi sang drill/giảng lại/ghi note là vẫn tiến, vẫn đúng Method 2.0
   (retrieval practice mới là thứ ăn tiền, không phải số dòng code đọc được).
4. **Claude phải chủ động hỏi khi buổi bắt đầu sau 21h HOẶC user báo vừa OT về:** *"hôm nay OT à —
   đổi sang drill/giảng lại thay vì đọc code nhé?"* Đừng chờ user tự nhận ra lúc đã ngồi 30 phút.
   Buổi tối bắt đầu ~19h thì **không cần hỏi**, cứ xếp việc như ca sáng.
5. **Dấu hiệu phải dừng ngay, không cần hỏi thêm:** sai 2 lượt liên tiếp mà cả 2 đều là lỗi **đọc**
   (nhìn nhầm dòng, nhầm biến, tính nhầm độ dài) chứ không phải lỗi lý luận.

> Không mâu thuẫn với luật cấm "phạt bằng cách cắt giấc ngủ" ở [so-gio.md](Learning-document/notes/so-gio.md):
> luật này **bảo vệ** đúng thứ đó — ngủ đủ để ca sáng còn dùng được, thay vì đốt cả hai đầu.

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

⏰ **Trước khi chốt nội dung buổi, xem giờ đã** — nếu buổi bắt đầu sau **21h** *hoặc* user báo vừa
OT về, áp [§3.9](#39-xếp-việc-theo-mức-tỉnh-táo--không-đọc-code-lúc-mệt-chốt-2026-09-09): **không
xếp việc đọc code / trace code cũ**, đổi sang drill ép chọn hoặc giảng lại bằng lời.
Buổi tối bắt đầu **~19:00-19:30 khi về sớm thì xếp việc y như ca sáng** — đó là ca có sản lượng cao
nhất dự án này (05/09, 06/09, 07/09), đừng cắt nhầm nó.

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
.venv/bin/python -m pytest -q                   # toàn bộ test — CHẠY TOÀN BỘ, không giới hạn thư mục
uvicorn app.main:app --port 8000                # KHÔNG --reload (xem bug #31)
export OLLAMA_BASE_URL=http://<host>:11434      # bắt buộc, Ollama qua Tailscale
```

**Dựng môi trường trên máy mới** (`.venv` KHÔNG đi qua git — xem §7):
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```
Lần chạy `pytest` đầu tiên sẽ tải ~4.4GB weights (bge-m3 + bge-reranker-v2-m3) về
`~/.cache/huggingface` → **~18 phút**. Các lần sau ~2 phút. Đo thật trên Fedora 44 /
Python 3.14.7 / RTX 4060 8GB ngày 06/09: **70 passed in 127.34s**.

**Bẫy đã biết:**
- ~~`data/manifest.json` lệch pha với 3 kho in-memory~~ → **bug #25 đã FIX 06/09**: manifest giờ
  là `dict` trong RAM (`app.state.manifest`), chết cùng tiến trình như 3 kho. Không còn file
  manifest, không cần `rm` gì nữa.
- **VRAM:** `lifespan` nạp 2 model BGE fp32 (~2.3GB VRAM mỗi cái) trên GPU 8GB. Đã thêm khối
  shutdown sau `yield` để nhả ra (bug #31). Đừng bỏ khối đó — bỏ là `--reload` hoặc test dựng
  app nhiều lần sẽ CUDA OOM.

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
  *(⚠️ `/ingest` từng gãy âm thầm 28/08→05/09 vì bug #27, đã fix. Suite: **70 passed**, đo thật 06/09 trên máy Fedora mới.)*
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
  **2026-09-03 ca tối (~1h): mở Trạm 3 (CRAG), làm được nửa đầu rồi dừng vì mệt.** Bảng
  state-vs-closure của `retrieve_node`: **user đảo ngược cả 4 ô** (nói `tenant_id`/`query` là
  closure, `candidate_k`/`top_k` là state — suy từ *ý định* "CRAG phải tìm rộng hơn" thay vì đọc
  code). Đã sửa + giải thích bằng ẩn dụ "đúc khuôn 1 lần": `build_graph()` chạy 1 lần → hàm
  `retrieve_node` được đúc 1 lần → `candidate_k=10`/`top_k=5` khắc chết trong closure → 4 input
  lần 2 y hệt lần 1 → `verdict` không bao giờ khá lên → vòng lặp chỉ thoát bằng van an toàn
  `attempts >= max_attempts` rồi generate trên đúng đám docs vừa bị chê. **Xác nhận note nói dối:**
  chữ "tìm rộng hơn" trong `03-crag.md` là thứ định làm mà code chưa làm. User suy đúng hướng fix
  (đọc `candidate_k` từ `state`), sai chỗ đặt (nói `retrieve` ghi → thực ra `grade_node`, nơi đã
  đếm `attempts`). Đã thêm **Cặp 9 (state ↔ closure)** vào `the-phan-biet.md`, chưa drill.
  **Còn nợ ở Trạm 3:** bảng trace số thật · teach-back 2 ý · tự sửa `03-crag.md` bằng lời mình ·
  ghi bug vào `bug-log.md`. Trạm 4 chưa đụng.
  ⚠️ **Lỗi phương pháp của Claude tối 03/09 (đã ghi vào 00-trace-exercises.md):** 2 lần liên tiếp
  gộp nhiều tầng suy luận vào 1 lượt hỏi (teach-back 2 ý cùng lúc) → user tắc ngay, lặp lại đúng
  lỗi §3.6 mục 6 đã vá 01/09. Trạm này lần sau: 1 ô bảng / 1 câu, số thật, không hỏi "vì sao"
  trừu tượng khi cơ chế chưa vững.
  ⚠️ **04/09 thứ tự bắt buộc:** ôn bù 2 hàng treo → drill Cặp 9 → mới quay lại Trạm 3.
  Xem [review-schedule.md § Buổi 2026-09-04](Learning-document/notes/review-schedule.md).
  **2026-09-04 (21:42-23:30, OT về trễ nên chỉ 1h45): TRẠM 3 XONG PHẦN HIỂU.** Ôn bù 2 hàng treo
  **9.5/10** (hôm trước 1/4) → đã tick mốc +3. Drill Cặp 9 hai vòng, vẫn còn sai `max_attempts`
  (đoán state, thực ra closure) + bài đoán output closure Python thuần (4/5 dòng sai).
  **Chỗ tắc thật mất 3 lượt mới lòi ra:** không phải closure — mà là **không biết `build_graph()`
  chạy lúc nào**; user hỏi thẳng "chạy hồi nào?". Thiếu mảnh vòng đời app (`lifespan` trước
  `yield` = 1 lần lúc boot · `ask.py` chỉ lấy lại `app.state.graph`). **Thứ gỡ được nút, ghi nhớ
  để dùng lại:** khi user đã trượt dự đoán 2-3 lượt liên tiếp thì **thôi bắt tưởng tượng, cho
  chạy thật và in ra** — chạy `build_graph` + 3 node thật với 4 adapter giả, in `candidate_k` mỗi
  vòng; 3 dòng `candidate_k=10` giống hệt nhau nói được điều mà 3 lượt giải thích không nói nổi.
  Đã ghi [bug #26](Learning-document/notes/bug-log.md) + sửa note nói dối "tìm rộng hơn" trong
  `03-crag.md` — **nhưng do Claude viết, chưa qua bước 6 DOCUMENT thật**, user hẹn tự kể lại 05/09.
- 🚨 **User tự báo cuối buổi 04/09 — cái quan trọng nhất tuần này:** *"tôi chỉ hiểu chứ hoàn toàn
  code lại không được, fix bug không được luôn"*. Đúng lỗ hổng mà §1 đặt ra để bịt (mục tiêu là
  **tự implement lõi + tự debug**, không phải đọc-hiểu trôi chảy). **Hệ quả đã chốt:** buổi T7
  05/09 **không trace thêm trạm mới**, chuyển sang **code tay** — lấy chính fix #26 làm bài (nhỏ,
  đã hiểu rõ, có tiêu chí đúng/sai rõ) + 2 test regression. Chi tiết từng ca:
  [review-schedule.md § Buổi 2026-09-05](Learning-document/notes/review-schedule.md).
  Từ đây trở đi: **mỗi trạm trace xong phải kèm một việc làm bằng tay**, không dừng ở "hiểu rồi".
  **2026-09-05 (19:55-23:45, nghỉ 20' → ~3h30): buổi CODE TAY đầu tiên, và nó chạy.**
  - Drill closure tự viết 4/4 bài ([drills/2026-09-05-closure.py](Learning-document/drills/2026-09-05-closure.py))
    — kể cả bài **cố ý gây lại** `UnboundLocalError` rồi tự sửa. Tự lý luận đúng "mỗi lần gọi
    factory là một hàm mới" (hôm 03/09 trả lời sai đúng câu này).
  - **Tự code xong bản fix bug #26**, 3 chỗ: `retrieve_node` đọc state · `grade_node` ghi state ·
    `state.py` khai báo `candidate_k`. Kiểm chứng trên graph thật: `10→10→10` đã thành `10→20→40`.
  - **Tự viết test bắt quá trình** (`RecordingRetriever` + assert dãy `[10,20,40]`) và tự kiểm
    chứng nó đỏ đúng lúc phải đỏ. Chính test này phát hiện chỗ thứ ba (schema vứt khoá) mà cả
    user lẫn Claude đều đọc qua không thấy.
  - **Tự chẩn đoán được `return grade_node` bị thiếu** chỉ từ thông báo lỗi, không cần gợi ý.
  - Phát hiện + fix **bug #27**: commit tài liệu 88e6b7d (28/08) âm thầm xoá `save_manifest` →
    `/ingest` gãy và `pytest` toàn bộ chết ở collection suốt **8 ngày**. Sau fix: **67 passed**.
  - Lỗi lặp lại cần để ý: **2 lần sửa nhầm hàm**, 2 lần xoá mất dòng đang có người dùng
    (`attempts = ...`, `return grade_node`), 1 lần lẫn "khoá state" với "node"
    (`add_node("candidate_k", ...)`). Đều là lỗi lúc mệt, không phải lỗi hiểu — nhưng mỗi lần
    ngốn ~15 phút.
  - **Tiếng cuối (23:16-00:05):** tự viết nốt test nhánh ngược `test_khong_retry_khi_grader_hai_long`
    (chọn `== [10]` thay vì `len(...) == 1` — kiểm cả số lần gọi lẫn giá trị) → **68 passed**.
    Rồi làm luôn **Trạm 4a**: xác định `BM25Index` chỉ có 1 instance dùng chung cả server, và
    `bm25_index.py:16` là đọc-sửa-ghi không nguyên tử trong khi handler `def` chạy đa luồng →
    **race condition**, đã dựng thực nghiệm chứng minh mất 56.9% số lần cộng. Ghi thành
    [bug #29](Learning-document/notes/bug-log.md), **chưa fix**.
  - **Sợi chỉ xuyên suốt cả buổi, đáng nhắc lại mỗi khi gặp trạng thái dùng chung:** *thứ này
    thuộc về **cả server** hay thuộc về **một lượt chạy** — và có ai **ghi** vào nó không?*
    Dùng chung + chỉ đọc → an toàn. Dùng chung + có ghi → phải có người canh.
  **2026-09-06 (CN, ~4h, 13:30-17:30 — ĐỔI MÁY sang Fedora 44 mới):** mất ~40' dựng lại `.venv`
  (không đi qua git) + tải 4.4GB weights. **Trạm 4b và 4c XONG, và fix thật được 2 bug.**
  - **Trạm 4b → [bug #30](Learning-document/notes/bug-log.md):** `/ingest` trả `chunk_count` đếm
    **nhát cắt**, client đọc thành **số chunk ghi vào kho**. Fix: `ingest_document` đổi `-> None`
    thành `-> dict[str,int]`, response **thêm** 3 trường (additive change). User tự chọn `dict`
    thay `tuple` và tự lý luận đúng additive vs breaking.
  - **Trạm 4c → FIX THẬT [bug #25](Learning-document/notes/bug-log.md)** sau 23 ngày treo. Chọn
    hướng **"cùng dễ vỡ"**: manifest bỏ file, thành `dict` trong RAM cạnh 3 kho. Kèm test giả lập
    restart bằng **2 khối `with TestClient(app)` ngang hàng**, và **đã chứng minh test đỏ được**.
  - **[Bug #31](Learning-document/notes/bug-log.md) — MỚI, lòi ra khi viết test #25:** `lifespan`
    không có phần shutdown sau `yield` → 2 model BGE không được nhả → dựng app lần 2 là **CUDA
    OOM** (GPU 8GB còn trống 23MB). Đã thêm khối dọn; sau fix `nvidia-smi` báo 21 MiB.
  - Suite: **70 passed in 127.34s** (chạy toàn bộ, đo thật).
  - **Sợi chỉ của buổi, gặp 3 lần trong 1 ngày:** `recursive_chunk` không đệ quy · `chunk_count`
    không đếm cái nó có vẻ đếm · `test_..._restart` không hề restart. **Tên nói một đằng, thân
    làm một nẻo** — trước khi tin bất cứ cái tên nào, đọc thân.
  - **Lỗi lặp lại lần thứ 3 (đáng lo):** gọi hàm mà **không hứng giá trị trả về** → bịa số vào
    response. Cùng dạng với `split_by_separators` mồ côi và schema `candidate_k` thiếu khoá.
    Kiểm tra bắt buộc sau mỗi lần đổi chữ ký: *ai đang hứng giá trị này?*
  - **Vấp khác:** viết `from httpx import request` + `request.app.state` **trong tầng
    application** (`pipeline.py`) — bẻ ngược mũi tên kiến trúc hexagonal; lồng 3 khối `with`
    thay vì nối tiếp (thụt lề = phạm vi sống).
  - ⚠️ **Lỗi phương pháp của Claude:** 2 lần hỏi câu **thiết kế kiến trúc** trước khi giảng khái
    niệm → user phải nói *"không hiểu bạn hỏi gì"* và *"bạn là giáo sư mà không thể để tôi mù mờ
    như này"*. Tái phạm §3.6 mục 6. **Luật bổ sung: bài THIẾT KẾ (chọn giữa nhiều kiến trúc) thì
    GIẢNG TRƯỚC — liệt kê phương án + cái giá từng cái + khuyến nghị — rồi mới hỏi user chọn.**
    Socratic thuần chỉ dùng cho thứ user đã có đủ vật liệu tự suy ra.
  - ⬜ **Còn nợ:** Trạm 4d · **fix bug #29** (race `BM25Index`) · nối `split_by_separators`.
    → **Phase 0 CHƯA đóng sổ** như kế hoạch.
  **2026-09-06 ca tối (20:45-23:00, ~2h):** Trạm **4d** ✅ → **TRẠM 4 XONG, hết bài trace 4 trạm**.
  Đo thực nghiệm chuyện chặn event loop (3 request: `await` → 2.0s · gọi hàm chặn → 6.0s, tuần tự
  hoàn toàn). Rồi **fix xong [bug #29](Learning-document/notes/bug-log.md)** (race condition `BM25Index`,
  user tự gõ): `from threading import Lock`, **một** chìa duy nhất trên object
  (`self._lock = Lock()` trong `__init__`), `with self._lock:` bao **trọn thân** cả
  `add_document` lẫn `remove_document`. Tự viết test 4 luồng × 2000 tài liệu, và **tự chứng minh
  test đỏ được** bằng mẹo đổi `Lock()` → `contextlib.nullcontext()` (gỡ khoá mà không phải sửa
  thụt lề dòng nào) → `assert 7560 == 8000`, mất 440 lần đếm, 9 test cũ vẫn xanh. Hoàn nguyên →
  **71 passed**. → **Phase 0 coi như đóng, chỉ còn `split_by_separators`.**
  - **Ba câu hỏi thiết kế user tự quyết đúng:** một object → **một** chìa, gắn lên `self` (chìa
    mới mỗi lần gọi thì mỗi luồng cầm một chìa, không chặn được ai mà nhìn code tưởng an toàn) ·
    khoá **TO** trọn thân hàm, vì ràng buộc `doc_count` khớp `doc_len` **trải qua nhiều dòng**,
    khoá riêng dòng nguy hiểm nhất vẫn để object rơi vào trạng thái nửa vời · `remove_document`
    phải dùng **đúng** chìa đó, hai chìa riêng = vẫn chạy song song = vô nghĩa.
  - **Bẫy riêng của test race:** nó **rất dễ xanh giả** vì race không phải lúc nào cũng xảy ra.
    Phải ép: `sys.setswitchinterval(1e-6)` + lặp đủ nhiều, và trả lại giá trị cũ trong `finally`.
    Con số đỏ (7560) **không tròn và mỗi lần chạy một khác** — dấu vân tay của race: *không tất định*.
  - Lỗi lặp: lại **dán đè lên dòng đang có người dùng** (lần thứ 3 — dòng `doc_count` thành bản
    sao dòng `doc_len`), và **copy nguyên cả lời giải thích của Claude vào file như thể là code**.
    Đối sách vẫn vậy: sau mỗi lần sửa, `git diff` đọc dòng `-` xem vừa xoá mất gì.

  **Cuối buổi tối 06/09 — đổi tên `recursive_chunk` → `fixed_size_chunk`**, và vấp
  [bug #32](Learning-document/notes/bug-log.md) trên đường: dùng **Replace in Files** thay vì
  Rename Symbol → `recursive_chunk` là **tiền tố** của `recursive_chunker` nên tên module bị nuốt
  theo (`ModuleNotFoundError`), và 8 file bị sửa thay vì 3, gồm cả `bug-log.md` — **làm hỏng nghĩa
  của ghi chép lịch sử** (note cũ biến thành "`fixed_size_chunk` mà thân hàm là fixed-size sliding
  window", vô nghĩa). Đã `git checkout --` toàn bộ rồi làm lại bằng `perl` với `\b` + liệt kê
  tường minh 3 file. **Luật mới: đổi tên trong CODE, KHÔNG đổi tên trong GHI CHÉP LỊCH SỬ** — note
  cũ giữ tên cũ, chỉ thêm dòng "đã đổi tên thành X ngày dd/mm".

  **2026-09-07 (T2, 20:45-22:41 ≈ 2h): VÁ NỀN + hàm đầu tiên user tự viết trọn vẹn.**
  Kế hoạch 40' ôn + 2-3h chunker, thực tế ôn trượt nặng nên vá tại chỗ hết buổi.
  - **Cặp 10 `def` ↔ `async def`:** sai **4 lượt liên tiếp, đảo ngược có hệ thống** — kể cả ngay
    sau khi vừa đọc bảng giải thích nói đúng điều ngược lại. Chỉ vá được bằng **tự đo**: 2 endpoint
    thân giống hệt, bắn 3 request → `def` **2.05s** (song song, threadpool) vs `async def` **6.02s**
    (xếp hàng, 1 event loop). **Bằng chứng sạch nhất từ trước tới nay cho luật "đọc giải thích
    không cài được phân biệt"** — chỉ số tự đo mới lật được nhãn.
  - `diff_manifest` dự đoán trước rồi chạy → **4/4**, Cặp 1 (`to_upsert`/`to_delete`) **sạch**.
  - **Chèn drill cú pháp Python 6 bài → 6/6** (§3.5), sau khi user tự báo "bí rồi" và xác nhận bí
    ở **cú pháp** chứ không phải logic. Đúng protocol, và hiệu quả lại ngay: gõ xong drill thì viết
    được `merge_pieces` liền.
  - **`merge_pieces` (bước "gộp" của recursive chunker) — user TỰ VIẾT, chạy đúng.** Đây là hàm đầu
    tiên tự viết trọn vẹn kể từ lúc tự chẩn 04/09 *"hiểu mà code lại không được"*. Bản tự viết còn
    **chặt hơn bản Copilot** đã xoá (có chốt `if current_merge:` chặn túi rỗng; bản Copilot thiếu).
  - **Chốt thiết kế user tự hỏi ra:** *"phải cắt chữ `ngu` ra à?"* → **KHÔNG.** **`size` là TRẦN,
    không phải CHỈ TIÊU** — thà túi lưng 8/10 còn hơn chém đôi một từ, vì chém giữa từ đúng là việc
    `fixed_size_chunk` đã làm. Đây là cả triết lý của recursive chunking, đã in đối chứng thật
    (`Cho t` | `hich chay` — chunk mở đầu bằng `hich`, vector của rác).
  - ⚠️ **Copilot gõ hộ giữa buổi** — user tự báo *"do gợi ý code chứ tôi không biết viết"* rồi tự
    quyết xoá đi viết lại. **Autocomplete đưa thẳng tới trạng thái "hiểu mà không code được"**, đúng
    lỗ hổng §1 tồn tại để bịt. **Luật: tắt Copilot khi làm phần lõi.**
  - **Ba lỗi lặp, không cái nào là lỗi quên:** (1) **đọc lướt** — cả 3 lỗi thật của buổi đều là trả
    lời theo cái mình *tưởng* đề đang hỏi, kể cả tin `0.05s` là kết quả đo trong khi đó là 404;
    (2) **trả về CON SỐ thay vì VẬT** — 3 lần trong 1 ngày, đã thành Cặp 11; (3) **chạy file chưa
    lưu** — 3 lần, đã đóng vĩnh viễn bằng auto-save trong `.vscode/settings.json`.
  - Suite: **71 passed** (chạy toàn bộ, đo thật).
  - ⬜ **Còn nợ:** test cho `merge_pieces` · giữ separator · overlap · nối `/ingest` ·
    ôn bù *Vòng đời trạng thái* · mốc **+3** CRAG (đã dời từ 07/09, phải **code tay lại**).
  **2026-09-08 (T3): NGHỈ — OT tới đêm, không mở máy.** Thực tế 0h, `BKK`, nợ giờ lên **3h15**
  (cao nhất từ khi lập sổ, trần là 6h). Toàn bộ kế hoạch chunker dồn sang 09/09.
  **2026-09-09 (T4) ca sáng 6:00-7:30 — ÔN, XONG. Ca tối 19:30-22:30 — đóng chunker.**
  Cam kết cả ngày 4h30 vs sàn 3h → trả 1h30, cuối ngày nợ còn **1h45**.
  - Drill ép chọn 13 câu gộp **6 mốc ôn cùng tới hạn** → **9/13**.
  - **Cặp 12 (SỔ ↔ KỆ HÀNG) — cặp mới, sai 3 lần liên tiếp trong 1 buổi**, cùng một hướng: gán
    quyết định skip cho 3 kho thay vì **manifest**. Giảng 2 lần không ăn, **chỉ vá được bằng bài
    đo** ([drills/2026-09-09-manifest-vs-kho.py](Learning-document/drills/2026-09-09-manifest-vs-kho.py),
    `ingest_document` thật + `BM25Index` thật, 5 kịch bản). Lại đúng cái pattern đã thấy 07/09 với
    Cặp 10: **đọc giải thích không cài được phân biệt, số tự đo mới lật được nhãn.**
  - Câu chốt user tự nói ra: *"con số 3 đó là láo — sổ ghi bỏ qua 3 mà kho không có gì; đáng lẽ sổ
    phải rỗng theo cái kho, sổ với kho đi đúng với nhau."*
  - ⚠️ **CÒN NỢ: phần (c) code-tay-lại của 4 hàng, chưa trả hàng nào** — thứ tự ưu tiên đã chốt:
    (1) lõi fix #26 CRAG *(mốc này đã bị dời **3 lần**: 07→08→09/09)* · (2) `get_doc_manifest` +
    3 dòng quyết định của `ingest_document` · (3) `Lock` + test race · (4) `reciprocal_rank_fusion`.
    Bảng đầy đủ ở [review-schedule.md § Buổi 2026-09-09](Learning-document/notes/review-schedule.md).
  - ⚠️ **Lỗi phương pháp của Claude ca sáng:** dựng bài đo xong lại **bắt user tự chạy** → user tắc
    ở đường dẫn/`PYTHONPATH`, nhắn *"KHÓ QUÁ BẠN KHÔNG BIẾT CHẠY SAO"*. Trộn cái khó **thao tác**
    vào giữa cái khó **khái niệm** = hỏng cả hai. **Luật: bài đo do Claude dựng thì Claude chạy hộ,
    user chỉ dự đoán và đọc số.**
  ⚠️ **Hệ quả cần nhìn thẳng:** recursive chunker là kỹ thuật của slot 07-08/09, sang **ngày thứ 3**
  vẫn chưa đóng → **slot đã trượt** theo luật "1 kỹ thuật / 2 ngày". Mốc tự kiểm **10/09** giờ là
  mốc thật, phải re-plan tháng 9 bằng số thật. Và 3 món code-tay-lại còn lại phải **ghi thẳng vào
  kế hoạch 10/09**, đừng để trôi thành nợ ngầm như mốc CRAG đã bị dời 3 lần.

- 📊 **ĐÁNH GIÁ TIẾN ĐỘ THÁNG 9 (chốt 2026-09-06, dùng lại mỗi lần cần kiểm):**
  Đếm theo đúng granularity của [LEARNING_ROADMAP.md dòng 40](Learning-document/LEARNING_ROADMAP.md), ~13 milestone:
  ```
  ✅ Trạm 2-4 trace          (xong 06/09)
  ✅ fix bug #25             (xong 06/09, treo 23 ngày)
  ⬜ nối split_by_separators
  ⬜ 5 chunking: Document-based · Semantic · Contextual · Parent-Child · Versioning
  ⬜ 6 Phase 2.4: Metadata filter · Query Transform · Temporal · MMR · Compression · Adaptive-RAG
  ────────────────────────────────────────────────
  2/13 xong sau 6 ngày · còn 11 milestone / 24 ngày
  11 × ~6h = 66h cần  vs  24 × 3h = 72h có  →  đệm chỉ 6h cho CẢ THÁNG
  ```
  **Chỗ đáng lo:** 11 milestone còn lại **toàn bộ là kỹ thuật mới chưa đụng**, mỗi cái phải đủ vòng
  6 bước + code tay. Trong khi 6 ngày qua chủ yếu là trace lại + fix bug (**5 bug mới #26→#31 chỉ
  trong 2 ngày**). Việc đó cực kỳ đáng giá cho lỗ hổng "hiểu mà không code được" và đang có tác
  dụng thật — nhưng **bug không nằm trong roadmap**, và với nhịp phát hiện bug hiện tại nó sẽ ăn
  hết 6h đệm rất nhanh.

- 🔍 **Rà soát roadmap 2026-09-06 (user hỏi "roadmap có đủ so với xu hướng không?"):**
  Đọc lại cả 10 phase → **roadmap KHÔNG mỏng**, rộng hơn phần lớn JD Senior AI Engineer: đã có
  vLLM/Triton · LGTM qua OpenTelemetry · RAGAS + **judge calibration (κ/Pearson)** · A/B harness có
  significance · MCP · LangFuse · output sanitization · circuit breaker · LoRA thuần PyTorch.
  **Rủi ro thật nằm ở hướng ngược lại: quá rộng so với thời gian còn lại** → tuyệt đối không thêm
  phase mới.
  Tìm được **3 lỗ hổng thật** (grep xác nhận, không đoán) và đã **chèn vào phase sẵn có**, không mở
  phase mới:
  1. **Phase 0 mục 11 — Document parsing** (`PDF` chỉ xuất hiện 1 lần, `parsing`/`table` 0 lần).
     Cả pipeline đang bắt đầu từ `text: str` → bỏ qua đúng chỗ RAG thật chết nhiều nhất.
  2. **Phase 3 mục 11 — RAG vs long-context** (`long context` 0 lần). Câu *"khi nào KHÔNG dùng
     RAG?"* là câu phân loại Senior; phải trả lời bằng **ngưỡng đo được**, không phải cảm tính.
  3. **Phase 4 mục 12 — Agent evaluation / trajectory** (`trajectory` 0 lần). Phase 3 đo kết quả
     cuối; agent phải đo đường đi — **cùng bài học với bug #26/#29: assert kết quả cuối mù với bug
     nằm trong quá trình**.
  Đã thêm 6 câu tương ứng vào [interview-questions.md](Learning-document/interview-questions.md).
  **Ghi nhớ khi bị sốt ruột "học thêm cho đủ":** phỏng vấn Senior không chấm độ dài danh sách kỹ
  thuật. Tài sản hiếm nhất user đang có là **bug-log 32 bug tự tìm-tự sửa-tự viết test chặn** —
  kể được một chuyện debug cụ thể thuyết phục hơn liệt kê 40 kỹ thuật.

- 🧭 **Luật tiến độ, áp từ 2026-09-07:**
  1. **Mỗi 2 ngày phải khởi động xong 1 kỹ thuật mới.** Không ngoại lệ.
  2. **Bug tìm thấy dọc đường thì GHI vào bug-log, KHÔNG fix ngay** — trừ khi nó chặn việc đang
     làm, hoặc nó chính là bài tập code-tay của kỹ thuật đang học (như #29 gắn với Trạm 4d).
     Bug đi vào hàng đợi, không cướp chỗ của milestone.
  3. **Mốc tự kiểm 2026-09-10:** nếu tới đó chưa khởi động được kỹ thuật mới nào → **dừng lại
     re-plan thật**, đừng để trôi tới cuối tháng mới biết.

- 🧾 **MỐC TỰ KIỂM 2026-09-10 — BÁO CÁO TRUNG THỰC (user yêu cầu, ghi 22:45 ngày 10/09):**
  ```
  Mốc tháng 9:  2/14 xong — Y NGUYÊN như 06/09. Bốn ngày 07→10/09: 0 mốc đóng.
                (đếm lại 10/09: danh sách 06/09 ghi "13" nhưng liệt kê ra 14 mục → CÒN 12, không phải 11)
  Đường thẳng:  ngày 10/30 lẽ ra ~4.7 mốc → hụt ~2.7 mốc ≈ 5-6 ngày lịch
                → VƯỢT ngưỡng "lệch 3-4 ngày → re-plan" của roadmap.
  Lịch còn lại: 12 mốc × 2 ngày = 24 ngày  vs  20 ngày (11→30/09) → thiếu 4 ngày ngay trên giấy.
  Giờ cần:      12 × ~6h = 72h  vs  20 × 3h = 60h − nợ 4h25 ≈ 55h (thiếu ~17h)
                theo nhịp THẬT 2h27/ngày ≈ 49h − nợ ≈ 45h (thiếu ~27h ≈ 4-5 mốc).
  Giờ 03→10/09: ~19h35 / 24h cam kết → nợ ~4h25 (toàn BKK). Chỉ 2/8 ngày đạt sàn 3h (05, 06/09).
  Code 07→10/09: 14 dòng app (`merge_pieces`), 0 test. Mọi commit còn lại là docs/drill.
  Suite:        71 passed đo lần cuối 07/09, chưa chạy lại từ đó.
  ```
  **Luật tiến độ mục 1** ("mỗi 2 ngày khởi động xong 1 kỹ thuật mới"): **TRƯỢT** — recursive chunker
  khởi động 07/09, sang ngày thứ 4 chưa đóng; Document-based chưa đụng. **Mục 3** (mốc tự kiểm): đúng
  chữ thì có khởi động 1 kỹ thuật, nhưng tinh thần luật là **nhịp** — nhịp đã trượt → **bắt buộc re-plan**.
  ⚠️ **Re-plan bằng số đã bị hoãn 2 lần** (09/09 hẹn "10/09 phải re-plan thật" → 10/09 xếp mục cuối →
  dời 11/09). Sáng 11/09 nó là **VIỆC SỐ 1, ~15', trước khi đụng code** — không được là việc cuối nữa.
  Không re-plan tối 10/09 vì §3.9 cấm bài thiết kế sau 21h.
  **Được gì thật (không phải an ủi):** 10/09 bóc ra gốc rễ của "hiểu mà không code được" — **6 lỗ nền mô
  hình chạy Python**, không phải lỗ RAG. Tối 10/09 drill đọc-chạy 8/9, bài `merge_pieces` đội lốt đúng
  kèm trace, tự tìm ra input "ca túi cuối". Đây là nền để code tay nhanh lên — nhưng **nền không nằm
  trong 13 mốc**, nên lịch vẫn trượt. ~6h/mốc có thể **lạc quan**: recursive chunker (mốc dễ) đã ngốn
  ~3h mà còn ~2h20 việc.
  **Sai của Claude trong kỳ:** sáng 09/09 báo *"chưa tới ngưỡng re-plan, slack bằng 0"* — **quá dễ dãi**
  (không so với đường thẳng, không tính nhịp giờ thật) · tối 09/09 vẫn đẩy bài trace khi user vừa OT về ·
  *"gần như 100% lỗi chú ý"* nói quá (đã sửa) · gọi số dòng trong file user đã chèn chữ. · báo cáo lúc
  22:45 đếm "còn 11 mốc" — **sai, còn 12** (sửa ngay trong tối 10/09).

- 🧮 **RE-PLAN 2026-09-10** (làm ngay tối 10/09 theo yêu cầu user, dù §3.9 khuyên để sáng). Bản đầy đủ ở
  [LEARNING_ROADMAP.md § RE-PLAN 2026-09-10](Learning-document/LEARNING_ROADMAP.md) — roadmap là nguồn sự thật.
  Tóm tắt để Claude áp **mỗi buổi**:
  - **Toán cả năm:** nhịp thật 2h27/ngày → xong nội dung ~03/03/2027, **sau Tết 06/02/2027 → không kịp**.
    Sàn 3h → ~30/01 (~1 tuần ôn). **3h ngày thường + 6h T7/CN** → ~30/12 (~5.5 tuần ôn).
  - **Tháng 9:** 12 mốc theo thứ tự cố định, hộp giờ cứng (🔴 8h · 🟡 5h), checkpoint **17/09 = 4 mốc**,
    **24/09 = 8 mốc**. Giả định 6h/mốc phải kiểm bằng giờ-mốc thật tại 17/09.
  - **Đầu mỗi buổi Claude phải nói ra:** đang ở mốc nào · hộp giờ còn bao nhiêu · hôm nay có trễ checkpoint không.
  - **Trong buổi Claude phải chặn:** bug ngoài mốc → bug-log · trace trạm cũ → không · ôn/drill quá 30' → dừng.
  - **Phương án B** (dời Versioning → Temporal → Adaptive-RAG sang tháng 10) — ✅ **user chốt 10/09**, cùng mức **6h Thứ Bảy/Chủ Nhật**.
    Cắt độ sâu vòng 6 bước **chỉ user được quyết**.

- 🧭 **Luật mới, bắt buộc từ 2026-09-05 (rút ra từ bug #27):**
  1. Trước khi commit: chạy `pytest -q` **toàn bộ**, không giới hạn thư mục. Chạy theo thư mục con
     rồi tưởng là xanh chính là thứ nuôi bug #27 sống 8 ngày.
  2. Trước khi commit: đọc `git diff`, đừng tin message mình vừa gõ. Cẩn thận `git add -A` khi
     trong cây còn sửa đổi dở dang.
  3. Con số trong tài liệu ("66 test xanh", "`/ingest` chạy thật") phải đến từ **một lần chạy
     thật**, không phải trí nhớ — cả hai câu đó đã sai suốt 28/08 → 05/09.
- ⏱️ **Sổ nợ giờ (mới, 04/09):** [Learning-document/notes/so-gio.md](Learning-document/notes/so-gio.md)
  — cam kết sàn 3h/ngày, ghi cam kết/thực tế/nợ lũy kế mỗi buổi, phân loại `BKK` (không lãi) vs
  `TRÔI` (lãi 1.5x, hạn trả 7 ngày), trần nợ 6h thì cấm học kỹ thuật mới 1 buổi để re-plan.
  Nợ hiện tại **30'** (06/09 làm 6h/ngày, vượt sàn 3h nên trả bớt được).
  ⚠️ **04/09 phải ôn bù** 2 kỹ thuật này trước, chưa được tính mốc +3.
  (2026-09-01 đã chèn 1 đợt drill cú pháp Python giữa buổi — xem §3.5. Cấu trúc dict-vs-list
  vẫn còn lệch lai rai khi trace, sửa 1 lần là ra.)
- ⏳ Kế tiếp: **recursive chunker** — ~~bước gộp (`merge_pieces`)~~ ✅ 07/09 (user tự viết) · ⬜ test cho nó · ⬜ giữ separator · ⬜ overlap · ⬜ nối `/ingest` → *(hết Phase 0)*
  ~~Trạm 4d~~ ✅ · ~~bug #29~~ ✅ · ~~bug #25~~ ✅ đều 06/09
  → Document-based chunking (kỹ thuật MỚI đầu tiên của tháng 9). ~~Trạm 2, Trạm 3~~ ✅ 02/09, 05/09
  → Phase 2.4 (Metadata filter → MMR) → Phase 3 (Eval)

**Phát hiện khi trace (2026-08-25):**
1. ✅ **XỬ LÝ 2026-09-06:** `/ingest` gọi `recursive_chunk` nhưng thân hàm là fixed-size sliding
   window → **đã đổi tên thành `fixed_size_chunk`** (commit `899a1bc`). Tên hết nói dối. Tên file
   `recursive_chunker.py` **giữ nguyên** vì recursive chunker thật sẽ nằm trong đó.
2. ⬜ `split_by_separators` (đệ quy thật) có test xanh nhưng **không nơi nào trong `app/` gọi**.
   **Đọc kỹ 06/09 mới thấy: nó KHÔNG cắm thẳng vào được**, vì mới làm một nửa recursive chunking —
   nó chỉ **cắt nhỏ**, không **gộp lại** cho tới gần `size` (cắt `"a b c d"` bằng `" "` ra 4 mẩu
   bé tí), lại **nuốt mất separator** (`str.split` bỏ luôn dấu) và **không có overlap**.
   → Milestone roadmap ghi *"nối `split_by_separators`"* là **under-specified**. Nối bừa = chất
   lượng retrieval tệ đi để đánh dấu tick. Việc đúng là **viết nốt bước gộp + giữ separator +
   overlap**, và việc đó xứng đáng là **milestone riêng ~2-3h**, không phải cái đuôi 30'.
   Đã chốt: làm nó ngày **07/09** (thay chỗ Document-based chunking, cả hai đều trong Phase 0).

---

## 7. Đồng bộ giữa 2 máy (Fedora ↔ Mac)

Sống qua git (đồng bộ được): `CLAUDE.md` · `Learning-document/` · `.claude/settings.json` · code + test.
KHÔNG đồng bộ được: `~/.claude/` (memory, transcript, settings user-level), `.env`, `data/manifest.json`.

→ Trước khi đổi máy: `git add -A && git commit && git push`. Sang máy kia `git pull` là Claude
đọc lại đúng file này và hành xử giống hệt.
