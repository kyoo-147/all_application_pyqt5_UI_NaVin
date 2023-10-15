from winotify import Notification, audio

# Notification template
toast = Notification(app_id="windows app",
                     title="Winotify Test Toast",
                     msg="New Notification!",
                     icon=r"c:\path\to\icon.png",
                     duration="short")

toast.set_audio(audio.Default, loop=False)

toast.show()