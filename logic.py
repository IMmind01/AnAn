from datetime import datetime
from typing import Dict, List, Optional, Tuple
import uuid


def validate_input(subject: str, duration: int) -> Tuple[bool, str]:
    """
    ตรวจสอบความถูกต้องของข้อมูลที่ผู้ใช้กรอก
    เงื่อนไข:
      - ชื่อวิชาต้องไม่เป็นค่าว่าง
      - เวลาเรียนต้องเป็นจำนวนเต็มระหว่าง 1 - 240 นาที
    """
    if not isinstance(subject, str) or not subject.strip():
        return False, "กรุณากรอกชื่อวิชา (ต้องไม่เป็นค่าว่าง)"

    # ใน Python bool เป็น subclass ของ int จึงต้องดักเช็กด้วย
    if isinstance(duration, bool) or not isinstance(duration, int):
        return False, "เวลาเรียนต้องเป็นจำนวนเต็มเท่านั้น"

    if duration < 1 or duration > 240:
        return False, "เวลาเรียนต้องอยู่ระหว่าง 1 ถึง 240 นาที"

    return True, ""


def classify_duration(duration: int) -> str:
    """
    จำแนกระยะเวลาเรียนตามเกณฑ์ที่กำหนด
      - น้อยกว่า 30 นาที       = Short
      - 30 - 59 นาที         = Medium
      - ตั้งแต่ 60 นาทีขึ้นไป   = Long
    """
    if duration < 30:
        return "Short"
    elif duration <= 59:
        return "Medium"
    else:
        return "Long"


def create_study_record(
    subject: str, duration: int
) -> Tuple[Optional[Dict], Optional[str]]:
    """
    ตรวจสอบข้อมูลและสร้าง Dictionary สำหรับบันทึก
    คืนค่า (record, error_message)
    """
    is_valid, error_msg = validate_input(subject, duration)
    if not is_valid:
        return None, error_msg

    record = {
        "id": str(uuid.uuid4())[:8],
        "subject": subject.strip(),
        "duration": duration,
        "category": classify_duration(duration),
        "timestamp": datetime.now().strftime("%d %b %Y · %H:%M"),
    }
    return record, None


def calculate_stats(records: List[Dict]) -> Dict:
    """คำนวณสถิติภาพรวมเพื่อแสดงบน Dashboard"""
    if not records:
        return {
            "total_minutes": 0,
            "avg_minutes": 0,
            "counts": {"Short": 0, "Medium": 0, "Long": 0},
        }

    total_minutes = sum(r.get("duration", 0) for r in records)
    avg_minutes = round(total_minutes / len(records))
    counts = {"Short": 0, "Medium": 0, "Long": 0}

    for r in records:
        cat = r.get("category")
        if cat in counts:
            counts[cat] += 1

    return {
        "total_minutes": total_minutes,
        "avg_minutes": avg_minutes,
        "counts": counts,
    }


def format_minutes_display(total_minutes: int) -> str:
    """แปลงนาทีรวมให้อ่านง่าย เช่น 135 -> 2 ชม. 15 นาที"""
    if total_minutes < 60:
        return f"{total_minutes} นาที"
    hours, mins = divmod(total_minutes, 60)
    if mins == 0:
        return f"{hours} ชม."
    return f"{hours} ชม. {mins} นาที"