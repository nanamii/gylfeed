from gi.repository import Gtk

#Callback-Funktion
def print_hello(button):
    print("Hello")

button = Gtk.Button("Print Hello")          # Erstellung eines Buttons
button.connect('clicked', print_hello)      # Verknüpfen mit Signal 'clicked'
                                            # und Angabe der Callback-Funktion

window = Gtk.Window()                       # Erstellung eines Fensters
window.add(button)                          # Hinzufügen von Button zu Fenster
window.show_all()                           # Alle Bestandteile von window anzeigen

Gtk.main()                                  # Gtk Main-Loop
