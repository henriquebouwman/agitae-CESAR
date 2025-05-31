import sqlite3 as con
from datetime import datetime, timedelta

def create_tables():
    """Cria todas as tabelas necessárias do sistema"""
    tables = {
        'users': """
        CREATE TABLE IF NOT EXISTS users (
            id_user INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL,
            fitness_level TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        'challenges': """
        CREATE TABLE IF NOT EXISTS challenges (
            id_challenge INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            type TEXT NOT NULL, -- 'weekly' ou 'monthly'
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            points_reward INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        'training_groups': """
        CREATE TABLE IF NOT EXISTS training_groups (
            id_group INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            location TEXT NOT NULL,
            max_members INTEGER DEFAULT 10,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id_user)
        );
        """,
        'workouts': """
        CREATE TABLE IF NOT EXISTS workouts (
            id_workout INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            duration INTEGER NOT NULL, -- em minutos
            intensity TEXT NOT NULL, -- 'baixa', 'media', 'alta'
            calories_burned INTEGER DEFAULT 0,
            notes TEXT,
            workout_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id_user)
        );
        """,
        'user_challenges': """
        CREATE TABLE IF NOT EXISTS user_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            status TEXT DEFAULT 'active', -- 'active', 'completed', 'failed'
            progress INTEGER DEFAULT 0,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL,
            FOREIGN KEY (user_id) REFERENCES users(id_user),
            FOREIGN KEY (challenge_id) REFERENCES challenges(id_challenge)
        );
        """,
        'group_members': """
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES training_groups(id_group),
            FOREIGN KEY (user_id) REFERENCES users(id_user)
        );
        """,
        'achievements': """
        CREATE TABLE IF NOT EXISTS achievements (
            id_achievement INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            points_earned INTEGER DEFAULT 0,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id_user)
        );
        """
    }
    
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        
        for table_name, sql in tables.items():
            cursor.execute(sql)
        
        conn.commit()
        status = "Todas as tabelas criadas com sucesso"
    except con.DatabaseError as error:
        status = f"Erro ao criar tabelas: {error}"
    finally:
        if conn:
            conn.close()
    return status

# ============ CRUD USUÁRIOS ============
def create_user(username, password, name, age, city, fitness_level):
    sql_user = """
    INSERT INTO users (username, password, name, age, city, fitness_level) 
    VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql_user, (username, password, name, age, city, fitness_level))
        conn.commit()
        status = "Usuário cadastrado com sucesso"
    except con.IntegrityError:
        status = "Erro: Nome de usuário já existe"
    except con.DatabaseError as error:
        status = f"Erro ao cadastrar usuário: {error}"
    finally:
        if conn:
            conn.close()
    return status

def check_login(username, password):
    sql_user = """
    SELECT id_user, name, points FROM users WHERE username = ? AND password = ?;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql_user, (username, password))
        result = cursor.fetchone()
        
        if result:
            status = f"Login realizado com sucesso! Bem-vindo, {result[1]}! Pontos: {result[2]}"
            return status, result[0]  # retorna status e user_id
        else:
            status = "Usuário ou senha incorretos"
            return status, None
    except con.DatabaseError as error:
        status = f"Erro no login: {error}"
        return status, None
    finally:
        if conn:
            conn.close()

def update_user_profile(user_id, name, age, city, fitness_level):
    sql = """
    UPDATE users SET name = ?, age = ?, city = ?, fitness_level = ? 
    WHERE id_user = ?;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (name, age, city, fitness_level, user_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            status = "Perfil atualizado com sucesso"
        else:
            status = "Usuário não encontrado"
    except con.DatabaseError as error:
        status = f"Erro ao atualizar perfil: {error}"
    finally:
        if conn:
            conn.close()
    return status

def delete_user_account(user_id, password):
    sql = """
    DELETE FROM users WHERE id_user = ? AND password = ?;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, password))
        conn.commit()
        
        if cursor.rowcount > 0:
            status = "Conta deletada com sucesso"
        else:
            status = "Senha incorreta ou usuário não encontrado"
    except con.DatabaseError as error:
        status = f"Erro ao deletar conta: {error}"
    finally:
        if conn:
            conn.close()
    return status

