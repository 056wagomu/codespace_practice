# XRDで取った回折データとICSDからとったデータをグラフにして比較する
# XRDからのデータはtxt　ICSDからはcsv

# %%
import pandas as pd
from bokeh.models import ColumnDataSource, CrosshairTool, HoverTool, Range1d, RedoTool, UndoTool
from bokeh.plotting import figure, output_file, save

# %%
# XRDからのデータ
#今回は炭素ドープ2度焼き後データ
XRD_data_path = "/workspaces/codespace_practice/XRD_graph/XRD_data/Bi2ZnB2O7_XRD/Bi2ZnB1.6C0.4O7_2doyaki.txt"
XRD_data = pd.read_csv(XRD_data_path, sep=",")

#今回bはGaドープのデータ
XRD_data_B = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Bi2ZnB2O7_XRD/Bi2Zn0.8Ga0.2B2O7_2doyaki.txt", sep=",")

#今回Cは3個目のデータ
XRD_data_C = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/Bi2ZnB2O7_XRD/Bi2ZnB2O7_3kome.txt", sep=",")

# ICSDからのデータ
ICSD_data = pd.read_csv("/workspaces/codespace_practice/XRD_graph/XRD_data/ICSD/B2ZnBi2O7_xy_ICSD.csv")

# グラフとして見やすくするためにそれぞれの最大値をもとにスケーリング ICSDのほうがでかいのでこっちを小さくする
XRD_max = XRD_data["Intensity"].max()

XRD_B_max = XRD_data_B["Intensity"].max()

XRD_C_max = XRD_data_C["Intensity"].max()

ICSD_max = ICSD_data["Intensity"].max()

ICSD_data["Intensity"] = ICSD_data["Intensity"] * XRD_max / ICSD_max

XRD_data_B["Intensity"] = XRD_data_B["Intensity"] * XRD_max / XRD_B_max

XRD_data_C["Intensity"] = XRD_data_C["Intensity"] * XRD_max / XRD_C_max


# %%
# bokehで描画 他ICSDのデータとの比較
# 目的は物質が出来ているかどうか

source_XRD = ColumnDataSource(data=dict(x=XRD_data["2theta"], y=XRD_data["Intensity"]))
source_ICSD = ColumnDataSource(data=dict(x=ICSD_data["2theta"], y=ICSD_data["Intensity"]))
source_XRD_B = ColumnDataSource(data=dict(x=XRD_data_B["2theta"], y=XRD_data_B["Intensity"]))
source_XRD_C = ColumnDataSource(data=dict(x=XRD_data_C["2theta"], y=XRD_data_C["Intensity"]))


# グラフの範囲を設定
x_range = Range1d(start=10, end=60, bounds=(10, 60))
y_range = Range1d(start=0, end=XRD_max * 1.1, bounds="auto")
p = figure(title="Bi2ZnB2O7 XRD data", x_axis_label="2theta", y_axis_label="Intensity", x_range=x_range, width=1200, height=400, y_range=y_range)

p.line("x", "y", source=source_XRD, legend_label="XRD_Bi2ZnB2O7_Cdope", line_width=1, color="blue")
p.line("x", "y", source=source_ICSD, legend_label="ICSD_Bi2ZnB2O7", line_width=1, color="red")
p.line("x", "y", source=source_XRD_B, legend_label="XRD_Bi2Zn0.8Ga0.2B2O7_no3", line_width=1, color="green")
p.line("x", "y", source=source_XRD_C, legend_label="XRD_Bi2ZnB2O7_3kome", line_width=1, color="orange")

p.add_tools(HoverTool(), CrosshairTool(), UndoTool(), RedoTool())
p.legend.click_policy = "hide"

output_file("/workspaces/codespace_practice/XRD_graph/Bi2ZnB2O7_Cdope_hikaku.html")
save(p)
# %%
