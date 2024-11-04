from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.clock import Clock
import os
# Get the directory where the current file (custom_widgets.py) is located
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the full path to the custom_widgets.kv file
kv_file_path = os.path.join(current_dir, 'custom_widgets.kv')
# Load the KV file
Builder.load_file(kv_file_path)

class CustomPopup(Popup):
    pass
class CustomDropdown(DropDown):
    pass
class CustomDropBtn(Button):
    pass

class DragBarHorizontal(Widget):
    touch_x = NumericProperty(0)
    scroll_widget = ObjectProperty(None)
    relative_x = NumericProperty(0)  # The relative position between 0 and 1
    text_widget = None
    is_dragged = False
    text_width = 0

    def update_width(self,text_widget):
        self.text_widget = text_widget
        # if the codeinput text is cleared before its updated, just return
        if not text_widget.text:
            return
        
        label = Label(text=text_widget.text, 
                      font_name=text_widget.font_name, 
                      font_size=text_widget.font_size)
        
        # Get the width of the text using the label's texture with delay to let the label render
        Clock.schedule_once(lambda dt: self.update_bar_width(label), 0)
    
    def update_bar_width(self, label):
        # save width to be used in update from scroll
        self.text_width = label.texture_size[0]
        if self.text_width != 0:
            new_size = self.parent.width / self.text_width
            self.size_hint_x = new_size if new_size <= 1 else 1
    
    def update_from_scroll(self):
        """Update the bar's horizontal position based on the relative scroll_x."""
        if not self.is_dragged and self.text_widget is not None:
            # Calculate relative_x based on scroll_x and the width of the scrollable content
            relative_x = self.text_widget.scroll_x / (self.text_width - self.text_widget.width) if (self.text_width - self.text_widget.width) > 0 else 0
            if self.parent and (self.parent.width - self.width) > 0:
                # Calculate the x position based on relative_x (0 to 1)
                self.x = relative_x * (self.parent.width - self.width)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Grab the touch so the widget will receive the touch events even if the touch leaves its bounds
            touch.grab(self)
            self.is_dragged = True
            self.touch_x = touch.x
            return True
        return super(DragBarHorizontal, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # Calculate the new position
            new_x = self.x + (touch.x - self.touch_x)
            parent = self.parent
            if parent:
                # Constrain within the parent's bounds
                if new_x < 0:
                    new_x = 0
                elif new_x + self.width > parent.width:
                    new_x = parent.width - self.width

            # Update the widget's position
            self.x = new_x
            self.touch_x = touch.x

            # Calculate and update the relative position
            self.update_relative_x()
            self.update_pixel_x()
            return True
        return super(DragBarHorizontal, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.is_dragged = False
            return True
        return super(DragBarHorizontal, self).on_touch_up(touch)

    def update_relative_x(self):
        """Update the relative position (0 to 1) based on the widget's current position."""
        if self.parent and (self.parent.width - self.width) > 0:
            # Safely calculate relative_x only if the parent size is valid
            self.relative_x = self.x / (self.parent.width - self.width)
        else:
            # Default to 0 if the size is invalid
            self.relative_x = 0

    def update_pixel_x(self):
        """Update the pixel position based on the widget's current position within the parent."""
        if self.parent and (self.parent.width - self.width) > 0:
            # Safely calculate the pixel position in absolute terms
            self.pixel_x = self.relative_x * (self.parent.width - self.width)
            if self.text_widget:
                self.text_widget.scroll_x = self.pixel_x
                self.text_widget._trigger_update_graphics()
        else:
            # Default to 0 if the size is invalid
            self.pixel_x = 0
            if self.text_widget:
                self.text_widget.scroll_x = self.pixel_x
                self.text_widget._trigger_update_graphics()

class DragBarVertical(Widget):
    touch_y = NumericProperty(0)
    scroll_widget = ObjectProperty(None)
    relative_y = NumericProperty(0)  # The relative position between 0 and 1 for vertical movement
    text_widget = None
    is_dragged = False

    def update_height(self, text_widget):
        self.text_widget = text_widget
        # if the codeinput text is cleared before its updated, just return
        if not text_widget.text:
            return
        
        label = Label(text=text_widget.text, 
                      font_name=text_widget.font_name, 
                      font_size=text_widget.font_size)
        
        # Get the height of the text using the label's texture with delay to let the label render
        Clock.schedule_once(lambda dt: self.update_bar_height(label), 0)
    
    def update_bar_height(self, label):
        text_height = label.texture_size[1]
        if text_height != 0:
            new_size = self.parent.height / text_height
            self.size_hint_y = new_size if new_size <= 1 else 1
            # Reset scroll bar position
            Clock.schedule_once(lambda dt: self.update_from_scroll(), 0)

    def update_from_scroll(self):
        if not self.is_dragged and self.text_widget is not None:
            relative_y = self.text_widget.scroll_y / (self.text_widget.minimum_height - self.text_widget.height) if (self.text_widget.minimum_height - self.text_widget.height) > 0 else 0
            if self.parent and (self.parent.height - self.height) > 0:
                # Calculate the y position based on the relative_y value (0 to 1)
                self.y = (1 - relative_y) * (self.parent.height - self.height)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Grab the touch so the widget will receive the touch events even if the touch leaves its bounds
            touch.grab(self)
            self.is_dragged = True
            self.touch_y = touch.y
            return True
        return super(DragBarVertical, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # Calculate the new position
            new_y = self.y + (touch.y - self.touch_y)
            parent = self.parent
            if parent:
                # Constrain within the parent's bounds
                if new_y < 0:
                    new_y = 0
                elif new_y + self.height > parent.height:
                    new_y = parent.height - self.height

            # Update the widget's position
            self.y = new_y
            self.touch_y = touch.y

            # Calculate and update the relative position
            self.update_relative_y()
            self.update_pixel_y()
            return True
        return super(DragBarVertical, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self.is_dragged = False
            return True
        return super(DragBarVertical, self).on_touch_up(touch)

    def update_relative_y(self):
        """Update the relative position (0 to 1) based on the widget's current vertical position."""
        if self.parent and (self.parent.height - self.height) > 0:
            # Safely calculate relative_y only if the parent size is valid
            self.relative_y = self.y / (self.parent.height - self.height)
        else:
            # Default to 0 if the size is invalid
            self.relative_y = 0

    def update_pixel_y(self):
        """Update the pixel position based on the widget's current position within the parent."""
        if self.parent and (self.parent.height - self.height) > 0:
            # Invert the relative_y to get the correct pixel position
            self.pixel_y = (1 - self.relative_y) * (self.text_widget.minimum_height - self.text_widget.height)
            
            if self.text_widget:
                # Scroll in the direction matching user expectations
                self.text_widget.scroll_y = self.pixel_y
                self.text_widget._trigger_update_graphics()
        else:
            self.pixel_y = 0
            if self.text_widget:
                self.text_widget.scroll_y = self.pixel_y
                self.text_widget._trigger_update_graphics()



    