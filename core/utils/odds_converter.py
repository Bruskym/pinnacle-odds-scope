def american_to_decimal(odd_american):
    if odd_american > 0:
        return (odd_american / 100) + 1
    return (100 / abs(odd_american)) + 1