import secrets, base64
from pathlib import Path

out_path = Path(__file__).resolve().parent / "file_access.txt"

key = secrets.token_bytes(32)

b64 = base64.b64encode(key).decode("ascii")  # valid UTF-8 text

out_path.write_text(b64 + "\n", encoding="utf-8")

print(f"Wrote 32-byte key to {out_path}")
