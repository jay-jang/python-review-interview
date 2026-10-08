"""Python code review lab (Python 3.11+, standard library only).

Run: python python_review_lab.py
No network calls and no external packages are required.
Intentional defects are reproduced only in isolated test functions.
"""
import asyncio
from contextlib import closing
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from functools import lru_cache, wraps
from pathlib import Path
import sqlite3
import tempfile
import unittest


def add_tag(tag, tags=None):
    result = [] if tags is None else list(tags)
    result.append(tag)
    return result


def mean(values):
    total = count = 0
    for value in values:
        total += value
        count += 1
    if count == 0:
        raise ValueError("empty input")
    return total / count


def stream_lines(path):
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            yield line.removesuffix("\n")


def apply_nights_patch(payload):
    if "nights" not in payload:
        return "unchanged"
    value = payload["nights"]
    if value is None:
        return "delete"
    if type(value) is not int or value <= 0:
        raise ValueError("invalid nights")
    return f"set:{value}"


def search(conn, city, sort):
    columns = {"price": "price", "name": "name"}
    if sort not in columns:
        raise ValueError("unsupported sort")
    column = columns[sort]
    query = (
        "SELECT name, price FROM hotels "
        f"WHERE city = ? ORDER BY {column}"
    )
    return conn.execute(query, (city,)).fetchall()


async def run_bounded(items, handle, workers=10):
    if workers < 1:
        raise ValueError("workers must be positive")
    queue = asyncio.Queue(maxsize=workers * 2)
    stop = object()

    async def produce():
        for item in items:
            await queue.put(item)
        for _ in range(workers):
            await queue.put(stop)

    async def consume():
        while True:
            item = await queue.get()
            try:
                if item is stop:
                    return
                await handle(item)
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as group:
        group.create_task(produce())
        for _ in range(workers):
            group.create_task(consume())


async def best_price(hotel_id, suppliers, api):
    if not suppliers or len(suppliers) > 100:
        raise ValueError("1..100 suppliers required")
    sem = asyncio.Semaphore(10)

    async def one(supplier):
        async with sem:
            data = await api.fetch(supplier, hotel_id)
        raw = data["price"]
        if (
            not isinstance(raw, str)
            or not raw.isascii()
            or not raw.isdecimal()
        ):
            raise ValueError("invalid KRW price")
        value = int(raw)
        if value <= 0:
            raise ValueError("positive price required")
        return value

    async with asyncio.timeout(3):
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(one(s)) for s in suppliers
            ]
    return min(task.result() for task in tasks)


