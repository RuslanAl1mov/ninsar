# Ninsar Leaderboard API (Django + DRF + JWT)

## 📜 Техническое задание

* В базе есть таблица **CompetitionResult** с полями:

  | поле          | тип                                | примечание                       |
  | ------------- | ---------------------------------- | -------------------------------- |
  | `competition` | FK → `Competition`                 | название/ID соревнования         |
  | `room`        | FK → `Room`, nullable              | комната/сессия                   |
  | `team`        | FK → `Team`, nullable              | команда                          |
  | `user`        | FK → `User`                        | участник                         |
  | `scenario`    | `practice / qualification / final` | сценарий попытки                 |
  | `flight_time` | `float`                            | время полёта, **меньше = лучше** |
  | `false_start` | `bool`                             | признак фальстарта               |

* Требуется защищённый эндпоинт **POST** `/results/results/get-competition-result/`
  *Заголовок*: `Authorization: Bearer <access‑token>`.

* **Запрос**

  ```jsonc
  {
    "competition": "Summer Cup 2025", // name
    "user_name":  "user1",            // username
    "scenario":   "qualification"     // FlightScenario
  }
  ```

* **Ответ**

  ```jsonc
  {
    "user_result": {           // место и результат запрашивающего
      "position": 5,
      "user_name": "user1",
      "flight_time": 12.34,
      "command_name": "Falcons"
    },
    "other_results": [         // до 9 лучших, без alice
      { "position": 1, "user_name": "bob",   "flight_time": 10.98, "command_name": "Eagles" },
      { "position": 2, ... }
    ]
  }
  ```

## ⚙️ Установка

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt  # Django, djangorestframework, simplejwt
python manage.py migrate
python manage.py createsuperuser   # admin интерфейс
```

### (Опционально) Загрузить демо‑данные

```bash
python manage.py loaddata fixture_20_results.json
```

## 🔐 Проверка авторизации

### 1. Получить токен

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"alice","password":"secret123"}'
```

Ответ:

```json
{"access":"<ACCESS>","refresh":"<REFRESH>"}
```

### 2. Запрос без токена ➜ 401

```bash
curl -X POST http://127.0.0.1:8000/api/v1/results/results/get-competition-result/ \
     -H "Content-Type: application/json" \
     -d '{"competition":"Summer Cup 2025","user_name":"alice","scenario":"qualification"}'
```

### 3. Запрос с токеном ➜ 200

```bash
curl -X POST http://127.0.0.1:8000/api/v1/results/results/get-competition-result/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <ACCESS>" \
     -d '{"competition":"Summer Cup 2025","user_name":"user1","scenario":"qualification"}'
```

### 4. Обновить `access`

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh":"<REFRESH>"}'
```

## 🧪 Тест в Postman

1. **POST** `/api/v1/login/` – получить пару токенов.
2. Создайте переменную `access_token` со значением из поля `access`.
3. **POST** `/api/v1/results/results/get-competition-result/`
   *Authorization → Bearer Token*: `{{access_token}}`
   *Body*: JSON как в примере.
4. Убедитесь, что ответ содержит нужную структуру.

## 🛠️ Параметры в `settings.py`

```
REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES = [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
]
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```
