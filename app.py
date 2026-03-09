import rumps
import subprocess
import threading
import time


TIMERS = {
    "30 minutes": 30 * 60,
    "1 hour": 60 * 60,
    "2 hours": 2 * 60 * 60,
    "4 hours": 4 * 60 * 60,
    "Indefinitely": None,
}

ICON_AWAKE = "☕"
ICON_SLEEP = "💤"


class MacAwakeApp(rumps.App):
    def __init__(self):
        super().__init__(ICON_SLEEP, quit_button=None)

        self._caffeinate_proc = None
        self._timer_thread = None
        self._start_time = None
        self._duration = None          # seconds, or None = indefinite
        self._stop_event = threading.Event()

        # ---- menu items ----
        self.toggle_item = rumps.MenuItem("Keep Awake: OFF", callback=self.toggle)

        self.status_item = rumps.MenuItem("Idle")
        self.status_item.set_callback(None)   # not clickable

        timer_menu = rumps.MenuItem("Set Timer")
        self._timer_items = {}
        for label in TIMERS:
            item = rumps.MenuItem(label, callback=self._set_timer)
            self._timer_items[label] = item
            timer_menu.add(item)

        self.menu = [
            self.toggle_item,
            None,                          # separator
            self.status_item,
            None,
            timer_menu,
            None,
            rumps.MenuItem("Quit", callback=self._quit),
        ]

        # default timer selection
        self._selected_timer_label = "Indefinitely"
        self._timer_items[self._selected_timer_label].state = True

    # ------------------------------------------------------------------
    # Toggle awake / sleep
    # ------------------------------------------------------------------
    def toggle(self, _):
        if self._caffeinate_proc is None:
            self._start_awake()
        else:
            self._stop_awake()

    def _start_awake(self):
        duration = TIMERS[self._selected_timer_label]
        self._duration = duration
        self._start_time = time.time()
        self._stop_event.clear()

        cmd = ["caffeinate", "-di"]
        if duration:
            cmd += ["-t", str(duration)]
        self._caffeinate_proc = subprocess.Popen(cmd)

        self.title = ICON_AWAKE
        self.toggle_item.title = "Keep Awake: ON"

        # start background thread to update the status ticker
        self._timer_thread = threading.Thread(target=self._tick, daemon=True)
        self._timer_thread.start()

    def _stop_awake(self):
        self._stop_event.set()

        if self._caffeinate_proc:
            self._caffeinate_proc.terminate()
            self._caffeinate_proc = None

        self.title = ICON_SLEEP
        self.toggle_item.title = "Keep Awake: OFF"
        self.status_item.title = "Idle"
        self._start_time = None

    # ------------------------------------------------------------------
    # Background tick — updates elapsed time label & watches for timeout
    # ------------------------------------------------------------------
    def _tick(self):
        while not self._stop_event.is_set():
            elapsed = int(time.time() - self._start_time)

            if self._duration and elapsed >= self._duration:
                # timer expired
                rumps.notification(
                    "mac-awake",
                    "Timer expired",
                    "Your Mac can now go to sleep.",
                )
                self._stop_awake()
                return

            label = _fmt_elapsed(elapsed)
            if self._duration:
                remaining = _fmt_elapsed(self._duration - elapsed)
                label = f"Awake {label}  ({remaining} left)"
            else:
                label = f"Awake {label}"

            self.status_item.title = label
            time.sleep(5)

    # ------------------------------------------------------------------
    # Timer selection
    # ------------------------------------------------------------------
    def _set_timer(self, sender):
        # uncheck previous
        self._timer_items[self._selected_timer_label].state = False
        self._selected_timer_label = sender.title
        self._timer_items[self._selected_timer_label].state = True

        # if already running, restart with new duration
        if self._caffeinate_proc is not None:
            self._stop_awake()
            self._start_awake()

    # ------------------------------------------------------------------
    # Quit
    # ------------------------------------------------------------------
    def _quit(self, _):
        self._stop_awake()
        rumps.quit_application()


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def _fmt_elapsed(seconds: int) -> str:
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h}h {m:02d}m"
    if m:
        return f"{m}m {s:02d}s"
    return f"{s}s"


if __name__ == "__main__":
    MacAwakeApp().run()
