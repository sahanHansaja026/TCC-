# download postgresql
-------------------------------------------------------
```bash
https://www.postgresql.org/download/
```

# download pgadmin
``` bash
https://www.pgadmin.org/download/
```

# backend run
--------------------------------------------------------
```bash
cd backend
```

```bash
Remove-Item -Recurse -Force .\venv
```

```bash
python -m venv venv
```

```bash
.\venv\Scripts\Activate
```

```bash
pip install -r requirements.txt
```

```bash
uvicorn main:app --reload

```
# client (front end) run
--------------------------------------------------------
```bash
cd client
```

```bash
npm i
```
```bash
npm run dev
```
