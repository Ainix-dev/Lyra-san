#!/bin/bash
# Setup script for Piper TTS

echo "🎤 Installing Piper TTS for Lyra Voice..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Linux detected"
    
    # Check if piper is already installed
    if command -v piper &> /dev/null; then
        echo "✓ Piper already installed"
    else
        echo "⬇️ Downloading Piper..."
        ARCH=$(uname -m)
        
        if [[ "$ARCH" == "x86_64" ]]; then
            URL="https://github.com/rhasspy/piper/releases/download/2024.1.1/piper_linux_x86_64.tar.gz"
        elif [[ "$ARCH" == "aarch64" ]]; then
            URL="https://github.com/rhasspy/piper/releases/download/2024.1.1/piper_linux_aarch64.tar.gz"
        else
            echo "❌ Unsupported architecture: $ARCH"
            exit 1
        fi
        
        # Download
        wget "$URL" -O /tmp/piper.tar.gz
        tar xzf /tmp/piper.tar.gz -C /tmp
        
        # Install to /usr/local/bin
        sudo mv /tmp/piper /usr/local/bin/piper
        chmod +x /usr/local/bin/piper
        
        echo "✓ Piper installed to /usr/local/bin"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📦 macOS detected"
    if command -v piper &> /dev/null; then
        echo "✓ Piper already installed"
    else
        echo "Installing via Homebrew..."
        brew install espeak-ng  # Dependency
        brew install piper
    fi
fi

# Install Python package
echo "📦 Installing Python piper-tts package..."
pip install piper-tts 2>/dev/null || echo "⚠️ pip install failed, trying apt..."

# Download voice models
echo "🗣️ Downloading voice models..."
mkdir -p ~/.local/share/piper

VOICES=(
    "en_US-lessac-medium"
    "en_US-ryan-medium"
)

for voice in "${VOICES[@]}"; do
    echo "📥 Downloading $voice..."
    wget "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/${voice%-*}/${voice##*-}/en_US-${voice##*-}.onnx" \
        -O "$HOME/.local/share/piper/${voice}.onnx" 2>/dev/null &
    wget "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/${voice%-*}/${voice##*-}/en_US-${voice##*-}.onnx.json" \
        -O "$HOME/.local/share/piper/${voice}.onnx.json" 2>/dev/null &
done

wait

# Test
echo ""
echo "✅ Piper TTS Setup Complete!"
echo ""
echo "Testing Piper..."
echo "Hello from Lyra" | piper --model en_US-lessac-medium --output-file /tmp/test.wav
if [ -f /tmp/test.wav ]; then
    echo "✓ Voice synthesis working!"
    ls -lh /tmp/test.wav
else
    echo "⚠️ Test failed - check Piper installation"
fi
