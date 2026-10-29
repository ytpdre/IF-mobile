#!/usr/bin/env python3
"""Stream-inspect a multi-part (split) zip archive without extracting it.

Concatenates the parts virtually, walks the local file headers sequentially,
and prints per-directory statistics plus the largest entries.

Usage:
    python3 inspect_release.py InFalsus.zip.001 InFalsus.zip.002 ...
"""
import collections
import os
import struct
import sys

CHUNK = 1 << 24


class MultiFileReader:
    """Reads across a list of part files as one continuous byte stream."""

    def __init__(self, parts):
        self.sizes = []
        self.files = []
        for p in parts:
            f = open(p, "rb")
            f.seek(0, 2)
            self.sizes.append(f.tell())
            self.files.append(f)
        self.size = sum(self.sizes)
        self.pos = 0

    def tell(self):
        return self.pos

    def seekable(self):
        return True

    def seek(self, offset, whence=0):
        self.pos = self.size + offset if whence == 2 else offset
        return self.pos

    def read(self, n=-1):
        if n < 0:
            n = self.size - self.pos
        chunks = []
        while n > 0 and self.pos < self.size:
            acc = 0
            idx = len(self.sizes) - 1
            for i, s in enumerate(self.sizes):
                if self.pos < acc + s:
                    idx = i
                    break
                acc += s
            self.files[idx].seek(self.pos - acc)
            take = min(n, self.sizes[idx] - (self.pos - acc))
            data = self.files[idx].read(take)
            if not data:
                break
            chunks.append(data)
            self.pos += len(data)
            n -= len(data)
        return b"".join(chunks)


def parse_headers(stream):
    """Yield (name, compressed_size, uncompressed_size) for each stored member."""
    while True:
        sig = stream.read(4)
        if sig != b"PK\x03\x04":
            break
        (_, _, comp, _, _, _, csize, usize, nlen, elen) = struct.unpack(
            "<HHHHHIIIHH", stream.read(26)
        )
        name = stream.read(nlen).decode("utf-8", "replace")
        extra = stream.read(elen)
        # zip64 extra field overrides 32-bit sizes
        e = 0
        while e + 4 <= len(extra):
            eid, esz = struct.unpack("<HH", extra[e:e + 4])
            ed = extra[e + 4:e + 4 + esz]
            if eid == 1:
                f = 0
                if usize == 0xFFFFFFFF:
                    usize = struct.unpack("<Q", ed[0:8])[0]
                    f = 8
                if csize == 0xFFFFFFFF:
                    csize = struct.unpack("<Q", ed[f:f + 8])[0]
            e += 4 + esz
        yield name, csize, usize
        remaining = csize
        while remaining > 0:
            data = stream.read(min(remaining, CHUNK))
            if not data:
                return
            remaining -= len(data)


def fmt(n):
    return f"{n / 1e6:10.1f} MB"


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    stream = MultiFileReader(sys.argv[1:])
    entries = list(parse_headers(stream))

    files = [(u, n) for u, n in entries if not n.endswith("/")]
    total = sum(u for u, _ in files)
    print(f"entries: {len(entries)}  files: {len(files)}  total: {total / 1e9:.2f} GB\n")

    dirs = collections.defaultdict(lambda: [0, 0])
    for u, n in files:
        parts = n.split("/")
        key = "/".join(parts[:3]) if len(parts) > 3 else n
        dirs[key][0] += 1
        dirs[key][1] += u

    print("== largest directories (3 levels) ==")
    for k, (c, s) in sorted(dirs.items(), key=lambda x: -x[1][1])[:20]:
        print(f"{fmt(s)}  {c:>6} files  {k}")

    print("\n== largest files ==")
    for u, n in sorted(files, key=lambda x: -x[0])[:15]:
        print(f"{fmt(u)}  {n}")

    exts = collections.Counter()
    for u, n in files:
        exts[os.path.splitext(n)[1].lower()] += u
    print("\n== by extension ==")
    for e, s in exts.most_common(12):
        print(f"{fmt(s)}  {e or '(none)'}")


if __name__ == "__main__":
    main()