# ============ CRUD DESAFIOS ============
def create_challenge(title, description, challenge_type, duration_days, points_reward):
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=duration_days)
    
    sql = """
    INSERT INTO challenges (title, description, type, start_date, end_date, points_reward)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (title, description, challenge_type, start_date, end_date, points_reward))
        conn.commit()
        status = "Desafio criado com sucesso"
    except con.DatabaseError as error:
        status = f"Erro ao criar desafio: {error}"
    finally:
        if conn:
            conn.close()
    return status

def get_active_challenges():
    sql = """
    SELECT id_challenge, title, description, type, start_date, end_date, points_reward
    FROM challenges 
    WHERE is_active = 1 AND end_date >= date('now')
    ORDER BY start_date DESC;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        challenges = cursor.fetchall()
        return "Desafios carregados", challenges
    except con.DatabaseError as error:
        return f"Erro ao carregar desafios: {error}", []
    finally:
        if conn:
            conn.close()

def join_challenge(user_id, challenge_id):
    sql = """
    INSERT INTO user_challenges (user_id, challenge_id)
    VALUES (?, ?);
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, challenge_id))
        conn.commit()
        status = "Inscrição no desafio realizada com sucesso"
    except con.IntegrityError:
        status = "Você já está inscrito neste desafio"
    except con.DatabaseError as error:
        status = f"Erro ao se inscrever no desafio: {error}"
    finally:
        if conn:
            conn.close()
    return status

# ============ CRUD GRUPOS DE TREINO ============
def create_training_group(name, description, location, max_members, created_by):
    sql = """
    INSERT INTO training_groups (name, description, location, max_members, created_by)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (name, description, location, max_members, created_by))
        conn.commit()
        group_id = cursor.lastrowid
        
        # Adicionar o criador como membro do grupo
        join_group_sql = "INSERT INTO group_members (group_id, user_id) VALUES (?, ?);"
        cursor.execute(join_group_sql, (group_id, created_by))
        conn.commit()
        
        status = "Grupo de treino criado com sucesso"
    except con.DatabaseError as error:
        status = f"Erro ao criar grupo: {error}"
    finally:
        if conn:
            conn.close()
    return status

def get_groups_by_location(location):
    sql = """
    SELECT g.id_group, g.name, g.description, g.location, g.max_members,
           COUNT(gm.user_id) as current_members,
           u.name as creator_name
    FROM training_groups g
    LEFT JOIN group_members gm ON g.id_group = gm.group_id
    LEFT JOIN users u ON g.created_by = u.id_user
    WHERE g.location LIKE ?
    GROUP BY g.id_group
    ORDER BY g.created_at DESC;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (f"%{location}%",))
        groups = cursor.fetchall()
        return "Grupos encontrados", groups
    except con.DatabaseError as error:
        return f"Erro ao buscar grupos: {error}", []
    finally:
        if conn:
            conn.close()

def join_training_group(user_id, group_id):
    sql = """
    INSERT INTO group_members (group_id, user_id)
    VALUES (?, ?);
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (group_id, user_id))
        conn.commit()
        status = "Entrada no grupo realizada com sucesso"
    except con.IntegrityError:
        status = "Você já é membro deste grupo"
    except con.DatabaseError as error:
        status = f"Erro ao entrar no grupo: {error}"
    finally:
        if conn:
            conn.close()
    return status

