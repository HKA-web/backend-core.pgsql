# Arsitektur
```
+----------------+
|    API Gateway |
+----------------+
       |
       | REST / HTTP
       v
+-------------------------+
|  QueryTool Microservice |
|-------------------------|
| - PgSQL (py micro)      |
+-------------------------+
       |
       | Pool / driver
       v
+----------------+
| Databases      |
| - Postgres     |
+----------------+
```

## Manual Debug, jalankan di terminal:
```
source venv/Scripts/activate
uvicorn src.main:app --reload --port 8002
curl -X POST http://127.0.0.1:8002/pgsql/query \
  -H "Content-Type: application/json" \
  -d '{"sql": "select * from sc_mst.karyawan", "skip": 0, "take": 10}'
```

## Hasil
```
{"columns":["branch","nik"],"rows":[{"branch":"NBISMG","nik":
"49xxxxx    ","nmlengkap":"LOREM IPSUM"}],"totalCount":5556}
```
