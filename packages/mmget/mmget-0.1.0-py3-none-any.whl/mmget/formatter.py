class Formatter:
    @staticmethod
    def format_bytes(bytes_received: int):
        units = ["B", "KB", "MB", "GB", "TB"]
        size = float(bytes_received)
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        if unit_index == 0:
            return f"{bytes_received}{units[unit_index]}"
        return f"{size:.2f}{units[unit_index]}"
