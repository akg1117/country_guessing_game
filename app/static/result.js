document.addEventListener("DOMContentLoaded", () => {
    const resultMessage = document.getElementById("result-message");
    const countrySummary = document.getElementById("country-summary");
    const hintExplanation = document.getElementById("hint-explanation");
    if (resultMessage) {
        (async () => {
            try {
                const res = await fetch("/response_result", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({})
                });
                const data = await res.json();
                resultMessage.innerHTML =
                    `<strong>あなたの予想:</strong> ${data.guess}<br>` +
                    `<strong>正解の国:</strong> ${data.answer}<br>` +
                    `<strong>スコア:</strong> ${data.score} 点<br>` +
                    `<strong>コメント:</strong> ${data.comment}`;
                if (countrySummary) {
                    countrySummary.textContent = data.country_summary || "情報取得中...";
                }
                if (hintExplanation && Array.isArray(data.hints) && Array.isArray(data.hint_explanations)) {
                    let html = "";
                    for (let i = 0; i < data.hints.length; i++) {
                        html += `<div class="hint-card"><strong>ヒント${i+1}:</strong> ${data.hints[i]}<br><span class="hint-desc">${data.hint_explanations[i] || ""}</span></div>`;
                    }
                    hintExplanation.innerHTML = html;
                }
            } catch (error) {
                console.error("結果取得エラー:", error);
                resultMessage.textContent = "結果の取得に失敗しました。";
                if (countrySummary) countrySummary.textContent = "取得失敗";
                if (hintExplanation) hintExplanation.textContent = "取得失敗";
            }
        })();
    }
});
