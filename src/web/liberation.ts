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

interface Extension {
    name: string;
    commands?: Command[];
    setup?: () => Promise<void>;
}

interface Command {
    id: string;
    label: string;
    icon: string;
    function: () => void;
}

interface KeyStatus {
    configured: boolean;
    source?: "local" | "pass" | null;
    pass_path?: string | null;
}

interface StatusData {
    patched: boolean;
    mapped_patterns: number;
    unmapped_endpoints: string[];
    unmapped_count: number;
}

type KeysData = Record<string, KeyStatus>;

// =============================================================================
// Assets / Constants
// =============================================================================

const CSS_URL = new URL("./liberation.css", import.meta.url).href;
const LIBERATION_ERR = /LIBERATION_(MISSING_KEY|INVALID_KEY):([a-z0-9_]+):/i;

// Inline critical CSS so the modal stays usable even if the stylesheet fails to load.
const INLINE_STYLE_ID = "liberation-inline-style";
// Inline fallback uses ComfyUI's CSS vars with hardcoded defaults for resilience.
const INLINE_CSS = `
.liberation-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;z-index:999999}
.liberation-modal{background:var(--comfy-menu-bg,#353535);border:1px solid var(--border-color,#4e4e4e);border-radius:6px;width:90%;max-width:700px;max-height:85vh;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 0 4px #111}
.liberation-header{display:flex;justify-content:space-between;align-items:center;padding:4px 10px;height:40px;border-bottom:1px solid var(--border-color,#4e4e4e)}
.liberation-header h2{margin:0;font-size:1rem;color:var(--fg-color,#fff)}
.liberation-close{background:none;border:none;color:var(--descrip-text,#999);font-size:1.4em;cursor:pointer;padding:0 8px}
.liberation-content{padding:16px;overflow-y:auto;color:var(--input-text,#ddd)}
`;

// =============================================================================
// Provider API Key URLs — fetched from backend (single source of truth in
// mappings/PROVIDER_REGISTRY). Populated on setup() via /api/liberation/providers.
// =============================================================================

let PROVIDER_KEY_URLS: Record<string, string> = {};
let PASS_AVAILABLE = true;

/**
 * Fetch provider key URLs from the backend registry.
 * Called once during setup() so the data is available for error popups.
 */
async function loadProviderKeyUrls(): Promise<void> {
    try {
        const resp = await api.fetchApi("/api/liberation/providers");
        if (resp.ok) {
            const data = await resp.json();
            if (data.key_urls) {
                PROVIDER_KEY_URLS = data.key_urls;
                console.log(`[liberation] Loaded ${Object.keys(PROVIDER_KEY_URLS).length} provider key URLs`);
            }
            PASS_AVAILABLE = data.pass_available !== false;
        }
    } catch (e) {
        console.warn("[liberation] Failed to load provider key URLs:", e);
    }
}

/**
 * Get the API key signup URL for a provider, or null if unknown.
 */
function getProviderKeyUrl(provider: string): string | null {
    return PROVIDER_KEY_URLS[provider.toLowerCase()] || null;
}

// =============================================================================
// Modal System
// =============================================================================

function ensureStylesLoaded(): void {
    if (!document.getElementById(INLINE_STYLE_ID)) {
        const style = document.createElement("style");
        style.id = INLINE_STYLE_ID;
        style.textContent = INLINE_CSS;
        document.head.appendChild(style);
    }

    if (document.querySelector('link[data-liberation-css="true"]')) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = CSS_URL;
    link.dataset.liberationCss = "true";
    link.addEventListener("error", () => {
        console.warn("[liberation] Failed to load liberation.css, using inline fallback styles only.");
    });
    document.head.appendChild(link);
}

function createModal(title: string, content: string, options?: { highlight?: string; onClose?: () => void }): HTMLElement {
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

    const closeBtn = overlay.querySelector(".liberation-close") as HTMLElement;
    closeBtn.onclick = closeModal;
    overlay.onclick = (e) => {
        if (e.target === overlay) closeModal();
    };

    document.body.appendChild(overlay);

    // Highlight specific provider if requested
    if (options?.highlight) {
        const row = overlay.querySelector(`.key-row[data-provider="${options.highlight}"]`);
        if (row) {
            row.classList.add("highlighted");
            row.scrollIntoView({ behavior: "smooth", block: "center" });
            const input = row.querySelector(".key-input") as HTMLInputElement;
            input?.focus();
        }
    }

    return overlay;
}

