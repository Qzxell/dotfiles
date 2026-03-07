#!/usr/bin/env python3
import requests
import sys
import random  # <--- NUqqqqqqqEVO: Necesario para la aleatoriedad

# --- CONFIGURACIÓN ---
# API de Kenkoooo
URL_PROBLEMS = "https://kenkoooo.com/atcoder/resources/problems.json"
URL_DIFFICULTY = "https://kenkoooo.com/atcoder/resources/problem-models.json"
URL_USER = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={}&from_second=0"

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def get_data(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"{Colors.RED}Error conectando a la API: {e}{Colors.END}")
        sys.exit(1)

def main():
    print(f"{Colors.BOLD}=== AtCoder Recommendation (Random Mode) ==={Colors.END}")
    
    # 1. Obtener usuario
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    else:
        user_id = input("Usuario de AtCoder: ").strip()

    print(f"Descargando datos para: {Colors.BLUE}{user_id}{Colors.END}...")

    # 2. Descargar datos
    problems_list = get_data(URL_PROBLEMS)
    difficulty_dict = get_data(URL_DIFFICULTY)
    user_submissions = get_data(URL_USER.format(user_id))

    # 3. Procesar lo que ya resolviste (AC)
    solved_ids = set()
    for sub in user_submissions:
        if sub['result'] == 'AC':
            solved_ids.add(sub['problem_id'])

    # 4. Cruzar problemas con dificultades
    recommendations = []

    print("Analizando problemas...")

    for p in problems_list:
        pid = p['id']
        
        if pid in solved_ids: continue
        if pid not in difficulty_dict: continue
        
        difficulty = difficulty_dict[pid].get('difficulty')
        
        if difficulty is None: continue
        if difficulty < 0: continue

        recommendations.append({
            'diff': difficulty,
            'title': p['title'],
            'id': pid,
            'contest': p['contest_id'],
            'url': f"https://atcoder.jp/contests/{p['contest_id']}/tasks/{pid}"
        })

    # Nota: Ya no ordenamos 'recommendations' globalmente aquí, 
    # porque lo haremos aleatorio dentro de cada bloque.

    # 5. Función para mostrar bloque aleatorio
    def show_block(name, min_d, max_d, color, count=5):
        print(f"\n{color}{Colors.BOLD}--- {name} (Rating {min_d}-{max_d}) ---{Colors.END}")
        
        # Filtramos todos los problemas que caen en este rango
        filtered = [r for r in recommendations if min_d <= r['diff'] < max_d]
        
        if not filtered:
            print("  ¡No hay problemas disponibles en este rango!")
            return

        # --- CAMBIO IMPORTANTE: Aleatoriedad ---
        # Mezclamos la lista filtrada al azar
        random.shuffle(filtered)
        
        # Seleccionamos los primeros 'count' (que ahora son aleatorios)
        selection = filtered[:count]

        # Opcional: Ordenamos ESTA selección pequeña por dificultad 
        # para que se vea ordenado en pantalla, aunque la elección fue al azar.
        selection.sort(key=lambda x: x['diff'])

        for item in selection:
            print(f" [{int(item['diff'])}] {item['title']}")
            print(f"       {item['url']}")

    # 6. Definir rangos
    # Warmup
    show_block("WARMUP (High Green)", 800, 1200, Colors.GREEN)
    
    # Target E
    show_block("TARGET E (Cyan/Blue)", 1200, 1600, Colors.YELLOW)
    
    # Target F
    show_block("TARGET F (Blue/Yellow)", 1600, 2200, Colors.RED)

    print("\nTip: Cada vez que ejecutes esto, te dará problemas distintos.")

if __name__ == "__main__":
    main()
