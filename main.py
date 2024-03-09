import asyncio
import machine
from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
import motorManager
import accelManager
# import home_page

Response.default_content_type = 'text/html'

app = Microdot()
motor_task = None


@app.before_request
async def pre_request_manager(request):
    print("Entering pre_request_manager=> request.path=", request.path)
    if "motor" in request.path:
        if motor_task:
            motor_task.cancel()
            print("motor_task has been cancelled")

@app.get('/')
async def index(request):
    print("Index request has been recieved")
    return render_template('index.html', name="world")
    #return render_template('index.html')

@app.route('/blink')
async def blink(request):
    if led.value() == 1:
        led_state = "ON"
        print("led is ON")
        led.off()
    elif led.value()== 0:
        led_state = "OFF"
        print("led is OFF")
        led.on()

@app.post('/motor/control') 
async def start_motor(request):
    print("starting motors...")
    print("motor_level:", request.json['level'])
    level = int(request.json['level'])
    #level = (level-1)
    global motor_task
    motor_task = asyncio.create_task(motorManager.intensity(level))
    return 'Motor command accepted :)'
    
    
@app.get('/accel') 
async def get_accel_values(request):
    print("Getting shoe position..")
    return accelManager.get_data()
    #await asyncio.sleep_ms(1_000)


@app.route('/assets/<path:path>')
def static(request, path):
    if '..' in path:
        # directory traversal is not allowed
        return 'Not found', 404
    return send_file('assets/' + path)   
    

def start_webserver():
    print ("Booting up Microdot")
    try:
        app.run(port=80, debug = True)
    except:
        app.shutdown()
        
        
asyncio.run(start_webserver())

