import datetime
from random import randint

import fastapi.responses
import uvicorn
from fastapi import FastAPI

from src.UI.ui import templates
from src.db.db_funcs import *

app = FastAPI()

conn = create_db("random_user.db")
glob_cursor = conn.cursor()


@app.get("/random")
def get_random_user(request: fastapi.Request):
    """Получение случайной карточки пользователя с сервера"""
    cursor_random = conn.cursor()
    total_users = get_users_count(glob_cursor)
    random_id = randint(0, total_users)
    try:
        random_user_data = cursor_random.execute("SELECT * from random_user WHERE id = ?", (random_id,)).fetchone()
        return templates.TemplateResponse("random.html", {"request": request, "user": random_user_data})
    except Exception as e:
        with open("log/log.txt", "a", encoding="utf-8") as fl:
            tm = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
            fl.write(f"{tm} -- {e}\n")
    finally:
        cursor_random.close()


@app.get("/get-photo/{user_id}")
def get_user_photo(user_id: int):
    """Получение фотографии пользователя"""
    cursor_1 = conn.cursor()
    try:
        photo = cursor_1.execute("SELECT photo FROM random_user WHERE id = ?", (int(user_id),)).fetchone()
    except Exception as e:
        with open("log/log.txt", "a", encoding="utf-8") as fl:
            tm = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S")
            fl.write(f"{tm} -- {e}\n")
    finally:
        cursor_1.close()
    if photo and photo[0]:
        return fastapi.Response(content=photo[0], media_type="image/jpeg")
    else:
        return fastapi.Response(status_code=404)


@app.get('/', response_class=fastapi.responses.HTMLResponse)
def root(request: fastapi.Request, count: int = 10, show_counter: int = 50):
    """Главная страница с таблицей"""
    total_users = get_users_count(glob_cursor)
    limit = min(count, show_counter)
    users = get_users_info_from_db(glob_cursor, limit)
    return templates.TemplateResponse("table.html",
                                      {"request": request, "show_counter": int(show_counter), "count": count,
                                       "users": users, "total_users": total_users})


@app.get("/{user_id}", response_class=fastapi.responses.HTMLResponse)
def get_user_card(request: fastapi.Request, user_id: int):
    """Получение карточки пользователя по id из БД"""
    user_page_cursor = conn.cursor()
    user_data = user_page_cursor.execute("SELECT * FROM random_user WHERE id = ?", (user_id,)).fetchone()
    if not user_data:
        return fastapi.Response(content="No user with this ID on a Server", status_code=404)
    user_page_cursor.close()
    return templates.TemplateResponse("user_card.html", {"request": request, "user_data": user_data})


if __name__ == "__main__":
    make_table_random_user(glob_cursor)
    db_row_value = glob_cursor.execute("SELECT COUNT(*) FROM random_user")
    if not db_row_value.fetchone()[0]:
        push_data_to_table(glob_cursor, conn)
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
