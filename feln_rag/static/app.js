const $ = (id) => document.getElementById(id);
let defaultPrompt = "";
let examples = [];
let retrievedQuery = "";
let busy = false;
let output = "";

function status(text, kind = "") {
  $("status").textContent = text;
  $("status").className = `status ${kind}`;
}

async function request(path, data) {
  const response = await fetch(path, data === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data),
  });
  const result = await response.json();
  if (!response.ok) throw new Error(result.error || "The request failed. Please try again.");
  return result;
}

function setBusy(value) {
  busy = value;
  for (const id of ["generate", "retrieve", "query", "prompt", "reset-prompt"]) $(id).disabled = value;
  $("query-form").setAttribute("aria-busy", String(value));
}

function clearResult() {
  output = "";
  $("result-content").hidden = true;
  $("result-empty").hidden = false;
  $("result-badge").textContent = "OUTPUT";
  $("result-badge").className = "small-tag";
  $("result-footer-text").textContent = "Retrieve examples, then generate FELN.";
}

function renderExamples() {
  $("examples").replaceChildren();
  $("examples-empty").hidden = examples.length > 0;
  $("example-count").textContent = `${examples.length} / 5 RETRIEVED`;
  for (const [rank, example] of examples.entries()) {
    const card = $("example-template").content.cloneNode(true);
    card.querySelector(".example-rank").textContent = String(rank + 1).padStart(2, "0");
    card.querySelector(".similarity").textContent = `${example.score.toFixed(3)} similarity`;
    card.querySelector(".example-text").textContent = example.text;
    card.querySelector("pre").textContent = JSON.stringify(example.meta, null, 2);
    for (const layer of example.meta.layers || []) {
      const chip = document.createElement("span");
      chip.className = "layer-chip";
      chip.textContent = layer;
      card.querySelector(".example-layers").append(chip);
    }
    $("examples").append(card);
  }
}

async function retrieve(query) {
  if (retrievedQuery === query && examples.length === 5) return;
  status("Finding the five closest examples… The first query may take a moment to load the encoder.", "busy");
  const result = await request("/api/retrieve", { query });
  examples = result.examples;
  retrievedQuery = query;
  renderExamples();
  $("examples-description").textContent = "Ranked by cosine similarity. These exact five examples will be sent in this order.";
}

async function run(generate) {
  if (busy || !$("query").reportValidity()) return;
  if (generate && !$("prompt").value.trim()) {
    $("prompt").closest("details").open = true;
    $("prompt").focus();
    status("Enter a system prompt before generating.", "error");
    return;
  }
  const query = $("query").value.trim();
  if (!query) return status("Enter a question to get started.", "error");
  setBusy(true);
  clearResult();
  const started = performance.now();
  try {
    await retrieve(query);
    if (!generate) {
      status("Five examples ready. Expand any card to inspect its FELN, or generate your answer.");
      return;
    }
    status("Five examples found. Generating your FELN…", "busy");
    $("result-badge").textContent = "GENERATING";
    const result = await request("/api/generate", {
      query, prompt: $("prompt").value, ids: examples.map((example) => example.id),
    });
    output = result.valid ? JSON.stringify(result.feln, null, 2) : result.raw;
    $("result-code").textContent = output;
    $("result-empty").hidden = true;
    $("result-content").hidden = false;
    $("result-badge").textContent = result.valid ? "VALID FELN" : "INVALID OUTPUT";
    $("result-badge").className = `small-tag ${result.valid ? "valid" : "invalid"}`;
    $("result-description").textContent = result.valid ? "FELN / JSON" : "RAW MODEL OUTPUT";
    $("copy").textContent = result.valid ? "Copy JSON" : "Copy output";
    $("result-summary").textContent = result.valid
      ? `${result.feln.layers.join(" → ")} · ${result.feln.relations.join(" · ") || "No spatial join"}`
      : "The model returned an invalid FELN. Review the raw output above, then adjust your prompt and try again.";
    $("result-footer-text").textContent = `5 examples used · ${((performance.now() - started) / 1000).toFixed(1)} seconds`;
    $("examples-description").textContent = "These exact five examples were passed to the model, in the order shown.";
    status(result.valid ? "Your FELN is ready. Validated against the FELN schema." : "Generation finished, but the output did not pass FELN validation.", result.valid ? "" : "error");
  } catch (error) {
    $("result-badge").textContent = "TRY AGAIN";
    status(error.message || "Could not connect to the server. Please try again.", "error");
  } finally {
    setBusy(false);
  }
}

$("query-form").addEventListener("submit", (event) => { event.preventDefault(); run(true); });
$("retrieve").addEventListener("click", () => run(false));
$("query").addEventListener("input", () => {
  $("character-count").textContent = `${$("query").value.length} characters`;
  examples = [];
  retrievedQuery = "";
  renderExamples();
  clearResult();
  $("examples-description").textContent = "The closest matches from your corpus, in the exact order sent to the model.";
  status("Query changed. Find fresh examples or generate a new FELN.");
});
$("prompt").addEventListener("input", () => {
  clearResult();
  $("examples-description").textContent = "Ranked by cosine similarity. These examples will be sent with your updated prompt.";
  status("Prompt updated. Generate a new FELN to use it.");
});
$("reset-prompt").addEventListener("click", () => {
  $("prompt").value = defaultPrompt;
  $("prompt").dispatchEvent(new Event("input"));
});
$("copy").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(output);
    $("copy").textContent = "Copied!";
  } catch {
    status("Clipboard unavailable. Select and copy the output directly.", "error");
  }
});

async function init() {
  setBusy(true);
  $("character-count").textContent = `${$("query").value.length} characters`;
  try {
    const config = await request("/api/config");
    defaultPrompt = config.prompt;
    $("prompt").value = defaultPrompt;
    $("model").textContent = config.model;
    $("corpus-info").textContent = `${config.count.toLocaleString()} examples · ${config.encoder.replace("local:", "")}`;
    setBusy(false);
    status("Workspace ready. Start with the query above, or write your own.");
  } catch {
    $("model").textContent = "Disconnected";
    status("Could not connect to the local server. Start python -m feln_rag.web and reload this page.", "error");
  }
}
init();
