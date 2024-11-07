`whatsapp-messager` is a Python library that makes it easy to send messages using WhatsApp's official API. This library is built to interact with the WhatsApp Business API, providing a simple way to send text messages and OTP messages.

## Features

- Send OTP messages via WhatsApp.
    
- Send general text messages via WhatsApp.

## Installation

You can install the library using `pip`:

`pip install whatsapp-sender`

## Usage
To start using `whatsapp-sender`, you need to create an instance of the `WhatsAppSender` class with your access token, phone number ID, and version number.

### Import and Setup
```
from whatsapp_messager.messaging import WhatsAppSender

# Initialize the WhatsAppSender
sender = WhatsAppSender(
    access_token="your_access_token",
    phone_number_id="your_phone_number_id",
    version_number="v15.0"  # Optional, default is v15.0
)
```

### Send OTP Message

To send an OTP message:
```
response = sender.send_otp_message(recipient_phone_number="1234567890", otp="123456")
print(response)
```
### Send Text Message

To send a text message:
```
response = sender.send_text_message(
    recipient_phone_number="1234567890",
    message="Hello from WhatsApp Sender!",
    country_code="+1"  # Include the appropriate country code
)
print(response)
```
## Requirements

- Python 3.7+
    
- `requests` library

## Error Handling

The library provides basic error handling and returns success or failure messages based on the API response. If an error occurs, the response will contain details about the failure.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

- John Gbaya-kokoya
    
- gbayakokoyajohnjr@gmail.com
    

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to improve the library.

## Links

- [GitHub Repository](https://github.com/John-sys/whatsapp-sender_library)
    
- [Bug Reports](https://github.com/John-sys/whatsapp-sender_library/issues)
    
- [Documentation](https://github.com/John-sys/whatsapp-sender_library)