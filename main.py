import paho.mqtt.client as mqtt
import paho.mqtt.reasoncodes as mqtt_rc
import paho.mqtt.enums as mqtt_enums


class MyMQTTClient(mqtt.Client):
    """MQTTクライアントを管理するクラス"""

    def __init__(
        self, broker_host: str, broker_port: int, topic: str, keep_alive: int
    ) -> None:
        """MQTTクライアントを初期化"""
        super().__init__(callback_api_version=mqtt_enums.CallbackAPIVersion.VERSION2)
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.keep_alive = keep_alive

    def on_connect(
        self, client: mqtt.Client, userdata, flags, rc: mqtt_rc.ReasonCode, properties
    ) -> None:
        """接続時に呼ばれるコールバック関数"""
        if rc.is_failure:
            print(f"Failed to connect: {rc.getName()}")
        else:
            print(f"Connected with result code {rc}")
            client.subscribe(self.topic)

    def on_message(self, client, userdata, msg: mqtt.MQTTMessage) -> None:
        """メッセージ受信時に呼ばれるコールバック関数"""
        print(f"Received message: {msg.payload.decode()} from topic: {msg.topic}")

    def run(self) -> None:
        """MQTTクライアントを実行"""
        self.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.loop_forever()


if __name__ == "__main__":
    # MQTTクライアントを作成して実行
    mqtt_client = MyMQTTClient(
        broker_host="broker.emqx.io",
        broker_port=1883,
        topic="test/topic",
        keep_alive=60,
    )
    mqtt_client.run()
