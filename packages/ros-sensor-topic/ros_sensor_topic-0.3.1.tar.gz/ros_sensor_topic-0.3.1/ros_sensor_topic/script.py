import subprocess
import logging
import logging.config


def get_image_topic():
    result = subprocess.run(
        ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
    )
    topics = result.stdout.splitlines()

    for topic_name in topics:

        if "/camera/color/image_raw" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        elif "/oak/rgb/image_raw" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name

    return "/camera/color/image_raw"

def get_pointcloud_topic():
    result = subprocess.run(
        ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
    )
    topics = result.stdout.splitlines()

    for topic_name in topics:

        if "/camera/camera/depth/color/points" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        elif "/oak/points" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        
    return "/camera/camera/depth/color/points"

def get_camera_info_topic():
    result = subprocess.run(
        ["ros2", "topic", "list"], stdout=subprocess.PIPE, text=True
    )
    topics = result.stdout.splitlines()

    for topic_name in topics: 

        if "/camera/depth/camera_info" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        elif "/oak/stereo/camera_info" in topic_name:
            logging.info("Subscribed Topic is: ")
            logging.info(topic_name)
            return topic_name
        
    return "/camera/depth/camera_info"