change migration_status default value on ilmira.local and dockertest.rgwork.ru

```sql
ALTER TABLE articles ALTER COLUMN migration_status DROP DEFAULT;
ALTER TABLE ONLY articles ALTER COLUMN migration_status SET DEFAULT 'en_GB';
ALTER TABLE table_name ADD COLUMN IF NOT EXISTS column_name INTEGER;
```