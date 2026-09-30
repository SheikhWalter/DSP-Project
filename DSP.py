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

dpg.create_viewport(title='DSP Project', width=1000, height=800)

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
        name = sig_name()
        SIGNALS[name] = {float(n): float(x) for n,x in [s.split(" ") for s in content[3:]]}
    
    new_sig = dpg.add_selectable(label=name, parent="signals_list")
    with dpg.drag_payload(parent=new_sig, drag_data=name, payload_type="signal"):
        dpg.add_text(name)

def display_signal():
    global SIGNALS
    if len(SIGNALS) == 0:
        return
    for name in SIGNALS.keys():
        if dpg.does_item_exist(name):
            continue
        sig = SIGNALS[name]
        xs, ys = list(sig.keys()), list(sig.values())
        dpg.add_stem_series(list(xs), list(ys), label=name, parent="y_axis", tag=name)
        dpg.fit_axis_data("x_axis")
        dpg.fit_axis_data("y_axis")

def on_drop(sender, app_data):
    if dpg.does_item_exist(app_data):
        return
    sig = SIGNALS[app_data]
    xs, ys = list(sig.keys()), list(sig.values())
    dpg.add_stem_series(xs, ys, label=app_data, parent="y_axis", tag=app_data)
    dpg.fit_axis_data("x_axis")
    dpg.fit_axis_data("y_axis")

def on_resize():
    dpg.configure_item("Main task", height=int(dpg.get_viewport_client_height() * 0.5))

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
                    pass

                # Task 2
                with dpg.group(tag="Task 2", show=False):
                    dpg.add_text("Under construction :)")

                # Task 3
                with dpg.group(tag="Task 3", show=False):
                    dpg.add_text("Under construction :)")

            with dpg.group(tag="Signal display", horizontal=True):
                with dpg.child_window(width=210, height=-1):
                    with dpg.group(horizontal=True):
                        dpg.add_button(label="Select Signal", callback=read_signal)  

                    with dpg.child_window(height=275):
                        dpg.add_group(tag="signals_list")
                    
                    dpg.add_button(label="Show all signals", width=-1, callback=display_signal)
                    dpg.add_button(label="Clear all signals", width=-1, callback=clear_signals)
                
                with dpg.child_window():
                    with dpg.plot(label="Signal", width=-1, height=-1, drop_callback=on_drop, payload_type="signal"):
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