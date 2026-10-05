import flet as ft
from core.loader import DataLoader
from core.engine import GameEngine

def create_app_ui(page: ft.Page):
    page.title = "Language Learning App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    
    # Inizializza i moduli core (nuova architettura)
    loader = DataLoader("words_db.json")
    engine = GameEngine(loader)

    # Componente UI principale che conterrà le varie schermate
    main_column = ft.Column(spacing=20, alignment=ft.MainAxisAlignment.CENTER)

    def show_menu(e=None):
        main_column.controls.clear()
        title = ft.Text("Seleziona un Minigioco", size=24, weight=ft.FontWeight.BOLD)
        
        # Bottoni che richiamano i moduli del nostro nuovo JSON
        btn_vocab = ft.ElevatedButton("Vocabolario (IT-EN)", on_click=lambda _: start_minigame("vocabulary", "it-en"))
        btn_articles = ft.ElevatedButton("Gioco Articoli (DE)", on_click=lambda _: start_minigame("articles", "de"))
        
        main_column.controls.extend([title, btn_vocab, btn_articles])
        page.update()

    def start_minigame(game_type, lang):
        success = engine.start_game(game_type, lang)
        main_column.controls.clear()
        
        if not success:
            main_column.controls.append(ft.Text(f"Errore: Nessun dato trovato per {game_type} ({lang}). Controlla il file words_db.json.", color=ft.Colors.RED))
            main_column.controls.append(ft.ElevatedButton("Torna al Menu", on_click=show_menu))
            page.update()
            return
            
        show_question()

    def show_question():
        main_column.controls.clear()
        item = engine.get_current_item()
        
        if not item:
            # Fine del gioco, mostra il punteggio
            main_column.controls.append(ft.Text(f"Gioco Terminato! Punteggio: {engine.score}", size=24, weight=ft.FontWeight.BOLD))
            main_column.controls.append(ft.ElevatedButton("Torna al Menu", on_click=show_menu))
        else:
            # Mostra la parola o la frase da tradurre/indovinare
            word_text = ft.Text(f"Parola: {item.get('word')}", size=20)
            answer_input = ft.TextField(label="La tua risposta", width=300, autofocus=True)
            
            # Logica dinamica: se è il gioco degli articoli usa 'correct_article', altrimenti 'translation'
            correct_answer = item.get('correct_article') if 'correct_article' in item else item.get('translation')
            
            def on_submit(e):
                engine.check_answer(answer_input.value, correct_answer)
                show_question()
                
            btn_submit = ft.ElevatedButton("Conferma", on_click=on_submit)
            main_column.controls.extend([word_text, answer_input, btn_submit])
            
        page.update()

    # Avvia l'app mostrando il menu iniziale
    show_menu()
    page.add(main_column)