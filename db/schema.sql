PRAGMA foreign_keys = ON;

-- Odalar: oyuncunun gezebileceği her mekan
CREATE TABLE IF NOT EXISTS rooms (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    image_path  TEXT
);

-- İpuçları: odalarda bulunabilecek fiziksel/belgesel kanıtlar
CREATE TABLE IF NOT EXISTS clues (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id     INTEGER NOT NULL REFERENCES rooms(id),
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    clue_type   TEXT    NOT NULL CHECK (clue_type IN ('physical', 'document', 'witness')),
    is_key_clue INTEGER NOT NULL DEFAULT 0  -- 1 = çelişki tespiti için zorunlu
);

-- Şüpheliler
CREATE TABLE IF NOT EXISTS suspects (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    NOT NULL,
    image_path  TEXT,
    is_killer   INTEGER NOT NULL DEFAULT 0,  -- 1 = gerçek katil (tek satır)
    motive      TEXT,
    alibi       TEXT
);

-- İfadeler: şüphelilerin sorgulama sırasında verdiği yanıtlar
-- trigger_type = 'initial'      → ilk karşılaşmada söylenir
-- trigger_type = 'after_clue'   → oyuncu belirli bir ipucunu topladıktan sonra açılır
-- trigger_type = 'confronted'   → çelişki yakalandıktan sonra açılır
CREATE TABLE IF NOT EXISTS statements (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    suspect_id   INTEGER NOT NULL REFERENCES suspects(id),
    trigger_type TEXT    NOT NULL CHECK (trigger_type IN ('initial', 'after_clue', 'confronted')),
    trigger_clue INTEGER REFERENCES clues(id),  -- after_clue için hangi ipucu tetikliyor
    content      TEXT    NOT NULL,
    is_lie       INTEGER NOT NULL DEFAULT 0      -- 1 = yalan ifade
);

-- Çelişkiler: hangi yalan ifade hangi ipucuyla çürütülüyor
CREATE TABLE IF NOT EXISTS contradictions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    statement_id   INTEGER NOT NULL REFERENCES statements(id),
    clue_id        INTEGER NOT NULL REFERENCES clues(id),
    explanation    TEXT    NOT NULL  -- çelişkinin metinsel açıklaması
);

-- Oyun oturumları: her oynanış bir satır
CREATE TABLE IF NOT EXISTS game_sessions (
    id                   INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name          TEXT    NOT NULL,
    started_at           TEXT    NOT NULL DEFAULT (datetime('now')),
    completed_at         TEXT,
    status               TEXT    NOT NULL DEFAULT 'active'
                             CHECK (status IN ('active', 'won', 'lost')),
    accusation_suspect_id INTEGER REFERENCES suspects(id)
);

-- Toplanan ipuçları (oturum bazlı)
CREATE TABLE IF NOT EXISTS session_clues (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id   INTEGER NOT NULL REFERENCES game_sessions(id) ON DELETE CASCADE,
    clue_id      INTEGER NOT NULL REFERENCES clues(id),
    collected_at TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (session_id, clue_id)
);

-- Yapılan sorgulamalar (oturum bazlı)
CREATE TABLE IF NOT EXISTS session_interrogations (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id       INTEGER NOT NULL REFERENCES game_sessions(id) ON DELETE CASCADE,
    suspect_id       INTEGER NOT NULL REFERENCES suspects(id),
    statement_id     INTEGER NOT NULL REFERENCES statements(id),
    interrogated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- Yakalanan çelişkiler (oturum bazlı)
CREATE TABLE IF NOT EXISTS session_contradictions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id       INTEGER NOT NULL REFERENCES game_sessions(id) ON DELETE CASCADE,
    contradiction_id INTEGER NOT NULL REFERENCES contradictions(id),
    caught_at        TEXT    NOT NULL DEFAULT (datetime('now')),
    UNIQUE (session_id, contradiction_id)
);
