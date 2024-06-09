## Get start

### Create ENV and Set Up
### 1. สรา้งไฟล์docker airflow โดยใช ้code
```sh
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml'
```

### 2. จากนั้นทําการ Run mkdir 

```sh
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

### 3.ตั้งค่า airflow_uid = 1000 ใน .env
```sh
AIRFLOW_UID=50000
```

### 4.สร้าง Environment ในการสร้าง project python สําหรับ project capstone นี้
```sh
python -m venv ENV
```
### 5.Activate เพื่อเข้าไปใน ENV
```sh
source ENV/bin/activate
```

### 6.เปิดใช้งาน Apache airflow port 8080
```sh
docker compose up
```
### 7.สร้าง Project และ key สําหรับ capstone บน Google cloud เปิดสิทธิ์ให้สามารถเชื่อมต่อ Google Cloud Storage (GCS) และ Google Bigquery
### 7.1 สร้าง Project และ Key บน Google Cloud
### 7.2 นําไฟล์JSON มาเก็บไวใน Folder ใน codespace เพื่อให้สามารถเชื่อมต่อกับ Airflow ได ้แต่ห้ามนําขึ้น Git จึงต้องสร้าง .gitignore เมื่อสร้างเสร็จแล้วชื่อไฟลจะแสดงเป็นสีเทา

### Step : Cloud Storage
### 8.สร้าง Bucket บน Google Cloud Storage โดยสร้าง ทั้งหมด 2 Bucket เพื่อใช้ในการเก็บข้อมูล ไดแก่ 
### - raw-data-online-retaila ใชในการเก็บ raw data 
### - de-capstone-08062024

### 9. เชื่อมต่อ airflow เข้ากับ Google Cloud โดยการใช ้key ที่โหลดมาเก็บไว้บน codespace
### 10. นํา Key จาก JSON File ที่ได้ จาก GCS มาใส่ใน Keyfile JSON เพื่อให้สามารถเชื่อมต่อกันได้
### 11. ทํา Automated pipeline ด้วย Airflow โดยจะมี Loop ดังนี้ GCS (raw-data-online-retail) ➔ GCS (de-capstone-08062024) ➔ Google Bigquery จากนั้นสร้าง DAG เพื่อสร้าง Loop การทํางานบน Airflow
### 12.สร้าง GCSToGCSOperator เพื่อนําข้อมูล จาก GCS Bucket : raw-data-online-retail ที่ทำการ manual ใส่ไฟล์ CSV เข้าสู่ Bucket : de-capstone-08062024 ข้อมูลทั้ง 2 Bucket ต้องมีไฟล์ csv เหมือนกัน

### Step: Data Warehouse
### 13.สร้าง datasets : raw_invoices บน Google Bigquery (BigQueryCreateEmptyDatasetOperator) เพื่อเตรียมในการนําข้อมูลจาก GCS เข้า Google Bigquery
### 14. นําข้อมูลจาก GCS : de-capstone-08062024 เข้าสู่ Google Bigquery (GCSToBigQueryOperator) จะมีสถานะเป็น tables
### 15. สร้าง Partition table เพื่อให้ข้อมูลสามารถ Query ได้เร็วขึ้น

### Step: Data Transformation (DBT)
### 16. Download library dbt-core dbt-bigquery เพื่อให้สามารถใช้งาน เครื่องมือ dbt และใช ้dbt เชี่อมต่อกับ bigquery ได้
```sh
pip install dbt-core dbt-bigquery
```
### 17.สร้าง project profile dbt ที่สร้างด้วย google bigqeury มีรายละเอียดดังนี้ เช่น dbt_datamodeling

```sh
dbt init
```
### 18.สร้างไฟล์ profiles.yml บน DW-AND-BI/Data-Engineering-Capstone/dbt_datamodeling folder และนําข้อมูลจาก code มาใส่ข้อมูลในไฟล์ profiles.yml ที่สร้างไว ้