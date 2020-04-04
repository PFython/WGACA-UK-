from ._anvil_designer import UserSetupTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

LOCALE = "United Kingdom"
ADDRESSES = anvil.server.call("get_address_hierarchy", LOCALE)

class UserSetup(UserSetupTemplate):
    locale = LOCALE
    addresses = ADDRESSES
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        user = anvil.users.get_user()       
        
        self.display_name.text = user['display_name']
        self.email.text = user['email']
        self.house_number.text = user['house_number']
        if user['street'] and user['county']:
            print(street, county)
            self.street.selected_value = user['street']
            self.county.selected_value = user['county']
            self.street_change()
        else:
            self.county_change()
        self.country.text = user['country']
        self.telephone.text = user['telephone'] 
  
    def county_change(self, **event_args):
        """This method is called when an item is selected"""
        towns = UserSetup.addresses[self.county.selected_value]
        streets = []
        for town in towns:
            streets.extend(UserSetup.addresses[self.county.selected_value][town])
        streets.sort()
        self.street.items = streets
        self.street.selected_value = streets[0]
        self.street_change()
        self.save_input()

    def street_change(self, **event_args):
        """This method is called when an item is selected"""
        towns = UserSetup.addresses[self.county.selected_value]
        for town, street_list in towns.items():
            if self.street.selected_value in street_list:
                break
        self.town.items = [town]
        self.town.selected_value = town
        self.save_input()
        
    def get_input_fields(self):
        return {'display_name' : (self.display_name, 'text'),
               'house_number' : (self.house_number, 'text'),
               'street' : (self.street, 'selected_value'),
               'town' : (self.town, 'selected_value'),
               'county' : (self.county, 'selected_value'),
               'country' : (self.country, 'text'),
               'postcode' : (self.postcode, 'text'),
               'telephone' : (self.telephone, 'text'),}
      
    def save_input(self, **event_args):
      """This method is called when the text in this text box is edited"""
      input_fields = self.get_input_fields()
      for field, _values in input_fields.items():
          component, attribute = _values
          anvil.server.call("save_user_setup", field, getattr(component, attribute))














