import openai
import json
import os
import random


class AIService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
        base_dir = os.path.dirname(__file__)
        self.prompts = self._load_json(os.path.join(base_dir, "data", "prompts.json"))
        self.countries = self._load_json(os.path.join(base_dir, "data", "countries.json"))

    def _load_json(self, path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def _format_prompt(self, key, **kwargs):
        prompt = self.prompts[key]
        return [
            {"role": "system", "content": prompt["system"].format(**kwargs)},
            {"role": "user", "content": prompt["user"].format(**kwargs)},
        ]

    def _ask(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return response.choices[0].message.content.strip()

    def choose_country(self,mode):
        if mode == "easy":
            selected_range = self.countries[0:10]
        elif mode == "normal":
            selected_range = self.countries[10:40]
        else:
            selected_range = self.countries[20:60]
        return random.choice(selected_range)

    def get_hints(self, country, k=3):
        reply = self._ask(self._format_prompt("get_hints", country=country))
        hints = [h.strip() for h in reply.split(",") if h.strip()]
        return hints[:k]

    def evaluate_guess(self, game):
        answer = game.get("answer", "")
        guess = game.get("guess", "")
        mode = game.get("mode", "normal")
        question_count = game.get("question_count", 0)

        reply = self._ask(self._format_prompt("evaluate_guess", guess=guess, answer=answer))
        try:
            score_str, comment = reply.split(",", 1)
            score = int(score_str.strip())
            comment = comment.strip()
        except Exception:
            score = 0
            comment = "評価できませんでした"
        return {"score": score, "comment": comment}

    def respond_to_question(self, answer, question_text):
        reply = self._ask(self._format_prompt("respond_to_question", answer=answer, question_text=question_text))
        return {"response": reply}

    def get_country_summary(self, country):
        reply = self._ask(self._format_prompt("country_summary", country=country))
        return reply

    def get_hint_explanation(self, country, hint):
        reply = self._ask(self._format_prompt("hint_explanation", country=country, hint=hint))
        return reply
