from dataclasses import dataclass
from litestar import Litestar, post, get, delete, put

@dataclass
class TodoItem:
    title: str
    done: bool

TODO_LIST: list[TodoItem] = []

@post("/")
async def add_item(data: TodoItem) -> list[TodoItem]:
    TODO_LIST.append(data)
    return TODO_LIST

@get("/")
async def get_list(done: bool | None = None) -> list[TodoItem]:
    if done is None:
        return TODO_LIST
    return [item for item in TODO_LIST if item.done == done]

@delete("/{index:int}")
async def delete_item(id: int) -> None:
    """Deletes a TodoItem from the list based on its ID."""
    try:
        del TODO_LIST[id]
    except IndexError:
        return {"error": "Item with ID not found"}
    return None 

@put("/{index:int}")
async def update_item(data: TodoItem, index: int) -> TodoItem | None:
    try:
        # Validate if index exists and data is valid
        if index >= len(TODO_LIST) or index < 0:
            return None

        # Update existing item at index with new data
        TODO_LIST[index] = TodoItem(title=data.title, done=data.done)
        return TODO_LIST[index]
    except IndexError:
        return None


app = Litestar([get_list, add_item, delete_item, update_item])
