from django.http import HttpResponse

def home(request):
    html_content = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ByteObe | Django + PostgreSQL + DRF</title>
        <style>
            :root {
                --bg-color: #0a0a0f;
                --card-bg: #14141a;
                --text-color: #e5e7eb;
                --accent: #3b82f6;
                --accent-gradient: linear-gradient(90deg, #2563eb, #3b82f6, #60a5fa);
                --font-family: 'Inter', system-ui, sans-serif;
            }
            body {
                background-color: var(--bg-color);
                color: var(--text-color);
                font-family: var(--font-family);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                text-align: center;
            }
            .card {
                background-color: var(--card-bg);
                padding: 3rem;
                border-radius: 1rem;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
                max-width: 520px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
            h1 {
                font-size: 2rem;
                margin-bottom: 1rem;
                background: var(--accent-gradient);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
            }
            p {
                font-size: 1rem;
                opacity: 0.85;
                line-height: 1.5;
            }
            a {
                color: var(--text-color);
                text-decoration: none;
                font-weight: 600;
                border: 1px solid var(--accent);
                padding: 0.6rem 1.2rem;
                border-radius: 0.5rem;
                display: inline-block;
                margin-top: 1.5rem;
                background: var(--accent);
                background: var(--accent-gradient);
                transition: opacity 0.3s ease, transform 0.2s ease;
            }
            a:hover {
                opacity: 0.9;
                transform: scale(1.03);
            }
            footer {
                position: absolute;
                bottom: 1rem;
                font-size: 0.8rem;
                opacity: 0.5;
                letter-spacing: 0.5px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🚀 Django + PostgreSQL + DRF</h1>
            <p>Bienvenido a la plantilla base de <strong>ByteObe</strong>.<br>
            Tu entorno de desarrollo está funcionando correctamente.<br>
            Empieza a construir tu API con velocidad, estructura y calidad.</p>
            <a href="/documentation/api/">Ver documentación de la API</a>
        </div>
        <footer>© 2025 ByteObe · Tecnología que impulsa tu desarrollo</footer>
    </body>
    </html>
    '''
    return HttpResponse(html_content)
