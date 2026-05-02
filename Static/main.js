document.addEventListener("DOMContentLoaded", () => {
 
  // ── Grab HTML elements by their id ──────────────────────
  // document.getElementById("xyz")  finds  <... id="xyz">
  const dropZone      = document.getElementById("dropZone");
  const fileInput     = document.getElementById("fileInput");
  const browseBtn     = document.getElementById("browseBtn");
  const previewWrapper= document.getElementById("previewWrapper");
  const imagePreview  = document.getElementById("imagePreview");
  const changeImgBtn  = document.getElementById("changeImageBtn");
  const analyzeBtn    = document.getElementById("analyzeBtn");
  const resultsSection= document.getElementById("resultsSection");
  const predictionsWrap=document.getElementById("predictionsWrap");
  const resultImage   = document.getElementById("resultImage");
  const tryAnotherBtn = document.getElementById("tryAnotherBtn");
  const errorBox      = document.getElementById("errorBox");
  const errorMessage  = document.getElementById("errorMessage");
 
  // Keep track of the selected file (or null if none)
  let selectedFile = null;
 
  // ══════════════════════════════════════════════════════════
  // SECTION 1 — File Selection
  // ══════════════════════════════════════════════════════════
 
  // ── Clicking "Browse Files" button opens the file picker ──
  browseBtn.addEventListener("click", (e) => {
    e.stopPropagation();   // Don't let click bubble to dropZone
    fileInput.click();     // Programmatically click the hidden input
  });
 
  // ── When user picks a file via the file picker ──
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      handleFileSelected(fileInput.files[0]);
    }
  });
 
  // ── Drag events on the drop zone ──────────────────────────
  // dragover: fires repeatedly while something is dragged over
  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();                    // Prevent browser default (open the file)
    dropZone.classList.add("drag-over");   // Add blue glow CSS class
  });
 
  // dragleave: fires when the dragged item leaves the zone
  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
  });
 
  // drop: fires when user releases the dragged file
  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    const files = e.dataTransfer.files;   // dataTransfer holds dropped files
    if (files.length > 0) {
      handleFileSelected(files[0]);
    }
  });
 
  // ── Keyboard accessibility: Enter/Space triggers file picker ──
  dropZone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });
 
  // ── "Change Image" button resets everything ──
  changeImgBtn.addEventListener("click", resetToUpload);
 
  // ══════════════════════════════════════════════════════════
  // SECTION 2 — Show preview after file is chosen
  // ══════════════════════════════════════════════════════════
 
  function handleFileSelected(file) {
    // Only accept image files (MIME type starts with "image/")
    if (!file.type.startsWith("image/")) {
      showError("Please select an image file (JPG, PNG, GIF, etc.)");
      return;
    }
 
    selectedFile = file;
    hideError();
 
    // FileReader converts the file into a data-URL (a base64 string
    // the browser can use as an <img src="...">)
    const reader = new FileReader();
 
    // onload fires once reading is complete
    reader.onload = (e) => {
      imagePreview.src = e.target.result;  // Set preview image source
      previewWrapper.classList.remove("hidden");  // Show preview
      dropZone.style.display = "none";            // Hide drop zone
      analyzeBtn.disabled = false;                // Enable Analyse button
    };
 
    reader.readAsDataURL(file);   // Start reading
  }
 
  // ══════════════════════════════════════════════════════════
  // SECTION 3 — Send image to Flask and get predictions
  // ══════════════════════════════════════════════════════════
 
  analyzeBtn.addEventListener("click", async () => {
    if (!selectedFile) return;
 
    // ── Show loading state ──
    setBtnLoading(true);
    hideError();
    resultsSection.classList.add("hidden");
 
    // ── Build FormData ──
    // FormData is like an envelope that holds file uploads.
    // The "file" key must match what Flask reads: request.files["file"]
    const formData = new FormData();
    formData.append("file", selectedFile);
 
    try {
      // ── Send POST request to /predict ──
      // fetch() sends an HTTP request and returns a Promise.
      // "await" pauses here until the response arrives
      // (without freezing the browser tab).
      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
        // Note: Do NOT set Content-Type header — the browser sets it
        // automatically with the correct multipart boundary.
      });
 
      // response.json() parses the JSON text the server sent back
      const data = await response.json();
 
      if (!response.ok || data.error) {
        showError(data.error || "Server error. Please try again.");
        return;
      }
 
      // ── Display results ──
      displayResults(data.predictions, data.image_url);
 
    } catch (err) {
      // Network error (server down, no internet, etc.)
      showError("Could not connect to the server. Is Flask running?");
      console.error(err);
    } finally {
      // Always restore the button, whether success or failure
      setBtnLoading(false);
    }
  });
 
  // ══════════════════════════════════════════════════════════
  // SECTION 4 — Render prediction results
  // ══════════════════════════════════════════════════════════
 
  function displayResults(predictions, imageUrl) {
    // Show the analysed image on the right card
    resultImage.src = imageUrl;
    resultImage.alt = "Analysed image";
 
    // Clear any previous predictions
    predictionsWrap.innerHTML = "";
 
    // Loop through each prediction object  { label, confidence }
    predictions.forEach((pred, index) => {
      const isTop = index === 0;   // First result = top prediction
 
      // Create the container div
      const item = document.createElement("div");
      item.className = `prediction-item${isTop ? " top" : ""}`;
      // animation-delay so bars appear one by one (cascading effect)
      item.style.animationDelay = `${index * 0.08}s`;
 
      // Build inner HTML
      // Template literals (`...`) let us embed variables with ${...}
      item.innerHTML = `
        <div class="prediction-header">
          <span class="prediction-label">
            ${isTop ? "🥇 " : ""}${escapeHtml(pred.label)}
          </span>
          <span class="prediction-pct">${pred.confidence.toFixed(1)}%</span>
        </div>
        <div class="prediction-bar-track">
          <div class="prediction-bar-fill" style="width: 0%"></div>
        </div>
      `;
 
      predictionsWrap.appendChild(item);
 
      // Animate the bar from 0% to the actual confidence width.
      // We use requestAnimationFrame to ensure the DOM has rendered
      // the 0% width before we change it (otherwise no animation).
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          item.querySelector(".prediction-bar-fill").style.width =
            `${pred.confidence}%`;
        });
      });
    });
 
    // Reveal the results section with a smooth appearance
    resultsSection.classList.remove("hidden");
    // Scroll smoothly to the results
    resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }
 
  // ══════════════════════════════════════════════════════════
  // SECTION 5 — Utility / Helper Functions
  // ══════════════════════════════════════════════════════════
 
  /** Reset the page back to the upload state */
  function resetToUpload() {
    selectedFile = null;
    fileInput.value = "";                       // Clear file input
    imagePreview.src = "";
    previewWrapper.classList.add("hidden");
    dropZone.style.display = "";               // Show drop zone again
    analyzeBtn.disabled = true;
    resultsSection.classList.add("hidden");
    hideError();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
 
  tryAnotherBtn.addEventListener("click", resetToUpload);
 
  /** Show the error box with a message */
  function showError(msg) {
    errorMessage.textContent = msg;
    errorBox.classList.remove("hidden");
  }
 
  /** Hide the error box */
  function hideError() {
    errorBox.classList.add("hidden");
  }
 
  /** Toggle the Analyse button between normal and loading states */
  function setBtnLoading(loading) {
    const text    = analyzeBtn.querySelector(".btn-text");
    const spinner = analyzeBtn.querySelector(".btn-spinner");
    analyzeBtn.disabled = loading;
    text.classList.toggle("hidden", loading);
    spinner.classList.toggle("hidden", !loading);
  }
 
  /**
   * Escape HTML special characters to prevent XSS attacks.
   * If a label came back as "<script>alert(1)</script>" we
   * don't want the browser to execute that script!
   * This converts  <  →  &lt;   >  →  &gt;   etc.
   */
  function escapeHtml(str) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }
 
});  // End of DOMContentLoaded