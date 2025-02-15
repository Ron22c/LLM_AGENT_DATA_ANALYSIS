Download Ollama: https://ollama.com/
ollama pull deepseek-r1:70b
ollama pull mxbai-embed-large
run ollama
create a virtual environment: python3 -m venv deepseek
activate virtual environment: source deepseek/bin/activate
pip install -r requirements.txt
edit main.py with your data, context, question
run python main.py
