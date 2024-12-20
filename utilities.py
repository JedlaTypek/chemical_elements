import pandas as pd
import json
import re
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

phase_cz = {
    "gas": "plynné",
    "solid": "pevné",
    "liq": "kapalina",
    "artificial": "umělé"
}

types = [
    "Nonmetal",
    "Noble Gas",
    "Alkali Metal",
    "Alkaline Earth Metal",
    "Metalloid",
    "Halogen",
    "Metal",
    "Transition Metal",
    "Lanthanide",
    "Actinide",
    "Transactinide"
]

def menu():
    print('\nMENU:')
    print('0 - Ukončení programu')
    print('1 - Vyhledávání prvku')
    print('2 - Export prvků ve vybrané skupině nebo periodě do XML')
    print('3 - Průměrná relativní atomová hmotnost prvků ve vybrané skupině nebo periodě')
    print('4 - Vygenerovat HTML periodickou tabulku prvků')
    print('5 - Přehled prvků v konkrétní skupině nebo periodě do markdown souboru')

    predvolba = -1
    while predvolba == -1:
        predvolba = input('Zadej číslo předvolby:')
        if predvolba >= '0' or predvolba <= '5':
            return predvolba
        else:
            print('Neznámá předvolba. Zkus to znova.')
            predvolba = -1

def find_element(elements, att, text):
    text = text.strip()
    element = None
    if att == '1':
        element = find_element_by_name(elements, text)
    elif att == '2':
        element = find_element_by_symbol(elements, text)
    elif att == '3':
        element = find_element_by_atomic_number(elements, text)
    if element is None:
        print('Nenašel jsem žádný prvek')
    else:
        print(f"""
Protonové číslo: {element['AtomicNumber']}
Prvek: {element['Element']}
Symbol: {element['Symbol']}
Atomová hmotnost: {element['AtomicMass']}
Počet neutronů: {element['NumberofNeutrons']}
Počet protonů: {element['NumberofProtons']}
Počet elektronů: {element['NumberofElectrons']}
Perioda: {element['Period']}
Skupina: {element['Group']}
Fáze: {element['Phase']}
Radioaktivní: {'ano' if element['Radioactive'] else 'ne'}
Přírodní: {element['Natural']}
Kov: {'ano' if element['Metal'] else 'ne'}
Nekov: {'ano' if element['Nonmetal'] else 'ne'}
Polokov: {'ano' if element['Metalloid'] else 'ne'}
Typ: {element['Type']}
Atomový poloměr: {element['AtomicRadius']} Å
Elektronegativita: {element['Electronegativity']}
První ionizační energie: {element['FirstIonization']} eV
Hustota: {element['Density']} g/cm³
Bod tání: {element['MeltingPoint']} K
Bod varu: {element['BoilingPoint']} K
Počet izotopů: {element['NumberOfIsotopes']}
Objevitel: {element['Discoverer']}
Rok objevu: {int(element['Year']) if element['Year'] else 'neznámý'}
Měrné teplo: {element['SpecificHeat']} J/(g·K)
Počet slupek: {element['NumberofShells']}
Počet valenčních elektronů: {element['NumberofValence']}
""")

def get_groups(filename):
    # Načte JSON soubor obsahující skupiny prvků a vrátí je jako slovník.
    with open(filename, 'r', encoding='utf-8') as json_file:
        groups = json.load(json_file)
        return groups

def get_elements(filename):
    # Načte CSV soubor obsahující prvky a vrátí jej jako seznam slovníků.
    csv_data = pd.read_csv(filename)
    return csv_data.to_dict(orient='records')

def find_element_by_symbol(elements, symbol):
    # Najde prvek podle zadaného symbolu.
    return next((e for e in elements if e['Symbol'].lower() == symbol.lower()), None)

def find_element_by_name(elements, name):
    # Najde prvek podle zadaného názvu.
    return next((e for e in elements if e['Element'].lower() == name.lower()), None)

