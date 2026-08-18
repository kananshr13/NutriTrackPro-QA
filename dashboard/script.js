const DATA_URL = "./data/test-results.json";

async function loadDashboard() {
    const response = await fetch(DATA_URL);

    if (!response.ok) {
        throw new Error(`Unable to load test results: ${response.status}`);
    }

    const data = await response.json();

    renderSummary(data.summary);
    renderSuites(data.suites);
    renderTests(data.tests);
    renderExecution(data);
    renderGeneratedTime(data.generated_at);
}


function renderSummary(summary) {
    document.querySelector("#total-tests").textContent = summary.total;
    document.querySelector("#passed-tests").textContent = summary.passed;
    document.querySelector("#failed-tests").textContent = summary.failed;
    document.querySelector("#pass-rate").textContent =
        `${summary.pass_rate}%`;
    document.querySelector("#duration").textContent =
        `${summary.duration}s`;
}


function renderSuites(suites) {
    const container = document.querySelector("#suite-container");

    container.innerHTML = "";

    Object.entries(suites).forEach(([name, suite]) => {

        const percentage =
            suite.total > 0
                ? (suite.passed / suite.total) * 100
                : 0;

        const row = document.createElement("div");

        row.className = "suite";

        row.innerHTML = `
            <div class="suite-name">
                ${escapeHtml(name)}
            </div>

            <div class="progress">
                <div
                    class="progress-bar"
                    style="width: ${percentage}%"
                ></div>
            </div>

            <div class="suite-count">
                ${suite.passed}/${suite.total}
            </div>
        `;

        container.appendChild(row);
    });
}


function renderTests(tests) {
    const container = document.querySelector("#test-results");

    container.innerHTML = "";

    tests.forEach(test => {

        const row = document.createElement("tr");

        const statusClass =
            test.status === "passed"
                ? "badge-pass"
                : test.status === "failed"
                    ? "badge-fail"
                    : "badge-skip";

        row.innerHTML = `
            <td>${escapeHtml(test.name)}</td>

            <td>${escapeHtml(test.suite)}</td>

            <td>
                <span class="badge ${statusClass}">
                    ${escapeHtml(test.status.toUpperCase())}
                </span>
            </td>

            <td>
                ${test.duration}s
            </td>

            <td>
                ${test.details
                    ? escapeHtml(test.details)
                    : "—"
                }
            </td>
        `;

        container.appendChild(row);
    });
}


function renderExecution(data) {

    const summary = data.summary;

    document.querySelector("#execution-framework").textContent =
        "Pytest";

    document.querySelector("#execution-type").textContent =
        "API Automation";

    document.querySelector("#execution-environment").textContent =
        "Production";

    document.querySelector("#execution-count").textContent =
        `${summary.total} tests`;
}


function renderGeneratedTime(timestamp) {

    const element =
        document.querySelector("#generated-time");

    const date = new Date(timestamp);

    element.textContent =
        date.toLocaleString("en-IN", {
            dateStyle: "medium",
            timeStyle: "short"
        });
}


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


loadDashboard().catch(error => {

    console.error("Dashboard loading failed:", error);

    document.querySelector("#dashboard-error").textContent =
        "Unable to load the latest test results.";
});