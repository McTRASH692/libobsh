#!/usr/bin/env python3
"""
binary_library.py - True binary Library of Babel
Every possible byte sequence exists at some coordinate.
No base64 encoding required.
"""
import sys
import json
sys.set_int_max_str_digits(10000)

BASE = 256
PAGE_SIZE = 3200
HEX_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"

WALLS = 4
SHELVES = 5
VOLUMES = 32
PAGES = 420

def encode_position(wall, shelf, volume, page):
    return page + volume * PAGES + shelf * VOLUMES * PAGES + wall * SHELVES * VOLUMES * PAGES

def decode_position(pos):
    wall = pos // (SHELVES * VOLUMES * PAGES)
    remainder = pos % (SHELVES * VOLUMES * PAGES)
    shelf = remainder // (VOLUMES * PAGES)
    remainder = remainder % (VOLUMES * PAGES)
    volume = remainder // PAGES
    page = remainder % PAGES
    return {"wall": wall, "shelf": shelf, "volume": volume, "page": page}

def binary_to_number(data: bytes) -> int:
    if len(data) > PAGE_SIZE:
        raise ValueError(f"Data exceeds page size: {len(data)} > {PAGE_SIZE}")
    padded = data.ljust(PAGE_SIZE, b'\x00')
    result = 0
    for byte in padded:
        result = (result << 8) | byte
    return result

def number_to_binary(num: int) -> bytes:
    result = bytearray(PAGE_SIZE)
    for i in range(PAGE_SIZE - 1, -1, -1):
        result[i] = num & 0xFF
        num >>= 8
    return bytes(result)

def number_to_hex(n: int) -> str:
    if n == 0:
        return "0"
    chars = []
    while n > 0:
        n, r = divmod(n, 36)
        chars.append(HEX_ALPHABET[r])
    return ''.join(reversed(chars))

def hex_to_number(s: str) -> int:
    return int(s, 36)

def store_binary(data: bytes, wall: int = 0, shelf: int = 0, volume: int = 0, page: int = 0) -> str:
    if len(data) > PAGE_SIZE:
        raise ValueError(f"Data too large: {len(data)} > {PAGE_SIZE}")
    pos = encode_position(wall, shelf, volume, page)
    page_num = binary_to_number(data)
    combined = (pos << (PAGE_SIZE * 8)) | page_num
    return number_to_hex(combined)

def retrieve_binary(hex_addr: str) -> bytes:
    combined = hex_to_number(hex_addr)
    mask = (1 << (PAGE_SIZE * 8)) - 1
    page_num = combined & mask
    full_page = number_to_binary(page_num)
    return full_page.rstrip(b'\x00')

def address_of_bytes(data: bytes) -> str:
    if len(data) > PAGE_SIZE:
        raise ValueError(f"Data too long: {len(data)} > {PAGE_SIZE}")
    return store_binary(data, 0, 0, 0, 0)

def bytes_at_address(hex_addr: str) -> bytes:
    return retrieve_binary(hex_addr)

def store_file(filepath: str, manifest_path: str = None) -> list:
    with open(filepath, 'rb') as f:
        data = f.read()
    chunks = [data[i:i+PAGE_SIZE] for i in range(0, len(data), PAGE_SIZE)]
    addresses = []
    for i, chunk in enumerate(chunks):
        wall = (i // (SHELVES * VOLUMES * PAGES)) % WALLS
        shelf = (i // (VOLUMES * PAGES)) % SHELVES
        volume = (i // PAGES) % VOLUMES
        page = i % PAGES
        addr = store_binary(chunk, wall, shelf, volume, page)
        addresses.append(addr)
        print(f"  Page {i}: {addr[:30]}...")
    if not manifest_path:
        manifest_path = filepath + ".manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump({
            "file": filepath,
            "size": len(data),
            "pages": len(addresses),
            "addresses": addresses
        }, f, indent=2)
    print(f"\nStored {len(addresses)} pages. Manifest: {manifest_path}")
    return addresses

def retrieve_file(manifest_path: str, output_path: str = None):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)
    all_data = b''
    for addr in manifest["addresses"]:
        chunk = retrieve_binary(addr)
        all_data += chunk
    all_data = all_data[:manifest["size"]]
    if not output_path:
        output_path = manifest.get("file", "retrieved_output")
    with open(output_path, 'wb') as f:
        f.write(all_data)
    print(f"Retrieved {len(all_data)} bytes to {output_path}")
    return all_data

if __name__ == "__main__":
    test_data = b"Hello\x00World\xFFBinary\x00Data"
    print(f"Original: {test_data}")
    addr = address_of_bytes(test_data)
    print(f"Address: {addr[:100]}...")
    retrieved = bytes_at_address(addr)
    print(f"Match: {test_data == retrieved}")
