##############################################################
# Muh Sooper Seecret App- RevHunter SkunkWorks
# By Nyowa225
# Warning, this is very unfinished, if you want to share it,
# please mention that so I don't look like a shithead.
# Special Thanks to Kahimi for helping my retarded ass get the right side of the bars working
#test edit
#############################################################

import sys
sys.path.insert(0, 'apps/python/RevHunterSkunkworks/dll')
import ac
import acsys
import math
import os
from sim_info.sim_info import SimInfo

sim_info = SimInfo()  #thanks Rombik for this extremely helpful bit of code

appWindow=0
windowx=960
windowy=105

max_rpm = 0
min_user_rpm = 80
max_user_rpm = 97
max_boost = 1
max_fuel = 0
gear_display = 0
rpm_delta = 0
gear = 0
alpha = 0
rpm_display = 0
speed_display = 0
boost_display = 0
fuel_display = 0
max_boost = 0.0001
current_boost = 0
percentage_rpm = 0
truncated_rpm = 0
shit = 0
current_fuel=0

min_rpm_spinner_Label = 0
min_rpm_spinner = 0
max_rpm_spinner_Label = 0
max_rpm_spinner = 0
units_spinner_Label = 0
units_spinner = 0
units = 1

settings_box_Label = 0
settings_box = 0

#####   Create Custom Class   #####
class Label:
    def __init__(self,appWindow,text = ""):
        self.label = ac.addLabel(appWindow, "  ")
        self.labelText = text
        self.labelSize  = {"width" : 0, "height" : 0}
        self.labelPosition = {"xpos" : 0, "ypos" : 0}
        self.labelFontSize  = 12
        self.labelFontAlign = "left"
        self.labelFontColor = {"red" : 1, "green" : 1, "blue" : 1, "alpha" : 0}
        self.labelbgTexture = ""

    def setText(self, text):
        self.labelText = text
        ac.setText(self.label, self.labelText)
        return self

    def setSize(self, width, height):
        self.labelSize["width"] = width
        self.labelSize["height"] = height
        ac.setSize(self.label, self.labelSize["width"], self.labelSize["height"])
        return self

    def setPosition(self, xposition, yposition):
        self.labelPosition["xposition"] = xposition
        self.labelPosition["yposition"] = yposition
        ac.setPosition(self.label, self.labelPosition["xposition"],self.labelPosition["yposition"])
        return self

    def setFontSize(self, fontSize):
        self.labelFontSize = fontSize
        ac.setFontSize(self.label, self.labelFontSize)
        return self

    def setFontAlign(self, fontAlign = "left"):
        self.labelFontAlign = fontAlign
        ac.setFontAlignment(self.label, self.labelFontAlign)
        return self

    def setFontColor(self, red, green, blue, alpha):
        self.labelFontColor["red"] = red
        self.labelFontColor["green"] = green
        self.labelFontColor["blue"] = blue
        self.labelFontColor["alpha"] = alpha
        ac.setFontColor(self.label, self.labelFontColor["red"],self.labelFontColor["green"],self.labelFontColor["blue"],self.labelFontColor["alpha"])
        return self

    def setbgTexture(self, texture):
        self.labelbgTexture = texture
        ac.setBackgroundTexture(self.label, self.labelbgTexture)
        return self

