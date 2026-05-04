const micBtn = document.getElementById("mic-btn");
const chatWindow = document.getElementById("chat-window");
const textInput = document.getElementById("text-input");
const sendBtn = document.getElementById("send-btn");
const modeToggleBtn = document.getElementById("mode-toggle-btn");
const textInputMode = document.getElementById("text-input-mode");
const micInputMode = document.getElementById("mic-input-mode");

// Add status indicator
let isRecording = false;
let mediaRecorder = null;
let audioChunks = [];
let currentMode = "typing"; // "typing" or "mic"

// Show initial message
function showWelcomeMessage() {
    const welcomeMsg = document.createElement("div");
    welcomeMsg.className = "message bot";
    
    // Check if using IP address instead of localhost
    const isLocalhost = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    let welcomeText = "👋 Welcome! Type your message or click the microphone button to start chatting. Use the toggle button to switch between typing and mic modes.";
    
    if (!isLocalhost && !isSecureContext()) {
        welcomeText += "\n\n💡 Tip: For microphone access, try accessing via http://localhost:5000";
    }
    
    welcomeMsg.textContent = welcomeText;
    chatWindow.appendChild(welcomeMsg);
}

// Show error message
function showError(message) {
    const errorMsg = document.createElement("div");
    errorMsg.className = "message error";
    errorMsg.textContent = `❌ Error: ${message}`;
    chatWindow.appendChild(errorMsg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Show loading message
function showLoading() {
    const loadingMsg = document.createElement("div");
    loadingMsg.className = "message loading";
    loadingMsg.id = "loading-msg";
    loadingMsg.textContent = "⏳ Processing your audio...";
    chatWindow.appendChild(loadingMsg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Remove loading message
function removeLoading() {
    const loadingMsg = document.getElementById("loading-msg");
    if (loadingMsg) {
        loadingMsg.remove();
    }
}

// Add message to chat
function addMessage(text, className) {
    const msg = document.createElement("div");
    msg.className = `message ${className}`;
    msg.textContent = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Check if getUserMedia is available
function checkMicrophoneSupport() {
    // Check for modern API
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        return true;
    }
    // Check for legacy API
    if (navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia) {
        return true;
    }
    return false;
}

// Check if page is served over secure context (HTTPS or localhost)
function isSecureContext() {
    return window.isSecureContext || location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1';
}

micBtn.addEventListener("click", async () => {
    // Prevent multiple clicks
    if (isRecording) {
        return;
    }

    // Check if microphone API is available
    if (!checkMicrophoneSupport()) {
        showError("Microphone API is not supported in this browser. Please use a modern browser like Chrome, Firefox, or Edge.");
        return;
    }

    // Check if we're in a secure context
    if (!isSecureContext()) {
        showError("Microphone access requires a secure connection (HTTPS). Please access the app via: https://localhost:5000 or use localhost instead of your IP address.");
        // Suggest using localhost
        addMessage("💡 Tip: Try accessing the app at http://localhost:5000 instead of using your IP address.", "bot");
        return;
    }

    try {
        isRecording = true;
        micBtn.textContent = "🔴";
        micBtn.disabled = true;
        micBtn.style.opacity = "0.6";

        // Request microphone access with proper error handling
        let stream;
        try {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                // Modern API
                stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            } else {
                // Legacy API fallback (for older browsers)
                stream = await new Promise((resolve, reject) => {
                    const getUserMedia = navigator.getUserMedia || 
                                       navigator.webkitGetUserMedia || 
                                       navigator.mozGetUserMedia || 
                                       navigator.msGetUserMedia;
                    if (getUserMedia) {
                        getUserMedia.call(navigator, { audio: true }, resolve, reject);
                    } else {
                        reject(new Error("getUserMedia not supported"));
                    }
                });
            }
        } catch (mediaError) {
            throw new Error(`Microphone access error: ${mediaError.message || mediaError.name || 'Unknown error'}`);
        }
        
        // Use MediaRecorder API (more reliable than ScriptProcessor)
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = async () => {
            // Stop all tracks
            stream.getTracks().forEach(track => track.stop());
            
            // Create blob from recorded chunks
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            
            // Convert to WAV format
            const wavBlob = await convertToWAV(audioBlob);
            
            // Show loading message
            showLoading();
            
            // Send to Flask
            const formData = new FormData();
            formData.append("audio_file", wavBlob, "user_audio.wav");

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();
                removeLoading();

                if (data.error) {
                    showError(data.error);
                    if (data.user_text) {
                        addMessage(`You said: ${data.user_text}`, "user");
                    }
                    if (data.bot_response) {
                        addMessage(data.bot_response, "bot");
                    }
                } else {
                    // Show user message
                    if (data.user_text && data.user_text.trim()) {
                        addMessage(`You: ${data.user_text}`, "user");
                    } else {
                        addMessage("You: [Audio recorded]", "user");
                    }

                    // Show bot response
                    if (data.bot_response && data.bot_response.trim()) {
                        addMessage(`Bot: ${data.bot_response}`, "bot");
                    }

                    // Play audio response
                    if (data.audio_file) {
                        const audio = new Audio(data.audio_file);
                        audio.play().catch(e => {
                            console.log("Could not play audio:", e);
                        });
                    }
                }
            } catch (error) {
                removeLoading();
                showError(`Failed to communicate with server: ${error.message}`);
                console.error("Fetch error:", error);
            }

            // Reset button
            micBtn.textContent = "🎤";
            micBtn.disabled = false;
            micBtn.style.opacity = "1";
            isRecording = false;
        };

        // Start recording
        mediaRecorder.start();
        
        // Stop recording after 5 seconds
        setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                mediaRecorder.stop();
            }
        }, 5000);

    } catch (error) {
        isRecording = false;
        micBtn.textContent = "🎤";
        micBtn.disabled = false;
        micBtn.style.opacity = "1";
        
        // Provide more helpful error messages
        let errorMsg = error.message || "Unknown error";
        if (errorMsg.includes("Permission denied") || errorMsg.includes("NotAllowedError")) {
            showError("❌ Microphone permission denied. Please allow microphone access in your browser settings and try again.");
        } else if (errorMsg.includes("NotFoundError") || errorMsg.includes("no microphone")) {
            showError("❌ No microphone found. Please connect a microphone and try again.");
        } else if (errorMsg.includes("NotReadableError") || errorMsg.includes("device unavailable")) {
            showError("❌ Microphone is being used by another application. Please close other apps using the microphone and try again.");
        } else {
            showError(`❌ Microphone error: ${errorMsg}`);
        }
        console.error("Microphone error:", error);
    }
});

