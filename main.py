from fastapi import FastAPI
from db import engine, Base
from routers import auth, donations, prayers, posts, daily_verses, events, podcasts, global_impact, chat, otp

app = FastAPI(title="Power of Hope API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(donations.router)
app.include_router(prayers.router)
app.include_router(posts.router)
app.include_router(daily_verses.router)
app.include_router(events.router)
app.include_router(podcasts.router)
app.include_router(global_impact.router)
app.include_router(chat.router)
app.include_router(otp.router)
