from . import _infinistore
import torch
import os
from typing import List, Tuple
import subprocess
import time
import re


# connection type: default is RDMA
TYPE_LOCAL_GPU = "LOCAL_GPU"
TYPE_RDMA = "RDMA"


def _get_bar1_memory_cap():
    result = subprocess.run(
        ["nvidia-smi", "-q", "-i", "0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise Exception("Error running nvidia-smi")

    pattern = re.compile(
        r"\s*BAR1 Memory Usage\s*\n"
        r"\s*Total\s*:\s*(\d+)\s*MiB\s*\n"
        r"\s*Used\s*:\s*(\d+)\s*MiB\s*\n"
        r"\s*Free\s*:\s*(\d+)\s*MiB",
        re.MULTILINE,
    )

    mem_cap = {}

    match = pattern.search(result.stdout)

    if match:
        total = int(match.group(1))
        used = int(match.group(2))
        free = int(match.group(3))

        mem_cap = {"bar1_total": total, "bar1_used": used, "bar1_free": free}
    else:
        raise Exception("No match found to get bar1 memory usage")

    pattern = re.compile(
        r"\s*FB Memory Usage\s*\n"
        r"\s*Total\s*:\s*(\d+)\s*MiB\s*\n"
        r"\s*Reserved\s*:\s*(\d+)\s*MiB\s*\n"
        r"\s*Used\s*:\s*(\d+)\s*MiB\s*\n"
        r"\s*Free\s*:\s*(\d+)\s*MiB",
        re.MULTILINE,
    )
    match = pattern.search(result.stdout)
    if match:
        mem_cap.update(
            {
                "total": int(match.group(1)),
                "reserved": int(match.group(2)),
                "used": int(match.group(3)),
                "free": int(match.group(4)),
            }
        )
    else:
        raise Exception("No match found to get fb memory usage")

    return mem_cap


class ClientConfig(_infinistore.ClientConfig):
    def __init__(self, **kwargs):
        super().__init__()
        self.connection_type = kwargs.get("connection_type", None)
        self.host_addr = kwargs.get("host_addr", None)
        self.dev_name = kwargs.get("dev_name", "")
        self.service_port = kwargs.get("service_port", None)
        # get log from system env
        # if log level is not set in Config and system env is not set either, use warning as default
        if "INFINISTORE_LOG_LEVEL" in os.environ:
            self.log_level = os.environ["INFINISTORE_LOG_LEVEL"]
        else:
            self.log_level = kwargs.get("log_level", "warning")

    def __repr__(self):
        return (
            f"ServerConfig(service_port={self.service_port}, "
            f"log_level='{self.log_level}', host_addr='{self.host_addr}', "
            f"connection_type='{self.connection_type.name}')"
        )

    def verify(self):
        if self.connection_type not in [TYPE_LOCAL_GPU, TYPE_RDMA]:
            raise Exception("Invalid connection type")
        if self.host_addr == "":
            raise Exception("Host address is empty")
        if self.service_port == 0:
            raise Exception("Service port is 0")
        if self.log_level not in ["error", "debug", "info", "warning"]:
            raise Exception("log level should be error, debug, info or warning")


class ServerConfig(_infinistore.ServerConfig):
    def __init__(self, **kwargs):
        super().__init__()
        self.manage_port = kwargs.get("manage_port", 0)
        self.service_port = kwargs.get("service_port", 0)
        self.log_level = kwargs.get("log_level", "warning")
        self.dev_name = kwargs.get("dev_name", "")
        self.prealloc_size = kwargs.get("prealloc_size", 16)

    def __repr__(self):
        return (
            f"ServerConfig(service_port={self.service_port}, manage_port={self.manage_port}, "
            f"log_level='{self.log_level}')"
        )

    def verify(self):
        if self.service_port == 0:
            raise Exception("Service port is 0")
        if self.manage_port == 0:
            raise Exception("Manage port is 0")
        if self.log_level not in ["error", "debug", "info", "warning"]:
            raise Exception("log level should be error, debug, info or warning")


class Logger:
    @staticmethod
    def info(msg):
        _infinistore.log_msg("info", str(msg))

    @staticmethod
    def debug(msg):
        _infinistore.log_msg("debug", str(msg))

    @staticmethod
    def error(msg):
        _infinistore.log_msg("error", str(msg))

    @staticmethod
    def warn(msg):
        _infinistore.log_msg("warning", str(msg))

    @staticmethod
    def set_log_level(level):
        _infinistore.set_log_level(level)


def register_server(loop, config: ServerConfig):
    """
    Registers a server with the given event loop.

    This function is intended for internal use only and should not be called by clients.

    Args:
        loop: The event loop to register the server with.

    """
    # client does not need to call this function
    from uvloop.loop import libuv_get_loop_t_ptr
    import ctypes
    from ctypes import pythonapi, c_void_p, py_object

    PyCapsule_GetPointer = pythonapi.PyCapsule_GetPointer
    PyCapsule_GetPointer.restype = c_void_p
    PyCapsule_GetPointer.argtypes = [py_object, ctypes.c_char_p]
    loop_ptr = PyCapsule_GetPointer(libuv_get_loop_t_ptr(loop), None)

    # from cpython.pycapsule import PyCapsule_GetPointer
    # <uint64_t>PyCapsule_GetPointer(obj, NULL)
    return _infinistore.register_server(loop_ptr, config)


def _kernel_modules():
    modules = set()
    try:
        with open("/proc/modules", "r") as f:
            for line in f:
                sep = line.find(" ")
                if sep != -1:
                    modules.add(line[:sep])
    except IOError as e:
        raise Exception(f"can not read /proc/modules: {e}")
    return modules


def _check_rdma_devices_ibv():
    try:
        result = subprocess.run(
            ["ibv_devinfo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            return
        output = result.stdout
        devices = output.split("\n\n")
        port_active = False
        for device_info in devices:
            if "hca_id" in device_info:
                if "PORT_ACTIVE" in device_info:
                    port_active = True
                    break
        if port_active is False:
            raise Exception("No active RDMA device found")
    except FileNotFoundError:
        raise Exception(
            "command ibv_devinfo not found, make sure RDMA tools are installed; for ubuntu, run apt install ibv_devinfo"
        )


def check_supported():
    # check if kernel module nv_peer_mem is available
    if (
        "nv_peer_mem" not in _kernel_modules()
        and "nvidia_peermem" not in _kernel_modules()  # noqa: W503
    ):
        raise Exception("nv_peer_mem module is not loaded")
    _check_rdma_devices_ibv()


class DisableTorchCaching:
    def __enter__(self):
        os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"] = "1"
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        del os.environ["PYTORCH_NO_CUDA_MEMORY_CACHING"]
        return


class InfinityConnection:
    OP_R = "R"
    OP_W = "W"
    OP_SYNC = "S"
    OP_RDMA_WRITE = "D"
    OP_RDMA_READ = "A"

    def __init__(self, config: ClientConfig):
        config.verify()
        self.conn = _infinistore.Connection()
        self.local_connected = False
        self.rdma_connected = False
        self.config = config

        mem_cap = _get_bar1_memory_cap()

        avail_bar1 = mem_cap["bar1_free"] - mem_cap["bar1_used"]
        avall_gpu_mem = mem_cap["total"] - mem_cap["reserved"]
        if avail_bar1 < avall_gpu_mem:
            # if BAR1 memory is not enough, set a flag.
            self.conn.limited_bar1 = True
            self.conn.bar1_mem_in_mib = mem_cap["bar1_free"] - mem_cap["bar1_used"]
        else:
            self.conn.limited_bar1 = False

    def connect(self):
        """
        Establishes an RDMA connection using the provided IP address.
        """
        if self.local_connected:
            raise Exception("Already connected to local instance")
        if self.rdma_connected:
            raise Exception("Already connected to remote instance")
        ret = _infinistore.init_connection(self.conn, self.config)
        if ret < 0:
            raise Exception("Failed to initialize remote connection")

        if self.config.connection_type == TYPE_LOCAL_GPU:
            if self.config.host_addr not in ["127.0.0.1", "localhost"]:
                raise Exception("Local GPU connection must be to localhost")
            self.local_connected = True
        else:
            ret = _infinistore.setup_rdma(self.conn, self.config)
            if ret < 0:
                raise Exception("Failed to setup RDMA connection")
            self.rdma_connected = True

    def write_cache(
        self, cache: torch.Tensor, blocks: List[Tuple[str, int]], page_size: int
    ):
        """
        Writes the given cache tensor to the specified blocks in memory.

        Args:
            cache (torch.Tensor): The tensor containing the data to be written.
            blocks (List[Tuple[str, int]]): A list of tuples where each tuple contains a key and an offset.
            each pair represents a page to be written to. The page is fixed size and is specified by the page_size parameter.
            page_size (int): How many element in one page.
        """
        self._verify(cache)
        ptr = cache.data_ptr()
        element_size = cache.element_size()

        # each offset should multiply by the element size
        blocks_in_bytes = [(key, offset * element_size) for key, offset in blocks]

        torch.cuda.synchronize()
        if self.local_connected:
            ret = _infinistore.rw_local(
                self.conn, self.OP_W, blocks_in_bytes, page_size * element_size, ptr
            )
            if ret < 0:
                raise Exception(f"Failed to write to infinistore, ret = {ret}")
        elif self.rdma_connected:
            ret = _infinistore.rw_rdma(
                self.conn,
                self.OP_RDMA_WRITE,
                blocks_in_bytes,
                page_size * element_size,
                ptr,
                cache.numel() * element_size,
            )
            if ret < 0:
                raise Exception(f"Failed to write to infinistore, ret = {ret}")
        else:
            raise Exception("Not connected to any instance")

    def read_cache(
        self, cache: torch.Tensor, blocks: List[Tuple[str, int]], page_size: int
    ):
        """
        Reads data from the cache using either local or RDMA connection.

        Args:
            cache (torch.Tensor): The tensor containing the cache data.
            blocks (List[Tuple[str, int]]): A list of tuples where each tuple contains a key and an offset.
            each pair represents a page to be written to. The page is fixed size and is specified by the page_size parameter.
            page_size (int): The size of the page to read.

        Raises:
            Exception: If the read operation fails or if not connected to any instance.
        """
        self._verify(cache)
        ptr = cache.data_ptr()
        element_size = cache.element_size()
        # each offset should multiply by the element size
        blocks_in_bytes = [(key, offset * element_size) for key, offset in blocks]
        if self.local_connected:
            ret = _infinistore.rw_local(
                self.conn, self.OP_R, blocks_in_bytes, page_size * element_size, ptr
            )
            if ret < 0:
                raise Exception(f"Failed to read to infinistore, ret = {ret}")
        elif self.rdma_connected:
            ret = _infinistore.rw_rdma(
                self.conn,
                self.OP_RDMA_READ,
                blocks_in_bytes,
                page_size * element_size,
                ptr,
                cache.numel() * element_size,
            )
            if ret < 0:
                raise Exception(f"Failed to read to infinistore, ret = {ret}")
        else:
            raise Exception("Not connected to any instance")

    def sync(self):
        """
        Synchronizes the current instance with the connected infinistore instance.
        This method attempts to synchronize the current instance using either a local
        connection or an RDMA connection. If neither connection is available, it raises
        an exception.
        Raises:
            Exception: If not connected to any instance.
            Exception: If synchronization fails with a negative return code.
        """
        ret = 0
        if self.local_connected:
            n = 0
            timeout = 1  # 1 second timeout
            while True:
                ret = _infinistore.sync_local(self.conn)
                if ret < 0:
                    raise Exception(f"Failed to sync to infinistore, ret = {ret}")
                elif ret > 0:
                    # how many inflight requests
                    # print(f"waiting for {ret} inflight requests")
                    if n > timeout * 10000:
                        raise Exception("Timeout waiting for inflight requests")
                    time.sleep(ret * 0.0001)
                else:
                    return
        elif self.rdma_connected:
            ret = _infinistore.sync_rdma(self.conn)
        else:
            raise Exception("Not connected to any instance")

        if ret < 0:
            raise Exception(f"Failed to sync to infinistore, ret = {ret}")
        return

    def _verify(self, cache: torch.Tensor):
        if cache.device.type != "cuda":
            raise Exception("Tensor must be on CUDA device")
        if cache.is_contiguous() is False:
            raise Exception("Tensor must be contiguous")

    def check_exist(self, key: str):
        ret = _infinistore.check_exist(self.conn, key)
        if ret < 0:
            raise Exception("Failed to check if this key exists")
        return True if ret == 0 else False

    def get_match_last_index(self, keys: List[str]):
        ret = _infinistore.get_match_last_index(self.conn, keys)
        if ret < 0:
            raise Exception("can't find a match")
        return ret
