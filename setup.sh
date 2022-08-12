mkdir -p ~/.streamlit/

echo "\
[theme]\n\
primaryColor='#e00a0a'\n\
backgroundColor='#02370a'\n\
secondaryBackgroundColor='#28bd2c'\n\
textColor='#ffffff'\n\
font='serif'\n\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml