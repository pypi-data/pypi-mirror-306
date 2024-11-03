# Rounds a measurement value

Rounds a measurement value and its uncertainty to a specified number
of significant digits.

Examples:

        >>> precise_rounding(123.45678, 0.01234)
        ('123.457', '0.013')

        >>> precise_rounding(123.45678, 0.515, 1)
        ('123.5', '0.6')
