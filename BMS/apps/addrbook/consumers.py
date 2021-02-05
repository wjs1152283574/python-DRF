from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.layers import get_channel_layer   #  可以在任意墓库奥中导入并使用 : 在这里导入风筝成一个公用方法:send_group_msg
from asgiref.sync import async_to_sync

import json


consumer_object_list = []

# 自定义websocket实例类

class AddrBookConsumers(WebsocketConsumer): 
    """基础匿名多人聊天"""
    def websocket_connect(self,msg):
        ''' 客户端请求简历连接时 自动触发 '''
        # print("有新请求0.0.0")
        self.accept()
        consumer_object_list.append(self)

    def websocket_receive(self,msg):
        ''' 客户端(已链接的任意客户端)发送数据过来接收到 自动触发 '''
        # print(msg)
        text = msg.get('text')
        # # 给客户端发送消息 单独发送
        # self.send(text_data=text)

        # 给所有的链接对象发送数据
        for obj in consumer_object_list:
            obj.send(text_data=text)

    def websocket_disconnect(self,msg):
        ''' 客户端断开连接 自动触发 '''
        # print('断开链接')
        # 客户端断开之后，应该将当前对象移除
        consumer_object_list.remove(self)
        raise StopConsumer()

class AsyncConsumer(AsyncWebsocketConsumer):
    """异步推送--配合redis"""
    async def connect(self):  # 连接时触发
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'notice_%s' % self.room_name  # 直接从用户指定的房间名称构造Channels组名称，不进行任何引用或转义。

        # 将新的连接加入到群组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):  # 断开时触发
        # 将关闭的连接从群组中移除
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 信息群发
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'system_message',
                'message': message
            }
        )

    # Receive message from room group
    async def system_message(self, event):   # 定义的额外方法  消息单点推送
        print(event)
        message = event['message']

        # Send message to WebSocket单发消息
        await self.send(text_data=json.dumps({
            'message': message
        }))

def send_group_msg(room_name, message):
    # 从Channels的外部发送消息给Channel
    """
    from assets import consumers
    consumers.send_group_msg('ITNest', {'content': '这台机器硬盘故障了', 'level': 1})
    consumers.send_group_msg('ITNest', {'content': '正在安装系统', 'level': 2})
    :param room_name:
    :param message:
    :return:
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notice_{}'.format(room_name),  # 构造Channels组名称
        {
            "type": "system_message",
            "message": message,
        }
    )