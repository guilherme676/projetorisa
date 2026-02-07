python -m venv venv
.\venv\Scripts\activate

 pip install -r requirements.txt

 "SECRET_KEY=XyzkojhP7024xtxrEEGciqXom5dczPs0`nALGORITHM=HS256`nACCESS_TOKEN_EXPIRE_MINUTES=30" | Out-File -FilePath .env -Encoding utf8

 alembic upgrade head
 alembic "Nova tabela"
 
