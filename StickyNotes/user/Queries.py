QUERY_INSERT_USER = 'INSERT INTO user(login, password) VALUES ("{login}", "{password}")'
QUERY_UPDATE_USER = 'UPDATE user SET {fields} WHERE id={id}'
QUERY_GET_USER_TOKEN = 'SELECT access_token FROM access_token WHERE user_id="{id}"'
QUERY_GET_USER_BY_ID = 'SELECT id, login, name, last_name FROM user WHERE id="{id}"'
QUERY_GET_USER_BY_LOGIN = 'SELECT id, login, name, last_name FROM user WHERE login="{login}"'
QUERY_GET_USER_ID_BY_CREDENTIALS = 'SELECT id FROM user WHERE login="{login}" AND password="{password}"'
QUERY_GET_USER_ID_BY_TOKEN = 'SELECT user_id AS id FROM access_token WHERE access_token="{access_token}"'
QUERY_SET_USER_TOKEN = 'INSERT INTO access_token(user_id, access_token) VALUES ({id}, "{token}")'
QUERY_SEARCH_USER = 'SELECT id, login, name, last_name FROM user WHERE login LIKE "%{query}%"'
