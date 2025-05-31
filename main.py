from sql import *
from ui import *

def main():
    """Função principal do sistema"""
    print("Inicializando sistema Agitae...")
    create_tables()
    print("Sistema inicializado com sucesso!\n")
    
    current_user_id = None
    current_user_name = None
    
    while True:
        if current_user_id is None:
            # Menu para usuários não logados
            opcao = plot_menu()
            
            if opcao == "1":
                # Cadastro de usuário
                username, password, name, age, city, fitness_level = plot_cadastro()
                result = create_user(username, password, name, age, city, fitness_level)
                print(f"\n✅ {result}")
                pause_screen()
                
            elif opcao == "2":
                # Login
                username, password = plot_login()
                result, user_id = check_login(username, password)
                print(f"\n{result}")
                
                if user_id:
                    current_user_id = user_id
                    current_user_name = username
                    print(f"Redirecionando para o painel...")
                pause_screen()
                
            elif opcao == "3":
                print("👋 Obrigado por usar o Agitae! Até logo!")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
                pause_screen()
        
        else:
            # Menu para usuários logados
            # Buscar pontos atuais do usuário
            status, progress = get_user_progress(current_user_id)
            user_points = progress[1] if progress else 0
            
            opcao = plot_user_menu(current_user_name, user_points)
            
            if opcao == "1":
                # Registrar treino
                workout_type, duration, intensity, calories, notes = plot_register_workout()
                result = register_workout(current_user_id, workout_type, duration, intensity, calories, notes)
                print(f"\n✅ {result}")
                
                # Verificar conquistas baseadas em treinos
                check_workout_achievements(current_user_id)
                pause_screen()
                
            elif opcao == "2":
                # Menu de desafios
                handle_challenges_menu(current_user_id)
                
            elif opcao == "3":
                # Menu de grupos
                handle_groups_menu(current_user_id)
                
            elif opcao == "4":
                # Progresso do usuário
                status, progress_data = get_user_progress(current_user_id)
                if progress_data:
                    display_user_progress(progress_data)
                    
                    # Mostrar histórico de treinos
                    print("\n")
                    status, workouts = get_user_workouts(current_user_id, 5)
                    display_workout_history(workouts)
                else:
                    print(f"❌ {status}")
                pause_screen()
                
            elif opcao == "5":
                # Ranking geral
                status, ranking = get_user_ranking()
                if ranking:
                    display_ranking(ranking)
                else:
                    print(f"❌ {status}")
                pause_screen()
                
            elif opcao == "6":
                # Encontrar parceiros
                status, progress_data = get_user_progress(current_user_id)
                if progress_data:
                    user_city = get_user_city(current_user_id)
                    user_fitness = get_user_fitness_level(current_user_id)
                    
                    status, partners = find_training_partners(user_city, user_fitness)
                    display_training_partners(partners)
                else:
                    print("❌ Erro ao carregar seus dados")
                pause_screen()
                
            elif opcao == "7":
                # Editar perfil
                name, age, city, fitness_level = plot_edit_profile()
                result = update_user_profile(current_user_id, name, age, city, fitness_level)
                print(f"\n✅ {result}")
                pause_screen()
                
            elif opcao == "8":
                # Deletar conta
                if confirm_action("Tem certeza que deseja DELETAR sua conta? Esta ação é IRREVERSÍVEL!"):
                    password = get_password_confirmation()
                    result = delete_user_account(current_user_id, password)
                    print(f"\n{result}")
                    
                    if "sucesso" in result:
                        print("Conta deletada. Redirecionando para o menu principal...")
                        current_user_id = None
                        current_user_name = None
                    pause_screen()
                
            elif opcao == "9":
                # Logout
                print(f"👋 Até logo, {current_user_name}!")
                current_user_id = None
                current_user_name = None
                pause_screen()
                
            else:
                print("❌ Opção inválida! Tente novamente.")
                pause_screen()

def handle_challenges_menu(user_id):
    """Gerencia o menu de desafios"""
    while True:
        opcao = plot_challenges_menu()
        
        if opcao == "1":
            # Ver desafios disponíveis
            status, challenges = get_active_challenges()
            display_challenges(challenges)
            
            if challenges:
                print("\n🎯 Deseja se inscrever em algum desafio?")
                try:
                    choice = int(input("Digite o número do desafio (0 para voltar): "))
                    if 1 <= choice <= len(challenges):
                        challenge_id = challenges[choice-1][0]
                        result = join_challenge(user_id, challenge_id)
                        print(f"\n✅ {result}")
                    elif choice != 0:
                        print("❌ Número inválido!")
                except ValueError:
                    print("❌ Digite um número válido!")
            pause_screen()
            
        elif opcao == "2":
            # Criar novo desafio
            title, description, challenge_type, duration_days, points_reward = plot_create_challenge()
            result = create_challenge(title, description, challenge_type, duration_days, points_reward)
            print(f"\n✅ {result}")
            pause_screen()
            
        elif opcao == "3":
            # Meus desafios ativos
            status, user_challenges = get_user_active_challenges(user_id)
            if user_challenges:
                print("="*60)
                print("🎯 MEUS DESAFIOS ATIVOS")
                print("="*60)
                for challenge in user_challenges:
                    title, progress, status_ch = challenge
                    print(f"📌 {title}")
                    print(f"   📊 Progresso: {progress}%")
                    print(f"   📈 Status: {status_ch}")
                    print("-" * 40)
            else:
                print("❌ Você não tem desafios ativos no momento.")
            pause_screen()
            
        elif opcao == "4":
            break
        else:
            print("❌ Opção inválida!")
            pause_screen()

