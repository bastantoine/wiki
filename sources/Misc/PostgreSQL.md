Below are some tips and tricks to use PostgreSQL more efficiently

> [!note]
> Most of the commands can show more information by appending a `+` at the end:
> ```
> $ psql postgresql://username:password@hostname/db
> db=> \l
> db=> \l+
> ```

## Listing databases on a cluster

```
$ psql postgresql://username:password@hostname/db
db=> \l
                                      List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |       Access privileges
-----------+----------+----------+-------------+-------------+-------------------------------
 postgres  | postgres | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 | =Tc/postgres                 +
           |          |          |             |             | postgres=CTc/postgres        +
           |          |          |             |             | gdt_agent=c/postgres
 db        | postgres | UTF8     | fr_FR.UTF-8 | fr_FR.UTF-8 | =Tc/postgres                 +
           |          |          |             |             | postgres=CTc/postgres        +
           |          |          |             |             | username=CTc/postgres        +
```

## Listing tables of a given database

```
$ psql postgresql://username:password@hostname/db
db=> \d
                         List of relations
 Schema |                Name                |   Type   |  Owner
--------+------------------------------------+----------+----------
 public | table_name                         | table    | username
 public | pg_stat_statements                 | view     | postgres
 public | pg_stat_statements_info            | view     | postgres
```

 ## Describing schema of a table

```
$ psql postgresql://username:password@hostname/db
db=> \d table_name
                                                Table "public.table_name"
     Column     |            Type             | Collation | Nullable |                         Default
----------------+-----------------------------+-----------+----------+---------------------------------------------------------
 id             | uuid                        |           | not null |
 insertion_date | timestamp without time zone |           | not null | '2024-09-25 12:46:06.1057'::timestamp without time zone
 comment        | character varying(1024)     |           | not null | ''::character varying
Indexes:
    "table_name_pkey" PRIMARY KEY, btree (id)
```
