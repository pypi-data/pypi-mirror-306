# VKMusix

## Установка и обновление
```bash
pip install --upgrade vkmusix
```

## Быстрый старт
```python
from vkmusix import Client

client = Client()

tracks = client.searchTracks(
    query="Маленький ярче",
    limit=10,
    
)

print(tracks)

client.close()
```
