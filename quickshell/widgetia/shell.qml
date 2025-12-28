import Quickshell // for PanelWindow
import QtQuick // for Text

PanelWindow {
  implicitHeight: 500
  implicitWidth: 200

  Text {
    // center the bar in its parent component (the window)
    anchors.centerIn: parent

    text: "hello world"
  }
}