from falsk import Flask

app = Flask(__name__)

@app.get('/')
def home():
  return 'Hello, Lucky!'


@app.get('/about')
def about():
  return 'learning backend at Moringa'