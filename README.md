# Periodická tabulka prvků

Tento projekt implementuje jednoduchý interaktivní program pro práci s periodickou tabulkou prvků. Uživatel má možnost hledat prvky, exportovat data do různých formátů (XML, HTML, Markdown), počítat průměrné atomové hmotnosti pro zadané skupiny nebo periody a generovat HTML tabulku všech prvků.

## Funkce programu

1. **Vyhledávání prvku** - Možnost vyhledat prvek podle názvu, symbolu nebo protonového čísla.

2. **Export prvků do XML** - Exportuje prvky ve vybrané skupině nebo periodě do XML souboru.

3. **Výpočet průměrné atomové hmotnosti** - Spočítá průměrnou atomovou hmotnost pro vybranou skupinu nebo periodu.

4. **Generování HTML periodické tabulky** - Vygeneruje HTML tabulku periodické tabulky a uloží ji do souboru.

5. **Export do Markdown souboru** - Exportuje přehled prvků ve vybrané skupině nebo periodě do formátu Markdown.

## Použití
1. **Naklonování repozitáře**
    ```bash
   git clone https://github.com/JedlaTypek/chemical_elements
   cd chemical_elements
   ```
2. **Instalace požadavků**
   Pro běh programu je potřeba mít nainstalované knihovny ze souboru requirements.txt. Instalaci provedete následujícím příkazem:

    ```bash
    pip install -r requirements.txt
    ```
3. **Spuštění programu** - Program spustíte jedním z následujících příkazů:
    ```bash
   python main.py
   # nebo
   python3 main.py
   ```
4. **Předpokládaný výstup:**
    ```
    MENU:
    0 - Ukončení programu
    1 - Vyhledávání prvku
    2 - Export prvků ve vybrané skupině nebo periodě do XML
    3 - Průměrná relativní atomová hmotnost prvků ve vybrané skupině nebo periodě
    4 - Vygenerovat HTML periodickou tabulku prvků
    5 - Přehled prvků v konkrétní skupině nebo periodě do markdown souboru
    Zadej číslo předvolby:
    ```
5. **Průchod programem je intuitivní a nepotřebuje další popis**