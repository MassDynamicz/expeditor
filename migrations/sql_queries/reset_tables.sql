DO $$
DECLARE
    r RECORD;
BEGIN
    -- Отключить ограничения внешних ключей
    EXECUTE 'SET session_replication_role = replica';

    -- Удалить все данные из всех таблиц
    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
        EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
    END LOOP;

    -- Включить ограничения внешних ключей
    EXECUTE 'SET session_replication_role = DEFAULT';
END $$;
