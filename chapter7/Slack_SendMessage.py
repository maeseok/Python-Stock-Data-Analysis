from slacker import Slacker
import requests
 
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
 
myToken = "xoxb-4195322639751-4206941850933-C8iOhK3paaOceOYWPhv6MFLO"
markdown_text = '''
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
'''

post_message(myToken,"#랜덤",markdown_text)


'''attach_dict = {
    'color'      :'#ff0000',
    'author_name':'Test',
    "author_link":'github.com/investar',
    'title'      :'오늘의 증시 KOSPI',
    'title_link' :'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    'text'       :'2,326.13 △11.89 (+0.51%)',
    'image_url'  :'ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
}'''

#attach_list = [attach_dict]
#slack.chat.post_message(channel="#랜덤", text=markdown_text, attachments=attach_list)