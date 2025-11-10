#!/usr/bin/env python3
"""
Verificador Automático de Badges

Descrição: Verifica quais badges você pode desbloquear baseado no progresso atual
Base Acessada: MULTIPLAS
Autor: AI Notion Manager
Data: 28/10/2025
Versão: 1.0
"""

def check_badges(total_xp, streak_days, tasks_today, studies_aulas, youtube_eps, duolingo_days):
    """Verifica badges disponíveis"""
    
    badges_desbloqueados = []
    badges_proximos = []
    
    # XP Total Badges
    if total_xp >= 100 and total_xp < 500:
        badges_proximos.append(("🌱 Começou", 500 - total_xp, "500 XP total", "+50 XP"))
    if total_xp >= 500:
        badges_desbloqueados.append(("🥉 Bronze", "+100 XP"))
    if total_xp >= 2500:
        badges_desbloqueados.append(("🥈 Prata", "+250 XP"))
    
    # Streak Badges
    if streak_days >= 3 and streak_days < 7:
        badges_desbloqueados.append(("🔥 Aquecendo", "+50 XP"))
    if streak_days >= 7 and streak_days < 14:
        badges_desbloqueados.append(("🔥 Esquentou", "+100 XP"))
    if streak_days >= 14 and streak_days < 30:
        badges_desbloqueados.append(("🔥 Pegando Fogo", "+250 XP"))
    if streak_days >= 30:
        badges_desbloqueados.append(("🔥 Incendiário", "+500 XP"))
    
    # Tasks em 1 dia
    if tasks_today >= 5:
        badges_desbloqueados.append(("⚡ Sprint", "+150 XP"))
    if tasks_today >= 10:
        badges_desbloqueados.append(("🎯 Sniper", "+300 XP"))
    
    # Studies
    if studies_aulas >= 1:
        badges_desbloqueados.append(("🎓 Primeiro Passo", "+25 XP"))
    if studies_aulas >= 10:
        badges_desbloqueados.append(("📖 Estudioso", "+100 XP"))
    
    # YouTube
    if youtube_eps >= 1:
        badges_desbloqueados.append(("🎬 Estreante", "+50 XP"))
    if youtube_eps >= 10:
        badges_desbloqueados.append(("📹 Produtor", "+250 XP"))
    
    # Duolingo
    if duolingo_days >= 7:
        badges_desbloqueados.append(("🦉 Duolingo Semana", "+50 XP"))
    if duolingo_days >= 30:
        badges_desbloqueados.append(("🦉 Duolingo Mês", "+100 XP"))
    if duolingo_days >= 100:
        badges_desbloqueados.append(("🦉 Duolingo Centenário", "+500 XP"))
    
    return badges_desbloqueados, badges_proximos

def main():
    """Função principal"""
    
    print("🏆 VERIFICADOR DE BADGES")
    print("=" * 60)
    
    # Input dos dados atuais
    print("\n📊 Digite seus dados atuais:\n")
    
    total_xp = int(input("XP Total Acumulado: "))
    streak_days = int(input("Streak Geral (dias): "))
    tasks_today = int(input("Tarefas hoje: "))
    studies_aulas = int(input("Total aulas completas (Studies): "))
    youtube_eps = int(input("Total episódios publicados (YouTube): "))
    duolingo_days = int(input("Streak Duolingo (dias): "))
    
    # Verificar badges
    desbloqueados, proximos = check_badges(
        total_xp, streak_days, tasks_today, 
        studies_aulas, youtube_eps, duolingo_days
    )
    
    print(f"\n{'=' * 60}")
    print("🏆 BADGES DESBLOQUEADOS")
    print(f"{'=' * 60}\n")
    
    if desbloqueados:
        for badge, xp in desbloqueados:
            print(f"  ✅ {badge} {xp}")
    else:
        print("  Nenhum badge novo desbloqueado")
    
    print(f"\n{'=' * 60}")
    print("🎯 PRÓXIMOS BADGES")
    print(f"{'=' * 60}\n")
    
    if proximos:
        for badge, falta, requisito, xp in proximos:
            print(f"  ⏳ {badge} - Falta {falta} ({requisito}) {xp}")
    else:
        print("  Continue jogando para desbloquear mais!")
    
    # Calcular XP total de badges
    total_badge_xp = sum(int(xp.replace('+', '').replace(' XP', '')) for _, xp in desbloqueados)
    
    if total_badge_xp > 0:
        print(f"\n💎 BONUS TOTAL DE BADGES: +{total_badge_xp} XP")
        print(f"📊 SEU NOVO XP: {total_xp + total_badge_xp} XP")

if __name__ == "__main__":
    main()

