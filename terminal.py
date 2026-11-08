def create_bar(percentage):
    filled = int(percentage / 5)
    bar = "█" * filled + "░" * (20 - filled)
    return bar
