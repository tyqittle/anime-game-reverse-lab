"""Conservative file signatures; unknown formats are not guessed as verified."""
from pathlib import Path

MAGIC = (
    (b"UnityFS", "UnityFS asset bundle"),
    (b"UnityRaw", "UnityRaw bundle"),
    (b"UnityWeb", "UnityWeb bundle"),
    (b"\x89PNG\r\n\x1a\n", "PNG image"),
    (b"\xff\xd8\xff", "JPEG image"),
    (b"OggS", "Ogg media"),
    (b"DDS ", "DDS texture"),
    (b"\xabKTX 20\xbb\r\n\x1a\n", "KTX2 texture"),
    (b"\xabKTX 11\xbb\r\n\x1a\n", "KTX1 texture"),
    (b"SQLite format 3\x00", "SQLite database"),
    (b"PK\x03\x04", "ZIP archive"),
    (b"PK\x05\x06", "Empty ZIP archive"),
    (b"\x1f\x8b\x08", "GZIP stream"),
    (b"\x28\xb5\x2f\xfd", "Zstandard stream"),
    (b"\x04\x22\x4d\x18", "LZ4 frame"),
    (b"ID3", "MP3 ID3 audio"),
    (b"MZ", "Windows PE candidate"),
    (b"\x7fELF", "ELF binary"),
)


def identify_bytes(data: bytes, suffix: str = "") -> dict[str, str]:
    """Identify via reliable header patterns; do not trust extensions alone."""
    if len(data) >= 12 and data[:4] == b"RIFF":
        riff = {b"WAVE": "WAV audio", b"WEBP": "WebP image", b"AVI ": "AVI video"}.get(data[8:12])
        if riff:
            return {"format": riff, "confidence": "signature"}
    if len(data) >= 12 and data[4:8] == b"ftyp":
        return {"format": "ISO Base Media (MP4/HEIF family)", "confidence": "signature"}
    if data.startswith(b"\x00\x00\x01\x00"):
        return {"format": "ICO image", "confidence": "signature"}
    for sig, name in MAGIC:
        if data.startswith(sig):
            return {"format": name, "confidence": "signature"}
    stripped = data.lstrip(b" \t\r\n")
    if stripped.startswith((b"{", b"[")) and suffix.lower() == ".json":
        return {"format": "JSON candidate", "confidence": "heuristic"}
    return {"format": "unknown", "confidence": "none"}


def identify_file(path: Path) -> dict[str, str]:
    with path.open("rb") as handle:
        data = handle.read(256)
    return identify_bytes(data, path.suffix)
