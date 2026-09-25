"""Đo thật: `def` vs `async def` trong FastAPI — cái nào chạy song song?

Cách chạy:
    .venv/bin/python Learning-document/drills/2026-09-07-def-vs-async.py

Khung đã dựng sẵn: server thật + bắn 3 request đồng thời + bấm giờ.
Việc của bạn: viết 2 handler ở phần TODO. Thân hai hàm GIỐNG HỆT nhau
(cùng `time.sleep(2)`), chỉ khác đúng MỘT từ khoá ở dòng khai báo.
"""

import threading
import time

import httpx
import uvicorn
from fastapi import FastAPI

app = FastAPI()

SLEEP = 2.0
N_REQUESTS = 3
PORT = 8899


# ---------------------------------------------------------------- TODO
# Viết 2 endpoint ở đây. Cả hai đều `time.sleep(SLEEP)` trong thân.
#
#   @app.get("/sync")   -> khai báo bằng từ khoá nào?
#   @app.get("/async")  -> khai báo bằng từ khoá nào?
#
@app.get("/sync")
def sync_endpoint():
    time.sleep(SLEEP)
    return {"message": "Sync endpoint completed."}

@app.get("/async")
async def async_endpoint():
    time.sleep(SLEEP)
    return {"message": "Async endpoint completed."}
# (Đừng dùng asyncio.sleep — phải là time.sleep, tức lệnh CHẶN thật.)
# ---------------------------------------------------------------- TODO


def fire(path):
    """Bắn N_REQUESTS request đồng thời vào `path`, trả về tổng thời gian."""
    url = "http://127.0.0.1:{}{}".format(PORT, path)

    def one():
        r = httpx.get(url, timeout=60)
        if r.status_code != 200:
            raise SystemExit(
                "\n>>> {} tra ve {} — endpoint chua ton tai.\n"
                ">>> Khoi TODO van con trong: chua co handler nao duoc viet.\n"
                ">>> Khong co gi duoc do ca.".format(path, r.status_code))

    threads = [threading.Thread(target=one) for _ in range(N_REQUESTS)]
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return time.perf_counter() - start


def main():
    config = uvicorn.Config(app, host="127.0.0.1", port=PORT, log_level="error")
    server = uvicorn.Server(config)
    threading.Thread(target=server.run, daemon=True).start()

    while not server.started:
        time.sleep(0.05)

    print("Mỗi endpoint ngủ {}s, bắn {} request đồng thời.".format(SLEEP, N_REQUESTS))
    print("Nếu chạy song song  -> tổng ~{:.1f}s".format(SLEEP))
    print("Nếu xếp hàng tuần tự -> tổng ~{:.1f}s".format(SLEEP * N_REQUESTS))
    print("-" * 46)

    for path in ("/sync", "/async"):
        print("{:<8} -> {:.2f}s".format(path, fire(path)))

    server.should_exit = True


if __name__ == "__main__":
    main()
