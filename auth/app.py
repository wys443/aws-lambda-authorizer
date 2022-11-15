import requests

REGION = 'ap-southeast-1'
ACCOUNT_ID = '076433462823'
API_ID = 'v6aetkjxv9'

API_PERMISSIONS = [
    {
        'arn': f'arn:aws:execute-api:{REGION}:{ACCOUNT_ID}:{API_ID}',
        'resource': '*',
        'stage': '*',
        'httpVerb': '*',
        'scope': '*',
    }
]

DEFAULT_DENY_ALL_POLICY = {
    'principalId': 'user',
    'policyDocument': {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Action': 'execute-api:Invoke',
                'Effect': 'Deny',
                'Resource': '*',
            }
        ],
    }
}


def generate_policy_statement(api_name, api_stage, api_verb, api_resource, action):
    method_arn = f'{api_name}/{api_stage}/{api_verb}/{api_resource}'

    statement = {
        'Action': 'execute-api:Invoke',
        'Effect': action,
        'Resource': method_arn,
    }

    return statement


def generate_policy(principal_id, policy_statements):
    policy_document = {
        'Version': '2012-10-17',
        'Statement': policy_statements,
    }

    auth_response = {
        'principalId': principal_id,
        'policyDocument': policy_document,
    }

    return auth_response


def verify_access_token(access_token):
    URL = 'https://api1.iam.omnicloudapi.com/auth/checktoken'
    headers = {
        'origin': 'https://www.kunyek.com',
        'referer': 'https://www.kunyek.com/',
        'Content-Type': 'application/json',
        'authority': 'api1.iam.omnicloudapi.com',
    }
    data = {
        "userid": "ye.thu@kernellix.com",
        "appid": "kunyek",
        "atoken": access_token,
    }
    response = requests.post(URL, json=data, headers=headers)

    return response


def generate_iam_policy(scope_claims):
    policy_statements = []

    for permission in API_PERMISSIONS:
        # if scope_claims in permission['scope']:
        policy_statements.append(
            generate_policy_statement(
                permission['arn'],
                permission['stage'],
                permission['httpVerb'],
                permission['resource'],
                'Allow',
            )
        )

    if len(policy_statements) == 0:
        return DEFAULT_DENY_ALL_POLICY
    else:
        return generate_policy('user', policy_statements)


def lambda_handler(event, context):
    token = event['authorizationToken'].replace("Bearer ", "")

    data = verify_access_token(token)
    scope_claims = ['email']
    iam_policy = generate_iam_policy(scope_claims)

    return iam_policy


if __name__ == '__main__':
    test_token = ''
    print(verify_access_token(test_token))
