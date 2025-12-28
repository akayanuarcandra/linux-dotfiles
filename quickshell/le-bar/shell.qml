import Quickshell
import Quickshell.Io
import QtQuick

Scope {
    Variants {
        model: Quickshell.screens

        delegate: Component {
            PanelWindow {
                // the screen from the screens list will be injected into this
                // property
                required property var modelData

                // we can then set the window's screen to the injected property
                screen: modelData
                
                anchors {
                    top: true
                    left: true
                    bottom: true
                }

                implicitWidth: 30

                Text {
                    text: Qt.formatDateTime(clock.date, "hh")
                }

                Text {
                    text: Qt.formatDateTime(clock.date, "mm")
                }
            }
        }
    }
    SystemClock {
        id: clock
        precision: SystemClock.Seconds
    }
}
