
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Codeex AI Chat - Professional Ollama Interface</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #1e3a8a;
            --secondary: #3b82f6;
            --accent: #60a5fa;
            --dark: #0f172a;
            --darker: #020617;
            --light: #f8fafc;
            --success: #059669;
            --gradient: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #60a5fa 100%);
        }

        body {
            font-family: 'Inter', sans-serif;
            background: var(--darker);
            color: var(--light);
            overflow-x: hidden;
            line-height: 1.6;
        }

        /* Animated Background */
        .bg-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(45deg, #0f172a, #1e293b, #334155);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }

        .stars {
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .star {
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            animation: twinkle 3s infinite;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes twinkle {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* Header */
        header {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(10px);
            padding: 1.5rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
        }

        nav {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }

        .logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 2rem;
            font-weight: 900;
            background: var(--gradient);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(59, 130, 246, 0.5);
            animation: pulse 2s infinite;
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }

        .nav-links a {
            color: var(--light);
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s;
            position: relative;
        }

        .nav-links a:hover {
            color: var(--accent);
        }

        .nav-links a::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--gradient);
            transition: width 0.3s;
        }

        .nav-links a:hover::after {
            width: 100%;
        }

        /* Hero Section */
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 8rem 2rem 4rem;
            position: relative;
        }

        .hero-content {
            max-width: 1200px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }

        .hero-text {
            animation: slideInRight 1s ease-out;
        }

        .hero h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            background: var(--gradient);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1.2;
        }

        .hero h2 {
            font-size: 1.8rem;
            color: var(--accent);
            margin-bottom: 1.5rem;
            font-weight: 600;
        }

        .hero p {
            font-size: 1.2rem;
            color: #94a3b8;
            margin-bottom: 2rem;
        }

        .cta-buttons {
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
        }

        .btn {
            padding: 1rem 2.5rem;
            border-radius: 50px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.1rem;
            border: none;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .btn-primary {
            background: var(--gradient);
            color: white;
            box-shadow: 0 10px 40px rgba(59, 130, 246, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(59, 130, 246, 0.6);
        }

        .btn-secondary {
            background: rgba(59, 130, 246, 0.1);
            border: 2px solid var(--secondary);
            color: var(--accent);
        }

        .btn-secondary:hover {
            background: rgba(59, 130, 246, 0.2);
            transform: translateY(-3px);
        }

        /* 3D Card */
        .hero-visual {
            perspective: 1000px;
            animation: slideInUp 1s ease-out;
        }

        .demo-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            border: 1px solid rgba(59, 130, 246, 0.3);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            transform-style: preserve-3d;
            animation: float 3s ease-in-out infinite;
        }

        .demo-card img {
            width: 100%;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }

        /* Features Section */
        .features {
            padding: 6rem 2rem;
            background: rgba(15, 23, 42, 0.5);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .section-title {
            text-align: center;
            margin-bottom: 4rem;
        }

        .section-title h2 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3rem;
            background: var(--gradient);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .section-title p {
            font-size: 1.2rem;
            color: #94a3b8;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }

        .feature-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 15px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: all 0.3s;
            cursor: pointer;
        }

        .feature-card:hover {
            transform: translateY(-10px);
            border-color: var(--accent);
            box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
        }

        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            display: block;
        }

        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
        }

        .feature-card p {
            color: #94a3b8;
            line-height: 1.8;
        }

        .feature-list {
            list-style: none;
            margin-top: 1rem;
        }

        .feature-list li {
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: #cbd5e1;
        }

        .feature-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--success);
            font-weight: bold;
        }

        /* Installation Section */
        .installation {
            padding: 6rem 2rem;
            background: rgba(30, 41, 59, 0.3);
        }

        .steps-grid {
            display: grid;
            gap: 2rem;
            margin-top: 3rem;
        }

        .step {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            border-left: 4px solid var(--secondary);
            transition: all 0.3s;
        }

        .step:hover {
            border-left-color: var(--accent);
            transform: translateX(10px);
        }

        .step-number {
            display: inline-block;
            width: 40px;
            height: 40px;
            background: var(--gradient);
            border-radius: 50%;
            text-align: center;
            line-height: 40px;
            font-weight: 900;
            margin-bottom: 1rem;
            font-family: 'Orbitron', sans-serif;
        }

        .step h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
        }

        .code-block {
            background: rgba(0, 0, 0, 0.5);
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
            border: 1px solid rgba(59, 130, 246, 0.3);
            position: relative;
            overflow-x: auto;
        }

        .code-block code {
            color: #10b981;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
        }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: var(--secondary);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.3s;
        }

        .copy-btn:hover {
            background: var(--accent);
        }

        /* System Requirements */
        .requirements {
            padding: 6rem 2rem;
            background: rgba(15, 23, 42, 0.5);
        }

        .req-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .req-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: all 0.3s;
        }

        .req-card:hover {
            transform: scale(1.05);
            border-color: var(--accent);
        }

        .req-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .req-card h4 {
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: var(--accent);
        }

        .req-card p {
            color: #94a3b8;
        }

        /* Contact Section */
        .contact {
            padding: 6rem 2rem;
            background: rgba(30, 41, 59, 0.3);
        }

        .contact-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .contact-card {
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(10px);
            padding: 2.5rem;
            border-radius: 15px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            text-align: center;
            transition: all 0.3s;
        }

        .contact-card:hover {
            transform: translateY(-10px);
            border-color: var(--accent);
            box-shadow: 0 20px 60px rgba(59, 130, 246, 0.3);
        }

        .contact-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }

        .contact-card h3 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--accent);
        }

        .contact-card a {
            color: var(--light);
            text-decoration: none;
            transition: color 0.3s;
        }

        .contact-card a:hover {
            color: var(--accent);
        }

        /* Footer */
        footer {
            background: rgba(2, 6, 23, 0.8);
            backdrop-filter: blur(10px);
            padding: 3rem 2rem 1.5rem;
            border-top: 1px solid rgba(59, 130, 246, 0.3);
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }

        .footer-logo {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.5rem;
            background: var(--gradient);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .footer-links {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }

        .footer-links a {
            color: var(--light);
            text-decoration: none;
            transition: color 0.3s;
        }

        .footer-links a:hover {
            color: var(--accent);
        }

        .copyright {
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid rgba(59, 130, 246, 0.2);
            color: #64748b;
        }

        .made-by {
            margin-top: 1rem;
            font-size: 1.1rem;
            color: var(--accent);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero-content {
                grid-template-columns: 1fr;
            }

            .hero h1 {
                font-size: 2.5rem;
            }

            .nav-links {
                display: none;
            }

            .cta-buttons {
                flex-direction: column;
            }

            .section-title h2 {
                font-size: 2rem;
            }
        }

        /* Scroll animations */
        .fade-in {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.6s ease-out;
        }

        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }

        /* Floating particles */
        .particle {
            position: fixed;
            width: 4px;
            height: 4px;
            background: var(--accent);
            border-radius: 50%;
            pointer-events: none;
            opacity: 0.5;
            animation: rise 10s linear infinite;
        }

        @keyframes rise {
            0% {
                transform: translateY(0) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 0.5;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <!-- Animated Background -->
    <div class="bg-animation"></div>
    <div class="stars" id="stars"></div>

    <!-- Header -->
    <header>
        <nav>
            <div class="logo">⚡ CODEEX</div>
            <ul class="nav-links">
                <li><a href="#features">Features</a></li>
                <li><a href="#installation">Installation</a></li>
                <li><a href="#requirements">Requirements</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="hero-content">
            <div class="hero-text">
                <h1>CODEEX AI CHAT</h1>
                <h2>Professional Ollama Interface</h2>
                <p>Experience the next generation of AI chat with advanced features, beautiful UI, and seamless model management. Built with ❤️ for developers and AI enthusiasts.</p>
                <div class="cta-buttons">
                    <a href="https://github.com/heoster/codeex-v5" class="btn btn-primary" target="_blank">
                        ⭐ Star on GitHub
                    </a>
                    <a href="#installation" class="btn btn-secondary">
                        📥 Get Started
                    </a>
                </div>
            </div>
            <div class="hero-visual">
                <div class="demo-card">
                    <h3 style="color: var(--accent); margin-bottom: 1rem;">🤖 AI-Powered Chat</h3>
                    <div style="background: rgba(0,0,0,0.3); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">
                        <p style="color: #60a5fa; margin-bottom: 0.5rem;">👤 You:</p>
                        <p style="color: #cbd5e1;">What can you do?</p>
                    </div>
                    <div style="background: rgba(5, 150, 105, 0.1); padding: 1.5rem; border-radius: 10px;">
                        <p style="color: #34d399; margin-bottom: 0.5rem;">🤖 Codeex AI:</p>
                        <p style="color: #cbd5e1;">I can help you with coding, answer questions, and much more! ✨</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features fade-in" id="features">
        <div class="container">
            <div class="section-title">
                <h2>🚀 Powerful Features</h2>
                <p>Everything you need for professional AI conversations</p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">⚡</span>
                    <h3>Auto-Start System</h3>
                    <p>Intelligent initialization that handles everything for you</p>
                    <ul class="feature-list">
                        <li>Auto-starts Ollama service</li>
                        <li>Auto-downloads models</li>
                        <li>Service health checks</li>
                        <li>Zero manual setup</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <h3>Smart Model Manager</h3>
                    <p>Intelligent model selection based on your system</p>
                    <ul class="feature-list">
                        <li>RAM-based recommendations</li>
                        <li>One-click downloads</li>
                        <li>20+ models available</li>
                        <li>Instant model switching</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">💬</span>
                    <h3>Advanced Chat</h3>
                    <p>Professional chat interface with real-time streaming</p>
                    <ul class="feature-list">
                        <li>Streaming responses</li>
                        <li>Context-aware AI</li>
                        <li>Message history</li>
                        <li>Beautiful formatting</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🔊</span>
                    <h3>Text-to-Speech</h3>
                    <p>Hear AI responses with customizable voice settings</p>
                    <ul class="feature-list">
                        <li>Toggle TTS on/off</li>
                        <li>Adjustable speed</li>
                        <li>Volume control</li>
                        <li>Auto-speak responses</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">💾</span>
                    <h3>Chat Management</h3>
                    <p>Save, load, and export your conversations</p>
                    <ul class="feature-list">
                        <li>Save conversations</li>
                        <li>Load previous chats</li>
                        <li>Export to TXT</li>
                        <li>Quick access sidebar</li>
                    </ul>
                </div>

                <div class="feature-card">
                    <span class="feature-icon">🎨</span>
                    <h3>Professional UI</h3>
                    <p>Modern, dark-themed interface with Codeex branding</p>
                    <ul class="feature-list">
                        <li>Clean dark theme</li>
                        <li>Color-coded messages</li>
                        <li>Responsive design</li>
                        <li>Smooth animations</li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Installation Section -->
    <section class="installation fade-in" id="installation">
        <div class="container">
            <div class="section-title">
                <h2>📦 Quick Installation</h2>
                <p>Get started in just 3 simple steps</p>
            </div>
            <div class="steps-grid">
                <div class="step">
                    <span class="step-number">1</span>
                    <h3>Install Ollama</h3>
                    <p>Download and install Ollama from the official website:</p>
                    <div class="code-block">
                        <code>https://ollama.ai</code>
                        <button class="copy-btn" onclick="copyCode(this, 'https://ollama.ai')">Copy</button>
                    </div>
                    <p style="color: #94a3b8; margin-top: 1rem;">Available for Windows, macOS, and Linux</p>
                </div>

                <div class="step">
                    <span class="step-number">2</span>
                    <h3>Install Python Dependencies</h3>
                    <p>Install required Python packages:</p>
                    <div class="code-block">
                        <code>pip install customtkinter pillow requests psutil pyttsx3</code>
                        <button class="copy-btn" onclick="copyCode(this, 'pip install customtkinter pillow requests psutil pyttsx3')">Copy</button>
                    </div>
                    <p style="color: #94a3b8; margin-top: 1rem;">Python 3.8 or higher required</p>
                </div>

                <div class="step">
                    <span class="step-number">3</span>
                    <h3>Clone & Run</h3>
                    <p>Clone the repository and run the application:</p>
                    <div class="code-block">
                        <code>git clone https://github.com/heoster/codeex-v5.git<br>
cd codeex-v5<br>
python codeex_chat.py</code>
                        <button class="copy-btn" onclick="copyCode(this, 'git clone https://github.com/heoster/codeex-v5.git\ncd codeex-v5\npython codeex_chat.py')">Copy</button>
                    </div>
                    <p style="color: #94a3b8; margin-top: 1rem;">The app will auto-start Ollama and download the default model!</p>
                </div>
            </div>

            <div style="margin-top: 3rem; text-align: center;">
                <h3 style="color: var(--accent); margin-bottom: 1rem;">Alternative: Download Directly</h3>
                <a href="https://github.com/heoster/codeex-v5/archive/refs/heads/main.zip" class="btn btn-primary">
                    📥 Download ZIP
                </a>
            </div>
        </div>
    </section>

    <!-- System Requirements -->
    <section class="requirements fade-in" id="requirements">
        <div class="container">
            <div class="section-title">
                <h2>💻 System Requirements</h2>
                <p>Optimized for various system configurations</p>
            </div>
            <div class="req-grid">
                <div class="req-card">
                    <div class="req-icon">🖥️</div>
                    <h4>Operating System</h4>
                    <p>Windows 10/11<br>macOS 11+<br>Linux (Ubuntu, Debian, etc.)</p>
                </div>
                <div class="req-card">
                    <div class="req-icon">🧠</div>
                    <h4>RAM</h4>
                    <p>Minimum: 4GB<br>Recommended: 8GB+<br>Optimal: 16GB+</p>
                </div>
                <div class="req-card">
                    <div class="req-icon">🐍</div>
                    <h4>Python</h4>
                    <p>Version: 3.8 - 3.12<br>Required: pip<br>Virtual env recommended</p>
                </div>
                <div class="req-card">
                    <div class="req-icon">💾</div>
                    <h4>Storage</h4>
                    <p>App: ~50MB<br>Models: 500MB - 40GB<br>SSD recommended</p>
                </div>
            </div>

            <div style="margin-top: 3rem; background: rgba(30, 41, 59, 0.6); padding: 2rem; border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h3 style="color: var(--accent); margin-bottom: 1.5rem; text-align: center;">📊 Model Recommendations by RAM</h3>
                <div style="display: grid; gap: 1rem;">
                    <div style="padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 10px; border-left: 4px solid #ef4444;">
                        <strong style="color: #fca5a5;">< 8GB RAM:</strong> <span style="color: #cbd5e1;">phi3:mini, tinyllama, qwen2:0.5b</span>
                    </div>
                    <div style="padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 10px; border-left: 4px solid #f59e0b;">
                        <strong style="color: #fcd34d;">8-16GB RAM:</strong> <span style="color: #cbd5e1;">llama3.2:1b, gemma2:2b, phi3:medium</span>
                    </div>
                    <div style="padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 10px; border-left: 4px solid #3b82f6;">
                        <strong style="color: #93c5fd;">16-32GB RAM:</strong> <span style="color: #cbd5e1;">llama3.2:3b, gemma2:9b, mistral</span>
                    </div>
                    <div style="padding: 1rem; background: rgba(0,0,0,0.3); border-radius: 10px; border-left: 4px solid #10b981;">
                        <strong style="color: #6ee7b7;">32GB+ RAM:</strong> <span style="color: #cbd5e1;">llama3.1:8b, mixtral:8x7b, llama3:70b</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section class="contact fade-in" id="contact">
        <div class="container">
            <div class="section-title">
                <h2>📞 Get in Touch</h2>
                <p>Connect with us for support, feedback, or collaboration</p>
            </div>
            <div class="contact-grid">
                <div class="contact-card">
                    <div class="contact-icon">📧</div>
                    <h3>Email</h3>
                    <p><a href="mailto:codeex.care@gmail.com">codeex.care@gmail.com</a></p>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">📸</div>
                    <h3>Instagram</h3>
                    <p><a href="https://instagram.com/codeex._.heoster" target="_blank">@codeex._.heoster</a></p>
                </div>
                <div class="contact-card">
                    <div class="contact-icon">⭐</div>
                    <h3>GitHub</h3>
                    <p><a href="https://github.com/heoster/codeex-v5" target="_blank">heoster/codeex-v5</a></p>
                </div>
            </div>

            <div style="margin-top: 3rem; text-align: center; background: rgba(30, 41, 59, 0.6); padding: 2rem; border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3);">
                <h3 style="color: var(--accent); margin-bottom: 1rem;">🌟 Open Source & Free</h3>
                <p style="color: #94a3b8; margin-bottom: 1.5rem;">
                    Codeex AI Chat is completely open source and free to use. <br>
                    Contributions, bug reports, and feature requests are welcome!
                </p>
                <a href="https://github.com/heoster/codeex-v5/issues" class="btn btn-secondary" target="_blank">
                    🐛 Report an Issue
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="footer-logo">⚡ CODEEX</div>
            <p style="color: #94a3b8; margin-bottom: 1.5rem;">
                Professional AI Chat Interface for Ollama
            </p>
            <div class="footer-links">
                <a href="https://github.com/heoster/codeex-v5" target="_blank">GitHub</a>
                <a href="https://instagram.com/codeex._.heoster" target="_blank">Instagram</a>
                <a href="mailto:codeex.care@gmail.com">Email</a>
                <a href="https://ollama.ai" target="_blank">Ollama</a>
            </div>
            <div class="copyright">
                <p>&copy; 2024 Codeex. All rights reserved.</p>
                <p class="made-by">Made with ❤️ by <strong>heoster</strong></p>
            </div>
        </div>
    </footer>

    <script>
        // Generate stars
        function createStars() {
            const starsContainer = document.getElementById('stars');
            const starCount = 100;

            for (let i = 0; i < starCount; i++) {
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                starsContainer.appendChild(star);
            }
        }

        // Create floating particles
        function createParticles() {
            setInterval(() => {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.bottom = '-10px';
                document.body.appendChild(particle);

                setTimeout(() => {
                    particle.remove();
                }, 10000);
            }, 2000);
        }

        // Scroll animations
        function handleScrollAnimations() {
            const elements = document.querySelectorAll('.fade-in');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    }
                });
            }, { threshold: 0.1 });

            elements.forEach(element => {
                observer.observe(element);
            });
        }

        // Copy code function
        function copyCode(button, text) {
            navigator.clipboard.writeText(text).then(() => {
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.style.background = '#059669';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.style.background = '';
                }, 2000);
            });
        }

        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            createStars();
            createParticles();
            handleScrollAnimations();
        });

        // 3D card effect
        document.querySelectorAll('.demo-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
            });
        });
    </script>
</body>
</html>
