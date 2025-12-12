from fast_depends import Provider
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from src.config import settings


broker = RabbitBroker(settings.AMQP_URL)

provider = Provider()

faststream_app = FastStream(broker, provider=provider)

