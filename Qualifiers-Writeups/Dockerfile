# Dockerfile for LsCTF Finals Environment
FROM python:3.11-slim

# Metadata
LABEL maintainer="famed_maxximus"
LABEL description="LsCTF Finals Environment - Team: We Thought This Was World War III"

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make cmake \
    git curl wget unzip \
    wireshark-bin tshark \
    binwalk \
    radare2 \
    openjdk-17-jre-headless \
    strace ltrace \
    netcat-openbsd \
    socat \
    tcpdump \
    iproute2 \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Install Ghidra (headless)
ARG GHIDRA_VERSION=11.1.2
RUN cd /opt && \
    wget -q "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_${GHIDRA_VERSION}_build/ghidra_${GHIDRA_VERSION}_PUBLIC_20240129.zip" && \
    unzip -q "ghidra_${GHIDRA_VERSION}_PUBLIC_20240129.zip" && \
    rm "ghidra_${GHIDRA_VERSION}_PUBLIC_20240129.zip" && \
    ln -s /opt/ghidra_${GHIDRA_VERSION}_PUBLIC/ghidraRun /usr/local/bin/ghidra

# Python dependencies
COPY scripts/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# CTF-specific tools
RUN pip install --no-cache-dir \
    pwntools==4.10.0 \
    z3-solver==4.13.0.0 \
    pycryptodome==3.20.0 \
    cryptography==43.0.0 \
    fpylll==0.5.10 \
    gmpy2==2.1.5 \
    sympy==1.13.1 \
    numpy==1.26.4 \
    scipy==1.13.0 \
    pandas==2.2.1 \
    aiohttp==3.9.3 \
    requests==2.31.0 \
    rich==13.7.1 \
    textual==0.52.1 \
    capstone==5.0.1 \
    keystone-engine==0.9.2 \
    unicorn==2.0.1.post1 \
    pefile==2023.11.28 \
    python-magic==0.4.27 \
    pyyaml==6.0.1 \
    tqdm==4.66.4 \
    python-dotenv==1.0.1 \
    mkdocs==1.5.3 \
    mkdocs-material==9.5.3 \
    mkdocs-mermaid2-plugin==1.1.0 \
    pymdown-extensions==10.7

# Workspace
WORKDIR /ctf
COPY . .

# Create useful aliases
RUN echo 'alias ll="ls -la"' >> /root/.bashrc && \
    echo 'alias ctf="cd /ctf"' >> /root/.bashrc && \
    echo 'export PATH="/opt/ghidra_11.1.2_PUBLIC:$PATH"' >> /root/.bashrc

# Default command
CMD ["bash"]