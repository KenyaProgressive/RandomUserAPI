import fastapi.responses
import uvicorn
from fastapi import FastAPI

from src.UI.ui import templates
from src.const import START_SERVER_DATA_GENERATE_LIMIT
from src.db.db_funcs import *

app = FastAPI()
conn = create_db("db/random_user.db")
cursor = conn.cursor()
make_table_random_user(cursor)



@app.get('/', response_class=fastapi.responses.HTMLResponse)
def root(request: fastapi.Request, show_counter: int = 50):
    users = get_users_info()
    return templates.TemplateResponse("table.html", {"request": request, "shown_count": int(show_counter), "users": users})


if __name__ == "__main__":
    db_row_value = cursor.execute("SELECT COUNT(*) FROM random_user")
    if not db_row_value.fetchone()[0]:
        push_data_to_table(cursor, conn)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

