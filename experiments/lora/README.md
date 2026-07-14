# experiments/lora

Phase 6 — Fine-tuning. Ngoài `app/` vì đây là script thí nghiệm 1 lần (train/eval), không
phải service code chạy production.

| File (sẽ build) | Kỹ thuật |
|---|---|
| `manual_lora.py` | tự implement LoRA layer thuần PyTorch: `W + (B@A)*scale` trên 1 linear nhỏ, train toy task |
| `train_qwen.py` | LoRA/QLoRA thật trên `Qwen2.5-7B` (dùng PEFT sau khi hiểu bản tay) |

**Bug cố ý:** quên freeze base weights → mất điểm low-rank. Debug bằng cách đếm trainable params.
