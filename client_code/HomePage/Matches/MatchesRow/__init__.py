from ._anvil_designer import MatchesRowTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class MatchesRow(MatchesRowTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user = anvil.users.get_user()

    # Any code you write here will run when the form opens.

  def volunteer_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    alert("Wow, what a Karma Star you are!\nThanks so much for volunteering...\nThis function is still being worked on.")

