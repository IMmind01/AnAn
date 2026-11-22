import json
from pathlib import Path
from typing import Dict, List

# กำหนดตำแหน่งไฟล์ study_records.json ให้อยู่โฟลเดอร์เดียวกับโค้ด
DATA_FILE = Path(__file__).parent / "study_records.json"


def load_records() -> List[Dict]:
    """อ่านประวัติการเรียนทั้งหมดจากไฟล์ JSON"""
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_records(records: List[Dict]) -> None:
    """เขียนข้อมูลทั้งหมดลงไฟล์ JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=2)


def add_record(record: Dict) -> List[Dict]:
    """เพิ่มรายการใหม่ไว้บนสุด (ล่าสุดขึ้นก่อน) แล้วบันทึกลง JSON"""
    records = load_records()
    records.insert(0, record)
    save_records(records)
    return records


def delete_record(record_id: str) -> List[Dict]:
    """ลบรายการตาม id และอัปเดตไฟล์ JSON"""
    records = load_records()
    updated = [r for r in records if r.get("id") != record_id]
    save_records(updated)
    return updated


def clear_all_records() -> None:
    """ล้างประวัติการเรียนทั้งหมด"""
    save_records([])