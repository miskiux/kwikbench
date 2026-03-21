CREATE TABLE IF NOT EXISTS public.sysb (
    id SERIAL PRIMARY KEY,

    -- environment
    exec_env TEXT,s
    test_start_time TIMESTAMP WITH TIME ZONE,
    hostname TEXT,
    created_on TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    pgver INTEGER,
    pgminor INTEGER,

    -- sybench params
    test_name TEXT,
    table_count INTEGER,      
    table_size INTEGER,        
    threads INTEGER,          
    duration_sec INTEGER,   
    warmup_sec INTEGER,        

    -- sybench stdout
    total_tps NUMERIC,
    total_qps NUMERIC,
    p95_latency_ms NUMERIC,
    errors_total   BIGINT,

    -- pg_stat_statements
    mean_exec_time NUMERIC,
    stddev_exec_time NUMERIC,
    calls BIGINT,
    rows BIGINT,
    shared_blks_hit BIGINT,
    shared_blks_read BIGINT,
    blk_read_time DOUBLE PRECISION,
    blk_write_time DOUBLE PRECISION,
    query TEXT,

    -- postgresql.conf
    conf JSONB
);