def acMain(ac_version):
    global rpm_display, boost_display, gear_display, speed_display, fuel_display
    global min_rpm_spinner_Label, min_rpm_spinner, max_rpm_spinner_Label, max_rpm_spinner, settings_box_Label
    global units_spinner_Label, units_spinner
    global rpm_tag, speed_tag, boost_tag, fuel_tag

    appWindow=ac.newApp("RevHunterSkunkworks")
    ac.setTitle(appWindow, " ")
    ac.setSize(appWindow,windowx,windowy)
    ac.drawBorder(appWindow,0)
    ac.setBackgroundOpacity(appWindow,0)
    ac.addRenderCallback(appWindow, onFormRender)

    rpm_display  = Label(appWindow, "").setSize(0,0).setPosition((2.05*windowx/3),(1.05*windowy/3)).setFontSize(50).setFontAlign("right")
    gear_display = Label(appWindow).setSize(0,0).setPosition((windowx / 2),-50).setFontSize(140).setFontAlign("center")
    speed_display= Label(appWindow, "").setSize(0,0).setPosition((1.25*windowx/3),(1.05*windowy/3)).setFontSize(50).setFontAlign("right")
    fuel_display = Label(appWindow, "").setSize(0,0).setPosition((0.8*windowx/3),(1.25*windowy/3)).setFontSize(35).setFontAlign("right")
    settings_box_Label = Label(appWindow, "").setSize(0,0).setPosition(940,83).setFontSize(15).setFontAlign("left")

    rpm_tag = Label(appWindow, "").setText("RPM").setSize(0,0).setPosition((2.06*windowx/3),(2.1*windowy/3)).setFontSize(15).setFontAlign("left")
    speed_tag=Label(appWindow, "").setText("MPH").setSize(0,0).setPosition((1.26*windowx/3),(2.1*windowy/3)).setFontSize(15).setFontAlign("left")
    fuel_tag = Label(appWindow, "").setText("%FUEL").setSize(0,0).setPosition((0.81*windowx/3),(1.9*windowy/3)).setFontSize(15).setFontAlign("left")

    min_rpm_spinner = ac.addSpinner(appWindow, "Min %RPM")
    spinnerConfig(min_rpm_spinner,0,125,80,20,0,1,100,80,setMinRPM,0)
    max_rpm_spinner = ac.addSpinner(appWindow, "Max %RPM")
    spinnerConfig(max_rpm_spinner,100,125,80,20,90,1,100,97,setMaxRPM,0)

    units_spinner = ac.addSpinner(appWindow, "Units")
    spinnerConfig(units_spinner,200,125,80,20,1,1,2,1,setUnits,0)

    settings_box = ac.addCheckBox(appWindow, "")
    ac.setPosition(settings_box,950,95)
    ac.setSize(settings_box,10,10)

    ac.addOnCheckBoxChanged(settings_box,toggle_settings_visiblity)

    return "RevHunterSkunkworks"

def acUpdate(deltaT):
    global appWindow
    global current_gear, current_rpm, max_rpm, shift_light, alpha, images_light, images_digits, gear_display, current_speed, max_fuel, current_fuel
    global rpm_display, boost_display, percentage_boost, current_boost, max_boost, percentage_rpm, truncated_rpm, fuel_display, percentage_fuel
    global min_rpm_spinner_Label, max_rpm_spinner_Label, units_spinner_Label

    #Keep app window transparent
    ac.setBackgroundOpacity(appWindow, 0)
    ac.drawBorder(appWindow, 0)

    max_rpm = sim_info.static.maxRpm if max_rpm == 0 else max_rpm      #This is pulled from shared memory, read only once
    max_fuel     = sim_info.static.maxFuel if max_fuel == 0 else max_fuel   #This is read from shared memory, read only once
    current_fuel = sim_info.physics.fuel                                    #This is read from shared memory, read every deltaT
    percentage_fuel = current_fuel/max_fuel*100

    current_gear = ac.getCarState(0, acsys.CS.Gear)                    #This is read from the API every update
    current_gear = current_gear - 1

    current_rpm  = ac.getCarState(0, acsys.CS.RPM)                     #This is read from the API every update
    truncated_rpm = 100*round(current_rpm/100)

    current_boost = ac.getCarState(0,acsys.CS.TurboBoost)                   #This is read from the API every update
    if units == 1:
        current_speed = ac.getCarState(0,acsys.CS.SpeedMPH)
    if units == 2:
        current_speed = ac.getCarState(0,acsys.CS.SpeedKMH)

    if (current_boost > max_boost):                                         #Calcualate maximum turbo boost pressure - Due to limitations in the api/shared memory currently the only way
        max_boost = current_boost

    percentage_boost = current_boost/max_boost*100                              #Calculate the percent of turbo boost being generated
    percentage_rpm = current_rpm/max_rpm*100

    speed_display.setText("%d" % current_speed)


    if (current_gear >0):
        if (percentage_rpm < max_user_rpm):
            gear_display.setText("%d" % current_gear).setFontColor(1,1,1,1)
        else:
            gear_display.setText("%d" % current_gear).setFontColor(1,0,0,1)
    if (current_gear == 0):
        if (percentage_rpm < max_user_rpm):
            gear_display.setText("N").setFontColor(1,1,1,1)
        else:
            gear_display.setText("N").setFontColor(1,0,0,1)
    if (current_gear < 0):
        if (percentage_rpm < max_user_rpm):
            gear_display.setText("R").setFontColor(1,1,1,1)
        else:
            gear_display.setText("R").setFontColor(1,0,0,1)
    rpm_display.setText("%d" % abs(truncated_rpm))

    #fuel_display.setText("%0.1f" % percentage_fuel).setFontColor(1,0,1,1)
    if (percentage_fuel > 10):
        fuel_display.setText("%0.1f" % percentage_fuel).setFontColor(1,1,1,1)
    if (percentage_fuel < 10):
        fuel_display.setText("%0.1f" % percentage_fuel).setFontColor(1,1,0,1)
    if (percentage_fuel < 5):
        fuel_display.setText("%0.1f" % percentage_fuel).setFontColor(1,0,0,1)

