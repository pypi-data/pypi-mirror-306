import os
import pika
import threading
from functools import wraps
import time
import logging

# Thiết lập logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler để in ra console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Tạo formatter và gắn vào handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Gắn handler vào logger
logger.addHandler(console_handler)


class QueueListener:
    def __init__(self, input_queue, output_queue=None, error_queue=None, host=None, port=None, user=None, password=None,
                 retry_interval=5, min_messages=5, timeout=30):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.error_queue = error_queue
        self.host = host or os.getenv('RABBITMQ_HOST', 'localhost')
        self.port = port or int(os.getenv('RABBITMQ_PORT', 5672))
        self.user = user or os.getenv('RABBITMQ_USER', 'guest')
        self.password = password or os.getenv('RABBITMQ_PASS', 'guest')
        self.retry_interval = retry_interval
        self.min_messages = min_messages  # Số lượng tin nhắn tối thiểu để gửi ra ngoài
        self.timeout = timeout  # Thời gian chờ tối đa trước khi gửi tin nhắn

        # Thiết lập logger
        self.logger = logger
        self.lock = threading.Lock()

        # Buffer để lưu trữ các tin nhắn đã xử lý
        self.message_buffer = []
        self.last_sent_time = time.time()

        self.error_buffer = []
        self.last_error_time = time.time()

        # Tạo và khởi động thread kiểm tra timeout
        self.flush_thread = threading.Thread(target=self._check_timeout)
        self.flush_thread.daemon = True
        self.flush_thread.start()

    def _check_timeout(self):
        while True:
            time.sleep(5)  # Kiểm tra mỗi giây
            if len(self.message_buffer) > 0 and (time.time() - self.last_sent_time) >= self.timeout:
                self.logger.info("Timeout reached, flushing buffer...")
                with self.lock:
                    self.flush_buffer()
                    self.flush_error_buffer()

    def start_listening(self, func, *args, **kwargs):
        while True:
            try:
                # Thiết lập thông tin đăng nhập
                credentials = pika.PlainCredentials(self.user, self.password)
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
                )
                channel = connection.channel()

                # Đảm bảo queue tồn tại
                channel.queue_declare(queue=self.input_queue)
                if self.output_queue:
                    channel.queue_declare(queue=self.output_queue)

                # Hàm callback được gọi khi có message
                def callback(ch, method, properties, body):
                    try:
                        # Gọi hàm gốc với nội dung message
                        result = func(body.decode(), *args, **kwargs)
                        self.message_buffer.append(result)

                        current_time = time.time()
                        if len(self.message_buffer) >= self.min_messages:
                            self.logger.info(f"Min messages reached, flushing buffer...")
                            with self.lock:
                                self.flush_buffer(channel)
                            self.last_sent_time = current_time
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                        error_msg = {
                            'message': body.decode(),
                            'error': str(e)
                        }
                        self.error_buffer.append(error_msg)
                        if self.error_queue and len(self.error_buffer) >= self.min_messages:
                            self.flush_error_buffer(channel)
                        

                # Đăng ký callback
                channel.basic_consume(queue=self.input_queue, on_message_callback=callback, auto_ack=True)

                self.logger.info(f"[*] Listening on queue: {self.input_queue}. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                self.logger.error(f"Connection error: {e}, retrying in {self.retry_interval} seconds...")
                time.sleep(self.retry_interval)

    def flush_error_buffer(self, channel=None):
        if self.error_queue:
            """Init channel nếu chưa có"""
            should_close_connection = False
            if not channel:
                credentials = pika.PlainCredentials(self.user, self.password)
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
                )
                channel = connection.channel()
                should_close_connection = True

            """Gửi tất cả các tin nhắn trong buffer ra queue error"""
            for error_msg in self.error_buffer:
                channel.basic_publish(exchange='', routing_key=self.error_queue, body=error_msg)
            self.logger.info(f"[*] Sent {len(self.error_buffer)} error messages to error queue: {self.error_queue}")

            self.error_buffer.clear()
            if should_close_connection and channel:
                channel.close()
            self.last_error_time = time.time()


    def flush_buffer(self, channel=None):
        if self.output_queue:
            """Init channel nếu chưa có"""
            should_close_connection = False
            if not channel:
                credentials = pika.PlainCredentials(self.user, self.password)
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=self.host, port=self.port, credentials=credentials)
                )
                channel = connection.channel()
                should_close_connection = True

            """Gửi tất cả các tin nhắn trong buffer ra queue output"""
            for message in self.message_buffer:
                channel.basic_publish(exchange='', routing_key=self.output_queue, body=message)
            self.logger.info(f"[*] Sent {len(self.message_buffer)} messages to output queue: {self.output_queue}")

            self.message_buffer.clear()
            if should_close_connection and channel:
                channel.close()
            self.last_sent_time = time.time()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            listener_thread = threading.Thread(target=self.start_listening, args=(func,) + args, kwargs=kwargs)
            listener_thread.start()

        return wrapper
