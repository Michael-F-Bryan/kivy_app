__version__ = '0.1.0'

from collections import namedtuple
from kivy.app import App
from kivy.properties import (ObjectProperty, ListProperty, StringProperty, 
        NumericProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton


Location = namedtuple('Location', ('city', 'country'))
API_KEY = 'cf267c34f8652831dc9b714fb0576fbb'
base_url = 'http://api.openweathermap.org/data/2.5/' 


class CurrentWeather(BoxLayout):
    location = ListProperty(['Perth', 'AU'])
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def update_weather(self):
        weather_template = base_url + 'weather?q={},{}&units=metric&APPID={APPID}'
        url = weather_template.format(*self.location, APPID=API_KEY)
        UrlRequest(url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        

class WeatherRoot(BoxLayout):
    """The root widget for the app"""
    current_weather = ObjectProperty()

    def show_current_weather(self, location=None):
        self.clear_widgets()

        if self.current_weather is None:
            self.current_weather = CurrentWeather()

        if location is not None:
            self.current_weather.location = location

        self.current_weather.update_weather()
        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())



class LocationButton(ListItemButton):
    """A subclass of ListItemButton so we can give it event handlers"""
    location = ListProperty()


class AddLocationForm(BoxLayout):
    """A form for adding new locations for the app"""
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        """Send off a request to the API"""
        if not self.search_input.text:
            return

        search_template = base_url + 'find?q={query}&type=like&APPID={API_KEY}'
        url = search_template.format(query=self.search_input.text,
                API_KEY=API_KEY)

        request = UrlRequest(url, self.found_location)

    def found_location(self, request, data):
        """The callback executed when we get a response back"""
        cities = [Location(d['name'], d['sys']['country']) 
                for d in data['list']]
        self.search_results.item_strings = cities

        self.search_results.adapter.data.clear()
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()

    def args_converter(self, index, data_item):
        return {'location': Location(*data_item)}

class WeatherApp(App):
    """The app itself"""

    def on_pause(self):
        """
        Do whatever we need to when the screen turns off. If it returns True 
        then the app can resume. Otherwise it exits.
        """
        return True


if __name__ == "__main__":
    WeatherApp().run()
