# ArbiterOS-Beta

LLM Gateway-based ArbiterOS, integrating LiteLLM proxy and MLflow for comprehensive LLM monitoring and management.

## Getting Started

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Python package manager)

### Installation

1. **Install dependencies**
   ```bash
   uv sync --all-extras
   ```

2. **Set up pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```

### Running the Services

Start both services in separate terminals:

**Terminal 1 - MLflow Server:**
```bash
uv run poe mlflow
```

**Terminal 2 - LiteLLM Proxy:**
```bash
uv run poe litellm
```

Once running, you can access:
- **MLflow Server**: <http://localhost:5000> - Experiment tracking and model registry
- **LiteLLM Proxy**: <http://localhost:4000> - LLM gateway for request/response handling

## LiteLLM Configuration

### Modify and Reject Incoming Requests

Implement custom request/response hooks to control incoming and outgoing data:

<https://docs.litellm.ai/docs/proxy/call_hooks>

### Tracing and Monitoring

Configure logging and tracing to monitor all LLM API calls:

<https://docs.litellm.ai/docs/proxy/logging>