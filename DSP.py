import dearpygui.dearpygui as dpg
import numpy as np
import time
from PIL import Image
from tkinter import filedialog, Tk

dpg.create_context()

# Spinning Cat :)

gif = Image.open("spinning-cat.gif")
frames = []
try:
    while True:
        frame = gif.copy().convert("RGBA").resize((150,150))
        width, height = frame.size
        data = (np.asarray(frame, dtype=np.float32) / 255.0).ravel()
        frames.append((width, height, data))
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

current_frame = 0
frame_count = len(frames)
width, height, first_data = frames[0]

with dpg.texture_registry():
    texture_id = dpg.add_dynamic_texture(width, height, first_data, tag="spinning_cat")

# Plot Theme

with dpg.theme() as global_plot:
    with dpg.theme_component(dpg.mvStemSeries):
        dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Circle, category=dpg.mvThemeCat_Plots)
        dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)

    with dpg.theme_component(dpg.mvPlot):
        dpg.add_theme_color(dpg.mvPlotCol_PlotBg, (220, 240, 250), category=dpg.mvThemeCat_Plots)
        dpg.add_theme_color(dpg.mvPlotCol_AxisGrid, (0, 0, 0, 100), category=dpg.mvThemeCat_Plots)  

dpg.bind_theme(global_plot)

dpg.create_viewport(title='DSP Project', width=1300, height=800)

# Constants

TASKS = ["Task 1", "Task 2", "Task 3"]
N_SAMPLES = None
SIGNALS = {}

# Helper functions

def select_task(sender, app_data):
    for task in TASKS:
        dpg.configure_item(task, show=(task == app_data))

SIG_NUM = 0
def sig_name():
    global SIG_NUM
    SIG_NUM += 1
    return f"Sig_{SIG_NUM}"

def clear_signals():
    dpg.delete_item("y_axis", children_only=True)

def delete_signal(sender, app_data, name):
    for id, item in get_id_labels("signals_list"):
        if item == name:
            dpg.delete_item(id)
    dpg.configure_item(dpg.get_item_parent(sender), show=False)

def read_signal():
    global N_SAMPLES, SIGNAL
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(
        title="Select Target Image"
    )
    root.destroy()
    with open(path, "r") as file:
        content = file.read()
        content = content.split("\n")
        N_SAMPLES = content[2]
        new_sig = {float(n): float(x) for n,x in [s.split(" ") for s in content[3:]]}
    
    name = sig_name()
    register_signal(new_sig, name)

def register_signal(signal, name):
    if name in SIGNALS.keys():
        return
    SIGNALS[name] = signal
    new_sig = dpg.add_selectable(label=name, parent="signals_list")
    with dpg.popup(dpg.last_item(), min_size=[0, 0]):
        dpg.add_button(label="Remove signal", callback=delete_signal, user_data=name)
        dpg.add_button(label="Export signal", callback=export_signal, user_data=name)
    with dpg.drag_payload(parent=new_sig, drag_data=name, payload_type="signal"):
        dpg.add_text(name)

def export_signal(sender, app_data, name):
    signal = ["0", "0", f"{len(SIGNALS[name])}"] + [f"{int(n)} {int(x)}" for n,x in SIGNALS[name].items()]
    output = "\n".join(signal)
    with open(f"{name}.txt", "w", encoding="utf-8") as file:
        file.write(output)
    dpg.configure_item(dpg.get_item_parent(sender), show=False)

def display_signals():
    global SIGNALS
    if len(SIGNALS) == 0:
        return
    for name in SIGNALS.keys():
        drop_on_plot(sender=None, app_data=name)

def get_values(container):
    return [dpg.get_value(i) for i in dpg.get_item_children(container, 1)]

def get_id_labels(container):
    return [(i, dpg.get_item_label(i)) for i in dpg.get_item_children(container, 1)]

def drop_on_window(sender, app_data):
    if app_data in get_values(sender):
        return
    text = dpg.add_text(app_data, parent=sender)
    with dpg.popup(dpg.last_item(), min_size=[0, 0]) as popup:
        dpg.add_button(label="Remove signal", callback=lambda: (dpg.delete_item(text), dpg.configure_item(popup, show=False)))

def drop_on_plot(sender, app_data):
    if dpg.does_item_exist(app_data):
        return
    sig = SIGNALS[app_data]
    xs, ys = list(sig.keys()), list(sig.values())
    dpg.add_stem_series(xs, ys, label=app_data, parent="y_axis", tag=app_data)
    dpg.add_button(label=f"Delete {app_data}", parent=dpg.last_item(), callback=lambda: dpg.delete_item(app_data))
    dpg.fit_axis_data("x_axis")
    dpg.fit_axis_data("y_axis")

def on_resize():
    dpg.configure_item("Main task", height=int(dpg.get_viewport_client_height() * 0.5))

#TODO Task 1:

def add_signals():
    names = get_values("added-sigs")

    tba_signals = tuple([SIGNALS[n] for n in names])
    indices = tba_signals[0].keys()
    for i in range(1,len(tba_signals)):
        indices = sorted(set(indices) | set(tba_signals[i].keys()))

    sum_signal = {}
    for i in indices:
        sum_signal[i] = sum([sig[i] if i in sig.keys() else 0 for sig in tba_signals])

    register_signal(sum_signal, "+".join(names))

