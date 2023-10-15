import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.0


ApplicationWindow {


    width: 1014
    height: 547
  //  property alias save: save
    opacity: 1
    visible: true
    id: main
    property var p: ""



        FileDialog {
        id: fileDialog
        nameFilters:"*.wav"
        title: "Please choose a file"
        folder: shortcuts.home
        onAccepted: {
           p=fileDialog.fileUrls
           clock.start_clock(fileDialog.fileUrls)
           console.log("You chose: " + fileDialog.fileUrls)

        }


    }
      Connections {
              target: clock

              onRecieveTime: {
                 p = _predict
                lbl.text=p
                lbl2.text=p
              }

          }














    SwipeView {
        id: swipeView
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        anchors.fill: parent
        currentIndex: 1


        Page {
            id: page
            width: 1014
            height: 547
            Image {
                id: offlineImage
                x: 0
                y: 0
                width: 1020
                height: 547
                visible: true
                source: "Untitled.png"
            }
            Button {
                id: browseOffline
                x: 30
                y: 66
                width: 244
                height: 70
                text: qsTr("Browse")
                onClicked: fileDialog.open()

                contentItem: Text {
                    color: "#0c20aa"
                    text: browseOffline.text
                    font.family: "Arial"
                    font.pointSize: 42
                    opacity: enabled ? 1.0 : 0.3
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                background: Rectangle {
                    implicitWidth: 100
                    implicitHeight: 40
                    opacity: enabled ? 1 : 0.3
                    border.color: "#f00303"
                    border.width: 3
                    radius: 4
                }
            }

            Button {
                id: playOffline
                x: 30
                y: 182
                width: 244
                height: 70
                text: qsTr("Play")
                contentItem: Text {
                    color: "#0c20aa"
                    text: playOffline.text
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pointSize: 42
                    opacity: enabled ? 1.0 : 0.3
                    elide: Text.ElideRight
                    font.family: "Arial"
                }
                background: Rectangle {
                    radius: 4
                    implicitHeight: 40
                    border.color: "#f00303"
                    opacity: enabled ? 1 : 0.3
                    border.width: 3
                    implicitWidth: 100
                }
                onClicked:{

                 clock.play()
                }
            }

            Button {
                id: predictOffline
               // onClicked:{swipeView.currentIndex = 3}
                x: 30
                y: 297
                width: 244
                height: 70
                text: qsTr("Predict")
                onClicked:{

                      clock.predict()

                   // swipeView.currentIndex = 3
                }

                contentItem: Text {
                    color: "#0c20aa"
                    text: predictOffline.text
                    verticalAlignment: Text.AlignVCenter
                    horizontalAlignment: Text.AlignHCenter
                    font.pointSize: 42
                    opacity: enabled ? 1.0 : 0.3
                    elide: Text.ElideRight
                    font.family: "Arial"
                }
                background: Rectangle {
                    radius: 4
                    implicitHeight: 40
                    border.color: "#f00303"
                    opacity: enabled ? 1 : 0.3
                    border.width: 3
                    implicitWidth: 100
                }
            }
            Label { // Answer
                x: 30
                y: 406
                width: 296
                height: 76
                id: lbl

                text : qsTr ( "" )
                font.pointSize: 49 // Change it with the prediction
                color : "#21be2b"
            }

        }

        Page {
            visible: true
            Image {
                id: welcomeImage
                width: 1014
                height: 547
                opacity: 1
                source: "try2.PNG"
            }
            Button {
                id: button
                onClicked:{swipeView.currentIndex = swipeView.currentIndex+1}
                x: 602
                y: 420
                width: 268
                height: 82
                highlighted: false
                opacity: 1
                background: Rectangle {
                    color: "#33f88913"
                    radius: 2
                    opacity: 0.5
                    implicitWidth: 100
                    implicitHeight: 40
                }
                contentItem: Text {
                    color: "#f5a016"
                    text: "Online"
                    textFormat: Text.AutoText
                    opacity: 1
                    renderType: Text.QtRendering
                    font.pointSize: 46
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideLeft
                }

            }

            Button {
                id: button1
                onClicked:{swipeView.currentIndex = swipeView.currentIndex-1}
                x: 148
                y: 420
                width: 268
                height: 82
                highlighted: false
                opacity: 1
                background: Rectangle {
                    color: "#33f88913"
                    radius: 2
                    opacity: 0.5
                    implicitWidth: 100
                    implicitHeight: 40
                }
                contentItem: Text {
                    color: "#f5a016"
                    text: "Offline"
                    textFormat: Text.AutoText
                    opacity: 1
                    renderType: Text.QtRendering
                    font.pointSize: 46
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideLeft
                }

            }

        }

        Page {

            width: 300
            height: 300



            Image {
                id: onlineImage
                x: 0
                y: 0
                width: 1014
                height: 547
                opacity: 1
                source: "try.PNG"
            }

            Frame {
                id: frame
                x: 610
                y: 0
                width: 404
                height: 547
                background : Rectangle {
                    color : "#80000000"
                    opacity: 1
                }

                Button {
                    id: browseOnline
                    x: 64
                    y: 30
                    width: 255
                    height: 54
                    onClicked: fileDialog.open()

                    hoverEnabled: false
                   // enabled: false
                    font.pointSize: 42
                    focusPolicy: Qt.StrongFocus
                    background: Rectangle {
                        color: "#80fafafa"
                        radius: 2
                        opacity: 0.5
                        implicitWidth: 100
                        implicitHeight: 40
                    }
                    contentItem: Text {
                        color: "white"
                        text: "Browse"
                        textFormat: Text.AutoText
                        opacity: 1
                        renderType: Text.QtRendering
                        font.pointSize: 35
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideLeft
                    }

                }

                Button {
                    id: play
                    x: 64
                    y: 251
                    width: 255
                    height: 54
                    onClicked:{
                    clock.play()
                    }

                    contentItem: Text {
                        color: "#ffffff"
                        text: "Play"
                        elide: Text.ElideLeft
                        textFormat: Text.AutoText
                        renderType: Text.QtRendering
                        font.pointSize: 35
                        verticalAlignment: Text.AlignVCenter
                        opacity: 1
                        horizontalAlignment: Text.AlignHCenter
                    }
                    focusPolicy: Qt.StrongFocus
                    background: Rectangle {
                        color: "#80fafafa"
                        radius: 2
                        implicitWidth: 100
                        implicitHeight: 40
                        opacity: 0.5
                    }
                    //font.pointSize: 35
                    hoverEnabled: false
                    //enabled: false
                }

                Button {
                    id: record
                    x: 64
                    y: 137
                    width: 255
                    height: 54
                    contentItem: Text {
                        color: "#ffffff"
                        text: "Record"
                        elide: Text.ElideLeft
                        textFormat: Text.AutoText
                        renderType: Text.QtRendering
                        font.pointSize: 35
                        verticalAlignment: Text.AlignVCenter
                        opacity: 1
                        horizontalAlignment: Text.AlignHCenter
                    }
                    focusPolicy: Qt.StrongFocus
                    background: Rectangle {
                        color: "#80fafafa"
                        radius: 2
                        implicitWidth: 100
                        implicitHeight: 40
                        opacity: 0.5
                    }
                    onClicked:{

                     // clock.play()

                     clock.record()

                }

                    //font.pointSize: 42
                    hoverEnabled: false
                   // enabled: false
                }



                Button {
                    id: predict
                    x: 64
                    y: 368
                    width: 255
                    height: 54
                      onClicked:{

                    clock.predict()
                   // swipeView.currentIndex = 3
                }
                    contentItem: Text {
                        color: "#ffffff"
                        text: qsTr("Predict")
                        elide: Text.ElideLeft
                        textFormat: Text.AutoText
                        renderType: Text.QtRendering
                        font.pointSize: 35
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        opacity: 1
                    }
                    focusPolicy: Qt.StrongFocus
                    background: Rectangle {
                        color: "#80fafafa"
                        radius: 2
                        implicitWidth: 100
                        implicitHeight: 35
                        opacity: 0.5
                    }
                   // enabled: false
                    hoverEnabled: false
                }

                Label { // Answer
                    x: 64
                    y: 440
                    width: 296
                    height: 76
                    id: lbl2

                    text : qsTr ( "" )
                    font.pointSize: 49 // Change it with the prediction
                    color : "#21be2b"
                }
            }
        }
        Page {

        }
    }


}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}
}
##^##*/
