module.exports = {
  apps: [{
    name: 'khmerx-api',
    script: './venv/bin/python',
    args: '-m uvicorn app.main:app --host 0.0.0.0 --port 3030',
    env: {
      OTP_SECRET: 'Cq2psHePo9mjddp5cduxDe8brEPkl-kIwsPHb-ykcE6HDWxX7ACCgE8Cs6xyqmjd',
      OTP_DEV_MODE: 'false',
      BOT_TOKENS: '8392441656:AAGenTw5Y3OStzge1c6dvqbmMLenWbahTuc,8647221385:AAGU_BkXTzpDqXPKetZAaY717Ffirk_nGIY',
      BOT_PRIMARY: '8392441656:AAGenTw5Y3OStzge1c6dvqbmMLenWbahTuc',
      BOT_BACKUP: '8647221385:AAGU_BkXTzpDqXPKetZAaY717Ffirk_nGIY',
    }
  }]
};
