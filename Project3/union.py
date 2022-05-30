import time
import sys
from Sets import *


if __name__ =='__main__':
    try:
        a = time.time()
        valid_email_1 = reading_file(sys.argv[1])
        valid_email_2 = reading_file(sys.argv[2])

        result = union(valid_email_1,valid_email_2)
        written_file = write_file(result)

        b = time.time()
        time_taken = b - a

        print(f"{sys.argv[1]}:{len(valid_email_1)},{sys.argv[2]}:{len(valid_email_2)},{sys.argv[3]}:{len(result)},Time taken:{time_taken}")
    except Exception as e:
        print(f"error is {e}")
















