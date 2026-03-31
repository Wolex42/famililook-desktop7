## CPO Spec: Duo/Group Room Chat (Sprint 5)

**Agent**: CPO
**Date**: 2026-03-24
**Products**: FamiliMatch (desktop6 FE + desktop7 BE)

---

### What

Real-time text chat in Duo and Group rooms. Players can message each other during the lobby, upload, and results phases.

### Why

Duo/Group modes feel empty without communication. Players are in a room together but can't interact beyond uploading photos. Chat adds social engagement and increases time-in-room.

### Backend (desktop7)

**Add 2 message types to WebSocket protocol:**
- Client → Server: `send_chat` with `{ text: string }`
- Server → Client: `chat_message` with `{ sender_id, sender_name, text, timestamp }`

**Rules:**
- Max message length: 200 characters (prevent spam)
- Rate limit: 3 messages per 5 seconds per player
- No empty messages
- Strip HTML (prevent XSS — plain text only)
- Broadcast to all players in room (including sender)

**Files**: protocol.py (types + model), main.py (handler + broadcast)
**Backend permission**: Already granted

### Frontend (desktop6)

**ChatPanel component:**
- Collapsible panel at bottom of RoomPage
- Message list (auto-scroll to latest)
- Text input + send button (44px min touch target)
- Sender name in bold, message text, timestamp
- Different colour for own messages vs others
- Max 50 messages displayed (older scroll off)

**Integration:**
- RoomPage renders ChatPanel when in a room
- useMatchConnection hook sends/receives chat messages
- Chat available in all room phases (lobby, upload, countdown, results)

**Files**: new ChatPanel.jsx, update RoomPage.jsx, update useMatchConnection.js

### Acceptance Criteria

- [ ] Chat messages appear in real-time for all room participants
- [ ] Own messages styled differently from others
- [ ] 200 char limit enforced (both FE and BE)
- [ ] Rate limited server-side (3/5s)
- [ ] No HTML rendering (XSS safe — textContent only)
- [ ] Chat persists across room phases (lobby → upload → results)
- [ ] Auto-scroll to latest message
- [ ] Input has 44px min height (iOS HIG)

### Effort: M (backend S + frontend M)
