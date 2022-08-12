mkdir -p ~/.streamlit/

echo "[theme]
primaryColor="#e00a0a"
backgroundColor="#02370a"
secondaryBackgroundColor="#28bd2c"
textColor="#ffffff"
font="serif"
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml