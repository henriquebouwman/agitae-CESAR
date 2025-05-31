def plot_menu():
    """Menu principal do sistema"""
    print("="*50)
    print("🏃‍♂️ Seja bem-vindo à plataforma Agitae 🏃‍♀️")
    print("="*50)
    print("1. Criar conta")
    print("2. Fazer login")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def plot_cadastro():
    """Interface de cadastro de usuário"""
    print("="*50)
    print("📝 Cadastro de Usuário")
    print("="*50)
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    name = input("Digite seu nome completo: ")
    
    # Validação de idade
    while True:
        try:
            age = int(input("Digite sua idade: "))
            if age < 13:
                print("Idade mínima: 13 anos")
                continue
            break
        except ValueError:
            print("Por favor, digite um número válido.")
    
    city = input("Digite sua cidade: ")
    
    # Seleção do nível de fitness
    print("\n🏋️‍♂️ Níveis de condicionamento físico:")
    print("1. Iniciante")
    print("2. Intermediário") 
    print("3. Avançado")
    
    while True:
        fitness_choice = input("Escolha seu nível (1-3): ")
        fitness_levels = {"1": "Iniciante", "2": "Intermediário", "3": "Avançado"}
        if fitness_choice in fitness_levels:
            fitness_level = fitness_levels[fitness_choice]
            break
        print("Opção inválida! Escolha 1, 2 ou 3.")
    
    return username, password, name, age, city, fitness_level

def plot_login():
    """Interface de login"""
    print("="*50)
    print("🔐 Login")
    print("="*50)
    username = input("Digite o nome de usuário: ")
    password = input("Digite a senha: ")
    return username, password