def onFormRender(deltaT):
    global percentage_rpm
    drawrpmBars(0,0)
    drawboostBars(0,0)

def drawrpmBars(x,y):
    if(abs(percentage_rpm)<max_user_rpm):ac.glColor4f(1,1,1,1)
    if(abs(percentage_rpm)>max_user_rpm):ac.glColor4f(1,0,0,1)
    if(percentage_rpm <min_user_rpm):
        ac.glQuad(0,20,0,20)
        ac.glQuad(960,20,0,20)
    if(percentage_rpm >min_user_rpm):
        ac.glQuad(0,20,abs(percentage_rpm-min_user_rpm)*435/(100-min_user_rpm),20)
        #ac.glQuad(960,20,-(abs(percentage_rpm-min_user_rpm)*435/(100-min_user_rpm)),20)
        ac.glBegin(acsys.GL.Quads)
        ac.glVertex2f(960,20)
        ac.glVertex2f(960-abs(percentage_rpm-min_user_rpm)*435/(100-min_user_rpm),20)
        ac.glVertex2f(960-abs(percentage_rpm-min_user_rpm)*435/(100-min_user_rpm),40)
        ac.glVertex2f(960, 40)
        ac.glEnd()
        

def drawboostBars(x,y):
    ac.glColor4f(1,0.31,0,1)
    ac.glQuad(0,42,percentage_boost*4.35,8)
    #ac.glQuad(960,42,-percentage_boost*4.35,8)
    ac.glBegin(acsys.GL.Quads)
    ac.glVertex2f(960,40)
    ac.glVertex2f(960-percentage_boost*4.35,40)
    ac.glVertex2f(960-percentage_boost*4.35,48)
    ac.glVertex2f(960,48)
    ac.glEnd()

def setMinRPM(minval):
    global min_rpm_spinner, min_user_rpm
    min_user_rpm = minval

def setMaxRPM(maxval):
    global min_rpm_spinner, max_user_rpm
    max_user_rpm = maxval

def setUnits(unitsval):
    global units_spinner, units, speed_tag
    units = unitsval
    if unitsval == 1:
        speed_tag.setText("MPH")
    if unitsval == 2:
        speed_tag.setText("KPH")

def toggle_settings_visiblity(name, state):
    if state == 1:
        ac.setVisible(min_rpm_spinner, 1)
        ac.setVisible(max_rpm_spinner, 1)
        ac.setVisible(units_spinner, 1)
    if state == 0:
        ac.setVisible(min_rpm_spinner, 0)
        ac.setVisible(max_rpm_spinner, 0)
        ac.setVisible(units_spinner, 0)

def spinnerConfig(spinner, spin_pos_x, spin_pos_y, spin_size_x, spin_size_y, spin_val_min, spin_val_step, spin_val_max, spin_value, spin_event, vis_value):
    ac.setPosition(spinner, spin_pos_x, spin_pos_y)
    ac.setSize(spinner, spin_size_x, spin_size_y)
    ac.setRange(spinner, spin_val_min, spin_val_max)
    ac.setStep(spinner, spin_val_step)
    ac.setValue(spinner, spin_value)
    ac.addOnValueChangeListener(spinner, spin_event)
    ac.setVisible(spinner, vis_value)


