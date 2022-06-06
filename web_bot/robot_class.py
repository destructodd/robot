import pigpio
import time
pi = pigpio.pi()

#duty controls speed, freq doesn't need to change, pulse sets the increment by which the camera moves

class robot():
    def __init__(self, duty = 75, freq = 20, pulse = 30):
        self.freq = freq
        self.duty = duty
        self.pulse = pulse
        #set initial values
        for servo in self.servo_pins:
            pi.set_servo_pulsewidth(servo, 1500)
        for motor in self.motor_pins:
            pi.set_PWM_frequency(motor, self.freq)
            pi.set_PWM_dutycycle(motor, 0)
    #rb,rf,lf,lb
    motor_pins = [7,8,9,10]
    #x,y
    servo_pins = [17,27]
    last_direction = 'stop'
    def set_duty(self, duty):
        self.duty = duty
    def drive(self, direction):
        if direction == 'forward':
            duty_list = [0, self.duty, self.duty, 0]
        elif direction == 'backward':
            duty_list = [self.duty, 0, 0, self.duty] 
        elif direction == 'left':
            duty_list = [0, self.duty, 0, self.duty]
        elif direction == 'right':
            duty_list = [self.duty, 0, self.duty, 0]
        else:
            duty_list = [0, 0, 0, 0]
        self.last_direction = direction
        for count, motor in enumerate(self.motor_pins):
            pi.set_PWM_dutycycle(motor, duty_list[count])   
    def cam_move(self, direction):
        if direction == 'centre':
            for pin in self.servo_pins:
                pi.set_servo_pulsewidth(pin, 1500)
                time.sleep(0.25)
        else:
            if direction == 'up':     
                x = 0
                y = -self.pulse
            elif direction == 'down':     
                x = 0
                y = self.pulse
            elif direction == 'left':     
                x = self.pulse
                y = 0
            elif direction == 'right':     
                x = -self.pulse
                y = 0
            x += pi.get_servo_pulsewidth(self.servo_pins[0])
            y += pi.get_servo_pulsewidth(self.servo_pins[1])
            x = max(800, min(2200, x))
            y = max(800, min(2200, y))
            pi.set_servo_pulsewidth(self.servo_pins[0], x)
            pi.set_servo_pulsewidth(self.servo_pins[1], y)
    def cam_increment(self, pin, value):
             pi.set_servo_pulsewidth(self.servo_pins[pin], value)