// Convert WebM/Opus to WAV using Web Audio API
async function convertToWAV(audioBlob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = async (e) => {
            try {
                const audioContext = new AudioContext();
                const audioBuffer = await audioContext.decodeAudioData(e.target.result);
                
                // Convert to mono and 16kHz
                const sampleRate = 16000;
                const numberOfChannels = 1;
                const length = audioBuffer.length * sampleRate / audioBuffer.sampleRate;
                const newBuffer = audioContext.createBuffer(numberOfChannels, length, sampleRate);
                
                // Resample and convert to mono
                const sourceData = audioBuffer.getChannelData(0);
                const targetData = newBuffer.getChannelData(0);
                const ratio = audioBuffer.sampleRate / sampleRate;
                
                for (let i = 0; i < length; i++) {
                    const index = Math.floor(i * ratio);
                    targetData[i] = sourceData[index];
                }
                
                // Convert to WAV
                const wavBuffer = encodeWAV(targetData, sampleRate);
                const wavBlob = new Blob([wavBuffer], { type: "audio/wav" });
                resolve(wavBlob);
            } catch (error) {
                reject(error);
            }
        };
        reader.onerror = reject;
        reader.readAsArrayBuffer(audioBlob);
    });
}

// WAV encoder
function encodeWAV(samples, sampleRate) {
    const buffer = new ArrayBuffer(44 + samples.length * 2);
    const view = new DataView(buffer);

    function writeString(view, offset, string) {
        for (let i = 0; i < string.length; i++) {
            view.setUint8(offset + i, string.charCodeAt(i));
        }
    }

    let offset = 0;

    writeString(view, offset, "RIFF"); offset += 4;
    view.setUint32(offset, 36 + samples.length * 2, true); offset += 4;
    writeString(view, offset, "WAVE"); offset += 4;
    writeString(view, offset, "fmt "); offset += 4;
    view.setUint32(offset, 16, true); offset += 4;
    view.setUint16(offset, 1, true); offset += 2; // PCM
    view.setUint16(offset, 1, true); offset += 2; // mono
    view.setUint32(offset, sampleRate, true); offset += 4;
    view.setUint32(offset, sampleRate * 2, true); offset += 4;
    view.setUint16(offset, 2, true); offset += 2; // block align
    view.setUint16(offset, 16, true); offset += 2; // bits per sample
    writeString(view, offset, "data"); offset += 4;
    view.setUint32(offset, samples.length * 2, true); offset += 4;

    // Convert float32 to int16
    let pos = 44;
    for (let i = 0; i < samples.length; i++, pos += 2) {
        let s = Math.max(-1, Math.min(1, samples[i]));
        view.setInt16(pos, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return view;
}

// Function to send text message
async function sendTextMessage() {
    const text = textInput.value.trim();
    if (!text) {
        return;
    }
    
    // Disable input while processing
    textInput.disabled = true;
    sendBtn.disabled = true;
    
    // Clear input
    const userText = text;
    textInput.value = "";
    
    // Show user message
    addMessage(`You: ${userText}`, "user");
    
    // Show loading message
    showLoading();
    
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: userText })
        });
        
        const data = await response.json();
        removeLoading();
        
        if (data.error) {
            showError(data.error);
            if (data.bot_response) {
                addMessage(data.bot_response, "bot");
            }
        } else {
            // Show bot response
            if (data.bot_response && data.bot_response.trim()) {
                addMessage(`Bot: ${data.bot_response}`, "bot");
            }
            
            // Play audio response
            if (data.audio_file) {
                const audio = new Audio(data.audio_file);
                audio.play().catch(e => {
                    console.log("Could not play audio:", e);
                });
            }
        }
    } catch (error) {
        removeLoading();
        showError(`Failed to communicate with server: ${error.message}`);
        console.error("Fetch error:", error);
    } finally {
        // Re-enable input
        textInput.disabled = false;
        sendBtn.disabled = false;
        textInput.focus();
    }
}

