from typing import List, Optional, Union, Sequence
from subprocess import Popen as _Popen, PIPE, TimeoutExpired, CompletedProcess
from abc import ABC, abstractmethod
from queue import Queue
from threading import Thread, Event
from time import sleep
import sys

from .string import startswith

if sys.platform == "win32":
    from select import select
else:
    from fcntl import F_GETFL, F_SETFL, fcntl
    from os import O_NONBLOCK

__all__ = [
    "Popen",
    "Disposable",
]


class Popen(_Popen):
    """
    用于交互式进程。
    """

    def __init__(self, args: Union[Sequence, str], verbose: bool = False) -> None:
        self._config = {}
        self.verbose = verbose
        if isinstance(args, str):
            shell = True
        elif isinstance(args, Sequence):
            shell = False
            args = tuple(map(str, args))
        else:
            raise TypeError("args must be a sequence or a string")
        super().__init__(
            args,
            shell=shell,
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            bufsize=1,
        )
        if self.poll() is not None:
            raise ChildProcessError("Process failed to start")

        def reader(self: __class__, handleType: str) -> None:
            def oneline(res: str):
                if res != "":
                    queue.put(res)
                    if self.verbose:
                        end = "" if res.endswith("\n") else "\n"
                        print(f"{handleType}: {res}", end=end)

            handle = getattr(self, handleType)
            queue = getattr(self, f"{handleType}_queue")

            if sys.platform == "linux":
                flags = fcntl(handle, F_GETFL)
                fcntl(handle, F_SETFL, flags | O_NONBLOCK)

            while True:
                if self.thread_event.is_set():
                    break
                if handle.closed:
                    break

                if sys.platform == "win32":
                    read, _, _ = select([handle], [], [], 0.1)
                    if not read:
                        continue

                if self.poll() is not None:
                    map(oneline, handle.readlines())
                    break
                oneline(handle.readline())
            return

        self._config["stdout_queue"] = Queue()
        self._config["stderr_queue"] = Queue()
        self._config["thread_event"] = Event()
        self._config["stdout_thread"] = Thread(
            target=reader, args=(self, "stdout"), daemon=True
        )
        self._config["stderr_thread"] = Thread(
            target=reader, args=(self, "stderr"), daemon=True
        )
        self.stdout_thread.start()
        self.stderr_thread.start()

    @property
    def verbose(self) -> bool:
        return self._config["verbose"]

    @verbose.setter
    def verbose(self, value: bool) -> None:
        self._config["verbose"] = True if value else False

    @property
    def stdout_queue(self) -> Queue:
        return self._config["stdout_queue"]

    @property
    def stderr_queue(self) -> Queue:
        return self._config["stderr_queue"]

    @property
    def thread_event(self) -> Event:
        return self._config["thread_event"]

    @property
    def stdout_thread(self) -> Thread:
        return self._config["stdout_thread"]

    @property
    def stderr_thread(self) -> Thread:
        return self._config["stderr_thread"]

    def stop(self, timeout: int = 300) -> None:
        if self.poll() is not None:
            return
        self.thread_event.set()
        self.stdout_thread.join()
        self.stderr_thread.join()
        if self.stdin and not self.stdin.closed:
            self.stdin.close()
        if self.stdout and not self.stdout.closed:
            self.stdout.close()
        if self.stderr and not self.stderr.closed:
            self.stderr.close()
        if self.poll() is None:
            self.terminate()
            self.wait(timeout=timeout)
            if self.poll() is None:
                self.kill()

    def wait(self, *args, **kwargs):
        returncode = None
        try:
            returncode = super().wait(*args, **kwargs)
        except TimeoutExpired:
            pass
        return returncode

    def send(self, *args: Union[str, int, float]) -> str:
        cmd = " ".join(map(str, args))
        stdin = self.stdin
        if stdin is None or stdin.closed:
            raise BrokenPipeError("stdin is closed")
        stdin.write((cmd + "\n"))
        stdin.flush()
        return cmd

    def recv(
        self,
        targets: Union[str, Sequence[str]],
        heads: Optional[list] = None,
        targets_regex: bool = False,
        targets_case: bool = False,
        heads_regex: bool = False,
        heads_case: bool = False,
    ) -> List[str]:
        if targets is None:
            raise ValueError("targets is None")
        elif isinstance(targets, Sequence):
            targets = list(targets)
        else:
            targets = [targets]
        if len(targets) < 1:
            raise ValueError("targets is empty")

        if heads is not None:
            if isinstance(heads, str):
                heads = [heads]
            elif isinstance(heads, list):
                pass
            else:
                raise ValueError("heads is not str or list")

        q = self.stdout_queue

        if heads is not None:
            while True:
                if q.empty():
                    sleep(0.1)
                    continue
                line = q.queue[0]
                if startswith(line, heads, regex=heads_regex, case=heads_case):
                    break
                q.get(timeout=1)
                q.task_done()

        result = []
        while True:
            if q.empty():
                sleep(0.1)
                continue
            line = q.get()
            result.append(line)
            q.task_done()
            if startswith(line, targets, regex=targets_regex, case=targets_case):
                break
        return result


