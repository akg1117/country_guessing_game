from flask import Blueprint, render_template, request, jsonify, session
import uuid, secrets
from .game_ai import AIService

bp = Blueprint("main", __name__)
ai_service = AIService()
MAX_QUESTION_COUNT = 5


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/game")
def game():
    return render_template("game.html")


@bp.route("/result")
def result():
    return render_template("result.html")


@bp.route("/start", methods=["POST"])
def start_game():
    data = request.get_json()
    mode = data.get("mode", "normal")

    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    session["game"] = {
        "mode": mode,
        "answer": ai_service.choose_country(mode),
        "question_count": 0,
    }
    return jsonify({"success": True})


@bp.route("/hint", methods=["POST"])
def provide_hint():
    game = session.get("game")
    if not game:
        return jsonify({"error": "ゲームが開始されていません"}), 400

    hints = ai_service.get_hints(game["answer"])
    game["hints"] = hints
    session["game"] = game
    result = {"hints": hints, "max_question_count": MAX_QUESTION_COUNT}
    return jsonify(result)


@bp.route("/request_result", methods=["POST"])
def request_result():
    data = request.get_json()
    guess = data.get("guess", "")
    game = session.get("game")
    if not game:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    game["guess"] = guess
    session["game"] = game
    return jsonify({"success": True})


@bp.route("/response_result", methods=["POST"])
def response_result():
    game = session.get("game")
    if not game:
        return jsonify({"error": "ゲームが開始されていません"}), 400
    result = ai_service.evaluate_guess(game)
    result["guess"] = game.get("guess", "")
    result["answer"] = game.get("answer", "")
    answer = game.get("answer", "")
    hints = game.get("hints", [])
    country_summary = ai_service.get_country_summary(answer)
    hint_explanations = [ai_service.get_hint_explanation(answer, h) for h in hints]
    result["country_summary"] = country_summary
    result["hints"] = hints
    result["hint_explanations"] = hint_explanations
    return jsonify(result)


@bp.route("/question", methods=["POST"])
def respond_to_question():
    data = request.get_json()
    question_text = data.get("question", "")
    game = session.get("game")
    if not game:
        return jsonify({"error": "ゲームが開始されていません"}), 400

    if game["question_count"] >= MAX_QUESTION_COUNT:
        return jsonify({"response": "わかりません"})

    game["question_count"] += 1
    session["game"] = game
    return jsonify(ai_service.respond_to_question(game["answer"], question_text))
