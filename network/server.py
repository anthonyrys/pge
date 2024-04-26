from pge.types import Singleton

import threading
import pickle
import socket
import typing
import time

@Singleton
class Server:
    '''
    Server singleton for the network socket.
    '''
        
    def __init__(self, ip: str, port: int, ticks: typing.Optional[int] = 120) -> None:
        '''
        Creates the `Server` instance.

        Takes the server `ip` address and `port`, as well as an 
        optional `tick_rate` for sending packets and checking
        client inactivity.
        '''

        self.BUFFER_SIZE: int = 1048
        self.SLEEP_TIME: float = 1 / ticks

        self.ticks: int = ticks

        self._ip: str = ip
        self._port: int = port

        self._socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind((self._ip, self._port))
        self._socket.settimeout(0.1)

        self.clients: list[tuple[str, int]] = []
        self._clients_timer: dict[tuple[str, int], int] = {}

        self.running: bool = True

        self._func_s: tuple[callable, typing.Sequence[any]] = None
        self._func_r: tuple[callable, typing.Sequence[any]] = None

        thread_send: threading.Thread = threading.Thread(target=self._run_s)
        thread_recv: threading.Thread = threading.Thread(target=self._run_r)

        thread_send.start()
        thread_recv.start()

    def set_send(self, func: callable, *args: typing.Sequence[any]) -> None:
        '''
        Set the `func` that will be called with it's `args`
        when a packet needs to be sent to a client.

        `func` will also be called with the client as an
        argument.
        '''

        self._func_s = (func, args)
 
    def set_received(self, func: callable, *args: typing.Sequence[any]) -> None:
        '''
        Set the `func` that will be called with it's `args`
        when a packet is received from a client.

        `func` will also be called with the packet as an 
        argument.
        '''

        self._func_r = (func, args)

    def unset(self, func_type: str) -> None:
        '''
        Removes a function set by either `set_send` or `set_received`.

        An assertion error will be raised if `func_type` is not
        `s` or `r`.
        '''

        assert func_type == 's' or func_type == 'r'

        if func_type == 's':
            self._func_s = None
        elif func_type == 'r':
            self._func_r = None

    def kill(self) -> None:
        '''
        Kills the `Server` threads.
        '''

        self.running = False

    def _run_s(self) -> None:
        '''
        Thread which handles the `Server` package sending and
        client inactivity.

        If a client has not sent a package in `self.ticks * 5`,
        it will be removed from `clients`.

        Sends a package specified by the function set with 
        `set_send` to each client in `clients`.
        '''

        while self.running:
            time.sleep(self.SLEEP_TIME)

            del_clients: list[tuple[str, int]] = []
            for client in self.clients:
                self._clients_timer[client] += 1
                if self._clients_timer[client] >= self.ticks * 5:
                    del_clients.append(client)

            for client in del_clients:
                del self._clients_timer[client]
                self.clients.remove(client)

            if not self._func_s:
                continue

            for client in self.clients:
                data: bytes = pickle.dumps(self._func_s[0](*self._func_s[1], client))
                self._socket.sendto(data, client)
            
    def _run_r(self) -> None:
        '''
        Thread which handles the `Server` package receiving.

        When receiving a packet from a client that is not apart
        of `clients`, they will be added.

        The function set with `set_received` will be called with
        the received packet as an argument.
        '''

        while self.running:
            try:
                data: tuple[bytes, tuple[str, int]] = self._socket.recvfrom(self.BUFFER_SIZE)
                if data[1] not in self.clients:
                    self.clients.append(data[1])

                self._clients_timer[data[1]] = 0

                data = (pickle.loads(data[0]), data[1])

                if self._func_r:
                    self._func_r[0](*self._func_r[1], data)

            except socket.error:
                ...
