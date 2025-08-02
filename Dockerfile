FROM python:3.12-slim

WORKDIR /app

# Install CrewAI and tools extras with upgrade
RUN pip install --no-cache-dir --upgrade crewai crewai[tools]

# Install OpenCode.ai (global in container)
RUN curl -fsSL https://opencode.ai/install | bash

# Copy project files (we'll mount volumes for dynamic use)
COPY . .

# Default command: Keep the container running or run your script
CMD ["tail", "-f", "/dev/null"]