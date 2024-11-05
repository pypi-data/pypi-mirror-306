import getopt
import sys

from loguru import logger
from mprerun.config import read_config
from mprerun.pose import main as pose_main


# 全局入口
@logger.catch
def main() -> int:
    logger.warning("mprerun start...")

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hc:",
            ["help", "config="])

    except getopt.GetoptError:
        print("usage: mprerun -h")
        sys.exit(2)

    config_filename = None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("mprerun -c <config-filename>")
            sys.exit()
        elif opt in ("-c", "--config"):
            config_filename = arg

    if config_filename is None:
        print("mprerun -c <config-filename>")
        sys.exit()

    config_object = read_config(config_filename)
    if config_object.pose is not None:
        logger.warning("pose run...")
        pose_main(config_object.pose)

    logger.warning("mprerun end!!!")
    return 0


# 测试
if __name__ == '__main__':
    logger.warning("test...")
    main()
