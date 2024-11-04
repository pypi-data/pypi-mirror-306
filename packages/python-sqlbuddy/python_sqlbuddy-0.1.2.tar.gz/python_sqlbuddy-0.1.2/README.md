
# SQL buddy

This is a project dedicated to generate SQL queries based on natural language from provided database config.

- Install sqluddy in your project using below command:

```echo ~ 
pip install sqlbuddy
```

- You can also clone this repo and install by setup.py:
    
    Clone project:

    ```echo ~
    https://github.com/pydevpk/sqlbuddy.git
    ```

- How to use this in your project:

    ```echo ~
    from sqlbuddy import Executor

    obj = Executor(DB_NAME='db_name', DB_HOST='db_host', DB_PORT=db_port, DB_USER='db_user', DB_PASSWORD='db_password', API_KEY='YOUR_OPENAI_API_KEY')
    query = obj.generate_query('ow many total physicians are there')

    cursor.execute(query)

While this is initial version of code, I am trying to improve this one, for your kind suggessions please write to me: pydev.pk@gmail.com

Happy coding :)