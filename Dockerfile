FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV SDL_AUDIODRIVER=dummy
ENV SDL_VIDEODRIVER=x11
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# Create a non-root user
RUN useradd -m -s /bin/bash gameuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    xvfb \
    x11-utils \
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Create X11 directory with correct permissions
RUN mkdir -p /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix && \
    chown root:root /tmp/.X11-unix

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Set ownership
RUN chown -R gameuser:gameuser /app

# Create a more robust startup script with cleanup, error handling, and debugging
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
cleanup() {\n\
    echo "Cleaning up..."\n\
    if [ ! -z "$XVFB_PID" ]; then\n\
        kill $XVFB_PID || true\n\
    fi\n\
    rm -f /tmp/.X99-lock\n\
}\n\
\n\
trap cleanup EXIT\n\
\n\
# Cleanup any existing lock files\n\
rm -f /tmp/.X99-lock\n\
\n\
echo "Starting Xvfb..."\n\
Xvfb :99 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &\n\
XVFB_PID=$!\n\
\n\
# Wait for X server to start\n\
for i in $(seq 1 10); do\n\
    if xdpyinfo -display :99 >/dev/null 2>&1; then\n\
        echo "X server started successfully"\n\
        break\n\
    fi\n\
    if [ $i -eq 10 ]; then\n\
        echo "Failed to start X server"\n\
        exit 1\n\
    fi\n\
    echo "Waiting for X server... ($i/10)"\n\
    sleep 1\n\
done\n\
\n\
echo "DISPLAY=$DISPLAY"\n\
echo "Starting game with debug output..."\n\
cd /app/src && PYTHONPATH=/app python -u main.py\n' > /app/start.sh && \
    chmod +x /app/start.sh && \
    chown gameuser:gameuser /app/start.sh

# Switch to non-root user
USER gameuser

# Set the working directory
WORKDIR /app/src

CMD ["/app/start.sh"]
