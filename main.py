from utilities import *  # Pomocné utility funkce

# Načtení prvků a skupin ze souborů
elements = get_elements('elements.csv')  # Načtení prvků z CSV souboru
groups = get_groups('groups.json')  # Načtení skupin z JSON souboru

# Nekonečný cyklus pro interakci s uživatelem přes menu
while True:
    menu_item = menu()  # Zobrazení menu a získání volby uživatele

    if menu_item == '0':  # Ukončení programu
        print('Program ukončen.')
        break
    elif menu_item == '1':  # Vyhledávání prvku
        print('Vybraná předvolba: 1 - Vyhledávání prvku')
        print('\nPodle:')
        print('1 - Názvu')  # Možnost hledat podle názvu
        print('2 - Značky')  # Možnost hledat podle značky
        print('3 - Protonového čísla')  # Možnost hledat podle protonového čísla

        predvolba = -1  # Počáteční hodnota pro volbu
        while predvolba == -1:
            predvolba = input('Zadej číslo předvolby:')
            if predvolba >= '1' or predvolba <= '3':  # Kontrola platnosti předvolby
                # Vyhledání prvku na základě předvolby
                find_element(elements, predvolba, input(f'Zadej {"název" if predvolba == "1" else ("značku" if predvolba == "2" else "protonové číslo")} prvku: '))
            else:
                print('Neznámá předvolba. Zkus to znova.')
                predvolba = -1  # Reset předvolby při neplatném vstupu
    elif menu_item == '2':  # Export prvků do XML
        print('Vybraná předvolba: 2 - Export prvků ve vybrané skupině nebo periodě do XML')
        cislo, vyber = group_or_period_input()  # Výběr skupiny nebo periody
        filename = filename_input('.xml')  # Zadání názvu souboru
        part_of_elements = None
        if vyber == '1':  # Filtrace podle skupiny
            part_of_elements = find_all_in_groups(elements, cislo)
        elif vyber == '2':  # Filtrace podle periody
            part_of_elements = find_all_in_periods(elements, cislo)
        # Export vyfiltrovaných prvků do XML souboru
        export_to_xml(filename, part_of_elements, f'Přehled prvků v {cislo}. {"skupině" if vyber == "1" else "periodě"}')

    elif menu_item == '3':  # Výpočet průměrné relativní atomové hmotnosti
        print('Vybraná předvolba: 3 - Průměrná relativní atomová hmotnost prvků ve vybrané skupině nebo periodě')
        cislo, vyber = group_or_period_input()  # Výběr skupiny nebo periody
        if vyber == '1':  # Výpočet pro skupinu
            print(f'Průměrná atomová hmotnost prvků ve {cislo}. skupině je {calculate_atomic_mass_avg(find_all_in_groups(elements, cislo))}')
        elif vyber == '2':  # Výpočet pro periodu
            print(f'Průměrná atomová hmotnost prvků v {cislo}. periodě je {calculate_atomic_mass_avg(find_all_in_periods(elements, cislo))}')
    elif menu_item == '4':  # Generování HTML tabulky
        print('\nVybraná předvolba: 4 - Vygenerovat HTML periodickou tabulku prvků')
        filename = filename_input('.html')  # Zadání názvu souboru
        export_table(filename, make_table(elements, groups))  # Export tabulky do HTML
    elif menu_item == '5':  # Export do Markdown souboru
        print('Vybraná možnost: 5 - Přehled prvků v konkrétní skupině nebo periodě do markdown souboru')
        cislo, vyber = group_or_period_input()  # Výběr skupiny nebo periody
        filename = filename_input('.md')  # Zadání názvu souboru
        part_of_elements = None
        if vyber == '1':  # Filtrace podle skupiny
            part_of_elements = find_all_in_groups(elements, cislo)
        elif vyber == '2':  # Filtrace podle periody
            part_of_elements = find_all_in_periods(elements, cislo)
        # Export vyfiltrovaných prvků do Markdown souboru
        export_to_md(filename, part_of_elements, f'Prvky v {cislo}. {"skupině" if vyber == "1" else "periodě"}: ')
