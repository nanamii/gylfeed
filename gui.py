from gi.repository import Gtk

def close_window(window):
    print("Window closed")
    Gtk.main_quit()

def show_label(button, label):
    label.set_text("Button geklickt")
    print("Tralala")

window = Gtk.Window(title = "gylfeed")
window.set_position(Gtk.WindowPosition.CENTER)
window.set_default_size(1200,800)
window.connect("destroy", close_window)

box = Gtk.Box()
window.add(box)

box_inner = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
box_inner2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
box_inner3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
box.pack_start(box_inner2, False, False, 10)
box.pack_start(box_inner, True, True, 5)
box.pack_start(box_inner3, False, False, 10)

label = Gtk.Label("Label-Text")
button1 = Gtk.Button("klick mich")
button1.connect("clicked", show_label, label)
box_inner3.pack_start(button1, False, False, 5)
box_inner3.pack_start(label, False, False, 0)

button3 = Gtk.Button("Button innerBox")
box_inner3.pack_start(button3, False, False, 10)

###############################################
liststore = Gtk.ListStore(str,str,str)
treeIter = liststore.append(["A","B","C"])
liststore.append(["A1","B1","C1"])

view = Gtk.TreeView(model = liststore)
renderer = Gtk.CellRendererText()
column1 = Gtk.TreeViewColumn("Title", renderer, text = 0)
column2 = Gtk.TreeViewColumn("Date", renderer, text = 1)
column3 = Gtk.TreeViewColumn("Author", renderer, text = 2)
view.append_column(column1)
view.append_column(column2)
view.append_column(column3)

##############################################
liststore2 = Gtk.ListStore(str)
treeIter2 = liststore2.append(["Sueddeutsche"])
liststore2.append(["Golem"])

view2 = Gtk.TreeView(model = liststore2)
renderer2 = Gtk.CellRendererText()
column11 = Gtk.TreeViewColumn("Quelle", renderer, text = 0)
view2.append_column(column11)

#############################################
liststore3 = Gtk.ListStore(str)
treeIter3 = liststore3.append(["Das ist der Plot ..."])
liststore3.append(["... und noch mehr vom Plot"])

view3 = Gtk.TreeView(model = liststore3)
renderer3 = Gtk.CellRendererText()
column111 = Gtk.TreeViewColumn("Plottest", renderer, text = 0)
view3.append_column(column111)


box_inner2.pack_start(view2, True, True, 10)
box_inner.pack_start(view, True, True, 10)
box_inner3.pack_start(view3, True, True, 10)

window.show_all()
#mainloop
Gtk.main()




