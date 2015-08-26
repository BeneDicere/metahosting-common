
def get_message_subject(message):
    if 'subject' not in message:
        return None
    return message.pop('subject')