function escapeHtml(text: string): string {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

type KeySource = "local" | "pass";

function getRowSource(row: HTMLElement): KeySource {
    return row.dataset.source === "pass" ? "pass" : "local";
}

function setRowSource(row: HTMLElement, source: KeySource): void {
    row.dataset.source = source;

    const input = row.querySelector<HTMLInputElement>(".key-input");
    const toggle = row.querySelector<HTMLButtonElement>(".btn-source-toggle");
    if (!input || !toggle) return;

    row.classList.toggle("source-pass", source === "pass");
    row.classList.toggle("source-local", source === "local");
    toggle.textContent = source === "pass" ? "pass" : "key";
    toggle.title = source === "pass" ? "Using a pass entry path" : "Using a locally stored key";

    if (source === "pass") {
        input.type = "text";
        input.placeholder = "pass path...";
        input.value = row.dataset.passPath || "";
    } else {
        input.type = "password";
        input.placeholder = row.dataset.configured === "true" ? "Stored locally" : "key...";
        input.value = "";
    }
}

function configurePopupSource(
    source: KeySource,
    sourceBtn: HTMLButtonElement,
    keyInput: HTMLInputElement,
    saveBtn: HTMLButtonElement,
    hintEl: HTMLElement,
): void {
    sourceBtn.dataset.source = source;
    sourceBtn.textContent = source === "pass" ? "pass" : "key";
    sourceBtn.title = source === "pass" ? "Store a pass entry path" : "Store a local key";

    if (source === "pass") {
        keyInput.type = "text";
        keyInput.placeholder = "Enter pass entry path...";
        saveBtn.textContent = "Save Path & Retry";
        hintEl.innerHTML = `
            Store the secret with the <code>pass</code> CLI and save only the entry path here.
            <br>
            The secret stays outside ComfyUI's config file.
            <br>
            <a href="#" id="show-all-keys">Manage all API keys...</a>
        `;
    } else {
        keyInput.type = "password";
        keyInput.placeholder = "Enter API key...";
        saveBtn.textContent = "Save & Retry";
        hintEl.innerHTML = `
            Your key is stored locally and never sent to ComfyUI servers.
            <br>
            <a href="#" id="show-all-keys">Manage all API keys...</a>
        `;
    }
}

// =============================================================================
// API Key Configuration Popup (for missing key errors)
// =============================================================================

async function showKeyConfigPopup(
    provider: string,
    opts?: { reason?: "missing" | "invalid"; details?: string },
): Promise<void> {
    console.log(`[liberation] Showing key config popup for: ${provider}`);

    // Prevent duplicate popups
    if (_popupShowing) return;
    _popupShowing = true;

    // Remove any existing liberation modal first
    document.getElementById("liberation-modal")?.remove();

    const keyUrl = getProviderKeyUrl(provider);
    const getKeyLink = keyUrl
        ? `<a href="${keyUrl}" target="_blank" rel="noopener" class="get-key-link">Get ${provider.toUpperCase()} API Key &rarr;</a>`
        : "";

    const reasonLine =
        opts?.reason === "invalid"
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
                <button id="liberation-key-source" class="btn-source-toggle large" type="button"${PASS_AVAILABLE ? "" : " disabled"}>key</button>
                <input type="password"
                       id="liberation-key-input"
                       class="key-input large"
                       placeholder="Enter your ${provider.toUpperCase()} API key..."
                       autofocus>
                <button id="liberation-save-key" class="btn-save large">Save & Retry</button>
            </div>

            <p class="hint" id="liberation-key-storage-hint">
                Your key is stored locally and never sent to ComfyUI servers.
                <br>
                <a href="#" id="show-all-keys">Manage all API keys...</a>
            </p>
        </div>
    `);

    // Wire up event handlers
    const saveBtn = modal.querySelector("#liberation-save-key") as HTMLButtonElement;
    const keyInput = modal.querySelector("#liberation-key-input") as HTMLInputElement;
    const sourceBtn = modal.querySelector("#liberation-key-source") as HTMLButtonElement;
    const hintEl = modal.querySelector("#liberation-key-storage-hint") as HTMLElement;
    configurePopupSource("local", sourceBtn, keyInput, saveBtn, hintEl);

    sourceBtn.onclick = () => {
        const nextSource: KeySource = sourceBtn.dataset.source === "pass" ? "local" : "pass";
        configurePopupSource(nextSource, sourceBtn, keyInput, saveBtn, hintEl);
        keyInput.focus();
    };

    saveBtn.onclick = async () => {
        const source: KeySource = sourceBtn.dataset.source === "pass" ? "pass" : "local";
        const value = keyInput.value.trim();
        if (!value) {
            alert(source === "pass" ? "Please enter a pass entry path" : "Please enter an API key");
            return;
        }

        saveBtn.disabled = true;
        saveBtn.textContent = "Saving...";

        try {
            const resp = await api.fetchApi(`/api/liberation/keys/${provider}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(
                    source === "pass"
                        ? { source, pass_path: value }
                        : { source, key: value },
                ),
            });

            if (!resp.ok) {
                const err = await resp.json();
                throw new Error(err.error || "Failed to save key");
            }

            console.log(`[liberation] Saved key for ${provider}`);
            modal.remove();
            _popupShowing = false;

            // Show success and suggest re-running
            showSuccessToast(
                source === "pass"
                    ? `${provider.toUpperCase()} pass path saved. Re-queue your prompt to continue.`
                    : `${provider.toUpperCase()} API key saved! Re-queue your prompt to continue.`,
            );
        } catch (e) {
            const error = e instanceof Error ? e.message : String(e);
            alert(`Error: ${error}`);
            saveBtn.disabled = false;
            configurePopupSource(source, sourceBtn, keyInput, saveBtn, hintEl);
        }
    };

    // Enter key to save
    keyInput.onkeydown = (e) => {
        if (e.key === "Enter") saveBtn.click();
    };

    modal.addEventListener("click", (e) => {
        const target = e.target as HTMLElement | null;
        if (target?.id === "show-all-keys") {
            e.preventDefault();
            modal.remove();
            showKeyManager();
        }
    });
}

