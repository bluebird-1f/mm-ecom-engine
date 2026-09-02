#ดึง Module logging ซึ่งเป็น Library มาตรฐานของ Python สำหรับใช้จัดการระบบบันทึกสถานะ (Log) ของโปรแกรม
import logging
#ดึง Module sys ที่เกี่ยวกับ System-specific parameters และฟังก์ชันต่างๆ มาใช้ เพื่ออ้างอิง Output Stream ของระบบ
import sys


#รับ พารามิเตอร์ name เป็นข้อความ (String) ค่าเริ่มต้นคือ "app" และส่งคืนค่า (Return) ออกมาเป็น Object ชนิด logging.Logger
def get_logger(name: str = "app") -> logging.Logger:
    #คำอธิบายหน้าที่ของฟังก์ชัน พารามิเตอร์ที่รับ และสิ่งที่ส่งคืนกลับไป เพื่อช่วยในการอ่านโค้ดและทำเอกสาร
    """
    Create and return a custom application logger.

    Args:
        name: Logger name.

    Returns:
        Configured logging.Logger instance.
    """
    #สร้างหรือดึง Logger Object ตามชื่อ name ที่ส่งเข้ามา ถ้าชื่อเดิมเคยถูกสร้างไว้แล้วจะไปดึง Instance เดิมกลับมาใช้งาน
    logger = logging.getLogger(name)

    #เช็กเงื่อนไขว่า Logger ตัวนี้มี Handler (ตัวจัดการการส่งออกข้อมูล Log) ติดตั้งอยู่แล้วหรือยัง
    if logger.handlers:
        #ถ้ามี Handler อยู่แล้ว ให้คืนค่า logger นั้นกลับไปทันที เพื่อป้องกันปัญหาการเพิ่ม Handler ซ้ำ ซึ่งจะทำให้ Log พิมพ์ข้อความซ้ำซ้อน
        return logger

    #กำหนดระดับการบันทึก Log ขั้นต่ำเป็นระดับ INFO (จะบันทึกตั้งแต่ระดับ INFO, WARNING, ERROR, CRITICAL ขึ้นไป ส่วน DEBUG จะถูกข้าม)
    logger.setLevel(logging.INFO)

    #สร้าง Object กำหนด รูปแบบ (Format) ของข้อความ Log ที่จะพิมพ์ออกมา
    formatter = logging.Formatter(
        #กำหนดโครงสร้างข้อความ Log: เวลาที่เกิดเหตุการณ์ (asctime) | ระดับของ Log (levelname) | ชื่อ Logger (name) | ข้อความแจ้งเตือน (message)
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        #กำหนดรูปแบบของ วันที่ และ เวลา ให้แสดงเป็น "ปี-เดือน-วัน ชั่วโมง:นาที:วินาที"
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    #สร้าง Handler สำหรับส่งข้อความ Log ออกทางหน้าจอ Console ผ่าน standard output stream (sys.stdout) ซึ่งเหมาะกับการทำงานร่วมกับ Docker
    console_handler = logging.StreamHandler(sys.stdout)
    #นำรูปแบบข้อความ (Formatter) ที่สร้างไว้ด้านบน มาติดตั้งให้กับ console_handler
    console_handler.setFormatter(formatter)

    #เพิ่ม console_handler เข้าไปใน Logger Object เพื่อให้เริ่มส่งข้อความออกหน้าจอตามรูปแบบที่กำหนด
    logger.addHandler(console_handler)
    #ตั้งค่าไม่ให้ส่ง Log นี้กระจาย (Propagate) ย้อนกลับไปหา Root Logger เพื่อป้องกันปัญหาข้อความแสดงซ้ำในระบบขนาดใหญ่
    logger.propagate = False

    #ส่งคืน Logger Object ที่ตั้งค่าเสร็จสมบูรณ์แล้วออกไปพร้อมใช้งาน
    return logger
