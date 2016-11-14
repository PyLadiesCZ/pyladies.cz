def tah(pole, index, symbol):
    if pole[index] != '-':
        raise ValueError('Pole {} je obsazeno symbolem {}'.format(index, pole[index]))
    return pole[:index] + symbol + pole[index + 1:]

def vyhodnot(pole):
    if 'ooo' in pole:
        return 'o'
    if 'xxx' in pole:
        return 'x'
    if '-' not in pole:
        return '!'
    return '-'
