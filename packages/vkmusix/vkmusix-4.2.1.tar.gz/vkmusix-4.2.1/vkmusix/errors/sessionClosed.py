#  VKMusix — VK Music API Client Library for Python
#  Copyright (C) 2024—present to4no4sv <https://github.com/to4no4sv/VKMusix>
#
#  This file is part of VKMusix.
#
#  VKMusix is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  VKMusix is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with VKMusix. If not, see <http://www.gnu.org/licenses/>.

from vkmusix.errors import Error

class SessionClosed(Error, RuntimeError):
    def __init__(self) -> None:
        self.ru = "Текущая сессия закрыта. Для отправки новых запросов потребуется создать новый объект класса `Client` или использовать метод `reconnect`."
        self.en = "The current session is closed. To send new requests, you need to create a new instance of the `Client` class or use `reconnect` method."