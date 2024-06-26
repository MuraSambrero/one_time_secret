## Приложение - One time secrets

## Запуск
- Первым делом создаем файл `.env`
- Запускаем docker-compose коммандой - `docker-compose up --build`
- Приложение готово к работе

## Endpoints
- `api/generate`
- `api/secrets/{secret_key}`

## Фичи
- Данные хранятся во внешнем хранилище. В качестве СУБД используется PostgreSQL
- Данные хранятся в зашифрованном виде.
При этом шифрование происходит при помощи библиотеки `cryptography`.
Ответ пользователь получит только в том случае, если введет верные ключ и кодовую фразу. Тем самым расшифрует и получит данные.
- Запросы обрабатываются асинхронно
- Есть возможность задавать время жизни - TTL(в секундах)

## Как пользоваться данным приложением
- ### Вам необходимо отправить данные в виде:
```python
{
  "secret_data": "string",
  "code_phrase": "stringst",
  "ttl_seconds": 3600
}
```
После чего будет сгенерирован случайным образом ключ.

Поле - `secret_data`. Здесь вы можете написать свою тайну.

Поле - `code_phrase`. Здесь написать свою кодовую фразу, которая будет нужна как одна из составляющих для получения тайны. (Второй составляющей является ключ)

Поле - `ttl_seconds`. Здесь вы указываете время в секундах(по дефолту это 7 дней). Именно столько будет доступен данный секрет

- ### Чтобы получить секрет вам необходимо отправить по маршруту `api/secrets/{secret_key}`, данные в виде:
```python
{
  "code_phrase": "stringst"
}
```
где поле `code_phrase` это та самая кодовая фраза которую вы задавали при создании секрета.

К слову `secret_key` вы также должны обязательно указать в запросе который описан выше - `api/secrets/{secret_key}`. Вместо `{secret_key}` вы указываете сгенерированный ключ который вы получили при создании секрета.