function showSuccessToast(message: string): void {
    const toast = document.createElement("div");
    toast.className = "liberation-toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

async function copyTextToClipboard(text: string): Promise<void> {
    if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
        return;
    }

    const textarea = document.createElement("textarea");
    textarea.value = text;
    textarea.setAttribute("readonly", "true");
    textarea.style.position = "fixed";
    textarea.style.opacity = "0";
    document.body.appendChild(textarea);
    textarea.select();

    try {
        if (!document.execCommand("copy")) {
            throw new Error("Clipboard copy command was rejected");
        }
    } finally {
        textarea.remove();
    }
}

// =============================================================================
// Error Interception
// =============================================================================

let _popupShowing = false;
let _lastPopupTime = 0;
let _dispatchPatched = false;

function parseLiberationError(text: string): { kind: "MISSING_KEY" | "INVALID_KEY"; provider: string; details: string } | null {
    const match = text.match(LIBERATION_ERR);
    if (!match) return null;
    const kind = match[1].toUpperCase() as "MISSING_KEY" | "INVALID_KEY";
    const provider = match[2].toLowerCase();
    const details = text.replace(match[0], "").trim();
    return { kind, provider, details };
}

function setupErrorInterception(): void {
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
    api.addEventListener("execution_error", (event: CustomEvent) => {
        const error = event.detail?.exception_message || event.detail?.message || "";
        handlePotentialLiberationError(error);
    });

    console.log("[liberation] Error interception active");
}

function checkForLiberationError(element: HTMLElement): void {
    // Debounce - don't fire multiple times
    const now = Date.now();
    if (_popupShowing || now - _lastPopupTime < 1000) return;

    // Look for error dialogs containing our marker
    const text = element.textContent || "";
    const parsed = parseLiberationError(text);
    if (!parsed) return;

    _lastPopupTime = now;
    console.log(`[liberation] Found liberation error dialog: ${parsed.kind} (${parsed.provider})`);

    // Hide ALL ComfyUI dialogs immediately (and keep them suppressed briefly)
    suppressComfyDialogsFor();

    showKeyConfigPopup(parsed.provider, {
        reason: parsed.kind === "INVALID_KEY" ? "invalid" : "missing",
        details: parsed.details,
    });
}

