import os
import json
import hashlib
import datetime
import urllib
import urllib.parse
import traceback

ilmservice_url = 'https://ilmservice-pre.alipay.com/api/v1/open/flow/service'

app_name = 'icontentcenter'
app_token = '8c5faaa94f2077863a2b34b3e64ebf2e'
timestamp = f'{int(datetime.datetime.now().timestamp())}'

md5_hash = hashlib.md5()
md5_hash.update(f'{app_token}{timestamp}'.encode('utf-8'))
app_token = md5_hash.hexdigest()

headers = {
    'X-DEPLOY-APP': app_name,
    'X-DEPLOY-TOKEN': app_token,
    'X-DEPLOY-TIMESTAMP': timestamp,

    'content-type': 'application/json'
}

# chat with image


def chat_with_image(service_id, sys_message, user_message, image_url=None, custom_request={}, debug=False):
    data = {
        'serviceId': service_id,
        'message': [
            {
                'role': 'system',
                'content': sys_message
            },
            {
                'role': 'user',
                'content': [
                    {
                        'type': 'text',
                        'text': user_message
                    }
                ]
            }
        ],
        'customRequest': custom_request,
        'debug': {} if not debug else {'DEBUG_NODE': True}
    }

    if image_url:
        data['message'][1]['content'].append({
            'type': 'image_url',
            'image_url': {
                'url': image_url
            },
            'detail': 'high'})

    # print(headers)
    # print(data)

    # post and get resp
    try:
        data = urllib.parse.urlencode(data).encode('utf-8')
        request = urllib.request.Request(ilmservice_url, data=data, headers=headers)
        response = urllib.request.urlopen(request, timeout=20)
        # print(response)
        # print(response.text)
        answer = json.loads(response.read())
        print(answer)

        assert answer, 'answer is None'
        assert answer['data'], 'answer.data is None'
        assert answer['data']['message'], 'answer.data.message is None'
        assert answer['data']['message'][0]['content'], 'answer.data.message[0].content is None'

        return json.loads(answer['data']['message'][0]['content'])
    
    except Exception as e:
        print(e)
        print(traceback.format_exc())
