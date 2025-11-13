from PyQt6.QtCore import pyqtSlot, QEvent, QObject, Qt, QTimer

class HoverEventFilter(QObject):
    """Event filter to track hover, focus, and selection events on number fields."""
    def __init__(self, field_name: str, label_widget=None, tts_callback=None, tts_stop_callback=None):
        super().__init__()
        self.field_name = field_name
        self.label_widget = label_widget
        self.tts_callback = tts_callback
        self.tts_stop_callback = tts_stop_callback
        self.is_hovered = False
        self.is_focused = False
        self.hover_timer = QTimer()
        self.hover_timer.timeout.connect(self._on_hover_timeout)
        self.hover_timer.setSingleShot(True)

    def _on_hover_timeout(self):
        """Called after 1 second hover to speak the label text."""
        if self.label_widget and self.tts_callback:
            label_text = self.label_widget.text()
            if label_text:
                #print(f"[TTS-HOVER] {self.field_name}: {label_text}")
                self.tts_callback(label_text)

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a1:
            # Track hover events with 1-second delay for TTS
            if a1.type() == QEvent.Type.Enter:
                self.is_hovered = True
                #print(f"[HOVER] {self.field_name}: entered (TTS in 1s...)")
                self.hover_timer.start(1000)  # 1 second delay
            elif a1.type() == QEvent.Type.Leave:
                self.is_hovered = False
                self.hover_timer.stop()  # Cancel TTS if mouse leaves
                #print(f"[HOVER] {self.field_name}: left")
            
            # Track focus events (Tab, click, or setFocus()) - immediate TTS
            elif a1.type() == QEvent.Type.FocusIn:
                self.is_focused = True
                #print(f"[FOCUS] {self.field_name}: focused")
                # Stop any ongoing TTS from other fields
                if self.tts_stop_callback:
                    self.tts_stop_callback()
                # Speak immediately on focus
                if self.label_widget and self.tts_callback:
                    label_text = self.label_widget.text()
                    if label_text:
                        #print(f"[TTS-FOCUS] {self.field_name}: {label_text}")
                        self.tts_callback(label_text)
            elif a1.type() == QEvent.Type.FocusOut:
                self.is_focused = False
                self.hover_timer.stop()  # Cancel pending hover TTS
                # Clear text selection when focus leaves
                if hasattr(a0, 'lineEdit') and a0.lineEdit():  # type: ignore
                    a0.lineEdit().deselect()  # type: ignore
                #print(f"[FOCUS] {self.field_name}: focus lost")
        
        return super().eventFilter(a0, a1)
    