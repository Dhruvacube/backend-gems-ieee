# IEEE GEMS Backend Task

Here are the ways to host it locally, first open a terminal and start executing the following commands:

(NOTE: You need to have [PostgreSQL ](https://www.postgresql.org/)installed installed in order to work with this API and this was tested and made in [Python3.11](https://www.python.org/downloads/release/python-3118/ "Python 3.11 relese page"))

Clone the repo

```bash
git clone https://github.com/Dhruvacube/backend-gems-ieee.git
```

Get into that directory

```bash
cd backend-gems-ieee
```

Now rename the `example.ini` to `.ini`. 

Now in the `.ini` in `line 5` at `DATABASE_URL` change the following:

- `<username>` : To your postgres username, eg `postgres`
- `<password>` : To your postgres user password, eg `cube12345`
- `<host>` : To your database host, where your database is being hosted, eg `localhost`
- `<db_name>` : To your desired database name in the PostgreSQL, eg `backendapi` (NOTE: you need to create this database in the PostgreSQL server preferably by the help of [pgadmin](https://www.pgadmin.org/ "PgAdmin website"))

A eg `DATABASE_URL` url string the `.ini`:

`postgresql+asyncpg://postgres:cube12345@localhost/backendapi`


Now in the same terminal where the first 2 bash commands were executed, execute the following commands now:

Install the dependency:

```bash
pip install -r requirements.txt
```

Setup the database programatically:

```bash
python launcher.py db init
python launcher.py db migrate
```

Now run the program:

```bash
python launcher.py
```

Now open the following links to work with api and know more about it:

- `API url where api is hosted`: [http://127.0.0.1:8000](http://127.0.0.1:8000)

- `Admin url where one see the scheduler scheduled`: [http://127.0.0.1:8000](http://127.0.0.1:8000)

- `The documentation of API (to see what all the routes and its syntax)`: [http://127.0.0.1/docs](http://127.0.0.1/docs)
