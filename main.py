from kivy.app import App
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton


API_KEY = 'cf267c34f8652831dc9b714fb0576fbb'


class WeatherRoot(BoxLayout):
    """The root widget for the app"""
    current_weather = ObjectProperty()

    def show_current_weather(self, location=None):
        self.clear_widgets()

        if location is None and self.current_weather is None:
            # Some convenient default value
            location = 'Perth (AU)'

        if location is not None:
            self.current_weather = Factory.CurrentWeather()
            self.current_weather.location = location

        self.add_widget(self.current_weather)

    def show_add_location_form(self):
        self.clear_widgets()
        self.add_widget(AddLocationForm())



class LocationButton(ListItemButton):
    """A subclass of ListItemButton so we can give it event handlers"""


class AddLocationForm(BoxLayout):
    """A form for adding new locations for the app"""
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        """Send off a request to the API"""
        if not self.search_input.text:
            return

        base_url = 'http://api.openweathermap.org/data/2.5/' 
        search_template = base_url + 'find?q={query}&type=like&APPID={API_KEY}'
        url = search_template.format(query=self.search_input.text,
                API_KEY=API_KEY)

        request = UrlRequest(url, self.found_location)

    def found_location(self, request, data):
        """The callback executed when we get a response back"""
        cities = ['{} ({})'.format(d['name'], d['sys']['country']) 
                for d in data['list']]
        self.search_results.item_strings = cities

        self.search_results.adapter.data.clear()
        self.search_results.adapter.data.extend(cities)
        self.search_results._trigger_reset_populate()


class WeatherApp(App):
    """The app itself"""


if __name__ == "__main__":
    WeatherApp().run()