def subtract_signals():
    names = get_values("subtracted-sigs")
    
    tbs_signals = tuple([SIGNALS[n] for n in names])
    indices = tbs_signals[0].keys()
    for i in range(1,len(tbs_signals)):
        indices = sorted(set(indices) | set(tbs_signals[i].keys()))

    sub_signal = {}
    for i in indices:
        sub_signal[i] = tbs_signals[0][i] - sum([sig[i] if i in sig.keys() else 0 for sig in tbs_signals[1:]])

    register_signal(sub_signal, "-".join(names))

def amplify_signal():
    name = get_values("amplified-sig")
    if not name:
        return
    name = name[0]
    sig = SIGNALS[name]
    value = float(dpg.get_value("amp_val"))
    amp_sig = {n: x*value for n,x in sig.items()}

    register_signal(amp_sig, f"{name}×{value}")

def shift_signal():
    name = get_values("shifted-sig")
    if not name:
        return
    name = name[0]
    sig = SIGNALS[name]
    k = float(dpg.get_value("shift_val"))
    shift_sig = {n-k: sig[n] for n in sig.keys()}

    register_signal(shift_sig, f"{name}^({k})")

def reverse_signal():
    name = get_values("reversed-sig")
    if not name:
        return
    name = name[0]
    sig = SIGNALS[name]
    rev_sig = {-n: sig[n] for n in list(sig.keys())[::-1]}

    register_signal(rev_sig, f"~{name}")

#TODO Task 2:



#TODO Task 3



# Main GUI
with dpg.window(tag="Primary Window"):
    with dpg.group(horizontal=True):
        with dpg.child_window(tag="Task selector", width=165):
            with dpg.collapsing_header(label="Spinning cat", default_open=True):
                dpg.add_image("spinning_cat")
            with dpg.collapsing_header(label="Tasks", leaf=True):
                dpg.add_radio_button(
                    items=TASKS,
                    callback=select_task
                )

        with dpg.group():
            with dpg.child_window(tag="Main task", width=-1, height=500):
                # Task 1
                with dpg.group(tag="Task 1"):
                    with dpg.table(header_row=False):
                        dpg.add_table_column(label="Add")
                        dpg.add_table_column(label="Subtract")
                        dpg.add_table_column(label="Multiply")
                        dpg.add_table_column(label="Delay/Advance")
                        dpg.add_table_column(label="Reverse")

                        with dpg.table_row():
                            with dpg.table_cell():
                                dpg.add_text("Signals to add:")
                                dpg.add_child_window(height=130, drop_callback=drop_on_window, payload_type="signal", tag="added-sigs")
                                dpg.add_button(label="Add", callback=add_signals)
                            
                            with dpg.table_cell():
                                with dpg.group(horizontal=True):
                                    dpg.add_text("Signals to subtract:")
                                dpg.add_child_window(height=130, drop_callback=drop_on_window, payload_type="signal", tag="subtracted-sigs")
                                dpg.add_button(label="Subtract", callback=subtract_signals)

                            with dpg.table_cell():
                                dpg.add_text("Signal to amplify:")
                                dpg.add_child_window(height=80, drop_callback=lambda s, a: (dpg.delete_item(s, children_only=True), drop_on_window(s, a)), payload_type="signal", tag="amplified-sig")
                                dpg.add_text("Amplification value:")
                                dpg.add_input_text(tag="amp_val")
                                dpg.add_button(label="Amplify", callback=amplify_signal)

                            with dpg.table_cell():
                                with dpg.group(horizontal=True):
                                    dpg.add_text("Signal to delay/advance:")
                                dpg.add_child_window(height=80, drop_callback=lambda s, a: (dpg.delete_item(s, children_only=True), drop_on_window(s, a)), payload_type="signal", tag="shifted-sig")
                                dpg.add_text("Shift value (K):")
                                dpg.add_input_text(tag="shift_val")
                                dpg.add_button(label="Shift", callback=shift_signal)

                            with dpg.table_cell():
                                with dpg.group(horizontal=True):
                                    dpg.add_text("Signal to reverse:")
                                dpg.add_child_window(height=80, drop_callback=lambda s, a: (dpg.delete_item(s, children_only=True), drop_on_window(s, a)), payload_type="signal", tag="reversed-sig")
                                dpg.add_button(label="Reverse", callback=reverse_signal)

                # Task 2
                with dpg.group(tag="Task 2", show=False):
                    dpg.add_text("Under construction :)")

                # Task 3
                with dpg.group(tag="Task 3", show=False):
                    dpg.add_text("Under construction :)")

            with dpg.group(tag="Signal display", horizontal=True):
                with dpg.child_window(width=270, height=-1):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Read Signal", callback=read_signal)  

                    with dpg.child_window(height=275):
                        dpg.add_group(tag="signals_list")
                    
                    dpg.add_button(label="Show all signals", width=-1, callback=display_signals)
                    dpg.add_button(label="Clear all signals", width=-1, callback=clear_signals)
                
                with dpg.child_window():
                    with dpg.plot(label="Signal display", width=-1, height=-1, drop_callback=drop_on_plot, payload_type="signal"):
                        dpg.add_plot_legend()
                        dpg.add_plot_axis(dpg.mvXAxis, label="n", tag="x_axis")
                        dpg.add_plot_axis(dpg.mvYAxis, label="x", tag="y_axis")

        
        
dpg.set_viewport_resize_callback(on_resize)

last = time.time()
FRAME_DELAY = 0.04

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
on_resize()
while dpg.is_dearpygui_running():
    now = time.time()
    if now - last >= FRAME_DELAY:
        current_frame = (current_frame + 1) % frame_count
        dpg.set_value("spinning_cat", frames[current_frame][2])
        last = now
    dpg.render_dearpygui_frame()
dpg.destroy_context()