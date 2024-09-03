def shortenAddress(address):
    if len(address) <= 8:
        return address
    return f"{address[:3]}...{address[-3:]}"

def get_user_name(user):
    user_name = user.get('discordUsername')
    symbol = '🎮'
    if user_name is None:
        user_name = user.get('twitterId')
        symbol = '🐦'
    if user_name is None:
        user_name = user.get('wallet')
        symbol = '💼'
    
    if user_name is None:
        user_name = "*Not Found*"
        symbol = '❓'
    else:
        if symbol == '💼':
            user_name = shortenAddress(user_name)
    
    return symbol, user_name