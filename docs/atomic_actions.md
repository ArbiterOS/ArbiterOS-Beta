# Atomic Agent Actions

For agents, a stream of tokens flows into a sequence of atomic actions...

## System Roles & Definitions
We define two primary roles within the interaction loop:

- **Agent**: An LLM entity equipped with tools and external memory, capable of performing various cognitive and functional actions.
- **Environment**: The external context that the agent interacts with. It encompasses any entity outside the agent's internal state:
    - **Digital/Physical World**: The execution boundaries (e.g., File System, Web, API, Shell).
    - **Human**: The user providing prompts and evaluating results.
    - **Peer Agents**: Other agents in the system available for collaboration or delegation.

## Types of Atomic Actions

### 1. COGNITIVE (LLM itself, without tools)
**Internal State: Logic, Decision Making, and Memory**

* **Reasoning & Decision***
    * `REASON`: **Internal Reasoning.** Generating Chain-of-Thought (CoT), logical deduction, and hypothesis generation.
    * `PLAN`: **Task Decomposition.** Breaking down high-level goals into executable sub-tasks and ordering them.
    * `CRITIQUE`: **Self-Correction.** Analyzing past actions or errors to adjust future strategies (e.g., analyzing a stack trace).
    * *: This can be related to agent's paradiam. For ReAct agents, only `REASON` is present. For Plan-and-execute agents, `PLAN` is added. For Reflexion agents, `CRITIQUE` is added...

* **Memory Management**
    * `STORE`: **Persist Experience.** Saving successful patterns, code snippets, or user preferences to long-term storage.
    * `RETRIEVE`: **Recall Context.** Fetching relevant history or knowledge (RAG) based on the current query.
    * `COMPRESS*`: **Summarization.** Condensing the context window to retain essential facts while discarding noise (Semantic Compression).
    * `PRUNE*`: **Context Pruning.** Selectively discarding specific parts of the context (e.g., sliding window, removing irrelevant history) to free up space.

### 2. ACTIVE ENV (agent as an actor)
**Interaction: Proactive Manipulation of the Environment**

* **Env Interaction**
    * `READ`: **Pull Information.** Actively pulling data from the environment. (e.g., read from file, website or email for coding agent. Observation for emboded AI.)
    * `WRITE`: **Change State.** Modifying the environment without side effects beyond storage (e.g., save to file).
    * `EXEC`: **Trigger Action.** Executing commands with side effects (e.g., `run build`, `send email`, `deploy`).
    * `WAIT`: **No Operation.** Choosing to do nothing when waiting for more information (e.g., `wait last exec is finished`).
* **Human Interaction**
    * `ASK*`: **Human-in-the-Loop.** Requesting user confirmation before executing critical actions (e.g., `Do you agree with current coding plan?`).
    * `RESPOND`: **Final Output.** Providing the final answer or result to the user after processing (e.g., `Here is the solution to your coding problem.`).
* **Agent Collaboration**
    * `HANDOFF*`: **Inter-Agent Delegation.** Delegating to another specialized agent.

### 3. PASSIVE ENV (environment as an actor)
**Perception: Reactive Handling of Environmental Events**

* **Perception**
    * `SUBSCRIBE*`: **Register Listener.** Establishing a channel to watch for specific environmental changes (e.g., watch file modifications for a coding agent, keep scanning from radar for an embodied AI).
    * `RECEIVE`: **Push Event.** Passively accepting data pushed by the environment (e.g., `onFileChange`, `onRadarSignal`) This is usually implemented as a user message.
* **Human Interaction**
    * `USER_MESSAGE*`: **User Prompting.** New user input interrupting the agent's current process, requiring immediate attention (e.g., a new question while the agent is still thinking).

## Properties of Atomic Actions

* `TRUSTWORTHINESS`: **External Reliability.** Rating if the source of information is trusted. Used for prompt injection defense.
* `CONFIDENCE`: **Internal Certainty.** Rating the agent's own confidence in a plan or memory. （NOTE: we need to think about LLM's calibration issue here...）
* `CONFIDENTIAL`: **Sensitive Information.** Marking data that should not be stored or shared (e.g., API keys, personal data).
* `REVERSIBLE`: **Undo Capability.** Indicating actions that can be undone if necessary (e.g., `write to temp file` vs `deploy to production`).
* `AUTHORITY`: **Permission Level.** Whether the action is approved by human or external policies.

[^1]: *: Atomic actions marked with an asterisk means they are more likely to be implemented in code instead of as a tool available to the agent (but still possible). Thus may be hard to be captured by our endpoint gateway design...
