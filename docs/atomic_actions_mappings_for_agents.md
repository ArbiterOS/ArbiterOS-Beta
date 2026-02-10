#  Atomic Agent Actions Mapping for Agents

This document analyzes how the implementation-level tools provided by different **Agent Clients** align with the high-level [**Atomic Agent Actions**](./atomic_actions.md)architecture.

Note the **Cognitive actions** are not included in this mapping as they are internal to the LLM's reasoning process and not directly observable as tool calls. Those should be implemented in **ArbiterOS's kernel**.

## OpenClaw

Definitions of tools provided by OpenClaw: <https://docs.openclaw.ai/tools>

### `apply_patch`

* **Category:** **`ACTIVE ENV`** → **`WRITE`**
* **Explanation:** This tool modifies the state of the file system by applying structured edits to files. It fits the **`WRITE`** definition perfectly as it changes the environment state (the code/text files) without necessarily triggering immediate external side effects (unlike executing a binary).

### `exec`

* **Category:** **`ACTIVE ENV`** → **`EXEC`**
* **Explanation:** This is the quintessential **`EXEC`** action. It runs shell commands (`command`) that have immediate functional side effects (e.g., building code, installing packages, deploying applications). It also supports background execution, which ties into the **`WAIT`** action (waiting for a long-running `exec` to finish).

### `process`

* **Category:** **`ACTIVE ENV`** → **`READ`** / **`EXEC`**
* **Explanation:**
* **`READ`**: When using `list`, `log`, or `poll` to check the status or output of a background task.
* **`EXEC`**: When using `kill` or `clear` to actively manage and terminate running processes.



### `web_search`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** This tool actively pulls information from the external world (the internet) using a search engine API. It maps directly to **`READ`** (Pull Information).

### `web_fetch`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** Similar to search, this tool retrieves specific content from a URL. It is a targeted **`READ`** action to ingest external data into the agent's context.

### `browser`

* **Category:** **`ACTIVE ENV`** → **`READ`** & **`EXEC`**
* **Explanation:** The browser is a complex tool covering multiple atomic actions:
* **`READ`**: `snapshot` (AI/Aria) and `screenshot` are purely for pulling visual or DOM information.
* **`EXEC`**: `act` (click, type, hover) triggers actions within the browser environment that change the state of the web page or application.



### `canvas`

* **Category:** **`ACTIVE ENV`** → **`RESPOND`** / **`WRITE`**
* **Explanation:**
* **`RESPOND`**: When `present` is used to show the final result or a UI interface to the human user.
* **`WRITE`**: When manipulating the canvas state (`a2ui_push`) as a scratchpad or intermediate display.



### `nodes`

* **Category:** **`ACTIVE ENV`** → **`READ`** & **`EXEC`**
* **Explanation:**
* **`READ`**: `status`, `describe`, and `location_get` are used to inspect the environment (connected devices).
* **`EXEC`**: `run` executes commands on remote nodes, and `notify` triggers system notifications (side effects).



### `image`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** This tool analyzes a visual file to extract semantic information. It is a perception action categorized under **`READ`** (pulling information from a file).

### `message`

* **Category:** **`ACTIVE ENV`** → **`EXEC`** / **`RESPOND`**
* **Explanation:**
* **`EXEC`**: Sending messages to external platforms (Slack, Discord) via API is a functional side effect.
* **`RESPOND`**: If the message is intended as the final answer to a user request within a chat flow, it functions as **`RESPOND`**.
* *Note:* Actions like `pin`, `kick`, or `ban` are strictly **`EXEC`**.



### `cron`

* **Category:** **`PASSIVE ENV`** → **`SUBSCRIBE`**
* **Explanation:** The `add` action in cron is exactly **`SUBSCRIBE`** (Register Listener). The agent is registering a listener for a specific time-based event. When the time comes, the system triggers a **`RECEIVE`** event (via `wake`) to the agent.

### `gateway`

* **Category:** **`ACTIVE ENV`** → **`EXEC`**
* **Explanation:** Tools like `restart`, `config.apply`, or `update.run` modify the agent's runtime environment itself. This is a high-impact **`EXEC`** action (modifying the infrastructure).

### `sessions_spawn`

* **Category:** **`ACTIVE ENV`** → **`HANDOFF`**
* **Explanation:** This is the primary mechanism for **Agent Collaboration**. It delegates a task to a new sub-agent process, perfectly matching the **`HANDOFF`** definition.

### `sessions_send`

* **Category:** **`ACTIVE ENV`** → **`WRITE`** (Inter-Agent)
* **Explanation:** This is the communication channel for collaboration. It involves writing data to another agent's context. In the atomic framework, this supports the **`HANDOFF`** workflow.

### `sessions_list` / `sessions_history` / `session_status`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** These tools allow the agent to inspect the state of its peers or sub-agents (Service Discovery and Observability). It acts as **`READ`** (pulling info about the multi-agent environment).

