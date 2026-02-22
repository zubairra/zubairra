-- users table
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'member',
  broker_name TEXT,
  broker_user_id TEXT,
  api_key TEXT,
  access_token TEXT,
  token_updated_at DATETIME,
  is_active BOOLEAN NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- trades table
CREATE TABLE IF NOT EXISTS trades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  broker TEXT NOT NULL,
  exchange TEXT NOT NULL,
  segment TEXT NOT NULL,
  symbol TEXT NOT NULL,
  side TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  buy_value REAL NOT NULL DEFAULT 0,
  sell_value REAL NOT NULL DEFAULT 0,
  brokerage REAL NOT NULL DEFAULT 0,
  stt REAL NOT NULL DEFAULT 0,
  exchange_charges REAL NOT NULL DEFAULT 0,
  gst REAL NOT NULL DEFAULT 0,
  net_pnl REAL NOT NULL DEFAULT 0,
  trade_date DATE NOT NULL,
  order_id TEXT,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_trades_user_date ON trades(user_id, trade_date);