def find_element_by_atomic_number(elements, atomic_number):
    # Najde prvek podle jeho atomového čísla.
    atomic_number = int(re.sub(r'\D', '', atomic_number))
    return next((e for e in elements if e['AtomicNumber'] == atomic_number), None)

def make_table(elements, groups):
    """
    Vytvoření dvourozměrného pole podle klíčů Group a Period, které jsou čísla sloupců a řádků
    """
    table = [['' for _ in range(18)] for _ in range(9)] # 7 - lanthanoidy, 8 - aktinoidy
    for element in elements:
        # Kontrola, zda je Group validní
        if not pd.isna(element['Group']):  # Pokud Group není NaN
            group = int(element['Group'])
            # Uložení do tabulky
            table[int(element['Period']) - 1][group - 1] = element

    # odstranění zdvojených prvků Lanthanum a Actinium
    table[5][2] = ''
    table[6][2] = ''

    for i, symbol in enumerate(groups[8]['elements']):
        table[7][i+2] = find_element_by_symbol(elements, symbol)

    for i, symbol in enumerate(groups[9]['elements']):
        table[8][i+2] = find_element_by_symbol(elements, symbol)

    return table

def export_table(filename, table):
    """
    Funkce pro zformátování dvourozměrného listu v parametru table s periodickou tabulkou prvků. A uloží jej do souboru s názvem v parametru filename.
    """
    with open(filename, 'w', encoding='utf-8') as htmlfile: # otevření souboru pro zápis
        # styly pro správné zobrazování tabulky včetně různých barev pro různé typy prvků
        html = """
        <style>
            .element{
                border: 1px solid;
                width: 90px;
                height: 90px;
            }
            
            table{
                text-align: center;
                font-size: 12px;
                border-collapse: collapse;
            }
            
            /* Barvy pro jednotlivé typy prvků v tabulce */
            .nonmetal {
                background-color: #aaffaa;
            }
            
            .nobleGas {
                background-color: #aaaaff;
            }
            
            .alkaliMetal {
                background-color: #ffaaaa;
            }
            
            .alkalineEarthMetal {
                background-color: #ffd700;
            }
            
            .metalloid {
                background-color: #ffa500;
            }
            
            .halogen {
                background-color: #ffb6c1;
            }
            
            .metal {
                background-color: #c0c0c0;
            }
            
            .transitionMetal {
                background-color: #87ceeb;
            }
            
            .lanthanide {
                background-color: #d8bfd8;
            }
            
            .actinide {
                background-color: #dda0dd;
            }
            
            .transactinide {
                background-color: #ff6347;
            }
        </style>
        """
        html += '<table>' # vložení tagu table
        for i, row in enumerate(table): # cyklus, který prochází řádky tabulky, index řádku se ukládá do proměnné i
            html += '<tr>' # vložení atributu pro řádek tabulky
            for j, column in enumerate(row): # cyklus, který prochází sloupce v jednotlivých řádcích, index sloupce se ukládá do proměnné j
                if column != '': # pokud pole v dvojrozměrném listu není prázdný řetězec, vypíše informace o prvku
                    # převedení typu do formátu v jakém je zapsán v třídách v css
                    if isinstance(column['Type'], str): # kontrola jestli hodnota je string
                        s = column['Type'].replace(" ", "")  # Odstraní mezery
                        class_name = s[0].lower() + s[1:] if s else ""  # Změní první písmeno na malé, pokud řetězec není prázdný
                    html = html + f'<td class="element {class_name if class_name else ''}">' # vložení sloupce tabulky s třídami element a proměnnou třídou podle typu
                    # výpis informací o prvku v políčku tabulky
                    html = html + f"""
                        {str(column['AtomicMass'])}<br>
                        <sub>{str(column['AtomicNumber'])}</sub>
                        <span style="font-size:24px">{str(column['Symbol'])}</span><br>
                        {str(column['Electronegativity']) if str(column['Electronegativity']) != 'nan' else ''}<br>
                        {str(column['Element'])}<br>
                        """
                else:
                    if i == 1 and 2 < j < 11: # v určené části tabulky se vypisuje legenda
                        # převedení typu do formátu v jakém je zapsán v třídách v css
                        if isinstance(types[j-3], str):
                            s = types[j-3].replace(" ", "")  # Odstraní mezery
                            class_name = s[0].lower() + s[1:] if s else ""  # Změní první písmeno na malé, pokud řetězec není prázdný
                        html += f'<td class="element {class_name}">{types[j-3]}'
                    else: # zapsání prázdného sloupce v řádku, pokud se tam nenachází žádný prvek a nemá tam být ani legenda
                        html += '<td>'
                html += '</td>' # ukončení každého sloupce v řádku ukončujícím tagem td
            html += '</tr>' # ukončení každého řádku tabulky ukončujícím tagem tr
            if i == 6: # přidání mezery mezi 7 a 8 řádkem tabulky
                html += '<tr style="height: 50px"></tr>'
        html += '</table>' #  přidání ukončení tagu table
        htmlfile.write(html) # zápis získaného kodu do souboru