class Disposable(ABC):
    """
    一次性进程，用于快捷封装自定义进程。
    """

    __slots__ = ("__config",)

    def __init__(self) -> None:
        self.__config = {
            "stdout": None,
            "stderr": None,
            "started": False,
            "process": None,
            "returncode": None,
        }

    @property
    def stdout(self) -> Optional[str]:
        return self.__config["stdout"]

    @property
    def stderr(self) -> Optional[str]:
        return self.__config["stderr"]

    @property
    def started(self) -> bool:
        return self.__config["started"]

    @property
    def process(self) -> _Popen:
        return self.__config["process"]

    @property
    def returncode(self) -> Optional[int]:
        return self.__config["returncode"]

    def start_init(self) -> None:
        """callback order:
        >>> self.start_init()  # here
        >>> if not self.started:
        >>>     self.process_args()
        >>>     if args is not None:
        >>>         self.process_kwargs()
        >>>         self.begin_before()
        >>>         `begin process`
        >>>         self.begin_after()
        """
        pass

    def begin_before(self) -> None:
        """callback order:
        >>> self.start_init()
        >>> if not self.started:
        >>>     self.process_args()
        >>>     if args is not None:
        >>>         self.process_kwargs()
        >>>         self.begin_before()  # here
        >>>         `begin process`
        >>>         self.begin_after()
        """
        pass

    @abstractmethod
    def process_args(self) -> Union[Sequence, str, None]:
        """callback order:
        >>> self.start_init()
        >>> if not self.started:
        >>>     self.process_args()  # here
        >>>     if args is not None:
        >>>         self.process_kwargs()
        >>>         self.begin_before()
        >>>         `begin process`
        >>>         self.begin_after()
        """
        pass

    def process_kwargs(self) -> dict:
        """callback order:
        >>> self.start_init()
        >>> if not self.started:
        >>>     self.process_args()
        >>>     if args is not None:
        >>>         self.process_kwargs()  # here
        >>>         self.begin_before()
        >>>         `begin process`
        >>>         self.begin_after()
        kwargs for Popen, without args, stdout, stderr and shell.
        """
        return {}

    def begin_after(self) -> None:
        """callback order:
        >>> self.start_init()
        >>> if not self.started:
        >>>     self.process_args()
        >>>     if args is not None:
        >>>         self.process_kwargs()
        >>>         self.begin_before()
        >>>         `begin process`
        >>>         self.begin_after()  # here
        """
        pass

    def start(self) -> None:
        self.start_init()
        if not self.started:
            args = self.process_args()
            if args is None:
                raise ValueError("args is None")
            elif isinstance(args, str):
                shell = True
            else:
                shell = False
            kwargs = self.process_kwargs()
            kwargs.update(
                {
                    "args": args,
                    "stdout": PIPE,
                    "stderr": PIPE,
                    "shell": shell,
                }
            )
            self.begin_before()
            self.__config["process"] = _Popen(**kwargs)
            self.__config["started"] = True
            self.begin_after()
        else:
            raise RuntimeError("Process already started")

    def join_before(self) -> None:
        """callback order:
        >>> self.join_before()  # here
        >>> `wait process`
        >>> self.join_after()
        """
        pass

    def join_after(self) -> None:
        """callback order:
        >>> self.join_before()
        >>> `wait process`
        >>> self.join_after()  # here
        """
        pass

    def join(self) -> None:
        proc = self.process
        if self.started and proc is not None and self.returncode is None:
            with proc:
                try:
                    self.join_before()
                    stdout, stderr = proc.communicate()
                    self.join_after()
                except Exception:
                    proc.kill()
                    raise ChildProcessError("some error happened.")
                finally:
                    self.__config["returncode"] = proc.poll()
                    self.__config["stdout"] = stdout.decode()
                    self.__config["stderr"] = stderr.decode()

    def run(self) -> CompletedProcess:
        self.start()
        self.join()
        proc = self.process
        if proc is not None and self.returncode is not None:
            returncode = self.returncode
        else:
            returncode = 1
        return CompletedProcess(proc.args, returncode, self.stdout, self.stderr)
