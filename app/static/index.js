document.addEventListener("DOMContentLoaded", () => {
    const startButton = document.getElementById("start-button");

    if (startButton) {
        startButton.addEventListener("click", async () => {
            try {
                const mode = document.querySelector('input[name="mode"]:checked')?.value;
                
                await fetch("/start", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ mode })
                });
                window.location.href = "/game";
            } catch (error) {
                console.error("ゲーム開始エラー:", error);
                alert("ゲームの開始に失敗しました。");
            }
        });
    }
});
