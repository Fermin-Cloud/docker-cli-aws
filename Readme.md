>[!WARNING]
> FOLLOW THE TUTORIAL, The use of client.py is optional

```bash
docker build -t aws-translate .
docker run -p 8000:8000 --env-file .env aws-translate

curl -X POST "http://localhost:8000/translate/" -H "Content-Type: application/json" -d '{"text":"Hola","source_language":"es","target_language":"en"} 
```
