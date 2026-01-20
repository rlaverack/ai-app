# Build Progress Log

## Current State
- **Day:** 0 (Not started)
- **App Idea:** TBD (deciding during Week 1)
- **Backend:** Not started
- **Mobile:** Not started
- **Web:** Not started
- **Blockers:** None

---

## Tech Stack (Confirmed)
- **Backend:** Python, FastAPI, Langgraph, SQLite (checkpointing)
- **Mobile:** React Native with Expo (compiles to native)
- **Web:** Next.js
- **Auth:** TBD (Clerk, Supabase, or Firebase)
- **Hosting:** TBD (Railway or Fly.io)
- **AI:** Claude API (Anthropic)
- **Tracing:** LangSmith

---

## Key Decisions Made
- Using Langgraph (not CrewAI/AutoGen) to get deep understanding
- React Native/Expo for mobile (native compilation, cross-platform codebase)
- Targeting real users by Day 21

---

## App Ideas (Brainstorm)
_Add ideas here during Week 1 as they come to you_

1. 
2. 
3. 

---

## Daily Log

### Day 1
**Date:** January 19, 2026
**Goal:** Environment setup + first Langgraph graph

**What I did:**
- Set up Python venv with langgraph, langchain-anthropic, langsmith, python-dotenv
- Created .env with API keys and LangSmith tracing config
- Built single-node StateGraph agent that calls Claude
- Added conversation loop with message history accumulation
- Verified traces showing up in LangSmith

**What I learned:**
- StateGraph defines the information architecture—how data flows and its shape
- Nodes are functions that take state in and return state updates
- add_messages annotation appends rather than replaces, enabling conversation history
- LangSmith traces show full message flow and latency per invocation

**Blockers/Questions:**
- None

**Tomorrow:**
- Multi-node graphs with conditional routing

### Day 2
**Date:** 
**Goal:** State and multi-node graphs
**What I did:**
- 

**What I learned:**
- 

**Blockers/Questions:**
- 

**Tomorrow:**
- 

---

_Continue adding daily entries..._