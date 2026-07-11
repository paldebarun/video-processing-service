import sys

from workers.video_worker import VideoWorker


WORKERS = {
    "video": VideoWorker,
}


def main():

    if len(sys.argv) != 2:

        raise RuntimeError(
            "Usage: python run_worker.py video"
        )

    worker = WORKERS[
        sys.argv[1]
    ]()

    worker.start()


if __name__ == "__main__":

    main()