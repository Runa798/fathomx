# Browser Automation Layer (Layer 2) Guide

Use this layer only after API-based tools (Grok Search MCP + Exa MCP) have failed or cannot access the required content.

---

## When to Use

| Situation | Use browser layer? |
|-----------|--------------------|
| Content behind a login wall (forums, paid platforms, SaaS dashboards) | Yes |
| JavaScript-rendered pages that `web_fetch` returns empty or garbled for | Yes |
| Sites actively blocking API-based crawlers (bot detection, rate limiting by IP) | Yes |
| Interactive content requiring navigation (paginated tables, drill-down UI) | Yes |
| Normal public web pages | No — use Grok `web_fetch` first |
| Already tried `web_fetch` and got good content | No |

---

## Prerequisites

The following must be set up on the host machine before browser layer can function:

- **System Chrome**: `google-chrome-stable` installed at `/usr/bin/google-chrome-stable`
- **CDP port**: Chrome DevTools Protocol running on port 9222
- **Display**: Xvfb or similar on `DISPLAY=:99`
- **Persistent profile**: `~/.agent-browser/profiles/main-system/` (retains login sessions)
- **Start script**: `~/.agent-browser/start-system-chrome.sh [url]`

To start Chrome before browser operations:
```bash
~/.agent-browser/start-system-chrome.sh
# Chrome starts in background with DISPLAY=:99, CDP on port 9222
```

> Note for public users: The browser layer requires local setup of Chrome, CDP, and the agent-browser npm package. This is documented as a capability but not auto-configured by the skill installation.

---

## Tool Selection Guide

### agent-browser — Precise Step-by-Step Automation

Use when the page structure is known and you need targeted data extraction.

```bash
# Open a URL
agent-browser --cdp 9222 open "https://example.com/page"

# Get a snapshot of current page state (DOM summary)
agent-browser --cdp 9222 snapshot

# Click an element by CSS selector or accessible text
agent-browser --cdp 9222 click "button[data-testid='load-more']"

# Extract text content
agent-browser --cdp 9222 get text

# Extract a specific element
agent-browser --cdp 9222 get "selector"
```

Best for:
- Extracting data from a known table or list
- Clicking through pagination on a known site
- Logging in with known credentials before scraping
- Targeted element extraction from a familiar page layout

### browser-use — Autonomous Multi-Step Navigation

Use when the page structure is unknown and you need the AI to figure out navigation.

```bash
# Connect to existing system Chrome via CDP
browser-use connect

# Or launch independently (separate Chrome instance)
browser-use open "https://example.com"
```

Then provide a natural-language goal; browser-use will autonomously navigate, click, scroll, and extract.

Best for:
- Exploratory browsing when you don't know the page structure
- Multi-step flows (login → navigate to dashboard → find report → download)
- Sites where the structure may have changed since last visit
- Complex interactive content requiring judgment about what to click next

---

## Critical Notes

1. **Do NOT use agent-browser's bundled Chrome for Testing** — it is a headless test browser that gets detected by Cloudflare and other anti-bot systems. Always connect via `--cdp 9222` to the system Chrome.

2. **Reuse system Chrome sessions** — The system Chrome at `~/.agent-browser/profiles/main-system/` retains login state for sites previously authenticated. Check if the target site is already logged in with `snapshot` before attempting login automation.

3. **CAPTCHA/Turnstile handling** — If the browser layer encounters a Cloudflare Turnstile challenge or any CAPTCHA:
   - Stop automation immediately
   - Report to the user: "The page at [URL] requires a CAPTCHA/Turnstile. Please navigate to it manually and complete the challenge."
   - Provide the URL for manual access
   - Do NOT attempt automated CAPTCHA solving in the public version of this skill

4. **Performance**: Browser operations are 10–50x slower than API calls. Always exhaust Grok (`web_fetch`) and Exa (`crawling_exa`) before escalating here.

5. **Screenshot for debugging**: If a browser operation produces unexpected results, take a screenshot to verify page state:
   ```bash
   DISPLAY=:99 import -window root /tmp/debug-screenshot.png
   ```

---

## Typical Escalation Flow

```
1. Try: mcp__grok-search__web_fetch(url)
   → If good content: done
   → If empty/garbled: continue

2. Try: mcp__exa__crawling_exa(url)
   → If good content: done
   → If empty/blocked: continue

3. Check: Is the page publicly accessible?
   → No (login wall): Check if system Chrome has active session
     → Session exists: agent-browser open + get text
     → No session: browser-use connect and navigate to login
   → Yes (JS rendering issue): agent-browser open + snapshot + get text

4. If CAPTCHA encountered at any browser step:
   → Halt; inform user; provide URL
```
