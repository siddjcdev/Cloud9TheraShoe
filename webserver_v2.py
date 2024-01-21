import asyncio
from microdot import Microdot
app = Microdot()

@app.route('/')
def hello(request):
    return ('Hello, WORLD!')

def start_server:
    print ("Booting up Microdot")
    try:
        app.run(port=80)
    except:
        app.shutdown()