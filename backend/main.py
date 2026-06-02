from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.exceptions import TerravaException
from database.firebase import is_mock_mode

# Import routers
from routes import (
    auth, profile, digital_twin, disease, chat,
    weather, market, schemes, sos, community,
    notifications, analytics, admin, ocr
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "Production-ready scalable Ag-OS backend for the TERRAVA platform. "
        "Integrates Firestore real-time indices, Firebase Authentication state engines, "
        "and 6 specialized Hugging Face AI pipeline models (MobileNet, DINOv2, Phi-4 Mini, Whisper, MMS-TTS, BGE)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Custom Exception Handler
@app.exception_handler(TerravaException)
async def terrava_exception_handler(request: Request, exc: TerravaException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.detail
        }
    )

# Native Root landing portal to guide developers and judges
@app.get("/", response_class=HTMLResponse, tags=["General Root"])
async def read_root():
    mode_text = "⚠️ MOCK DB SANDBOX ACTIVE" if is_mock_mode else "⚡ LIVE FIREBASE CONNECTOR ACTIVE"
    mode_color = "#f59e0b" if is_mock_mode else "#10b981"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>TERRAVA Ag-OS Backend</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
        <style>
            body {{
                background-color: #080f1d;
                color: #dae2fd;
                font-family: 'Outfit', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background-image: 
                    radial-gradient(at 0% 0%, rgba(74, 225, 118, 0.08) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(30, 41, 59, 0.2) 0px, transparent 50%);
            }}
            .card {{
                background: rgba(19, 27, 46, 0.7);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 24px;
                padding: 40px;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            }}
            h1 {{
                font-weight: 800;
                font-size: 3rem;
                margin: 0;
                letter-spacing: -1px;
                background: linear-gradient(135deg, #4be277, #3b82f6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .badge {{
                display: inline-block;
                background: {mode_color};
                color: #080f1d;
                font-family: 'JetBrains Mono', monospace;
                font-weight: bold;
                font-size: 0.75rem;
                padding: 6px 16px;
                border-radius: 9999px;
                margin-top: 15px;
                letter-spacing: 1px;
            }}
            p {{
                color: #94a3b8;
                font-size: 1.1rem;
                line-height: 1.6;
                margin: 25px 0;
            }}
            .btn {{
                display: inline-flex;
                align-items: center;
                background: #4be277;
                color: #080f1d;
                font-weight: bold;
                text-decoration: none;
                padding: 14px 32px;
                border-radius: 12px;
                transition: transform 0.2s, box-shadow 0.2s;
                font-size: 1rem;
                box-shadow: 0 4px 14px rgba(75, 226, 119, 0.3);
            }}
            .btn:hover {{
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(75, 226, 119, 0.5);
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>TERRAVA Ag-OS API</h1>
            <div class="badge">{mode_text}</div>
            <p>
                Welcome to the high-performance scalable engine of Terrava. 
                Ingesting complex satellite and crop telemetry indices, running zero-shot agricultural pathology classification, 
                and delivering predictive profit margins.
            </p>
            <a href="/docs" class="btn">Launch Swagger Documentation</a>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)


# Mount routers to API prefix
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(profile.router, prefix=settings.API_V1_STR)
app.include_router(digital_twin.router, prefix=settings.API_V1_STR)
app.include_router(disease.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(weather.router, prefix=settings.API_V1_STR)
app.include_router(market.router, prefix=settings.API_V1_STR)
app.include_router(schemes.router, prefix=settings.API_V1_STR)
app.include_router(sos.router, prefix=settings.API_V1_STR)
app.include_router(community.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(admin.router, prefix=settings.API_V1_STR)
app.include_router(ocr.router, prefix=settings.API_V1_STR)
