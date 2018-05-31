"""Validate parameter values for the Gitcoin API client."""

# Valid parameter values as seen at
# https://github.com/gitcoinco/web/blob/84babc30611c281c817582b4d677dda6366def83/app/dashboard/models.py#L119-L168
OPTIONS = {
    'experience_level': ['Beginner', 'Intermediate', 'Advanced', 'Unknown'],
    'project_length': ['Hours', 'Days', 'Weeks', 'Months', 'Unknown'],
    'bounty_type': ['Bug', 'Security', 'Feature', 'Unknown'],
    'idx_status': ['cancelled', 'done', 'expired', 'open', 'started', 'submitted', 'unknown'],
    'order_by': [
        'web3_type', 'title', 'web3_created', 'value_in_token', 'token_name',
        'token_address', 'bounty_type', 'project_length', 'experience_level',
        'github_url', 'github_comments', 'bounty_owner_address',
        'bounty_owner_email', 'bounty_owner_github_username',
        'bounty_owner_name', 'is_open', 'expires_date', 'raw_data', 'metadata',
        'current_bounty', '_val_usd_db', 'contract_address', 'network',
        'idx_experience_level', 'idx_project_length', 'idx_status',
        'issue_description', 'standard_bounties_id', 'num_fulfillments',
        'balance', 'accepted', 'interested', 'interested_comment',
        'submissions_comment', 'override_status', 'last_comment_date',
        'fulfillment_accepted_on', 'fulfillment_submitted_on',
        'fulfillment_started_on', 'canceled_on', 'snooze_warnings_for_days',
        'token_value_time_peg', 'token_value_in_usdt', 'value_in_usdt_now',
        'value_in_usdt', 'value_in_eth', 'value_true', 'privacy_preferences'
    ]
}


def _validate_options(field_name, value):
    """Validate values for the given field name."""
    if value in OPTIONS[field_name]:
        return value
    msg = 'Unknown value "{val}" for field "{name}".'
    raise ValueError(msg.format(val=value, name=field_name))


def experience_level(value):
    """Validate values for "experience_level"."""
    return _validate_options('experience_level', value)


def project_length(value):
    """Validate values for "project_length"."""
    return _validate_options('project_length', value)


def bounty_type(value):
    """Validate values for "bounty_type"."""
    return _validate_options('bounty_type', value)


def idx_status(value):
    """Validate values for "idx_status"."""
    return _validate_options('idx_status', value)


def order_by(direction):
    """Validate values for "order_by"."""
    if direction in OPTIONS['order_by']:
        return direction
    if direction[0:1] == '-' and direction[1:] in OPTIONS['order_by']:
        return direction
    msg = 'Unknown direction "{dir}" to order by.'
    raise ValueError(msg.format(dir=direction))