def whole_number_input(inputString):
    """
    Funkce pro zadání celého čísla s validací. Parametr input string je text, který se uživateli zobrazí před vstupem. Funkce vrací celé číslo.
    """
    while True: # opakuje dokud uživatel nezadá validní vstup
        cislo = input(inputString) # získá uživatelský vstup
        if re.fullmatch(r'[0-9]+', cislo): # validuje jestli obsahuje pouze čísla
            return int(cislo) # převede řetězec na číslo a to vrátí.
        else:
            print("Nezadal jsi celé číslo.")

def multiple_input(inputString):
    """
    Funkce pro zadání více čísel skupin nebo period. Do parametru inputString zadej skupin nebo period. Funkce vrací list se zadanými čísly.
    """
    user = input(f"Zadej čísla {inputString} (pro zadání více {inputString} odděluj čárkami):") # získá uživatelský vstup
    if re.fullmatch(r'[0-9, ]+', inputString): # validuje jestli obsahuje pouze čísla, čárky a mezery
        return [int(x.strip()) for x in user.split(',')] # z uživatelského vstupu odstraní mezery, rozdělí podle čárek a získané hodnoty vrátí pole s jednotlivými čísly
    else:
        print("Můžeš zadat pouze čísla, čárky a mezery.")


def find_all_in_groups(elements, groups):
    if isinstance(groups, int): # Pokud je `groups` celé číslo, převede se na seznam
        groups = [groups]
    return [e for e in elements if e.get('Group') in groups] # uloží do listu všechny prvky z listu elements, které mají v klíčí 'Group' zadané čísla skupiny

def find_all_in_periods(elements, periods):
    if isinstance(periods, int): # Pokud je `periods` jedno číslo, převede se na seznam
        periods = [periods]
    return [e for e in elements if e.get('Period') in periods] # uloží do listu všechny prvky z listu elements, které mají v klíčí 'Period' zadané čísla periody

def calculate_atomic_mass_avg(elements):
    return sum(e['AtomicMass'] for e in elements) / len(elements)

def group_or_period_input():
    """
    Uživatelské menu pro zjištění jestli chce uživatel vybírat číslo skupiny nebo periody a následný vstup čísla skupiny/periody s validací.
    FUnkce vrací číslo periody/skupiny a volbu (jestli si uživatel vybral periodu nebo skupinu)

    Příklad použití:
    cislo, volba = group_or_period_input()
    """
    print('1 - Ve skupině')
    print('2 - V periodě')

    predvolba = -1
    while predvolba == -1:
        predvolba = input('Vyber (1/2):')
        if '0' < predvolba < '3': # validace jestli uživatel zadal '1' nebo '2'
            while 1:
                cislo = input(f'Zadej číslo {'skupiny' if predvolba == '1' else 'periody'}:') # získá od uživatele vstupní řetězec
                if re.fullmatch(r'[0-9]+', cislo): # validace jestli vstupní řetězec obsahuje pouze čísla
                    cislo = int(cislo) # převedení řetězce na číslo
                    if predvolba == '1':
                        if 0 < cislo < 19: # validace čísla skupiny
                            return cislo, predvolba
                        else:
                            print(f'Skupina s číslem {cislo} neexistuje.')
                    elif predvolba == '2':
                        if 0 < cislo < 9: # validace čísla periody
                            return cislo, predvolba
                        else:
                            print(f'Skupina s číslem {cislo} neexistuje.')
                    else:
                        print('Neznámá předvolba.')
                else:
                    print('Nezadal jsi číslo.')
        else:
            print('Neznámá předvolba. Zkus to znova.')
            predvolba = -1

