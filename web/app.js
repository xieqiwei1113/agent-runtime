const runButton = document.querySelector("#run");
const tool = document.querySelector("#tool");
const text = document.querySelector("#text");
const output = document.querySelector("#output");
const status = document.querySelector("#status");

runButton.addEventListener("click", async () => {
  runButton.disabled = true;
  status.textContent = "Running...";
  try {
    const response = await fetch("/api/run", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({tool: tool.value, text: text.value}),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "request failed");
    status.textContent = data.status === "completed" ? "Completed" : data.status;
    output.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    status.textContent = "Failed";
    output.textContent = error.message;
  } finally {
    runButton.disabled = false;
  }
});
