import json

service_id = '8610937581523064704'

func_desc = [
    {
        "name": "generate_keywords",
        "description": "function for generating keywords",
        "parameters": {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "object",
                    "description": "the result of generating keywords, each of keyword includes 3 properties: caption, language and score",
                    "properties": {
                        "caption": {
                            "type": "string",
                            "description": "the caption of keyword"
                        },
                        "language": {
                            "type": "string",
                            "description": "the language code of keyword",
                            "enum": [
                                "zh_CN",
                                "zh_HK",
                                "zh_TW",
                                "th_TH",
                                "ja_JP",
                                "en_US",
                                "es_ES",
                                "de_DE",
                                "pt_BR",
                                "ru_RU",
                                "ko_KR",
                                "nl_NL",
                                "vi_VN",
                                "in_ID",
                                "pl_PL"
                            ]
                        },
                        "score": {
                            "type": "number",
                            "description": "the relevant score of keyword to it's categories"
                        }
                    },
                    "required": [
                        "caption",
                        "language",
                        "score"
                    ]
                },
            },
            "required": [
                "keywords"
            ],
        },
    }
]

custom_request = {
    'func_name': 'generate_keywords',
    'func_desc': json.dumps(func_desc, ensure_ascii=False)
}