def filename_input(extension):
    """
    Funkce získá od uživatele string s názvem souboru a validuje jestli obsahuje správnou příponu zadanou v parametru extension. Pokud chybí, přidá ji. Extension může být zadaná s tečkou i bez tečky.
    """
    if extension[0] != '.': # zjistí jestli extension obsahuje tečku
        extension = '.' + extension # pokud ne, přidá tečku
    filename = ''
    while True: # funkce se opakuje dokud uživatel nezadá správný vstup
        filename = input(f'Zadej název souboru s příponou {extension}:') # získá název souboru od uživatele
        if re.fullmatch(r'[a-zA-Z0-9.]+', filename): # zkontroluje jestli obsahuje pouze velká a malá písmena, čísla a tečku
            dot_index = filename.rfind(".")
            if dot_index != -1 and filename[dot_index:] == extension: # zkontroluje jestli uživatelem zadaný řetězec končí správnou připonou
                return filename
            else: # pokud nekončí správnou připonou, funkce informuje uživatele a doplní ji
                print('Nenalezena požadovaná přípona , doplňuji ...')
                filename = filename + extension
                return filename
        else:
            print('Název souboru musí obsahovat pouze čísla a písmena bez českých znaků a případně ')

def export_to_md(filename, elements, header):
    """
    Funkce, která zapíše list prvků v parametru elements do markdown souboru s názvem filename. Na začátek souboru se vypíše string z parametru header.
    """
    with open(filename, 'w', encoding='utf-8') as md_file: # otevře soubor s názvem filename v módu pro čtení a určí správné kódování
        text = f'# {header}\n' # zapíše do souboru hlavní nadpis (parametr header)
        for element in elements: # u každého elementu vypíše některé údaje
            text += f'## {element["AtomicNumber"]} - {element["Element"]} ({element["Symbol"]})\n'
            text += f'Počet protonů: {element["NumberofProtons"]}\n'
            text += f'Počet neutronů: {element["NumberofNeutrons"]}\n'
            text += f'Počet elektronů: {element["NumberofElectrons"]}\n'
            text += f'Skupenství: {phase_cz[element["Phase"]]}\n'
        md_file.write(text) # výsledný řetězec zapíše do souboru

def export_to_xml(filename, elements, description):
    """
    Funkce, která zapíše list prvků v parametru elements do markdown souboru s názvem filename. Na začátek souboru se vypíše string z parametru header.
    """
    # Vytvoření hlavního elementu
    root = ET.Element("Elements")

    # Přidání popisu na stejnou úroveň jako Element, pokud je zadán
    if description:
        desc_element = ET.SubElement(root, "Description")
        desc_element.text = description

    # Přidání jednotlivých záznamů do XML
    for e in elements:
        e_element = ET.SubElement(root, "Element")
        for key, value in e.items():
            child = ET.SubElement(e_element, key)
            child.text = str(value)

    # Převedení stromu na neformátovaný řetězec
    xml_str = ET.tostring(root, encoding="unicode")

    # Hezké formátování XML s odsazením
    pretty_xml_str = parseString(xml_str).toprettyxml(indent="    ")

    # zapíše výsledný XML řetězec do souboru
    with open(filename, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)


