def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def volume(value):
    return '{:,}'.format(value).replace(',', '.')
