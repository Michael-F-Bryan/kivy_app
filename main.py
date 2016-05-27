from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest



API_KEY = 'cf267c34f8652831dc9b714fb0576fbb'



class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()

    def search_location(self):
        if not self.search_input.text:
            return

        base_url = 'http://api.openweathermap.org/data/2.5/' 
        search_template = base_url + 'find?q={query}&type=like&APPID={API_KEY}'
        url = search_template.format(query=self.search_input.text,
                API_KEY=API_KEY)

        request = UrlRequest(url, self.found_location)

    def found_location(self, request, data):
        cities = ['{} ({})'.format(d['name'], d['sys']['country']) 
                for d in data['list']]
        self.search_results.item_strings = cities


class WeatherApp(App):
    pass


if __name__ == "__main__":
    WeatherApp().run()
