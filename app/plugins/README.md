# plugins

Phase 8 — Extensibility & Community. Bài Port/Adapter + Registry thật, đáng làm tay vì
open source sống nhờ nó ("người lạ có mở rộng được không").

| File (sẽ build) | Vai trò |
|---|---|
| `registry.py` | dict + decorator `register(kind, name)` / `get(kind, name)`, fail-loud khi trùng tên |
| `ports.py` | assert `issubclass(cls, PORTS[kind])` lúc đăng ký — chặn plugin sai interface sớm |

**3 bug thật của plugin system:** trùng tên im lặng (ghi đè, không báo) · import side-effect
(quên import module thì `get()` KeyError dù class tồn tại) · plugin sai interface (chỉ nổ lúc
pipeline gọi tới, phải chuyển sang lỗi đăng ký).

Test: `tests/plugins/test_registry.py` (trùng tên, tên sai, sai interface).
