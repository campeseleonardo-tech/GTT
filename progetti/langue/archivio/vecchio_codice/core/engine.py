# engine.py
import random
from typing import List, Dict, Optional
from dataclasses import dataclass, field

ARTICLES = ["il","lo","la","l'","i","gli","le"]

@dataclass
class Question:
    item: Dict
    options: List[str]
    index: int

@dataclass
class SessionResult:
    total_points: int
    correct_count: int
    rounds_target: int
    accuracy: float
    best_streak: int
    history: List[Dict] = field(default_factory=list)

class ArticlesEngine:
    def __init__(self, dataset: List[Dict], rounds_per_session: int = 10, options_per_question: int = 4):
        if not dataset:
            raise ValueError("Empty dataset")
        self.dataset = list(dataset)
        self.rounds_per_session = rounds_per_session
        self.options_per_question = options_per_question
        self.session = None

    def _sample_options(self, correct: str) -> List[str]:
        opts = {correct}
        pool = [a for a in ARTICLES if a != correct]
        random.shuffle(pool)
        for a in pool:
            if len(opts) >= self.options_per_question:
                break
            opts.add(a)
        opts_list = list(opts)
        random.shuffle(opts_list)
        return opts_list

    def new_session(self):
        pool = list(self.dataset)
        random.shuffle(pool)
        self.session = {
            "queue": pool[:],  # items to present/requeue
            "presented": 0,
            "correct": 0,
            "current_streak": 0,
            "best_streak": 0,
            "total_points": 0,
            "history": []
        }

    def next_question(self) -> Optional[Question]:
        if not self.session:
            return None
        if self.session["presented"] >= self.rounds_per_session:
            return None
        if not self.session["queue"]:
            self.session["queue"] = list(self.dataset)
            random.shuffle(self.session["queue"])
        item = self.session["queue"].pop(0)
        options = self._sample_options(item["correct_article"])
        self.session["presented"] += 1
        return Question(item=item, options=options, index=self.session["presented"])

    def submit_answer(self, question: Question, selected: str) -> Dict:
        if not self.session:
            raise RuntimeError("No active session")
        correct = selected == question.item["correct_article"]
        points = 0
        if correct:
            points += 10
            self.session["current_streak"] += 1
            if self.session["current_streak"] > self.session["best_streak"]:
                self.session["best_streak"] = self.session["current_streak"]
            # streak bonus
            if self.session["current_streak"] % 3 == 0:
                points += 5
            self.session["correct"] += 1
        else:
            self.session["current_streak"] = 0
            # simple requeue
            self.session["queue"].append(question.item)
        self.session["total_points"] += points
        record = {
            "index": question.index,
            "word": question.item["word"],
            "selected": selected,
            "correct": question.item["correct_article"],
            "points": points,
            "correct_flag": correct
        }
        self.session["history"].append(record)
        return record

    def end_session(self) -> SessionResult:
        if not self.session:
            raise RuntimeError("No active session")
        presented = self.session["presented"]
        correct = self.session["correct"]
        accuracy = (correct / presented * 100) if presented else 0.0
        result = SessionResult(
            total_points=self.session["total_points"],
            correct_count=correct,
            rounds_target=self.rounds_per_session,
            accuracy=accuracy,
            best_streak=self.session["best_streak"],
            history=self.session["history"][:]
        )
        self.session = None
        return result