class LanguageTests(unittest.TestCase):
    def test_q01_default_argument_shares_state(self):
        def bad(tag, tags=[]):
            tags.append(tag)
            return tags
        a = bad("wifi")
        b = bad("desk")
        self.assertIs(a, b)
        self.assertEqual(a, ["wifi", "desk"])

    def test_q01_fix_preserves_input(self):
        original = ["wifi"]
        self.assertEqual(add_tag("desk", original), ["wifi", "desk"])
        self.assertEqual(original, ["wifi"])
        self.assertEqual(add_tag("a"), ["a"])
        self.assertEqual(add_tag("b"), ["b"])

    def test_q02_nested_alias_and_copy(self):
        rooms = [{"tags": []}] * 2
        backup = rooms.copy()
        backup[0]["tags"].append("wifi")
        self.assertEqual(rooms, [{"tags": ["wifi"]}] * 2)
        self.assertIs(rooms[0], rooms[1])
        deep = deepcopy(rooms)
        self.assertIs(deep[0], deep[1])  # deepcopy preserves internal aliasing
        self.assertIsNot(deep[0], rooms[0])

    def test_q03_none_zero_and_sort(self):
        values = [100, 0, None, 50]
        self.assertEqual(sorted(p for p in values if p is not None), [0, 50, 100])
        self.assertIsNone([1, 2].sort())

    def test_q04_late_binding(self):
        bad = [lambda: i for i in range(3)]
        good = [lambda i=i: i for i in range(3)]
        self.assertEqual([f() for f in bad], [2, 2, 2])
        self.assertEqual([f() for f in good], [0, 1, 2])

    def test_q05_mutating_iteration(self):
        values = [0, 0, 1, 0]
        for value in values:
            if value == 0:
                values.remove(value)
        self.assertEqual(values, [1, 0])
        alias = values
        values[:] = [v for v in values if v != 0]
        self.assertIs(alias, values)
        self.assertEqual(alias, [1])

    def test_q07_strict_zip_partial_consumption(self):
        saved = []
        with self.assertRaises(ValueError):
            for row in zip(["A", "B"], [100], strict=True):
                saved.append(row)
        self.assertEqual(saved, [("A", 100)])

    def test_q08_timestamp_definition_time(self):
        def event(created_at=datetime.now(timezone.utc)):
            return created_at
        self.assertIs(event(), event())

    def test_q09_single_pass_mean(self):
        self.assertEqual(mean(x for x in [10, 20, 30]), 20)
        with self.assertRaises(ValueError):
            mean(iter([]))

    def test_q10_resource_lifetime(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.txt"
            path.write_text(" A \nB\n", encoding="utf-8")
            with closing(stream_lines(path)) as rows:
                self.assertEqual(next(rows), " A ")
            self.assertIsNone(rows.gi_frame)

    def test_q12_frozen_is_shallow(self):
        @dataclass(frozen=True)
        class Offer:
            tags: list[str] = field(default_factory=list)
        value = Offer()
        value.tags.append("wifi")
        self.assertEqual(value.tags, ["wifi"])
        with self.assertRaises(TypeError):
            hash(value)

    def test_cache_returns_same_mutable_object(self):
        @lru_cache
        def tags(key):
            return []
        tags("H1").append("private")
        self.assertEqual(tags("H1"), ["private"])

    def test_q14_missing_none_bool(self):
        self.assertEqual(apply_nights_patch({}), "unchanged")
        self.assertEqual(apply_nights_patch({"nights": None}), "delete")
        self.assertEqual(apply_nights_patch({"nights": 2}), "set:2")
        for value in [0, -1, True, "2", 2.5]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                apply_nights_patch({"nights": value})

    def test_q15_sql_parameters(self):
        with closing(sqlite3.connect(":memory:")) as conn:
            conn.execute("CREATE TABLE hotels(name TEXT, city TEXT, price INT)")
            conn.executemany("INSERT INTO hotels VALUES (?, ?, ?)", [
                ("A", "Seoul", 100), ("B", "O'City", 50),
            ])
            self.assertEqual(search(conn, "O'City", "price"), [("B", 50)])
            self.assertEqual(search(conn, "' OR 1=1 --", "price"), [])
            with self.assertRaises(ValueError):
                search(conn, "Seoul", "price; DROP TABLE hotels")

    def test_q22_property_descriptor(self):
        class Quote:
            @property
            def price(self):
                return 100
        quote = Quote()
        quote.__dict__["price"] = 1
        self.assertEqual(quote.price, 100)
        with self.assertRaises(AttributeError):
            quote.price = 2

    def test_decimal_policy(self):
        tax = (Decimal("19.99") * Decimal("0.10")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        self.assertEqual(str(tax), "2.00")

    def test_generator_execution_is_deferred(self):
        events = []
        def gen():
            events.append("start")
            yield 1
        g = gen()
        self.assertEqual(events, [])
        self.assertEqual(next(g), 1)
        self.assertEqual(events, ["start"])
        g.close()

    def test_finally_return_suppresses_exception(self):
        def bad():
            try:
                raise ValueError("bad")
            finally:
                return 0
        self.assertEqual(bad(), 0)


class AsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_q11_async_wrapper(self):
        calls = []
        def wrapped(fn):
            @wraps(fn)
            async def wrapper(*args, **kwargs):
                try:
                    return await fn(*args, **kwargs)
                finally:
                    calls.append("finished")
            return wrapper
        @wrapped
        async def value():
            return 3
        self.assertEqual(await value(), 3)
        self.assertEqual(value.__name__, "value")
        self.assertEqual(calls, ["finished"])

    async def test_gather_does_not_cancel_sibling(self):
        started = asyncio.Event()
        release = asyncio.Event()
        async def sibling():
            started.set()
            await release.wait()
            return 7
        async def fail():
            await started.wait()
            raise ValueError("fail")
        task = asyncio.create_task(sibling())
        try:
            with self.assertRaises(ValueError):
                await asyncio.gather(fail(), task)
            self.assertFalse(task.done())
        finally:
            release.set()
            self.assertEqual(await task, 7)

    async def test_q17_taskgroup_cleans_sibling(self):
        started = asyncio.Event()
        cleaned = asyncio.Event()
        async def sibling():
            try:
                started.set()
                await asyncio.Future()
            finally:
                cleaned.set()
        async def fail():
            await started.wait()
            raise ValueError("fail")
        with self.assertRaises(ExceptionGroup):
            async with asyncio.TaskGroup() as group:
                group.create_task(sibling())
                group.create_task(fail())
        self.assertTrue(cleaned.is_set())

    async def test_q18_cancellation_cleanup(self):
        started = asyncio.Event()
        cleaned = asyncio.Event()
        async def job():
            try:
                started.set()
                await asyncio.Future()
            finally:
                cleaned.set()
        task = asyncio.create_task(job())
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(cleaned.is_set())

    async def test_q19_bounded_worker_count(self):
        active = peak = 0
        seen = []
        async def handle(item):
            nonlocal active, peak
            active += 1
            peak = max(active, peak)
            try:
                await asyncio.sleep(0)
                seen.append(item)
            finally:
                active -= 1
        await run_bounded(range(50), handle, workers=3)
        self.assertLessEqual(peak, 3)
        self.assertEqual(sorted(seen), list(range(50)))
        self.assertEqual(active, 0)

    async def test_q19_worker_failure_terminates_producer(self):
        async def handle(item):
            raise ValueError("stop")
        async with asyncio.timeout(1):
            with self.assertRaises(ExceptionGroup):
                await run_bounded(range(10000), handle, workers=2)

    async def test_q20_race_and_lock(self):
        state = {"rooms": 1}
        async def bad():
            if state["rooms"] > 0:
                await asyncio.sleep(0)
                state["rooms"] -= 1
                return True
            return False
        self.assertEqual(await asyncio.gather(bad(), bad()), [True, True])
        self.assertEqual(state["rooms"], -1)
        state["rooms"] = 1
        lock = asyncio.Lock()
        async def good():
            async with lock:
                if state["rooms"] <= 0:
                    return False
                state["rooms"] -= 1
                return True
        self.assertEqual(sum(await asyncio.gather(good(), good())), 1)
        self.assertEqual(state["rooms"], 0)

    async def test_timeout_exception_outside_context(self):
        with self.assertRaises(TimeoutError):
            async with asyncio.timeout(0):
                await asyncio.Future()

    async def test_q24_best_price(self):
        class API:
            async def fetch(self, supplier, hotel_id):
                return {"price": str(supplier)}
        self.assertEqual(await best_price("H1", [300, 100, 200], API()), 100)
        with self.assertRaises(ExceptionGroup):
            await best_price("H1", [100, "nan"], API())
        with self.assertRaises(ValueError):
            await best_price("H1", [], API())


if __name__ == "__main__":
    unittest.main(verbosity=2)
