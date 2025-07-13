document.addEventListener("DOMContentLoaded", () => {
    const hintResult = document.getElementById("hint-result");
    const questionButton = document.getElementById("question-button");
    const guessButton = document.getElementById("guess-button");
    const lastQuestion = document.getElementById("last-question");
    const questionCount = document.getElementById("question-count");
    let MAX_QUESTION_COUNT = 5;
    let remaining = MAX_QUESTION_COUNT;

    const questionInput = document.getElementById("question");
    const initialQuestionValue = questionInput ? questionInput.value : "";

    if (hintResult) {
        (async () => {
            try {
                const res = await fetch("/hint", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({})
                });
                const data = await res.json();
                hintResult.innerHTML = data.hints.map(h => `${h}`).join("<br>");
                if (data.max_question_count) {
                    MAX_QUESTION_COUNT = data.max_question_count;
                    remaining = MAX_QUESTION_COUNT;
                    updateQuestionCount();
                }
            } catch (error) {
                console.error("ヒント取得エラー:", error);
                hintResult.textContent = "ヒントの取得に失敗しました。";
            }
        })();
    }

    function updateQuestionCount() {
        if (questionCount) {
            questionCount.textContent = `残り質問回数: ${remaining}`;
        }
    }
    updateQuestionCount();

    if (questionButton) {
        questionButton.addEventListener("click", async () => {
            if (remaining <= 0) {
                if (lastQuestion) {
                    lastQuestion.innerHTML = `<div>質問回数の上限に達しました。</div>`;
                }
                return;
            }
            try {
                const question = questionInput.value;
                const res = await fetch("/question", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question })
                });
                const data = await res.json();
                if (lastQuestion) {
                    lastQuestion.innerHTML = `<div>質問: ${question}<br>回答: ${data.response}</div>`;
                }
                remaining--;
                updateQuestionCount();
                questionInput.value = initialQuestionValue;
            } catch (error) {
                console.error("質問エラー:", error);
                if (lastQuestion) {
                    lastQuestion.innerHTML = `<div>質問の送信に失敗しました。</div>`;
                }
            }
        });
    }

    if (guessButton) {
        guessButton.addEventListener("click", async () => {
            try {
                const guess = document.getElementById("guess").value;
                await fetch("/request_result", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ guess })
                });
                window.location.href = "/result";
            } catch (error) {
                console.error("結果リクエストエラー:", error);
                alert("結果のリクエストに失敗しました。");
            }
        });
    }
});
