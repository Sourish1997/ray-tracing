def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    print('\r[%s] %s%s ...%s' % (bar, percents, '%', suffix), end='')


def split_range(count, parts):
    d, r = divmod(count, parts)
    return [
        (i * d + min(i, r), (i + 1) * d + min(i + 1, r)) for i in range(parts)
    ]
