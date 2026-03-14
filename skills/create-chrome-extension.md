---
name: create-chrome-extension
description: Production Chrome Extension with Manifest V3, React popup, background service worker, content scripts, and Chrome Storage sync
---

# Create Chrome Extension

Production-ready Chrome Extension oluşturur:
- Manifest V3 (MV3)
- React + TypeScript popup
- Background service worker
- Content script injection
- Chrome Storage sync
- Message passing architecture
- Vite build pipeline

## Usage
```
#create-chrome-extension <extension-name>
```

## manifest.json
```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0.0",
  "description": "Production Chrome Extension",
  "permissions": ["storage", "activeTab", "scripting"],
  "host_permissions": ["https://*/*"],
  "action": {
    "default_popup": "popup.html",
    "default_icon": { "16": "icons/16.png", "48": "icons/48.png", "128": "icons/128.png" }
  },
  "background": { "service_worker": "background.js", "type": "module" },
  "content_scripts": [{
    "matches": ["https://*/*"],
    "js": ["content.js"],
    "run_at": "document_idle"
  }],
  "icons": { "16": "icons/16.png", "48": "icons/48.png", "128": "icons/128.png" }
}
```

## src/background/index.ts
```typescript
import { MessageType, type Message } from '../types/messages';

// Service worker — no DOM access
chrome.runtime.onInstalled.addListener(({ reason }) => {
  if (reason === 'install') {
    chrome.storage.sync.set({ enabled: true, settings: {} });
  }
});

chrome.runtime.onMessage.addListener(
  (message: Message, sender, sendResponse) => {
    switch (message.type) {
      case MessageType.GET_DATA:
        handleGetData(message.payload).then(sendResponse);
        return true; // Keep channel open for async

      case MessageType.SAVE_SETTINGS:
        chrome.storage.sync.set({ settings: message.payload }, () => {
          sendResponse({ success: true });
        });
        return true;
    }
  }
);

async function handleGetData(payload: unknown) {
  // Fetch from API or process data
  return { data: null };
}
```

## src/content/index.ts
```typescript
import { MessageType } from '../types/messages';

// Injected into web pages
function extractPageData() {
  return {
    title: document.title,
    url: window.location.href,
    selectedText: window.getSelection()?.toString() ?? '',
  };
}

// Listen for messages from popup/background
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === MessageType.EXTRACT_DATA) {
    sendResponse(extractPageData());
  }
});

// Observe DOM changes
const observer = new MutationObserver((mutations) => {
  // React to page changes
});
observer.observe(document.body, { childList: true, subtree: true });
```

## src/popup/App.tsx
```tsx
import { useEffect, useState } from 'react';
import { MessageType } from '../types/messages';

type PageData = { title: string; url: string; selectedText: string };

export default function App() {
  const [pageData, setPageData] = useState<PageData | null>(null);
  const [enabled, setEnabled] = useState(true);

  useEffect(() => {
    // Get current tab data
    chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
      if (!tab.id) return;
      chrome.tabs.sendMessage(tab.id, { type: MessageType.EXTRACT_DATA }, setPageData);
    });

    // Load settings
    chrome.storage.sync.get(['enabled'], ({ enabled }) => setEnabled(enabled));
  }, []);

  const toggleEnabled = () => {
    const next = !enabled;
    setEnabled(next);
    chrome.runtime.sendMessage({ type: MessageType.SAVE_SETTINGS, payload: { enabled: next } });
  };

  return (
    <div className="w-80 p-4 font-sans">
      <header className="flex items-center justify-between mb-4">
        <h1 className="text-lg font-bold">My Extension</h1>
        <button onClick={toggleEnabled} className={`px-3 py-1 rounded text-sm ${enabled ? 'bg-green-500' : 'bg-gray-400'} text-white`}>
          {enabled ? 'ON' : 'OFF'}
        </button>
      </header>
      {pageData && (
        <div className="text-sm text-gray-600">
          <p className="truncate">{pageData.title}</p>
          {pageData.selectedText && <p className="mt-2 p-2 bg-gray-100 rounded">{pageData.selectedText}</p>}
        </div>
      )}
    </div>
  );
}
```

## src/types/messages.ts
```typescript
export enum MessageType {
  GET_DATA = 'GET_DATA',
  SAVE_SETTINGS = 'SAVE_SETTINGS',
  EXTRACT_DATA = 'EXTRACT_DATA',
}

export type Message = {
  type: MessageType;
  payload?: unknown;
};
```

## vite.config.ts
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { crx } from '@crxjs/vite-plugin';
import manifest from './manifest.json';

export default defineConfig({
  plugins: [react(), crx({ manifest })],
  build: { rollupOptions: { input: { popup: 'popup.html' } } },
});
```