def plot_user_menu(user_name, user_points):
    """Menu do usuário logado"""
    print("="*60)
    print(f"🏠 Painel do Usuário - {user_name} | Pontos: {user_points}")
    print("="*60)
    print("1. 💪 Registrar Treino")
    print("2. 🏆 Ver Desafios Disponíveis")
    print("3. 👥 Grupos de Treino")
    print("4. 📊 Meu Progresso")
    print("5. 🥇 Ranking Geral")
    print("6. 🤝 Encontrar Parceiros")
    print("7. ⚙️ Editar Perfil")
    print("8. ❌ Deletar Conta")
    print("9. 🚪 Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def plot_register_workout():
    """Interface para registrar treino"""
    print("="*50)
    print("💪 Registrar Novo Treino")
    print("="*50)
    
    # Tipos de treino
    print("Tipos de treino disponíveis:")
    workout_types = {
        "1": "Corrida",
        "2": "Musculação", 
        "3": "Natação",
        "4": "Ciclismo",
        "5": "Yoga",
        "6": "Crossfit",
        "7": "Caminhada",
        "8": "Outro"
    }
    
    for key, value in workout_types.items():
        print(f"{key}. {value}")
    
    while True:
        type_choice = input("Escolha o tipo de treino (1-8): ")
        if type_choice in workout_types:
            workout_type = workout_types[type_choice]
            break
        print("Opção inválida!")
    
    # Duração
    while True:
        try:
            duration = int(input("Duração do treino (em minutos): "))
            if duration > 0:
                break
            print("Duração deve ser maior que 0")
        except ValueError:
            print("Digite um número válido")
    
    # Intensidade
    print("\nIntensidade:")
    print("1. Baixa")
    print("2. Média")
    print("3. Alta")
    
    while True:
        intensity_choice = input("Escolha a intensidade (1-3): ")
        intensities = {"1": "baixa", "2": "media", "3": "alta"}
        if intensity_choice in intensities:
            intensity = intensities[intensity_choice]
            break
        print("Opção inválida!")
    
    # Calorias queimadas
    while True:
        try:
            calories = int(input("Calorias queimadas (estimativa): "))
            if calories >= 0:
                break
            print("Valor deve ser positivo")
        except ValueError:
            print("Digite um número válido")
    
    notes = input("Observações (opcional): ")
    
    return workout_type, duration, intensity, calories, notes

def plot_challenges_menu():
    """Menu de desafios"""
    print("="*50)
    print("🏆 Menu de Desafios")
    print("="*50)
    print("1. Ver desafios disponíveis")
    print("2. Criar novo desafio")
    print("3. Meus desafios ativos")
    print("4. Voltar")
    opcao = input("Escolha uma opção: ")
    return opcao

def plot_create_challenge():
    """Interface para criar desafio"""
    print("="*50)
    print("🎯 Criar Novo Desafio")
    print("="*50)
    
    title = input("Título do desafio: ")
    description = input("Descrição: ")
    
    print("\nTipo de desafio:")
    print("1. Semanal")
    print("2. Mensal")
    
    while True:
        type_choice = input("Escolha o tipo (1-2): ")
        if type_choice == "1":
            challenge_type = "weekly"
            duration_days = 7
            break
        elif type_choice == "2":
            challenge_type = "monthly"
            duration_days = 30
            break
        print("Opção inválida!")
    
    while True:
        try:
            points_reward = int(input("Pontos de recompensa: "))
            if points_reward > 0:
                break
            print("Pontos devem ser maiores que 0")
        except ValueError:
            print("Digite um número válido")
    
    return title, description, challenge_type, duration_days, points_reward

def plot_groups_menu():
    """Menu de grupos de treino"""
    print("="*50)
    print("👥 Menu de Grupos de Treino")
    print("="*50)
    print("1. Buscar grupos por localização")
    print("2. Criar novo grupo")
    print("3. Meus grupos")
    print("4. Voltar")
    opcao = input("Escolha uma opção: ")
    return opcao

def plot_create_group():
    """Interface para criar grupo de treino"""
    print("="*50)
    print("🏃‍♂️ Criar Grupo de Treino")
    print("="*50)
    
    name = input("Nome do grupo: ")
    description = input("Descrição: ")
    location = input("Localização: ")
    
    while True:
        try:
            max_members = int(input("Número máximo de membros: "))
            if max_members > 0:
                break
            print("Número deve ser maior que 0")
        except ValueError:
            print("Digite um número válido")
    
    return name, description, location, max_members

def plot_edit_profile():
    """Interface para editar perfil"""
    print("="*50)
    print("⚙️ Editar Perfil")
    print("="*50)
    
    name = input("Novo nome completo: ")
    
    while True:
        try:
            age = int(input("Nova idade: "))
            if age >= 13:
                break
            print("Idade mínima: 13 anos")
        except ValueError:
            print("Digite um número válido")
    
    city = input("Nova cidade: ")
    
    print("\n🏋️‍♂️ Novo nível de condicionamento:")
    print("1. Iniciante")
    print("2. Intermediário")
    print("3. Avançado")
    
    while True:
        fitness_choice = input("Escolha o nível (1-3): ")
        fitness_levels = {"1": "Iniciante", "2": "Intermediário", "3": "Avançado"}
        if fitness_choice in fitness_levels:
            fitness_level = fitness_levels[fitness_choice]
            break
        print("Opção inválida!")
    
    return name, age, city, fitness_level

def display_challenges(challenges):
    """Exibe lista de desafios"""
    if not challenges:
        print("Nenhum desafio disponível no momento.")
        return
    
    print("="*70)
    print("🏆 DESAFIOS DISPONÍVEIS")
    print("="*70)
    
    for i, challenge in enumerate(challenges, 1):
        id_challenge, title, description, type_ch, start_date, end_date, points = challenge
        print(f"\n{i}. {title}")
        print(f"   📝 {description}")
        print(f"   📅 Tipo: {type_ch.title()}")
        print(f"   📅 Período: {start_date} até {end_date}")
        print(f"   🎯 Recompensa: {points} pontos")
        print("-" * 50)

def display_ranking(ranking):
    """Exibe o ranking de usuários"""
    if not ranking:
        print("Nenhum usuário encontrado no ranking.")
        return
    
    print("="*60)
    print("🥇 RANKING GERAL")
    print("="*60)
    
    for i, (name, city, points, fitness_level) in enumerate(ranking, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
        print(f"{medal} {name} - {city}")
        print(f"    📊 {points} pontos | 💪 {fitness_level}")
        print("-" * 40)

def display_groups(groups):
    """Exibe lista de grupos"""
    if not groups:
        print("Nenhum grupo encontrado.")
        return
    
    print("="*70)
    print("👥 GRUPOS DE TREINO")
    print("="*70)
    
    for i, group in enumerate(groups, 1):
        id_group, name, description, location, max_members, current_members, creator = group
        print(f"\n{i}. {name}")
        print(f"   📝 {description}")
        print(f"   📍 {location}")
        print(f"   👥 {current_members}/{max_members} membros")
        print(f"   👤 Criado por: {creator}")
        print("-" * 50)

def display_user_progress(progress):
    """Exibe progresso do usuário"""
    if not progress:
        print("Erro ao carregar progresso.")
        return
    
    name, points, fitness_level, total_workouts, total_minutes, total_calories, active_challenges, achievements = progress
    
    print("="*60)
    print(f"📊 PROGRESSO DE {name.upper()}")
    print("="*60)
    print(f"💪 Nível de Condicionamento: {fitness_level}")
    print(f"🏆 Pontos Total: {points}")
    print(f"🏃‍♂️ Total de Treinos: {total_workouts or 0}")
    print(f"⏱️ Tempo Total de Treino: {total_minutes or 0} minutos")
    print(f"🔥 Calorias Queimadas: {total_calories or 0}")
    print(f"🎯 Desafios Ativos: {active_challenges or 0}")
    print(f"🏅 Conquistas: {achievements or 0}")
    print("="*60)

def display_workout_history(workouts):
    """Exibe histórico de treinos"""
    if not workouts:
        print("Nenhum treino registrado ainda.")
        return
    
    print("="*70)
    print("📋 HISTÓRICO DE TREINOS")
    print("="*70)
    
    for workout in workouts:
        workout_type, duration, intensity, calories, date, notes = workout
        print(f"📅 {date}")
        print(f"   💪 {workout_type} - {duration} min")
        print(f"   🔥 Intensidade: {intensity.title()}")
        print(f"   🔥 Calorias: {calories}")
        if notes:
            print(f"   📝 Observações: {notes}")
        print("-" * 50)

def display_training_partners(partners):
    """Exibe parceiros de treino sugeridos"""
    if not partners:
        print("Nenhum parceiro encontrado na sua região com o mesmo nível.")
        return
    
    print("="*60)
    print("🤝 PARCEIROS DE TREINO SUGERIDOS")
    print("="*60)
    
    for partner in partners:
        name, city, fitness_level, points = partner
        print(f"👤 {name}")
        print(f"   📍 {city}")
        print(f"   💪 Nível: {fitness_level}")
        print(f"   🏆 Pontos: {points}")
        print("-" * 40)

def confirm_action(message):
    """Confirma uma ação crítica"""
    print(f"\n⚠️ {message}")
    while True:
        confirm = input("Digite 'CONFIRMAR' para prosseguir ou 'CANCELAR' para voltar: ").upper()
        if confirm in ['CONFIRMAR', 'CANCELAR']:
            return confirm == 'CONFIRMAR'
        print("Digite apenas 'CONFIRMAR' ou 'CANCELAR'")

def get_password_confirmation():
    """Solicita confirmação de senha para ações críticas"""
    return input("Digite sua senha para confirmar: ")

def pause_screen():
    """Pausa a tela para leitura"""
    input("\nPressione ENTER para continuar...")

def clear_screen():
    """Limpa a tela (simulado com quebras de linha)"""
    print("\n" * 50)