from flask import Flask, render_template_string, request 
from time import sleep
#import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#define GPIO pins
GPIO_pins = (14, 15, 18) # (22,27,17)Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20 #23       # Direction -> GPIO Pin
step = 21 #24      # Step -> GPIO Pin

# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

app = Flask(__name__)

TPL = '''
<html>
     <head><title>Web Page Controlled Stepper</title></head>
    <body>
    <h2> Web Page to Control Stepper</h2>
        <form method="POST" action="test">
            <p>Slider   <input type="range" min="1" max="20" name="slider" /> </p>
            <input type="submit" value="submit" />
        </form>
    </body>
</html>

'''
 
@app.route("/")
def home():

    return render_template_string(TPL)
 
@app.route("/test", methods=["POST"])
def test():
    # Get slider Values
    slider = request.form["slider"]
    print(int(slider))
  
    if (int(slider)>10):
       mymotortest.motor_go(True, "Full" , 300,.0004, False, .05)
       print("Rotating Clockwise")
    
    if (int(slider)<10):
       mymotortest.motor_go(False, "Full" , 300,.0004, False, .05)
       print("Rotating Anti-Clockwise")

    
    return render_template_string(TPL)
 
# Run the app on the local development server
if __name__ == "__main__":
    app.run()
