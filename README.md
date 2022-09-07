#This repo is for our capstone project

To dump a database called capstone into an SQL-script file:

On linux, using postgres

```bash

	$ pg_dump capstone > databaseSqlScript.sql

```

To reload such a script into a (freshly created) database named capstone:

```bash

	$ psql -d capstone -f databaseSqlScript.sql

```


