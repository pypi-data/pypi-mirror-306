import sys
import json
import uuid
import shutil
import asyncio
from typing import List, Callable, Iterable, Optional, Awaitable, AsyncIterator
from pathlib import Path

import click
import aiofiles
import aiofiles.tempfile
from tqdm import tqdm

from objective import AsyncObjective
from objective._exceptions import ObjectiveError
from objective.types.object_batch_params import Operation, OperationPutOperation


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument(
    "file_path", type=click.Path(exists=True, dir_okay=False, path_type=str)
)
@click.option(
    "--id-field", type=str, help="Field to use as object ID for PUT operations"
)
@click.option(
    "--max-concurrency", type=int, default=32, help="Maximum number of concurrent tasks"
)
@click.option(
    "--max-batch-size", type=int, default=512 * 1024, help="Maximum batch size in bytes"
)
@click.option(
    "--max-operations",
    type=int,
    default=1000,
    help="Maximum number of operations per batch",
)
@click.option(
    "--client-timeout",
    type=float,
    default=60.0,
    help="Timeout for API requests in seconds for an individual batch",
)
@click.option(
    "--client-max-retries",
    type=int,
    default=3,
    help="Maximum number of retries for failed API requests",
)
@click.option(
    "--error-file",
    type=click.Path(dir_okay=False, path_type=str),
    help="Path to output failed operations for retry",
)
def upsert_file(
    file_path: str,
    id_field: Optional[str],
    max_concurrency: int,
    max_batch_size: int,
    max_operations: int,
    client_timeout: float,
    client_max_retries: int,
    error_file: Optional[str],
) -> None:
    """Batch upsert all rows in the given JSONL file."""
    asyncio.run(
        async_upsert_file_with_errors(
            file_path,
            id_field,
            max_concurrency,
            max_batch_size,
            max_operations,
            client_timeout,
            client_max_retries,
            error_file,
        )
    )


async def async_upsert_file_with_errors(
    file_path: str,
    id_field: Optional[str],
    max_concurrency: int,
    max_batch_size: int,
    max_operations: int,
    client_timeout: float,
    client_max_retries: int,
    error_file: Optional[str],
) -> None:
    temp_error_file = None
    error_file_lock = asyncio.Lock()  # Add lock for thread-safe file access

    if error_file:
        temp_error_file = await aiofiles.tempfile.NamedTemporaryFile(
            mode="w", delete=False
        )

    async def persist_errors(failed_objects: Iterable[str]) -> None:
        if temp_error_file:
            async with error_file_lock:
                for obj in failed_objects:
                    await temp_error_file.write(obj + "\n")

    try:
        await async_upsert_file(
            file_path,
            id_field,
            max_concurrency,
            max_batch_size,
            max_operations,
            client_timeout,
            client_max_retries,
            persist_errors,
        )

    finally:
        if temp_error_file:
            await temp_error_file.close()
            if error_file:
                # Only move the temp file if there were actually errors
                if Path(str(temp_error_file.name)).stat().st_size > 0:
                    shutil.move(str(temp_error_file.name), error_file)
                else:
                    # Remove empty temp file
                    Path(str(temp_error_file.name)).unlink()


async def async_upsert_file(
    file_path: str,
    id_field: Optional[str],
    max_concurrency: int,
    max_batch_size: int,
    max_operations: int,
    client_timeout: float,
    client_max_retries: int,
    persist_errors: Callable[[Iterable[str]], Awaitable[None]],
) -> None:
    async with AsyncObjective(
        timeout=client_timeout, max_retries=client_max_retries
    ) as client:

        async def process_line(
            line: str,
        ) -> Optional[Operation]:
            obj = json.loads(line)
            if id_field:
                if id_field not in obj:
                    click.echo(
                        f"Error: ID field '{id_field}' not found in object: {obj}",
                        err=True,
                    )
                    return None

            obj_id = obj.get(id_field)
            # If the ID is not set, generate a random one
            # This is necessary to avoid issues with retries.
            # The SDK automatically retries operations that fail
            # and it would cause issues if the same object was created twice using a POST.
            # The generated ID is generated the same way the Objective API does.
            if obj_id is None:
                obj_id = f"obj_{uuid.uuid4().hex}"
            return OperationPutOperation(
                method="PUT",
                object=obj,
                object_id=obj_id,
            )

        async def process_batch(
            batch: Iterable[Optional[Operation]],
        ) -> int:
            operations = [op for op in batch if op is not None]
            if operations:
                try:
                    await client.objects.batch(operations=operations)
                except ObjectiveError as e:
                    failed_objects = [
                        json.dumps(obj.get("object"))
                        for obj in operations
                        if obj.get("object") is not None
                    ]
                    await persist_errors(failed_objects)
                    click.echo(f"Batch failed: {str(e)}", err=True)

            return len(operations)

        async def read_and_process() -> AsyncIterator[List[Operation]]:
            operations: list[Operation] = []
            current_batch_size: int = 0
            async with aiofiles.open(file_path, mode="r") as file:
                async for line in file:
                    operation = await process_line(line)
                    if operation:
                        operation_size = sys.getsizeof(json.dumps(operation))
                        if (
                            len(operations) == max_operations
                            or current_batch_size + operation_size > max_batch_size
                        ):
                            yield operations
                            operations = []
                            current_batch_size = 0
                        operations.append(operation)
                        current_batch_size += operation_size
                if operations:
                    yield operations

        total_operations = 0
        pbar = tqdm(total=total_operations, desc="Processing operations")

        semaphore = asyncio.Semaphore(max_concurrency)

        async def process_with_semaphore(
            batch: Iterable[Operation],
            semaphore: asyncio.Semaphore,
        ) -> None:
            async with semaphore:
                processed = await process_batch(batch)
                pbar.update(processed)

        tasks: List[asyncio.Task[None]] = []

        async for batch in read_and_process():
            tasks.append(asyncio.create_task(process_with_semaphore(batch, semaphore)))
            total_operations += len(batch)
            pbar.total = total_operations  # Update the total count
            pbar.refresh()  # Refresh the progress bar

        await asyncio.gather(*tasks)
        pbar.close()
        click.echo("All operations processed.")


@cli.command()
@click.option(
    "--batch-size",
    default=1000,
    type=int,
    help="Number of objects to fetch per request",
)
def download_objects(batch_size: int) -> None:
    """Download all objects and output them to stdout."""
    asyncio.run(async_download_objects(batch_size))


async def async_download_objects(batch_size: int) -> None:
    async with AsyncObjective() as client:
        cursor: Optional[str] = None
        total_objects = 0
        with tqdm(desc="Downloading objects", unit="obj") as pbar:
            while True:
                if cursor:
                    response = await client.objects.list(
                        include_object=True, limit=batch_size, cursor=cursor
                    )
                else:
                    response = await client.objects.list(
                        include_object=True, limit=batch_size
                    )
                for obj in response.objects:
                    if obj.object:
                        print(json.dumps(obj.object), flush=True)  # noqa: T201
                        total_objects += 1
                        pbar.update(1)

                if not response.pagination.next:
                    break
                cursor = response.pagination.next

    click.echo(f"All objects downloaded. Total: {total_objects}", err=True)


if __name__ == "__main__":
    cli()
