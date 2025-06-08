# backend run
--------------------------------------------------------

cd backend

Remove-Item -Recurse -Force .\venv


python -m venv venv


.\venv\Scripts\Activate


pip install -r requirements.txt


uvicorn main:app --reload

# client (front end) run
--------------------------------------------------------

cd client

npm i

npm run dev
