/**
 * ComfyUI API Liberation - Frontend Extension
 * Adds API key management UI to ComfyUI
 *
 * Bypasses ComfyUI's credit-laundering proxy system by allowing users
 * to configure their own API keys for direct vendor access.
 */
// @ts-ignore - ComfyUI runtime imports
import { app } from "../../scripts/app.js";
// @ts-ignore - ComfyUI runtime imports
import { api } from "../../scripts/api.js";
// =============================================================================
// Assets / Constants
// =============================================================================
const CSS_URL = new URL("./liberation.css", import.meta.url).href;
const LIBERATION_ERR = /LIBERATION_(MISSING_KEY|INVALID_KEY):([a-z0-9_]+):/i;
// Inline critical CSS so the modal stays usable even if the stylesheet fails to load.
const INLINE_STYLE_ID = "liberation-inline-style";
const INLINE_CSS = `
.liberation-overlay{position:fixed;inset:0;background:rgba(0,0,0,.7);display:flex;align-items:center;justify-content:center;z-index:999999}
.liberation-modal{background:#1a1a2e;border:1px solid #4a4a6a;border-radius:8px;width:90%;max-width:700px;max-height:85vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 4px 20px rgba(0,0,0,.5)}
.liberation-header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;background:#16162a;border-bottom:1px solid #4a4a6a}
.liberation-header h2{margin:0;font-size:18px;color:#fff}
.liberation-close{background:none;border:none;color:#888;font-size:24px;cursor:pointer;padding:0 8px}
.liberation-content{padding:20px;overflow-y:auto;color:#ccc}
`;
// =============================================================================
// Provider API Key URLs - Direct links to get API keys from each vendor
// =============================================================================
const PROVIDER_KEY_URLS = {
    google: "https://aistudio.google.com/app/apikey",
    openai: "https://platform.openai.com/api-keys",
    stability: "https://platform.stability.ai/account/keys",
    bfl: "https://api.bfl.ml",
    ideogram: "https://ideogram.ai/manage-api",
    recraft: "https://www.recraft.ai/docs/api-reference/getting-started",
    luma: "https://lumalabs.ai/dream-machine/api/keys",
    runway: "https://dev.runwayml.com",
    kling: "https://app.klingai.com/global/dev/api-key",
    minimax: "https://platform.minimax.io",
    pika: "https://pika.art/api",
    tripo: "https://platform.tripo3d.ai",
    rodin: "https://hyperhuman.deemos.com/api-dashboard",
    topaz: "https://www.topazlabs.com/api",
    byteplus: "https://console.byteplus.com",
    pixverse: "https://platform.pixverse.ai",
    vidu: "https://platform.vidu.com",
    moonvalley: "https://www.moonvalley.com",
    ltx: "https://ltx.io/model/api",
    wan: "https://www.alibabacloud.com/help/en/model-studio/get-api-key",
};
/**
 * Get the API key signup URL for a provider, or null if unknown.
 */
