# Elevview IoT Camera

Elevview IoT Camera เป็นโปรเจคที่ใช้ Raspberry Pi 5 สำหรับถ่ายภาพใช้เว็บแอปพลิเคชันในการสั่งใช้งานกล้องถ่ายรูป โดยตัว Raspberry Pi 5 จะรับคำสั่งผ่าน MQTT จาก AWS IoT Core และหลังจากทำการถ่ายภาพเสร็จจะอัพรูปไปยัง Amazon S3 และทำการส่ง HTTP Post ไปยังเว็บแอปพลิเคชัน เพื่อทำการอัพเดต database

## การติดตั้ง

### 1. อัพเดตระบบ

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. ติดตั้งไลบรารีที่จำเป็น

ติดตั้งแพ็คเกจพื้นฐานที่จำเป็นสำหรับการทำงานของโปรเจค

```bash
sudo apt install -y git python3 python3-pip
```

### 3. ติดตั้ง AWS IoT SDK for Python

```bash
pip install awsiotsdk boto3
```

### 4. รายการแพ็คเกจที่ใช้ใน `pip`

ไฟล์ `pip_packages.txt` ใน GitHub Repository แสดงรายการแพ็คเกจที่ติดตั้งด้วย `pip list`

## วิธีใช้งาน

### 1. กำหนดค่า AWS IoT Core

- สร้าง Thing ใน AWS IoT Core และดาวน์โหลดไฟล์ `certificate.pem`, `private.pem.key`, และ `AmazonRootCA1.pem`
- แก้ไขไฟล์ config ในโค้ดเพื่อใส่รายละเอียดของ AWS IoT

### 2. การถ่ายภาพ

สามารถส่งคำสั่งผ่าน AWS IoT Core (MQTT) เพื่อให้ Raspberry Pi ทำการถ่ายภาพและอัพโหลดไปยัง S3

## License

This project is licensed under the MIT License.

---

สำหรับรายละเอียดเพิ่มเติม โปรดดูที่ [GitHub Repository](https://github.com/MONLEMON/Elevview_IoT_Camera)
