from django import template
import datetime 

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def format_time(value):
    if isinstance(value, datetime.time):
        hours = value.hour
        minutes = value.minute
        seconds = value.second
        
        parts = []
        
        # Collect time components
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds > 0:
            parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")

        # Return formatted string or "0 seconds" if no parts exist
        return ', '.join(parts) if parts else "0 seconds"

    return value  # Fallback if value is not a time object