### `agents_list`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** Similar to `sessions_list`, this retrieves available agent profiles (capabilities) from the registry, enabling the agent to decide who to **`HANDOFF`** to.

## Claude Code

Definitions of tools provided by Claude Code: <https://code.claude.com/docs/en/settings#tools-available-to-claude>

### `AskUserQuestion`

* **Category:** **`ACTIVE ENV`** → **`ASK`**
* **Explanation:** This tool explicitly requests input from the human user to resolve ambiguity. It maps directly to your **`ASK`** action (Human-in-the-Loop).

### `Bash`

* **Category:** **`ACTIVE ENV`** → **`EXEC`**
* **Explanation:** Executes shell commands that can have arbitrary side effects (installing dependencies, running servers, moving files). This is the definition of **`EXEC`**.

### `TaskOutput`

* **Category:** **`ACTIVE ENV`** → **`READ`** / **`WAIT`**
* **Explanation:** This tool retrieves the result of a background process. In your atomic model, this represents the **`READ`** phase that follows a **`WAIT`** action (polling for the completion of an asynchronous `EXEC`).

### `Edit`

* **Category:** **`ACTIVE ENV`** → **`WRITE`**
* **Explanation:** Modifies the content of existing files. It changes the state of the environment (the codebase) but is distinct from `EXEC` as it doesn't run code.

### `ExitPlanMode`

* **Category:** **`ACTIVE ENV`** → **`RESPOND`** / **`ASK`**
* **Explanation:** This tool signals a state transition in the conversation flow, effectively "responding" to the system that the planning phase is over and coding should begin.

### `Glob`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** A file system search tool. It pulls information about file existence and structure based on patterns.

### `Grep`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** A content search tool. It actively pulls specific information from the environment (file contents) based on query patterns.

### `KillShell`

* **Category:** **`ACTIVE ENV`** → **`EXEC`**
* **Explanation:** A functional side effect that terminates a running process. This is a control action on the environment.

### `MCPSearch`

* **Category:** **`ACTIVE ENV`** → **`READ`** (Discovery) / **`EXEC`** (Loading)
* **Explanation:**
* **`READ`**: Searches for available external capabilities (Model Context Protocol).
* **`EXEC`**: Dynamically loads a new tool into the context, modifying the agent's capabilities.



### `NotebookEdit`

* **Category:** **`ACTIVE ENV`** → **`WRITE`**
* **Explanation:** Similar to `Edit`, but specialized for Jupyter notebook cells. It modifies the static state of the file system.

### `Read`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** The fundamental action of pulling file content into the agent's context.

### `Skill`

* **Category:** **`ACTIVE ENV`** → **`EXEC`/`READ`**
* **Explanation:** Executes a pre-defined macro or script. It is an **`EXEC`** action that bundles multiple smaller actions. Could be reading a markdown text or running a script.

### `Task`

* **Category:** **`ACTIVE ENV`** → **`HANDOFF`**
* **Explanation:** "Runs a sub-agent." This is a perfect mapping to your **`HANDOFF`** action (Agent Collaboration), delegating a complex objective to another entity.

### `TaskCreate` / `TaskUpdate`

* **Category:** **`COGNITIVE`** → **`PLAN`** (Externalized)
* **Explanation:** In your architecture, **`PLAN`** is an internal cognitive process. Claude Code reifies this into explicit tools. The agent uses `TaskCreate` to "write down" its plan into the system's memory.
* *Alternative View:* It could be seen as **`WRITE`** (Internal State), where the environment includes the task management system.

### `TaskGet` / `TaskList`

* **Category:** **`COGNITIVE`** → **`RETRIEVE`** / **`READ`**
* **Explanation:** The agent is recalling its own plan.
* **`RETRIEVE`**: If the task list is considered internal memory.
* **`READ`**: If the task list is considered an external file/system the agent must query.



### `WebFetch`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** Pulling raw content from a URL.

### `WebSearch`

* **Category:** **`ACTIVE ENV`** → **`READ`**
* **Explanation:** Pulling information via a search engine query.

### `Write`

* **Category:** **`ACTIVE ENV`** → **`WRITE`**
* **Explanation:** Creates new files or overwrites them entirely. It is a state mutation of the file system.

### `LSP` (Language Server Protocol)

* **Category:** **`ACTIVE ENV`** → **`READ`** (Deep Analysis)
* **Explanation:** This tool provides "code intelligence" (definitions, references, errors). It is a highly specialized **`READ`** action that retrieves semantic information about the code, rather than just raw text.

Note: Besides the above tools, there are also hidden `SUBSCRIBE` and `RECEIVE` actions in the background for Claude code. For example, all user's edits to the code are pushed to the agent as `RECEIVE` events, and the agent can `SUBSCRIBE` (? not sure for that. The subscribe may written as code, so agent cannot actively subscribe...)  to file change events to trigger internal updates or re-planning. There are blogs explaining it or just trace it yourself...