built_modules = list(name for name in
    "Core;Gui;Widgets;PrintSupport;Sql;Network;Test;Concurrent;Designer;Xml;Help;OpenGL;OpenGLWidgets;Qml;Quick;QuickControls2;QuickWidgets;Scxml;StateMachine;Charts;Svg;SvgWidgets;DataVisualization;UiTools;AxContainer;3DCore;3DRender;3DInput;3DLogic;3DAnimation;3DExtras"
    .split(";"))

shiboken_library_soversion = str(6.1)
pyside_library_soversion = str(6.1)

version = "6.1.0"
version_info = (6, 1, 0, "", "")

__build_date__ = '2021-05-12T08:51:57+00:00'




__setup_py_package_version__ = '6.1.0'