function hideAllComfyDialogs(): void {
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

function handlePotentialLiberationError(errorMessage: string): void {
    // Debounce
    const now = Date.now();
    if (_popupShowing || now - _lastPopupTime < 1000) return;

    const parsed = parseLiberationError(errorMessage);
    if (!parsed) return;

    _lastPopupTime = now;
    console.log(`[liberation] Intercepted liberation error: ${parsed.kind} (${parsed.provider})`);
    suppressComfyDialogsFor();
    showKeyConfigPopup(parsed.provider, {
        reason: parsed.kind === "INVALID_KEY" ? "invalid" : "missing",
        details: parsed.details,
    });
}

function suppressComfyDialogsFor(ms = 1200): void {
    const end = Date.now() + ms;
    const tick = () => {
        hideAllComfyDialogs();
        if (Date.now() < end) {
            setTimeout(tick, 120);
        }
    };
    tick();
}

function parseProviderFromMessage(msg?: string | null): string | null {
    const parsed = msg ? parseLiberationError(msg) : null;
    return parsed ? parsed.provider : null;
}

function installDispatchInterceptor(): void {
    if (_dispatchPatched) return;
    const origDispatch = (api as any).dispatchCustomEvent?.bind(api);
    if (!origDispatch) return;

    (api as any).dispatchCustomEvent = function patchedDispatch(type: string, detail?: any) {
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

async function showKeyManager(highlightProvider?: string): Promise<void> {
    console.log("[liberation] Opening key manager...");

    let keysData: KeysData;
    let statusData: StatusData;

    try {
        const [keysResp, statusResp] = await Promise.all([
            api.fetchApi("/api/liberation/keys"),
            api.fetchApi("/api/liberation/status"),
        ]);

        if (!keysResp.ok) throw new Error(`Keys API returned ${keysResp.status}`);
        if (!statusResp.ok) throw new Error(`Status API returned ${statusResp.status}`);

        keysData = await keysResp.json();
        statusData = await statusResp.json();
    } catch (e) {
        const error = e instanceof Error ? e.message : String(e);
        console.error("[liberation] Failed to load data:", error);
        createModal("Error", `<p style="color: #f87171;">Failed to load API key data: ${escapeHtml(error)}</p>`);
        return;
    }

    const providersHtml = Object.entries(keysData)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([provider, info]) => {
            const highlightClass = provider === highlightProvider ? "highlighted" : "";
            const source = info.source === "pass" ? "pass" : "local";
            const keyUrl = getProviderKeyUrl(provider);
            const getKeyLink = keyUrl
                ? `<a href="${keyUrl}" target="_blank" rel="noopener" class="btn-get-key" title="Get API key from ${provider}">&#x2197;</a>`
                : `<span class="btn-get-key-spacer"></span>`;
            const statusDot = info.configured
                ? `<span class="status-dot configured" title="Configured">&#x25CF;</span>`
                : `<span class="status-dot missing" title="Not set">&#x25CB;</span>`;
            const sourceToggleTitle = source === "pass"
                ? "Using a pass entry path"
                : "Using a locally stored key";

            return `
                <div class="key-row ${highlightClass} source-${source}"
                     data-provider="${escapeHtml(provider)}"
                     data-source="${source}"
                     data-configured="${info.configured ? "true" : "false"}"
                     data-pass-path="${escapeHtml(info.pass_path || "")}">
                    ${statusDot}
                    <span class="provider-name">${escapeHtml(provider)}</span>
                    ${getKeyLink}
                    <button class="btn-source-toggle" data-provider="${escapeHtml(provider)}" type="button" title="${escapeHtml(sourceToggleTitle)}"${PASS_AVAILABLE ? "" : " disabled"}>
                        ${source === "pass" ? "pass" : "key"}
                    </button>
                    <input class="key-input"
                           placeholder="${source === "pass" ? "pass path..." : (info.configured ? "Stored locally" : "key...")}"
                           value="${source === "pass" ? escapeHtml(info.pass_path || "") : ""}"
                           ${source === "pass" ? 'type="text"' : 'type="password"'}
                           data-provider="${escapeHtml(provider)}">
                    <button class="btn-save" data-provider="${escapeHtml(provider)}">Save</button>
                    <button class="btn-delete" data-provider="${escapeHtml(provider)}" title="Clear key">&times;</button>
                </div>
            `;
        })
        .join("");

    const unmappedHtml = statusData.unmapped_endpoints.length > 0
        ? `<details>
               <summary>${statusData.unmapped_count} unmapped endpoints</summary>
               <div class="unmapped-actions">
                   <button class="btn-copy-unmapped" type="button">Copy Full List</button>
               </div>
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
            <p class="hint">Use <code>key</code> for local storage or <code>pass</code> to store only a CLI-managed pass entry path.</p>
            ${providersHtml}
        </div>

        <div class="liberation-unmapped">
            <h3>Coverage</h3>
            ${unmappedHtml}
        </div>
    `, { highlight: highlightProvider });

    // Attach event listeners
    modal.querySelectorAll<HTMLButtonElement>(".btn-save").forEach(btn => {
        btn.onclick = () => saveKey(btn.dataset.provider!);
    });
    modal.querySelectorAll<HTMLButtonElement>(".btn-delete").forEach(btn => {
        btn.onclick = () => deleteKey(btn.dataset.provider!);
    });
    modal.querySelectorAll<HTMLButtonElement>(".btn-source-toggle").forEach(btn => {
        btn.onclick = () => {
            const row = btn.closest<HTMLElement>(".key-row");
            if (!row) return;
            const nextSource: KeySource = getRowSource(row) === "pass" ? "local" : "pass";
            setRowSource(row, nextSource);
            row.querySelector<HTMLInputElement>(".key-input")?.focus();
        };
    });
    modal.querySelectorAll<HTMLElement>(".key-row").forEach(row => {
        setRowSource(row, getRowSource(row));
    });

    const copyBtn = modal.querySelector<HTMLButtonElement>(".btn-copy-unmapped");
    if (copyBtn) {
        copyBtn.onclick = async () => {
            const fullList = statusData.unmapped_endpoints.join("\n");
            try {
                await copyTextToClipboard(fullList);
                showSuccessToast(`Copied ${statusData.unmapped_count} unmapped endpoints.`);
            } catch (e) {
                const error = e instanceof Error ? e.message : String(e);
                alert(`Failed to copy unmapped endpoints: ${error}`);
            }
        };
    }
}

async function saveKey(provider: string): Promise<void> {
    const row = document.querySelector<HTMLElement>(
        `.key-row[data-provider="${provider}"]`,
    );
    const input = document.querySelector<HTMLInputElement>(
        `.key-row[data-provider="${provider}"] .key-input`
    );
    const source: KeySource = row?.dataset.source === "pass" ? "pass" : "local";
    const value = input?.value?.trim();

    if (!value) {
        alert(source === "pass" ? "Please enter a pass entry path" : "Please enter an API key");
        return;
    }

    try {
        const resp = await api.fetchApi(`/api/liberation/keys/${provider}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(
                source === "pass"
                    ? { source, pass_path: value }
                    : { source, key: value },
            ),
        });

        if (!resp.ok) {
            const err = await resp.json();
            throw new Error(err.error || "Failed to save key");
        }

        console.log(`[liberation] Saved key for ${provider}`);
        showKeyManager(); // Refresh
    } catch (e) {
        const error = e instanceof Error ? e.message : String(e);
        alert(`Error: ${error}`);
    }
}

async function deleteKey(provider: string): Promise<void> {
    if (!confirm(`Clear API key for ${provider}?`)) return;

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
    } catch (e) {
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
        await loadProviderKeyUrls();
        installDispatchInterceptor();

        // Set up error interception for missing API keys
        setupErrorInterception();

        // Try new-style menu first (ComfyUI 1.3+)
        try {
            // @ts-ignore - ComfyUI runtime module
            const buttonModule = await import("../../scripts/ui/components/button.js");
            const ComfyButton = buttonModule.ComfyButton as new (opts: {
                icon: string;
                action: () => void;
                tooltip: string;
                content: string;
                classList: string;
            }) => { element: HTMLElement };

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
        } catch (e) {
            console.log("[liberation] New menu not available:", e);
        }

        // Also add to legacy menu
        const menu = document.querySelector<HTMLElement>(".comfy-menu");
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
