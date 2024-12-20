#!/usr/bin/env python
import os


from confluent_kafka.admin import AdminClient


def get_bootstrap_url() -> list[str]:
    _bootstrap_url = os.getenv("KAFKA_BOOTSTRAP_URL", "")
    if not _bootstrap_url:
        raise ValueError("please set KAFKA_BOOTSTRAP_URL env var")

    return _bootstrap_url


def connect_kafka_admin() -> AdminClient:
    ac = AdminClient(
        {
            "bootstrap.servers": get_bootstrap_url(),
        }
    )

    return ac


def describe_topic():
    admin = connect_kafka_admin()

    metadatas = admin.list_topics(timeout=10)
    for name, metadata in metadatas.topics.items():
        partition = len(metadata.partitions)
        replication_factor = len(next(iter(metadata.partitions.values())).replicas)
        print(
            f"""topic name: {name} | partition: {partition} | replication factor: {replication_factor}"""
        )


if __name__ == "__main__":
    describe_topic()
