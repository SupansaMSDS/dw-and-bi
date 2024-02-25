##Building a Data Lake
#1.สร้าง Data set ชื่อ github บน bigquery
![Alt text](image-7.png)
#1.pip install -r requirements.txt
![Alt text](image-8.png)
#2.สร้าง service account บน bigquery และกำหนดสิทธิ์
![Alt text](image-1.png)
#3.เข้าไป service account แล้วทำการ download key เลือก Key type เป็น JSON
![Alt text](image-3.png)
![Alt text](image-4.png)
#4. นำไฟล์ Key ที่  download มาไว้ที่ Folder 03-building-a-data-warehouse 
#5.ไปที่ etl_bigquery.py แล้วนำชื่อไฟล์ Key ไปใส่ใน Key parth และใส่ชื่อ project_id ให้ตรงกับบน bigquery
![Alt text](image-6.png)
#6.python etl_bigquery.py
![Alt text](image-9.png)
#7.ไปที่ bigqury จะพบ table events ที่สร้างขึ้นมา
![Alt text](image-10.png)
#8.ทดลอง query data บน bigquery
![Alt text](image-11.png)