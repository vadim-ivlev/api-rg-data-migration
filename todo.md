- run in docker
- move pgdata on dtest to another location
- deploy to dtest

- done. change articles_new to articles in go code.

- done. change index names on articles on ilmira.local and dockertest.rgwork.ru
  
```sql  
-- new field
ALTER TABLE articles ADD COLUMN IF NOT EXISTS elastic_status text;

-- rename Индексов
ALTER INDEX IF EXISTS idx_articles_process_status RENAME TO articles_process_status__idx;
ALTER INDEX IF EXISTS idx_127405_articles_migration_status_idx RENAME TO articles_migration_status__idx;
ALTER INDEX IF EXISTS idx_127405_sqlite_autoindex_articles_1 RENAME TO articles_pkey;

-- create indexes
CREATE INDEX IF NOT EXISTS articles_migration_status__idx ON articles (migration_status);
CREATE INDEX IF NOT EXISTS articles_process_status__idx   ON articles (process_status);
CREATE INDEX IF NOT EXISTS articles_elastic_status__idx   ON articles (elastic_status);
```

- done. change migration_status default value on ilmira.local and dockertest.rgwork.ru
```sql
ALTER TABLE articles ALTER COLUMN migration_status DROP DEFAULT;
```



```sql
ALTER TABLE articles ALTER COLUMN migration_status DROP DEFAULT;
ALTER TABLE ONLY articles ALTER COLUMN migration_status SET DEFAULT 'en_GB';
ALTER TABLE table_name ADD COLUMN IF NOT EXISTS column_name INTEGER;
```