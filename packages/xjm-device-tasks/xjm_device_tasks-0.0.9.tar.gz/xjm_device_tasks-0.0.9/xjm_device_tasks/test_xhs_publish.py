from .client import PublishClient, create_usb_client, PublishData
from task_xhs_publish import XhsVideoPublishTask

data = PublishData(
    id="123123",
    # video_url="http://video.mj0.top:4140/duanshipin/pets/cat/fe986f5794411c2a0418da5b4ca8096e.mp4?response-content-type=video%2Fmp4&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=DPcdckj2R67KvDK8a2Fo%2F20240801%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240801T130515Z&X-Amz-Expires=1800&X-Amz-SignedHeaders=host&X-Amz-Signature=6eff0e8d1ab296ee3025ea0015aaa463bdd5f06b07b5764dd0b27cd533f60c42",
    # cover_url="",
    local_video_path="./dy_tmp/IMG_2009.mp4",
    # local_cover_path="./dy_tmp/output_image.jpg",
    wenan="文案的效果显而易见的好啊",
    topic=["热门音乐", "情感音乐"]
)

cli = create_usb_client("15992a1a0806")
task = XhsVideoPublishTask(data=data)
cli.set_task(task)
cli.run_current_task()