def handle_groups_menu(user_id):
    """Gerencia o menu de grupos"""
    while True:
        opcao = plot_groups_menu()
        
        if opcao == "1":
            # Buscar grupos por localização
            location = input("Digite a localização para buscar grupos: ")
            status, groups = get_groups_by_location(location)
            display_groups(groups)
            
            if groups:
                print("\n👥 Deseja entrar em algum grupo?")
                try:
                    choice = int(input("Digite o número do grupo (0 para voltar): "))
                    if 1 <= choice <= len(groups):
                        group_id = groups[choice-1][0]
                        result = join_training_group(user_id, group_id)
                        print(f"\n✅ {result}")
                    elif choice != 0:
                        print("❌ Número inválido!")
                except ValueError:
                    print("❌ Digite um número válido!")
            pause_screen()
            
        elif opcao == "2":
            # Criar novo grupo
            name, description, location, max_members = plot_create_group()
            result = create_training_group(name, description, location, max_members, user_id)
            print(f"\n✅ {result}")
            pause_screen()
            
        elif opcao == "3":
            # Meus grupos
            status, user_groups = get_user_groups(user_id)
            if user_groups:
                print("="*60)
                print("👥 MEUS GRUPOS")
                print("="*60)
                for group in user_groups:
                    name, location, members_count = group
                    print(f"🏃‍♂️ {name}")
                    print(f"   📍 {location}")
                    print(f"   👥 {members_count} membros")
                    print("-" * 40)
            else:
                print("❌ Você não faz parte de nenhum grupo ainda.")
            pause_screen()
            
        elif opcao == "4":
            break
        else:
            print("❌ Opção inválida!")
            pause_screen()

def check_workout_achievements(user_id):
    """Verifica e adiciona conquistas baseadas em treinos"""
    status, progress = get_user_progress(user_id)
    if not progress:
        return
    
    total_workouts = progress[3] or 0
    total_minutes = progress[4] or 0
    
    # Conquista: Primeiro treino
    if total_workouts == 1:
        add_achievement(user_id, "Primeiro Passo", "Registrou seu primeiro treino!", 50)
        print("🏅 Nova conquista desbloqueada: Primeiro Passo!")
    
    # Conquista: 10 treinos
    elif total_workouts == 10:
        add_achievement(user_id, "Dedicado", "Completou 10 treinos!", 100)
        print("🏅 Nova conquista desbloqueada: Dedicado!")
    
    # Conquista: 50 treinos
    elif total_workouts == 50:
        add_achievement(user_id, "Atleta", "Completou 50 treinos!", 250)
        print("🏅 Nova conquista desbloqueada: Atleta!")
    
    # Conquista: 1000 minutos
    if total_minutes >= 1000 and total_minutes < 1060:  # Margem para novo treino
        add_achievement(user_id, "Resistência", "Acumulou 1000 minutos de treino!", 200)
        print("🏅 Nova conquista desbloqueada: Resistência!")

def get_user_city(user_id):
    """Obtém a cidade do usuário"""
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute("SELECT city FROM users WHERE id_user = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else ""
    except:
        return ""
    finally:
        if conn:
            conn.close()

def get_user_fitness_level(user_id):
    """Obtém o nível de fitness do usuário"""
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute("SELECT fitness_level FROM users WHERE id_user = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else ""
    except:
        return ""
    finally:
        if conn:
            conn.close()

def get_user_active_challenges(user_id):
    """Obtém desafios ativos do usuário"""
    sql = """
    SELECT c.title, uc.progress, uc.status
    FROM user_challenges uc
    JOIN challenges c ON uc.challenge_id = c.id_challenge
    WHERE uc.user_id = ? AND uc.status = 'active'
    ORDER BY uc.joined_at DESC;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        challenges = cursor.fetchall()
        return "Desafios carregados", challenges
    except con.DatabaseError as error:
        return f"Erro ao carregar desafios: {error}", []
    finally:
        if conn:
            conn.close()

def get_user_groups(user_id):
    """Obtém grupos do usuário"""
    sql = """
    SELECT tg.name, tg.location, COUNT(gm2.user_id) as members_count
    FROM group_members gm1
    JOIN training_groups tg ON gm1.group_id = tg.id_group
    LEFT JOIN group_members gm2 ON tg.id_group = gm2.group_id
    WHERE gm1.user_id = ?
    GROUP BY tg.id_group
    ORDER BY gm1.joined_at DESC;
    """
    try:
        conn = con.connect('agitae.db')
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        groups = cursor.fetchall()
        return "Grupos carregados", groups
    except con.DatabaseError as error:
        return f"Erro ao carregar grupos: {error}", []
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()