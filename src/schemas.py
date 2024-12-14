definitions = {
    'Transaction': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'amount': {'type': 'number'},
            'commission': {'type': 'number'},
            'status': {'type': 'string'},
            'created_at': {'type': 'string', 'format': 'date-time'},
            'user_id': {'type': 'integer'}
        }
    },
    'User': {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'username': {'type': 'string'},
            'commission_rate': {'type': 'number'},
            'webhook_url': {'type': 'string'},
            'role': {'type': 'string'}
        }
    }
}