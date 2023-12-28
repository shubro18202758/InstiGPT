# Example Request

## Example Request using `cURL`

```sh
curl --location 'localhost:5000/chat' \
--header 'Content-Type: application/json' \
--data '{
    "messages": [
        {
            "role": "user",
            "content": "<question>"
        }
    ]
}'
```