# ============ CRUD TREINOS ============
def register_workout(user_id, workout_type, duration, intensity, calories_burned, notes=""):
    sql = """
    INSERT INTO workouts (user_id, type, duration, intensity, calories_burned, notes, workout_date)
    VALUES (?, ?, ?, ?, ?, ?, date('now'));
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, workout_type, duration, intensity, calories_burned, notes))
        
        # Calcular pontos baseado na duração e intensidade
        points = calculate_workout_points(duration, intensity)
        
        # Atualizar pontos do usuário
        update_points_sql = "UPDATE users SET points = points + ? WHERE id_user = ?;"
        cursor.execute(update_points_sql, (points, user_id))
        
        conn.commit()
        status = f"Treino registrado com sucesso! Você ganhou {points} pontos"
    except con.DatabaseError as error:
        status = f"Erro ao registrar treino: {error}"
    finally:
        if conn:
            conn.close()
    return status

def get_user_workouts(user_id, limit=10):
    sql = """
    SELECT type, duration, intensity, calories_burned, workout_date, notes
    FROM workouts 
    WHERE user_id = ?
    ORDER BY workout_date DESC
    LIMIT ?;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, limit))
        workouts = cursor.fetchall()
        return "Histórico carregado", workouts
    except con.DatabaseError as error:
        return f"Erro ao carregar histórico: {error}", []
    finally:
        if conn:
            conn.close()

# ============ RANKINGS E RELATÓRIOS ============
def get_user_ranking():
    sql = """
    SELECT name, city, points, fitness_level
    FROM users 
    ORDER BY points DESC
    LIMIT 10;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        ranking = cursor.fetchall()
        return "Ranking carregado", ranking
    except con.DatabaseError as error:
        return f"Erro ao carregar ranking: {error}", []
    finally:
        if conn:
            conn.close()

def get_user_progress(user_id):
    sql = """
    SELECT 
        u.name, u.points, u.fitness_level,
        COUNT(w.id_workout) as total_workouts,
        SUM(w.duration) as total_minutes,
        SUM(w.calories_burned) as total_calories,
        COUNT(uc.id) as active_challenges,
        COUNT(a.id_achievement) as total_achievements
    FROM users u
    LEFT JOIN workouts w ON u.id_user = w.user_id
    LEFT JOIN user_challenges uc ON u.id_user = uc.user_id AND uc.status = 'active'
    LEFT JOIN achievements a ON u.id_user = a.user_id
    WHERE u.id_user = ?
    GROUP BY u.id_user;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        progress = cursor.fetchone()
        return "Progresso carregado", progress
    except con.DatabaseError as error:
        return f"Erro ao carregar progresso: {error}", None
    finally:
        if conn:
            conn.close()

def find_training_partners(user_city, fitness_level):
    sql = """
    SELECT name, city, fitness_level, points
    FROM users 
    WHERE city = ? AND fitness_level = ?
    ORDER BY points DESC
    LIMIT 5;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_city, fitness_level))
        partners = cursor.fetchall()
        return "Parceiros encontrados", partners
    except con.DatabaseError as error:
        return f"Erro ao buscar parceiros: {error}", []
    finally:
        if conn:
            conn.close()

# ============ FUNÇÕES AUXILIARES ============
def calculate_workout_points(duration, intensity):
    """Calcula pontos baseado na duração e intensidade do treino"""
    intensity_multiplier = {
        'baixa': 1,
        'media': 1.5,
        'alta': 2
    }
    base_points = duration // 10  # 1 ponto a cada 10 minutos
    multiplier = intensity_multiplier.get(intensity.lower(), 1)
    return int(base_points * multiplier)

def add_achievement(user_id, title, description, points_earned):
    """Adiciona uma conquista para o usuário"""
    sql = """
    INSERT INTO achievements (user_id, title, description, points_earned)
    VALUES (?, ?, ?, ?);
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, title, description, points_earned))
        
        # Atualizar pontos do usuário
        update_points_sql = "UPDATE users SET points = points + ? WHERE id_user = ?;"
        cursor.execute(update_points_sql, (points_earned, user_id))
        
        conn.commit()
        return "Conquista adicionada com sucesso"
    except con.DatabaseError as error:
        return f"Erro ao adicionar conquista: {error}"
    finally:
        if conn:
            conn.close()