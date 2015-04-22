from gi.repository import Gtk


def print_entry(entry, buff):
    print(entry.get_text())
    oldText = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), True)
    buff.set_text(oldText + "\n" + entry.get_text())
    entry.set_text("")

builder = Gtk.Builder()
builder.add_from_file("chat.glade")

window = builder.get_object("window1")
window.connect("destroy", Gtk.main_quit)

buff = builder.get_object("textbuffer1")

entry = builder.get_object("entry1")
entry.connect("activate", print_entry, buff)









window.show_all()

Gtk.main()
