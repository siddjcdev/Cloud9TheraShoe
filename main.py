import asyncio
import machine
from microdot_asyncio import Microdot, Response,
from microdot_utemplate import render_template
import motorcontroller
import home_page

Response.default_content_type = 'text/html'

app = Microdot()
motor_task_start = None
motor_task_stop  = None



led = machine.Pin(2,machine.Pin.OUT)
led.off()


@app.before_request
async def pre_request_manager(request):

    if motor_task_start:
        motor_task_start.cancel()
        print("motor_task_start has been cancelled")
    if motor_task_stop:
        motor_task_stop.cancel()
        print("motor_task_stop has been cancelled")

@app.get('/')
async def index(request):
    print("Index request has been recieved")
    return render_template('index.html', name="world")
    #return render_template('index.html')

@app.route('/home')
async def index(request):
    return render_template('home.html', led_value=0)



# @app.route('/')
# def hello(request):
#     if led.value() == 1:
#         led_state = "ON"
#         print("led is ON")
#     elif led.value()== 0:
#         led_state = "OFF"
#         print("led is OFF")
#     return (home_page.build_home(led_state))

@app.route('/motor/start') 
async def start_motor(request):
    print("starting motors...")
    
    global motor_task_start
    motor_task_start = asyncio.create_task(motorcontroller.start_motors())
    #await asyncio.sleep_ms(1_000)
    
@app.route('/motor/stop') 
async def stop_motor(request):
    print("stopping motors...")
    
    global motor_task_stop
    motor_task_stop = asyncio.create_task(motorcontroller.stop_motors())
    #await asyncio.sleep_ms(1_000)
    
    

def start_webserver():
    print ("Booting up Microdot")
    try:
        app.run(port=80, debug = True)
    except:
        app.shutdown()
        
        
asyncio.run(start_webserver())

