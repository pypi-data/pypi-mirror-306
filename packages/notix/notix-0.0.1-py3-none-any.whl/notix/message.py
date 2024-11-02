import ctypes

class mbox:
    @staticmethod
    def show_info(title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000000)  # MB_OK
    @staticmethod
    def show_warning(title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000030)  # MB_OK | MB_ICONWARNING
    @staticmethod
    def show_error(title, message):
        ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000010)  # MB_OK | MB_ICONERROR
    @staticmethod
    def show_question(title, message):
        return ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000001 | 0x00000020) == 1  # MB_YESNO | MB_ICONQUESTION
    @staticmethod
    def show_yes_no(title, message):
        return ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000036) == 6  # MB_YESNO | MB_ICONQUESTION