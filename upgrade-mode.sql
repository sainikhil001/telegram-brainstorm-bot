-- Run this once in Neon's SQL Editor if you already ran the earlier schema.sql.
CREATE TABLE IF NOT EXISTS brainstorm_mode (
  chat_id BIGINT NOT NULL,
  thread_id BIGINT NOT NULL DEFAULT 0,
  mode TEXT NOT NULL DEFAULT 'normal'
    CHECK (mode IN ('normal', 'brainstorm', 'challenge')),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (chat_id, thread_id)
);
