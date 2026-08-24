// ==========================================================================
// Social Media Content Analyzer
// Frontend JavaScript
// ==========================================================================


// --------------------------------------------------------------------------
// DOM ELEMENTS
// --------------------------------------------------------------------------

const fileInput = document.getElementById("file-input");
const dropZone = document.getElementById("drop-zone");

const fileInfo = document.getElementById("file-info");
const fileName = document.getElementById("file-name");
const fileSize = document.getElementById("file-size");

const removeFileBtn = document.getElementById("remove-file");
const analyzeBtn = document.getElementById("analyze-btn");

const loadingSection = document.getElementById("loading-section");
const loadingText = document.getElementById("loading-text");

const errorSection = document.getElementById("error-section");
const errorMessage = document.getElementById("error-message");
const tryAgainBtn = document.getElementById("try-again-btn");

const resultsSection = document.getElementById("results-section");
const newAnalysisBtn = document.getElementById("new-analysis-btn");


// --------------------------------------------------------------------------
// CURRENT FILE
// --------------------------------------------------------------------------

let selectedFile = null;


// --------------------------------------------------------------------------
// FILE INPUT
// --------------------------------------------------------------------------

fileInput.addEventListener("change", function () {

    if (this.files.length > 0) {
        handleFile(this.files[0]);
    }

});


// --------------------------------------------------------------------------
// DRAG AND DROP
// --------------------------------------------------------------------------

dropZone.addEventListener("dragover", function (event) {

    event.preventDefault();

    dropZone.classList.add("dragover");

});


dropZone.addEventListener("dragleave", function () {

    dropZone.classList.remove("dragover");

});


dropZone.addEventListener("drop", function (event) {

    event.preventDefault();

    dropZone.classList.remove("dragover");

    const files = event.dataTransfer.files;

    if (files.length > 0) {
        handleFile(files[0]);
    }

});


// --------------------------------------------------------------------------
// HANDLE FILE
// --------------------------------------------------------------------------

function handleFile(file) {

    const allowedExtensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    ];

    const extension =
        "." + file.name.split(".").pop().toLowerCase();


    // Validate file type
    if (!allowedExtensions.includes(extension)) {

        showError(
            "Unsupported file type. Please upload a PDF, JPG, JPEG, or PNG file."
        );

        return;
    }


    // Validate file size - 10 MB
    if (file.size > 10 * 1024 * 1024) {

        showError(
            "File is too large. Maximum allowed size is 10 MB."
        );

        return;
    }


    selectedFile = file;

    fileName.textContent = file.name;

    fileSize.textContent =
        formatFileSize(file.size);


    fileInfo.classList.remove("hidden");

    analyzeBtn.disabled = false;

    hideError();
}


// --------------------------------------------------------------------------
// FORMAT FILE SIZE
// --------------------------------------------------------------------------

function formatFileSize(bytes) {

    if (bytes < 1024) {
        return `${bytes} Bytes`;
    }

    if (bytes < 1024 * 1024) {
        return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}


// --------------------------------------------------------------------------
// REMOVE FILE
// --------------------------------------------------------------------------

removeFileBtn.addEventListener("click", function () {

    resetFile();

});


function resetFile() {

    selectedFile = null;

    fileInput.value = "";

    fileInfo.classList.add("hidden");

    analyzeBtn.disabled = true;

}


// --------------------------------------------------------------------------
// ANALYZE BUTTON
// --------------------------------------------------------------------------

analyzeBtn.addEventListener("click", async function () {

    if (!selectedFile) {

        showError(
            "Please select a file first."
        );

        return;
    }

    await analyzeFile();

});


// --------------------------------------------------------------------------
// ANALYZE FILE
// --------------------------------------------------------------------------

async function analyzeFile() {

    hideError();

    resultsSection.classList.add("hidden");

    loadingSection.classList.remove("hidden");

    analyzeBtn.disabled = true;


    const formData = new FormData();

    formData.append("file", selectedFile);


    try {

        // Step 1
        loadingText.textContent =
            "Uploading file...";

        await delay(300);


        // Step 2
        loadingText.textContent =
            "Extracting text...";


        // IMPORTANT:
        // Flask endpoint is /api/analyze
        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",
                body: formData
            }
        );


        // Convert response to JSON
        const data = await response.json();


        // Check backend response
        if (!response.ok || !data.success) {

            throw new Error(
                data.error ||
                "Unable to analyze the file."
            );

        }


        // Step 3
        loadingText.textContent =
            "Analyzing content...";

        await delay(300);


        // Step 4
        loadingText.textContent =
            "Generating suggestions...";

        await delay(300);


        // Display results
        displayResults(data);


    } catch (error) {

        console.error(
            "Analysis error:",
            error
        );

        showError(
            error.message ||
            "Something went wrong. Please try again."
        );

    } finally {

        loadingSection.classList.add("hidden");

        analyzeBtn.disabled = false;

    }

}


// --------------------------------------------------------------------------
// DISPLAY RESULTS
// --------------------------------------------------------------------------

