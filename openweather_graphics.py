import time
import json
import displayio
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font

cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)

small_font = cwd+"/fonts/Arial-12.bdf"
medium_font = cwd+"/fonts/Arial-16.bdf"
large_font = cwd+"/fonts/Arial-Bold-24.bdf" #not really

class OpenWeather_Graphics(displayio.Group):
    def __init__(self, root_group, *, am_pm=True, celsius=True):
        super().__init__(max_size=2)
        self.am_pm = am_pm
        self.celsius = celsius

        root_group.append(self)
        self._icon_group = displayio.Group(max_size=1)
        self.append(self._icon_group)
        self._text_group = displayio.Group(max_size=10)
        self.append(self._text_group)

        self._icon_sprite = None
        self._icon_file = None
        self.set_icon(cwd+"/background.bmp")

        self.small_font = bitmap_font.load_font(small_font)
        self.medium_font = bitmap_font.load_font(medium_font)
        self.large_font = bitmap_font.load_font(large_font)
        glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '
        self.small_font.load_glyphs(glyphs)
        self.medium_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(glyphs)
        self.large_font.load_glyphs(('°',))  # a non-ascii character we need for sure
        self.city_text = None

        self.time_text = Label(self.small_font, max_glyphs=8)
        self.time_text.x = 200
        self.time_text.y = 12
        self.time_text.color = 0xFFFFFF
        self._text_group.append(self.time_text)

        

        self.going = Label(self.medium_font, max_glyphs=20)
        self.going.x = 10
        self.going.y = 10
        self.going.color = 0x00FF00
        self._text_group.append(self.going)
        self.going.text="Taking bus ? "


        self.bus_id1 = Label(self.small_font, max_glyphs=20)
        self.bus_id1.x = 10
        self.bus_id1.y = 65
        self.bus_id1.color = 0xFFFF00
        self._text_group.append(self.bus_id1)


        self.bus_id2 = Label(self.small_font, max_glyphs=20)
        self.bus_id2.x = 210
        self.bus_id2.y = 65
        self.bus_id2.color = 0xFFFF00
        self._text_group.append(self.bus_id2)





        self.bus1 = Label(self.large_font, max_glyphs=20)
        self.bus1.x = 30
        self.bus1.y = 115
        self.bus1.color = 0xFFFFFF
        self._text_group.append(self.bus1)

        self.bus2 = Label(self.large_font, max_glyphs=20)
        self.bus2.x = 235
        self.bus2.y = 115
        self.bus2.color = 0xFFFFFF
        self._text_group.append(self.bus2)

        
       

     

    def display_time(self, data):
        
        try:

            data = json.loads(data)
            time=self.update_time()
            time_in_min=time[3]*60+time[4]     

        except:
            print("okay")

        try:
            bus_id1=data['data'][0]['relationships']['route']['data']['id']
            bus_id2=data['data'][1]['relationships']['route']['data']['id']

        except:
            print("error")


        try: 
            timeresult1 = data['data'][0]['attributes']['arrival_time']
            bus_time1=timeresult1.split("T")[1].split("-")[0].split(":")
            actualtime1=int(bus_time1[0])*60+int(bus_time1[1])
            actualtime1=actualtime1-time_in_min

        except:
            print("error2")


        try:
            timeresult2 = data['data'][1]['attributes']['arrival_time']
            bus_time2=timeresult2.split("T")[1].split("-")[0].split(":")
            actualtime2=int(bus_time2[0])*60+int(bus_time2[1])
            actualtime2=actualtime2-time_in_min
            
        except:
            print("error4")

        try:
            if (actualtime1 or actualtime2) < 10:
                
                if (actualtime1 or actualtime2) < 3:
                    self.set_icon(cwd+"/icons/01dred.bmp")
                else :
                    self.set_icon(cwd+"/icons/01dyellow.bmp")
            else : 
                self.set_icon(cwd+"/icons/01dgreen.bmp")
        except:
            print("some error with icons")

        try:

            if bus_id1=='94': #so that the 94 gets always displayed on the right 
                self.bus_id1.text = "BUS ID : " + bus_id1
                self.bus_id2.text = "BUS ID : " + bus_id2
                self.bus1.text =  str(actualtime1)
                self.bus2.text =  str(actualtime2)
            elif bus_id1 == '80':
                self.bus_id2.text = "BUS ID : " + bus_id1
                self.bus_id1.text = "BUS ID : " + bus_id2
                self.bus2.text =  str(actualtime1)
                self.bus1.text =  str(actualtime2)
            elif bus_id1 == '101':
                self.bus_id1.text = "BUS ID : " + bus_id1
                self.bus_id2.text = "BUS ID : " + bus_id2
                self.bus1.text =  str(actualtime1)
                self.bus2.text =  str(actualtime2)
            else :
                self.bus_id1.text="No prediction"
                self.bus_id2.text="No prediction"
                self.bus2.text =  " "
                self.bus1.text =  " "

        except:
            print("some weird error that should not have happened")








    def update_time(self):
        """Fetch the time.localtime(), parse it out and update the display text"""
        now = time.localtime()
        hour = now[3]
        minute = now[4]
        format_str = "%d:%02d"
        if self.am_pm:
            if hour >= 12:
                hour -= 12
                format_str = format_str+" PM"
            else:
                format_str = format_str+" AM"
            if hour == 0:
                hour = 12
        time_str = format_str % (hour, minute)
        print(time_str)
        self.time_text.text = time_str
        return now

    def set_icon(self, filename):

        print("Set icon to ", filename)
        if self._icon_group:
            self._icon_group.pop()

        if not filename:
            return  # we're done, no icon desired
        if self._icon_file:
            self._icon_file.close()
        self._icon_file = open(filename, "rb")
        icon = displayio.OnDiskBitmap(self._icon_file)
        try:
            self._icon_sprite = displayio.TileGrid(icon,
                                                   pixel_shader=displayio.ColorConverter())
        except TypeError:
            self._icon_sprite = displayio.TileGrid(icon,
                                                   pixel_shader=displayio.ColorConverter(),
                                                   position=(0,0))
        self._icon_group.append(self._icon_sprite)