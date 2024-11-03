from typing import Any, overload, SupportsIndex
import pymongo
from pymongo.collection import Collection
from pymongo.synchronous.cursor import Cursor
from contextlib import suppress
from bson import ObjectId, json_util
import json as j
import pymongo.cursor
import pymongo.errors
import pymongo.synchronous
import pymongo.synchronous.cursor
from collections.abc import Sized, Container


class _Database:
    def __init__(self, db):
        self.db = db

    def __getitem__(self, item):
        return _Collection(self.db[item])


class _Client:
    def __init__(self, url, db="test", collection="test"):
        self.client = pymongo.MongoClient(url)

    def __getitem__(self, item):
        return _Database(self.client[item])


class _QueryResult(Cursor):
    def __init__(self, cursor):
        self.cursor: Cursor = cursor
        self._cached_results: list[dict[str, Any]] | None = None
        # print(vars(self.cursor))

    @property
    def _results(self) -> list[dict[str, Any]]:
        """Lazy load results only when needed"""
        if self._cached_results is None:
            self._cached_results = list(self.cursor)
        return self._cached_results

    @overload
    def __getitem__(self, key: slice) -> list[dict[str, Any]]: ...

    @overload
    def __getitem__(self, key: int) -> dict[str, Any]: ...

    def __getitem__(self, key: slice | int) -> list[dict[str, Any]] | dict[str, Any] | Any:
        match key:
            case slice():
                cursor = self.cursor
                start = key.start or 0

                if start:
                    cursor = cursor.skip(start)
                if key.stop:
                    cursor = cursor.limit(key.stop - start)
                if key.step == -1:
                    cursor = cursor.sort("_id", pymongo.DESCENDING)

                return cursor.to_list()

            case int():
                # For single document access, use limit and skip
                r = self.cursor.limit(1).skip(key).next()
                self.cursor.rewind()  # Reset cursor position after accessing single document
                return r

            case _:
                raise TypeError(f"Invalid key type: {type(key)}")

    def __len__(self) -> int:
        return self.cursor.collection.count_documents(self.cursor._spec)

    def __contains__(self, item: object) -> bool:
        return self.cursor.collection.count_documents({"_id": item}) > 0

    def __bool__(self) -> bool:
        try:
            r = self.cursor.limit(1).next()
        except StopIteration:
            return False
        finally:
            self.cursor.rewind()
            return True

    def __str__(self) -> str:
        return json_util.dumps(list(self.cursor.limit(10)), indent="  ")

    def __iter__(self):
        return self.cursor


class _Collection(Collection):
    """override read write methods while inheriting all default Collection methods/attributes"""

    def __init__(self, collection: Collection):
        super().__init__(collection.database, collection.name)
        self.collection = collection
        self.last_inserted = None  # Add this attribute

    def _parse_query_string(self, query_str: str) -> dict:
        # Handle different operators
        compound_operators = {">=": "$gte", "<=": "$lte", "!=": "$ne", "~=": "$regex", "*=": "$regex"}
        simple_operators = {"==": "$eq", ">": "$gt", "<": "$lt", "??": "$exists"}

        # Try compound operators first
        op = next((op for op in compound_operators if op in query_str), None)
        if op:
            field, value = [x.strip() for x in query_str.split(op, 1)]
        else:
            # Try simple operators if no compound operator found
            op = next((op for op in simple_operators if op in query_str), None)
            if not op:
                with suppress(Exception):
                    # If no operator found, treat it as an ID lookup
                    return {"_id": ObjectId(query_str.strip())}

            field, value = [x.strip() for x in query_str.split(op, 1)]

        with suppress(Exception):
            value = j.loads(value)

        if isinstance(value, str):
            # Remove quotes if present
            value = value.strip("'\"")

        if op == "~=":
            return {field: {"$regex": value, "$options": "i"}}
        elif op == "*=":
            return {field: {"$regex": value}}

        # Build MongoDB query for numeric/exact comparisons
        operators = {**compound_operators, **simple_operators}
        if op in operators:
            return {field: {operators[op]: value}}

        print("Warning Failed to parse QS")
        return {}

    def print(self, limit=10, reversed=False):
        for item in self.collection.find().limit(limit).sort("_id", pymongo.DESCENDING if reversed else pymongo.ASCENDING):
            print(item)

    def __iadd__(self, other):
        try:
            if isinstance(other, list):
                result = self.collection.insert_many(other, ordered=False)
                successful_ids = result.inserted_ids
            else:
                result = self.collection.insert_one(other)
                successful_ids = [result.inserted_id]
            self.last_inserted = _QueryResult(self.collection.find({"_id": {"$in": successful_ids}}))
            return self
        except Exception as e:
            self.last_inserted = None
            raise e

    def __setitem__(self, query_str: str | dict, value):
        try:
            if isinstance(query_str, str):
                q = self._parse_query_string(query_str)
            else:
                q = query_str
            # Perform the update  # should upsert? if inc in key
            upsert = False if any(x in ("$inc", "$addToSet") for x in value.keys()) else True
            updatable = value if not upsert else {"$set": value}
            result = self.collection.update_many(filter=q, update=updatable, upsert=upsert)

            # Store the updated/inserted document
            if result.upserted_id:
                self.last_inserted = _QueryResult(self.collection.find({"_id": result.upserted_id}))
            else:
                self.last_inserted = _QueryResult(self.collection.find(q))

            return self
        except Exception as e:
            self.last_inserted = None
            raise e

    def __getitem__(self, query_str: str | list | dict):
        if isinstance(query_str, (list, _QueryResult)):
            query = query_str[0]
        query = self._parse_query_string(query_str) if isinstance(query_str, str) else query_str
        # print(type(query_str), query)

        return _QueryResult(self.collection.find(query))

    def __str__(self):
        return str(list(self.collection.find()))


def mongo(url="mongodb://localhost:27017/"):
    return _Client(url)


def test():
    c = db["test"]["employees"]

    # Add test data

    # Example queries with slicing
    print("\nCase insensitive match with slice:")
    results = c["name ~= john"]
    print(results[0:2])  # First 2 matches

    print("\nReverse age query:")
    print(c["age >= 30"][::-1])  # All matches in reverse order

    print("\nSkip and limit:")
    print(c["age < 65"][0:5])  # Skip 2, get next 2

    # Can still use native Collection methods
    print("\nNative count:")
    print(c.count_documents({"age": {"$gte": 30}}))


if __name__ == "__main__":
    db = mongo()
    col = db["test"]["employees"]
    col["name == Jane"] = {"age": 30, "school": "bulchitdav"}  # Set document matching name John
