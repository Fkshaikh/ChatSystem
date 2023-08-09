def verify_auth(message):

    if message.get('token') == 'abcdefg':
        return True
    else:
        return False

