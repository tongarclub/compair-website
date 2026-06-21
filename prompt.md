Project Context & Requirements: Static AEO-Optimized Comparison Engine

1. Project Vision
สร้างเว็บ Application ประเภท "Comparison Engine & Calculator" สำหรับทำ AEO (Answer Engine Optimization) และ Programmatic SEO โดยเริ่มจากโครงสร้างที่เรียบง่ายที่สุด (MVP) รองรับ 2 โดเมนหลัก:

Domain A: AI Hardware VRAM Calculator

Domain B: Solar Cell ROI & Sizing Calculator

2. Tech Stack & Architecture

Frontend: ใช้ Pure HTML, CSS และ Vanilla JavaScript เป็นหลัก เพื่อความรวดเร็วและเบาที่สุด

Database: ไม่มี Database

Data Source: ใช้ไฟล์ .json แบบ Flat-file โดยแยกโฟลเดอร์ให้ชัดเจนเพื่อง่ายต่อการสเกลและอัปเดตในอนาคต เช่น:

/data/ai-models/llama3.json

/data/solar/inverters.json

Methodology: * ประยุกต์ใช้ Domain-Driven Design (DDD) ในฝั่ง JavaScript โดยแยก Logic การคำนวณของ AI และ Solar Cell ออกจากกัน

เขียนโค้ดให้พร้อมสำหรับการทำ Test-Driven Development (TDD) (เช่น แยกฟังก์ชันสมการคำนวณออกมาเป็น Pure Function ที่สามารถเอา Jest หรือ Vitest มาครอบทดสอบได้ง่าย)

3. Key Features สำหรับ AEO/SEO
หน้าเว็บ HTML จะต้องแสดงผลองค์ประกอบเหล่านี้ (อาจจะใช้ JS ดึง JSON มา Render):

Summary Card: แสดงผลลัพธ์ฟันธงตรงไปตรงมา (เช่น สเปค VRAM หรือขนาดแผงโซล่าเซลล์ที่แนะนำ)

Data Table: ตารางเปรียบเทียบข้อมูลที่ชัดเจน เพื่อให้ AI Search Engine เข้ามา Scrape ไปทำ RAG ได้ง่าย

JSON-LD Injector: มีฟังก์ชัน JavaScript ที่อ่านค่าผลลัพธ์การคำนวณ แล้วสร้าง Schema Markup (application/ld+json) ฝังลงในแท็ก <head> โดยอัตโนมัติ

4. Initial Task สำหรับคุณ (AI)
จากบริบทนี้ กรุณาช่วยฉันสร้างสิ่งต่อไปนี้เป็นอันดับแรก:

Directory Structure: ออกแบบโครงสร้างโฟลเดอร์ของโปรเจกต์ (HTML, JS, และโฟลเดอร์ Data JSON ที่แบ่งสัดส่วนอย่างชัดเจน)

JSON Schema Design: ออกแบบโครงสร้างไฟล์ JSON ตัวอย่าง 1 ไฟล์สำหรับ AI Model และ 1 ไฟล์สำหรับ Solar Cell

Core Calculation Function: เขียน JavaScript Pure Function เบื้องต้นสำหรับดึงข้อมูล JSON มาคำนวณ โดยคำนึงถึงการเขียน Unit Test