// Handle send button click
sendBtn.addEventListener("click", sendTextMessage);

// Handle Enter key in text input
textInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendTextMessage();
    }
});

// Mode toggle functionality
modeToggleBtn.addEventListener("click", () => {
    if (currentMode === "typing") {
        // Switch to mic mode
        currentMode = "mic";
        textInputMode.style.display = "none";
        micInputMode.style.display = "flex";
        modeToggleBtn.textContent = "⌨️";
        modeToggleBtn.title = "Switch to typing mode";
    } else {
        // Switch to typing mode
        currentMode = "typing";
        textInputMode.style.display = "flex";
        micInputMode.style.display = "none";
        modeToggleBtn.textContent = "🎤";
        modeToggleBtn.title = "Switch to mic mode";
        textInput.focus();
    }
});

// Check microphone support on page load
function checkMicSupportOnLoad() {
    if (!checkMicrophoneSupport()) {
        addMessage("⚠️ Warning: Microphone API is not supported in this browser. Please use Chrome, Firefox, or Edge for voice input.", "error");
    } else if (!isSecureContext()) {
        addMessage("⚠️ Warning: Microphone requires a secure connection. For best results, access via http://localhost:5000 or use HTTPS.", "error");
    }
}

// Show welcome message on load
showWelcomeMessage();

// Check microphone support after welcome message
checkMicSupportOnLoad();
