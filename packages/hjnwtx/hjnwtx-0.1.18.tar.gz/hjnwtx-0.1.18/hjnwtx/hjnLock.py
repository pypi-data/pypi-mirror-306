import datetime
import os
import time
from hjnwtx.mkNCHJN import mkDir

class lockHJN():
    def __init__(self,lockPath):
        self.lockPath = lockPath

    def getlockFile(self,UTC):
        UTCStr = UTC.strftime("%Y%m%d%H%M")
        lock_file = f"{self.lockPath}/{UTCStr}.lock"
        return lock_file
# 加锁
    def acquire_lock(self,UTC):
        lock_file = self.getlockFile(UTC)
        mkDir(lock_file)
        while os.path.exists(lock_file):
            time.sleep(0.1)  # 等待0.1秒
        open(lock_file, 'w').close()

# 解锁
    def release_lock(self,UTC):
        lock_file = self.getlockFile(UTC)
        if os.path.exists(lock_file):
            os.remove(lock_file)

    def get_lock(self,UTC):
        lock_file = self.getlockFile(UTC)
        return os.path.exists(lock_file)

def test():
    path = "/mnt/wtx_weather_forecast/WTX_DATA/RADA/.MQPFlock"
    a = lockHJN(path)
    # 使用锁
    UTC = datetime.datetime(2024, 8, 16, 0)
    a.acquire_lock(UTC)
    print(a.get_lock(UTC))
    time.sleep(5)  # 模拟关键操作
    a.release_lock(UTC)
    print(a.get_lock(UTC))


if __name__ == '__main__':
    test()
