# app_ui.py
import sys
from typing import Any
from loader import load_dataset  # from repo-articles-loader (you can vendor/copy or pip package)
from engine import ArticlesEngine  # from repo-articles-engine

def print_header():
    print("="*36)
    print(" Articles — Quick Game (English UI)")
    print("="*36)

def start_game(rounds: int = 10):
    dataset, ver = load_dataset()
    engine = ArticlesEngine(dataset, rounds_per_session=rounds)
    engine.new_session()
    print(f"Dataset version: {ver} · Items: {len(dataset)}")
    while True:
        q = engine.next_question()
        if q is None:
            break
        print(f"\nRound {q.index}/{rounds} — Word: {q.item['word']}")
        for i, opt in enumerate(q.options, start=1):
            print(f"  {i}. {opt}")
        sel = input("Choose option number (or 'q' to quit): ").strip()
        if sel.lower() == 'q':
            print("Session aborted.")
            return
        try:
            idx = int(sel) - 1
            chosen = q.options[idx]
        except Exception:
            print("Invalid selection — counted as wrong.")
            chosen = ""
        rec = engine.submit_answer(q, chosen)
        if rec["correct_flag"]:
            print("✓ Correct!")
        else:
            print(f"✕ Wrong — correct: {rec['correct']}")
    result = engine.end_session()
    print("\n--- Session complete ---")
    print(f"Score: {result.total_points} · Accuracy: {result.accuracy:.0f}% · Best streak: {result.best_streak}")
    print("------------------------")