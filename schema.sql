CREATE TABLE IF NOT EXISTS brainstorm_messages (
  chat_id BIGINT NOT NULL,
  thread_id BIGINT NOT NULL DEFAULT 0,
  message_id BIGINT NOT NULL,
  user_id BIGINT,
  speaker TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  command TEXT,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (chat_id, message_id)
);

CREATE INDEX IF NOT EXISTS brainstorm_messages_context_idx
  ON brainstorm_messages (chat_id, thread_id, created_at DESC, message_id DESC);

CREATE TABLE IF NOT EXISTS brainstorm_mode (
  chat_id BIGINT NOT NULL,
  thread_id BIGINT NOT NULL DEFAULT 0,
  mode TEXT NOT NULL DEFAULT 'normal'
    CHECK (mode IN ('normal', 'brainstorm', 'challenge')),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (chat_id, thread_id)
);
