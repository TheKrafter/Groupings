# 
# Groupings - GTK4/Libadwaita GroupMe Client
# Copyright (c) 2024 Krafter - krafterdev.xyz
# Licensed subject to the MPL version 2.0 or Later
# 
from typing import List, Optional

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

""" LabelWithWidgets is ported from Tuba and Fractal
Tuba - https://github.com/GeopJr/Tuba/blob/cbf10b3bb8d1fe02d5cb0c0f56756d8fd862d2ea/src/Widgets/LabelWithWidgets.vala
Fractal - https://gitlab.gnome.org/GNOME/fractal/-/blob/3f8a7e8bd06441d83a5f052a2ae68d7d228dfcd0/src/components/label_with_widgets.rs

How to use:
Set `text` to the label's content but use the `placeholder` keyword where widgets should be placed.
Then use `set_children` with a list of Widgets in order of how they should be placed in the label.
There are some helper functions like `append_child` to add children and
`LabelWithWidgets.with_label_and_widgets` to construct it with the desired text and widgets. """

class LWWWidget:
    def __init__(self, widget: Gtk.Widget, width: int=0, height: int=0):
        self.widget = widget
        self.width = width
        self.height = height

class LabelWithWidgets(Gtk.Widget):
    def __init__(self):
        self.widgets: List[LWWWidget] = []
        
        self.label = Gtk.Label.new("")
        self.label.set_wrap(True)
        self.label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
        self.label.set_xalign(0.0)
        self.label.set_valign(Gtk.Align.START)
        self.label.set_use_markup(False)
        self.label.set_parent(self)
        self.label.connect("activate-link" ,self.activate_link)
    
    _placeholder: str = "<widget>"
    def get_placeholder(self):
        return self._placeholder
    def set_placeholder(self, value: str):
        self._placeholder = value
        self.update_label()
    
    _label_text: str = ""
    _text: str = ""
    def get_text(self):
        return self._text
    def set_text(self, value):
        _text = value
        self.update_label()
        self.label.notify_property("label")
    
    _ellipsize: bool = False
    def get_ellipsize(self):
        return self._ellipsize
    def set_ellipsize(self, value: bool):
        if self._ellipsize == value:
            return
        else:
            self._ellipsize = value
            self.update_label()
    
    _use_markup: bool = False
    def get_use_markup(self):
        return self._use_markup
    def set_use_markup(self, value: bool):
        self._use_markup = value
        self.label.use_markup = self._use_markup

    OBJECT_REPLACEMENT_CHARACTER: str = "\xEF\xBF\xBC"

    def allocate_shapes(self):
        child_size_changed = False
        
        if self.text == "":
            return
        if len(self.widgets) == 0:
            self.label.attributes = None
            return
        
        for i in range(0, len(self.widgets)):
            size, natural_size = widgets[i].widget.get_preferred_size()
            width = natural_size.width
            height = natural_size.height

            old_width: int = self.widgets[i].width
            old_height: int = self.widgets[i].height
            if old_width > 0 or old_height > 0:
                if old_width != width or old_height != height:
                    self.widgets[i].width = width
                    self.widgets[i].height = height
                    child_size_changed = True
            else:
                self.widgets[i].width = width
                self.widgets[i].height = height

                child_size_changed = True
        
        if not child_size_changed:
            return
        
        attrs = Pango.AttrList.new()
        index = 0

        for i in range(0, len(self.widgets)):
            index = self._label_text.find(self.OBJECT_REPLACEMENT_CHARACTER, index)
            if index < 0:
                break

            logical_rect = Pango.Rectangle(
                x = 0,
                y = -(self.widgets[i].height - (self.widgets[i].height / 4)) * Pango.SCALE,
                width = self.widgets[i].width * Pango.SCALE,
                height = self.widgets[i].width * Pango.SCALE,
            )

            shape = Pango.AttrShape.new(logical_rect, logical_rect)
            shape.start_index = index
            shape.end_index = index + len(self.OBJECT_REPLACEMENT_CHARACTER)
            attrs.insert(shape.copy())
        
        self.label.attributes = attrs
    
    def allocate_children(self):
        if len(self.widgets) == 0:
            return
        
        run_iter = self.label.get_layout()
        i = 0

        while True:
            run = run_iter.get_run_readonly()
            if run != null:
                extra_attrs = run.item.analysis.extra_attrs.copy()
                has_shape_attr = False
                for attr in extra_attrs:
                    if attr.as_shape() != None:
                        has_shape_attr = True
                        break
                
                if has_shape_attr:
                    if i < self.widgets.length:
                        logical_rect: Pango.Rectangle = run_iter.get_run_extents()

                        offset_x, offset_y = self.label.get_layout_offsets()
                        
                        self.widgets[i].widget.allocate(
                            self.pango_pixels(logical_rect.x) + offset_x,
                            self.pango_pixels(logical_rect.y) + offset_y,
                            -1,
                            None
                        )

                        i += 1
                    else:
                        break
    def size_allocate(self, width, height, baseline):
        self.label.allocate(width, height, baseline, None)
        self.allocate_children()
    
    def get_request_mode(self):
        return self.label.get_request_mode()
    
    def measure(orientation: Gtk.Orientation, for_size: int):
        self.allocate_shapes()
        return self.label.measure(orientation, for_size)
    
    def update_label(self):
        old_label = self.label.label
        old_ellipsize = self.label.get_ellipsize() == Pango.EllipsizeMode.END
        new_ellipsize = self.get_ellipsize()
        new_label = self._text.replace(self.get_placeholder(), self.OBJECT_REPLACEMENT_CHARACTER)

        if new_ellipsize:
            pos = new_label.find("\n")
            if pos >= 0:
                new_label = new_label[:pos] + "…"
        
        if old_ellipsize != new_ellipsize or old_label != new_label:
            if new_ellipsize:
                # Workaround: if both wrap and ellipsize are set, and there are
                #  widgets inserted, Gtk.Label reports and erroneous minimum width.
                self.label.wrap = False
                self.label.ellipsize = Pango.EllipsizeMode.END
            else:
                self.label.wrap = True
                self.label.wrap_mode = Pango.WrapMode.WORD_CHAR
            
            self._text = new_label
            self.label.label = self._text
            self._label_text = self.label.get_text()
            self.invalidate_child_widgets()
    
    def append_child(self, child):
        self.widgets.append(
            LWWWidget(child, 0, 0)
        )
        child.set_parent(self)
        self.invalidate_child_widgets()
    
    @classmethod
    def with_label_and_widgets(self, t_text: str, t_widgets: List[Gtk.Widget]):
        for widget in t_widgets:
            self.append(widget)
        
        self.set_text(t_text)
    
    def set_children(self, t_widgets: List[Gtk.Widget]):
        for child in self.widgets:
            child.widget.unparent()
            child.widget.destroy()
        
        self.widgets = []
        for widget in t_widgets:
            self.append_child(widget)
    
    def invalidate_child_widgets(self):
        for i in range(0, len(self.widgets)):
            self.widgets[i].width = 0
            self.widgets[i].height = 0
        self.allocate_shapes()
        self.queue_resize()
    
    def pango_pixels(self, d) -> int:
        return (d + 512) >> 10
    
    def add_child(self, builder: Gtk.Builder, child: GLib.Object, type: str):
        widget: Gtk.Widget = Gtk.Widget(child)
        if widget != None:
            super().append_child(widget)
        else:
            self.parent.add_child(builder, child, type)
    
    def get_single_line_mode(self):
        return self.label.get_single_line_mode()
    def set_single_line_mode(self, value: bool):
        return self.label.set_single_line_mode(value)
    
    def get_xalign(self):
        return self.label.get_xalign()
    def set_xalign(self, value: float):
        return self.label.set_xalign(value)
    
    def get_selectable(self):
        return self.label.get_selectable()
    def set_selectable(self, value: bool):
        return self.label.set_selectable(value)
    
    def get_lines(self):
        return self.label.get_lines()
    def set_lines(self, value: int):
        return self.label.set_lines(value)
    
    def get_justify(self):
        return self.label.get_justify()
    def set_justify(self, value: Gtk.Justification):
        return self.label.set_justify(value)
