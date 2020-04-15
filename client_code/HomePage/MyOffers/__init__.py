from ._anvil_designer import MyOffersTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

from ...Globals import ITEM_HEIRARCHY, UNITS_OF_MEASURE

class MyOffers(MyOffersTemplate):

    def __init__(self, **properties):
        anvil.users.login_with_form()
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.repeating_panel_1.items = anvil.server.call("get_my_offers")
        self.unit_of_measure.items = UNITS_OF_MEASURE
        self.product_description.items = ITEM_HEIRARCHY
        anvil.server.call('generate_matches')
    
    def add_to_my_offers(self,product_key, units, expiry_date, notes):
        """ Add item to Offers database """
        result = anvil.server.call("save_to_offers_database", product_key, units, expiry_date, notes)
        if result == "Duplicate":
              self.debug_console.text = "ⓘ Unable to create new entry because this combination of Product, Unit of Measure, and Expiry Date already exists.  Please consider deleting old entry and creating a new one?"
        else:
              self.debug_console.text = "✓ Item added."
              anvil.server.call('generate_matches')
        self.repeating_panel_1.items = anvil.server.call("get_my_offers")

   
    def add_item_click(self, **event_args):
        """This method is called when the Add Item button is clicked"""
        unit_of_measure = self.unit_of_measure.selected_value or self.unit_of_measure.placeholder
        product_key = (self.product_description.selected_value, unit_of_measure)
        units = int(self.number_of_units.text or self.number_of_units.placeholder)
        expiry_date = self.expiry_date.date or datetime.datetime.today().date()
        notes = self.notes.text or "(No notes attached)"
        if not product_key[0] and product_key[1]:
            self.debug_console.text = "⚠ Please select a product and/or unit of measure."
        else:
            self.add_to_my_offers(product_key, units, expiry_date, notes)

    def drop_down_change(self, **event_args):
        """Clears old Notes when a Drop Down list is selected"""
        self.notes.text = ""