function displayResults(data) {

    // Flask returns:
    // data.analysis
    // data.analysis.metrics
    // data.analysis.engagement
    // data.suggestions
    // data.text

    const analysis =
        data.analysis || {};

    const metrics =
        analysis.metrics || {};

    const engagement =
        analysis.engagement || {};


    // ----------------------------------------------------------------------
    // OVERALL SCORE
    // ----------------------------------------------------------------------

    const overallScore =
        analysis.overall_score || 0;


    document.getElementById(
        "overall-score"
    ).textContent = overallScore;


    document.getElementById(
        "score-label"
    ).textContent =
        getScoreLabel(overallScore);


    // ----------------------------------------------------------------------
    // BASIC METRICS
    // ----------------------------------------------------------------------

    document.getElementById(
        "word-count"
    ).textContent =
        metrics.word_count || 0;


    document.getElementById(
        "character-count"
    ).textContent =
        metrics.character_count || 0;


    // ----------------------------------------------------------------------
    // ENGAGEMENT METRICS
    // ----------------------------------------------------------------------

    document.getElementById(
        "hashtag-count"
    ).textContent =
        engagement.hashtag_count || 0;


    document.getElementById(
        "mention-count"
    ).textContent =
        engagement.mention_count || 0;


    document.getElementById(
        "question-count"
    ).textContent =
        engagement.question_count || 0;


    document.getElementById(
        "cta-status"
    ).textContent =
        engagement.cta_present
            ? "Yes"
            : "No";


    // ----------------------------------------------------------------------
    // SCORES
    // ----------------------------------------------------------------------

    const engagementScore =
        analysis.engagement_score || 0;

    const readabilityScore =
        analysis.readability_score || 0;

    const hookScore =
        analysis.hook_score || 0;


    setProgress(
        "engagement-progress",
        engagementScore
    );


    setProgress(
        "readability-progress",
        readabilityScore
    );


    setProgress(
        "hook-progress",
        hookScore
    );


    document.getElementById(
        "engagement-score"
    ).textContent =
        `${engagementScore}/100`;


    document.getElementById(
        "readability-score"
    ).textContent =
        `${readabilityScore}/100`;


    document.getElementById(
        "hook-score"
    ).textContent =
        `${hookScore}/100`;


    // ----------------------------------------------------------------------
    // SUGGESTIONS
    // ----------------------------------------------------------------------

    displaySuggestions(
        data.suggestions || []
    );


    // ----------------------------------------------------------------------
    // EXTRACTED TEXT
    // ----------------------------------------------------------------------

    document.getElementById(
        "extracted-text"
    ).textContent =
        data.text ||
        "No text extracted.";


    // ----------------------------------------------------------------------
    // SHOW RESULTS
    // ----------------------------------------------------------------------

    resultsSection.classList.remove(
        "hidden"
    );


    window.scrollTo({
        top: resultsSection.offsetTop - 20,
        behavior: "smooth"
    });

}


// --------------------------------------------------------------------------
// SCORE LABEL
// --------------------------------------------------------------------------

function getScoreLabel(score) {

    if (score >= 90) {
        return "Excellent";
    }

    if (score >= 80) {
        return "Very Good";
    }

    if (score >= 70) {
        return "Good";
    }

    if (score >= 60) {
        return "Fair";
    }

    if (score >= 50) {
        return "Needs Improvement";
    }

    return "Needs Significant Improvement";
}


// --------------------------------------------------------------------------
// PROGRESS BAR
// --------------------------------------------------------------------------

function setProgress(
    elementId,
    score
) {

    const element =
        document.getElementById(elementId);


    if (!element) {
        return;
    }


    const safeScore =
        Math.min(
            100,
            Math.max(0, score)
        );


    element.style.width =
        `${safeScore}%`;

}


// --------------------------------------------------------------------------
// DISPLAY SUGGESTIONS
// --------------------------------------------------------------------------

function displaySuggestions(
    suggestions
) {

    const container =
        document.getElementById(
            "suggestions-list"
        );


    container.innerHTML = "";


    if (!suggestions.length) {

        container.innerHTML = `
            <div class="suggestion-item">

                <div class="suggestion-category">
                    Excellent
                </div>

                <div class="suggestion-message">
                    Your content looks well optimized!
                </div>

            </div>
        `;

        return;
    }


    suggestions.forEach(
        function (suggestion) {

            const category =
                suggestion.category ||
                "Suggestion";

            const message =
                suggestion.message ||
                "";


            const item =
                document.createElement("div");


            item.className =
                "suggestion-item";


            item.innerHTML = `
                <div class="suggestion-category">
                    ${escapeHtml(category)}
                </div>

                <div class="suggestion-message">
                    ${escapeHtml(message)}
                </div>
            `;


            container.appendChild(item);

        }
    );

}


// --------------------------------------------------------------------------
// ERROR HANDLING
// --------------------------------------------------------------------------

function showError(message) {

    errorMessage.textContent =
        message;


    errorSection.classList.remove(
        "hidden"
    );


    window.scrollTo({
        top: errorSection.offsetTop - 20,
        behavior: "smooth"
    });

}


function hideError() {

    errorSection.classList.add(
        "hidden"
    );

}


// --------------------------------------------------------------------------
// TRY AGAIN
// --------------------------------------------------------------------------

tryAgainBtn.addEventListener(
    "click",
    function () {

        hideError();

    }
);


// --------------------------------------------------------------------------
// NEW ANALYSIS
// --------------------------------------------------------------------------

newAnalysisBtn.addEventListener(
    "click",
    function () {

        resultsSection.classList.add(
            "hidden"
        );

        resetFile();

        hideError();

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });

    }
);


// --------------------------------------------------------------------------
// HTML ESCAPING
// --------------------------------------------------------------------------

function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value;

    return div.innerHTML;

}


// --------------------------------------------------------------------------
// DELAY
// --------------------------------------------------------------------------

function delay(milliseconds) {

    return new Promise(
        function (resolve) {

            setTimeout(
                resolve,
                milliseconds
            );

        }
    );

}