function getProviderKeyUrl(provider) {
    return PROVIDER_KEY_URLS[provider.toLowerCase()] || null;
}
// =============================================================================
// Modal System
// =============================================================================
function ensureStylesLoaded() {
    if (!document.getElementById(INLINE_STYLE_ID)) {
        const style = document.createElement("style");
        style.id = INLINE_STYLE_ID;
        style.textContent = INLINE_CSS;
        document.head.appendChild(style);
    }
    if (document.querySelector('link[data-liberation-css="true"]'))
        return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = CSS_URL;
    link.dataset.liberationCss = "true";
    link.addEventListener("error", () => {
        console.warn("[liberation] Failed to load liberation.css, using inline fallback styles only.");
    });
    document.head.appendChild(link);
}
function createModal(title, content, options) {
    ensureStylesLoaded();
    // Remove existing modal
    document.getElementById("liberation-modal")?.remove();
    const overlay = document.createElement("div");
    overlay.id = "liberation-modal";
    overlay.className = "liberation-overlay";
    // Super high z-index to be above everything
    overlay.style.zIndex = "999999";
    overlay.innerHTML = `
        <div class="liberation-modal">
            <div class="liberation-header">
                <h2>${escapeHtml(title)}</h2>
                <button class="liberation-close">&times;</button>
            </div>
            <div class="liberation-content">
                ${content}
            </div>
        </div>
    `;
    // Close handlers
    const closeModal = () => {
        overlay.remove();
        _popupShowing = false;
        options?.onClose?.();
    };
    const closeBtn = overlay.querySelector(".liberation-close");
    closeBtn.onclick = closeModal;
    overlay.onclick = (e) => {
        if (e.target === overlay)
            closeModal();
    };
    document.body.appendChild(overlay);
    // Highlight specific provider if requested
    if (options?.highlight) {
        const row = overlay.querySelector(`.key-row[data-provider="${options.highlight}"]`);
        if (row) {
            row.classList.add("highlighted");
            row.scrollIntoView({ behavior: "smooth", block: "center" });
            const input = row.querySelector(".key-input");
            input?.focus();
        }
    }
    return overlay;
}
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
// =============================================================================
// API Key Configuration Popup (for missing key errors)
// =============================================================================
async function showKeyConfigPopup(provider, opts) {
    console.log(`[liberation] Showing key config popup for: ${provider}`);
    // Prevent duplicate popups
    if (_popupShowing)
        return;
    _popupShowing = true;
    // Remove any existing liberation modal first
    document.getElementById("liberation-modal")?.remove();
    const keyUrl = getProviderKeyUrl(provider);
    const getKeyLink = keyUrl
        ? `<a href="${keyUrl}" target="_blank" rel="noopener" class="get-key-link">Get ${provider.toUpperCase()} API Key &rarr;</a>`
        : "";
    const reasonLine = opts?.reason === "invalid"
        ? `<p class="prompt-message" style="color:#f87171;margin-top:-8px;">Your saved key was rejected. Paste a new one below.</p>`
        : "";
    const detailsLine = opts?.details
        ? `<p class="hint" style="color:#9ca3af;margin-top:0;">${escapeHtml(opts.details)}</p>`
        : "";
    const modal = createModal(`Configure ${provider.toUpperCase()} API Key`, `
        <div class="liberation-key-prompt">
            <p class="prompt-message">
                This node requires a <strong>${provider.toUpperCase()}</strong> API key to work.
                <br><br>
                Enter your API key below to bypass ComfyUI's credit system and use the API directly.
            </p>

            ${reasonLine}
            ${detailsLine}

            ${getKeyLink ? `<div class="get-key-section">${getKeyLink}</div>` : ""}

            <div class="key-input-group">
                <input type="password"
                       id="liberation-key-input"
                       class="key-input large"
                       placeholder="Enter your ${provider.toUpperCase()} API key..."
                       autofocus>
                <button id="liberation-save-key" class="btn-save large">Save & Retry</button>
            </div>

            <p class="hint">
                Your key is stored locally and never sent to ComfyUI servers.
                <br>
                <a href="#" id="show-all-keys">Manage all API keys...</a>
            </p>
        </div>
    `);
    // Wire up event handlers
    const saveBtn = modal.querySelector("#liberation-save-key");
    const keyInput = modal.querySelector("#liberation-key-input");
    const showAllLink = modal.querySelector("#show-all-keys");
    saveBtn.onclick = async () => {
        const key = keyInput.value.trim();
        if (!key) {
            alert("Please enter an API key");
            return;
        }
        saveBtn.disabled = true;
        saveBtn.textContent = "Saving...";
        try {
            const resp = await api.fetchApi(`/api/liberation/keys/${provider}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ key }),
            });
            if (!resp.ok) {
                const err = await resp.json();
                throw new Error(err.error || "Failed to save key");
            }
            console.log(`[liberation] Saved key for ${provider}`);
            modal.remove();
            _popupShowing = false;
            // Show success and suggest re-running
            showSuccessToast(`${provider.toUpperCase()} API key saved! Re-queue your prompt to continue.`);
        }
        catch (e) {
            const error = e instanceof Error ? e.message : String(e);
            alert(`Error: ${error}`);
            saveBtn.disabled = false;
            saveBtn.textContent = "Save & Retry";
        }
    };
    // Enter key to save
    keyInput.onkeydown = (e) => {
        if (e.key === "Enter")
            saveBtn.click();
    };
    showAllLink.onclick = (e) => {
        e.preventDefault();
        modal.remove();
        showKeyManager();
    };
}
function showSuccessToast(message) {
    const toast = document.createElement("div");
    toast.className = "liberation-toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}
// =============================================================================
// Error Interception
// =============================================================================
let _popupShowing = false;
let _lastPopupTime = 0;
let _dispatchPatched = false;
function parseLiberationError(text) {
    const match = text.match(LIBERATION_ERR);
    if (!match)
        return null;
    const kind = match[1].toUpperCase();
    const provider = match[2].toLowerCase();
    const details = text.replace(match[0], "").trim();
    return { kind, provider, details };
}
function setupErrorInterception() {
    console.log("[liberation] Setting up error interception...");
    // Watch for DOM changes to catch error dialogs
    const observer = new MutationObserver((mutations) => {
        for (const mutation of mutations) {
            for (const node of mutation.addedNodes) {
                if (node instanceof HTMLElement) {
                    checkForLiberationError(node);
                }
            }
        }
    });
    observer.observe(document.body, {
        childList: true,
        subtree: true,
    });
    // Also listen for API events
    api.addEventListener("execution_error", (event) => {
        const error = event.detail?.exception_message || event.detail?.message || "";
        handlePotentialLiberationError(error);
    });
    console.log("[liberation] Error interception active");
}
function checkForLiberationError(element) {
    // Debounce - don't fire multiple times
    const now = Date.now();
    if (_popupShowing || now - _lastPopupTime < 1000)
        return;
    // Look for error dialogs containing our marker
    const text = element.textContent || "";
    const parsed = parseLiberationError(text);
    if (!parsed)
        return;
    _lastPopupTime = now;
    console.log(`[liberation] Found liberation error dialog: ${parsed.kind} (${parsed.provider})`);
    // Hide ALL ComfyUI dialogs immediately (and keep them suppressed briefly)
    suppressComfyDialogsFor();
    showKeyConfigPopup(parsed.provider, {
        reason: parsed.kind === "INVALID_KEY" ? "invalid" : "missing",
        details: parsed.details,
    });
}
function hideAllComfyDialogs() {
    // Hide all possible ComfyUI error dialogs
    const selectors = [
        ".comfy-modal",
        ".p-dialog",
        "[class*='global-dialog']",
    ];
    for (const selector of selectors) {
        document.querySelectorAll(selector).forEach((el) => {
            if (el instanceof HTMLElement && !el.id?.includes("liberation")) {
                el.style.display = "none";
                el.remove(); // Actually remove it
            }
        });
    }
    // Also hide any overlay/mask
    document.querySelectorAll(".p-dialog-mask, .comfy-modal-overlay").forEach((el) => {
        if (el instanceof HTMLElement) {
            el.style.display = "none";
            el.remove();
        }
    });
}
function handlePotentialLiberationError(errorMessage) {
    // Debounce
    const now = Date.now();
    if (_popupShowing || now - _lastPopupTime < 1000)
        return;
    const parsed = parseLiberationError(errorMessage);
    if (!parsed)
        return;
    _lastPopupTime = now;
    console.log(`[liberation] Intercepted liberation error: ${parsed.kind} (${parsed.provider})`);
    suppressComfyDialogsFor();
    showKeyConfigPopup(parsed.provider, {
        reason: parsed.kind === "INVALID_KEY" ? "invalid" : "missing",
        details: parsed.details,
    });
}
function suppressComfyDialogsFor(ms = 1200) {
    const end = Date.now() + ms;
    const tick = () => {
        hideAllComfyDialogs();
        if (Date.now() < end) {
            setTimeout(tick, 120);
        }
    };
    tick();
}
function parseProviderFromMessage(msg) {
    const parsed = msg ? parseLiberationError(msg) : null;
    return parsed ? parsed.provider : null;
}
function installDispatchInterceptor() {
    if (_dispatchPatched)
        return;
    const origDispatch = api.dispatchCustomEvent?.bind(api);
    if (!origDispatch)
        return;
    api.dispatchCustomEvent = function patchedDispatch(type, detail) {
        if (type === "execution_error") {
            const provider = parseProviderFromMessage(detail?.exception_message || "");
            if (provider) {
                _lastPopupTime = Date.now();
                suppressComfyDialogsFor();
                showKeyConfigPopup(provider);
                return true; // swallow so default Comfy dialog doesn't render
            }
        }
        return origDispatch(type, detail);
    };
    _dispatchPatched = true;
    console.log("[liberation] Patched api.dispatchCustomEvent for execution_error interception");
}
// =============================================================================
// Full Key Manager
// =============================================================================
async function showKeyManager(highlightProvider) {
    console.log("[liberation] Opening key manager...");
    let keysData;
    let statusData;
    try {
        const [keysResp, statusResp] = await Promise.all([
            api.fetchApi("/api/liberation/keys"),
            api.fetchApi("/api/liberation/status"),
        ]);
        if (!keysResp.ok)
            throw new Error(`Keys API returned ${keysResp.status}`);
        if (!statusResp.ok)
            throw new Error(`Status API returned ${statusResp.status}`);
        keysData = await keysResp.json();
        statusData = await statusResp.json();
    }
    catch (e) {
        const error = e instanceof Error ? e.message : String(e);
        console.error("[liberation] Failed to load data:", error);
        createModal("Error", `<p style="color: #f87171;">Failed to load API key data: ${escapeHtml(error)}</p>`);
        return;
    }
    const providersHtml = Object.entries(keysData)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([provider, info]) => {
        const statusClass = info.configured ? "configured" : "missing";
        const statusText = info.configured ? "Configured" : "Not set";
        const highlightClass = provider === highlightProvider ? "highlighted" : "";
        const keyUrl = getProviderKeyUrl(provider);
        const getKeyLink = keyUrl
            ? `<a href="${keyUrl}" target="_blank" rel="noopener" class="btn-get-key" title="Get API key from ${provider}">Get Key</a>`
            : "";
        return `
                <div class="key-row ${highlightClass}" data-provider="${escapeHtml(provider)}">
                    <div class="key-info">
                        <span class="provider-name">${escapeHtml(provider)}</span>
                        ${getKeyLink}
                        <span class="status ${statusClass}">${statusText}</span>
                    </div>
                    <div class="key-actions">
                        <input type="password"
                               class="key-input"
                               placeholder="Enter API key..."
                               data-provider="${escapeHtml(provider)}">
                        <button class="btn-save" data-provider="${escapeHtml(provider)}">Save</button>
                        <button class="btn-delete" data-provider="${escapeHtml(provider)}">Clear</button>
                    </div>
                </div>
            `;
    })
        .join("");
    const unmappedHtml = statusData.unmapped_endpoints.length > 0
        ? `<details>
               <summary>${statusData.unmapped_count} unmapped endpoints</summary>
               <ul class="unmapped-list">
                   ${statusData.unmapped_endpoints.slice(0, 20).map(ep => `<li>${escapeHtml(ep)}</li>`).join("")}
                   ${statusData.unmapped_count > 20 ? `<li>... and ${statusData.unmapped_count - 20} more</li>` : ""}
               </ul>
           </details>`
        : "<p>All endpoints mapped!</p>";
    const modal = createModal("API Key Manager", `
        <div class="liberation-status-bar">
            <span class="status-item ${statusData.patched ? 'active' : 'inactive'}">
                ${statusData.patched ? "Active" : "Inactive"} Direct Routing
            </span>
            <span class="status-item">
                ${statusData.mapped_patterns} providers mapped
            </span>
        </div>

        <div class="liberation-providers">
            <h3>API Keys</h3>
            <p class="hint">Enter your API keys below. Keys are saved locally.</p>
            ${providersHtml}
        </div>

        <div class="liberation-unmapped">
            <h3>Coverage</h3>
            ${unmappedHtml}
        </div>
    `, { highlight: highlightProvider });
    // Attach event listeners
    modal.querySelectorAll(".btn-save").forEach(btn => {
        btn.onclick = () => saveKey(btn.dataset.provider);
    });
    modal.querySelectorAll(".btn-delete").forEach(btn => {
        btn.onclick = () => deleteKey(btn.dataset.provider);
    });
}
async function saveKey(provider) {
    const input = document.querySelector(`.key-row[data-provider="${provider}"] .key-input`);
    const key = input?.value?.trim();
    if (!key) {
        alert("Please enter an API key");
        return;
    }
    try {
        const resp = await api.fetchApi(`/api/liberation/keys/${provider}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key }),
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.error || "Failed to save key");
        }
        console.log(`[liberation] Saved key for ${provider}`);
        showKeyManager(); // Refresh
    }
    catch (e) {
        const error = e instanceof Error ? e.message : String(e);
        alert(`Error: ${error}`);
    }
}
async function deleteKey(provider) {
    if (!confirm(`Clear API key for ${provider}?`))
        return;
    try {
        const resp = await api.fetchApi(`/api/liberation/keys/${provider}`, {
            method: "DELETE",
        });
        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.error || "Failed to delete key");
        }
        console.log(`[liberation] Deleted key for ${provider}`);
        showKeyManager(); // Refresh
    }
    catch (e) {
        const error = e instanceof Error ? e.message : String(e);
        alert(`Error: ${error}`);
    }
}
// =============================================================================
// Extension Registration
// =============================================================================
app.registerExtension({
    name: "comfy.api.liberation",
    commands: [
        {
            id: "Liberation.APIKeys.Show",
            label: "API Key Manager",
            icon: "pi pi-key",
            function: showKeyManager,
        }
    ],
    async setup() {
        console.log("[liberation] Setting up frontend extension...");
        ensureStylesLoaded();
        installDispatchInterceptor();
        // Set up error interception for missing API keys
        setupErrorInterception();
        // Try new-style menu first (ComfyUI 1.3+)
        try {
            // @ts-ignore - ComfyUI runtime module
            const buttonModule = await import("../../scripts/ui/components/button.js");
            const ComfyButton = buttonModule.ComfyButton;
            const liberationBtn = new ComfyButton({
                icon: "key",
                action: () => showKeyManager(),
                tooltip: "API Key Manager (bypass Comfy credits)",
                content: "API Keys",
                classList: "comfyui-button comfyui-menu-mobile-collapse"
            });
            if (app.menu?.settingsGroup?.element) {
                app.menu.settingsGroup.element.before(liberationBtn.element);
                console.log("[liberation] Button added to new-style menu");
            }
        }
        catch (e) {
            console.log("[liberation] New menu not available:", e);
        }
        // Also add to legacy menu
        const menu = document.querySelector(".comfy-menu");
        if (menu) {
            const btn = document.createElement("button");
            btn.id = "liberation-menu-btn";
            btn.textContent = "API Keys";
            btn.title = "Manage direct API keys (bypass Comfy credits)";
            btn.onclick = () => showKeyManager();
            btn.style.cssText = `
                background: linear-gradient(135deg, #4f46e5, #7c3aed);
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                cursor: pointer;
                margin: 4px;
            `;
            menu.appendChild(btn);
            console.log("[liberation] Button added to legacy menu");
        }
        console.log("[liberation] Frontend extension loaded successfully");
    },
});
